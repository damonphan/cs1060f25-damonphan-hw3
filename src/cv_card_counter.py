import cv2
import numpy as np
import os

RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

def load_rank_templates(folder="templates"):
    tmpls = {}
    for r in RANKS:
        p = os.path.join(folder, f"{r}.png")
        if os.path.exists(p):
            img = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
            _, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            tmpls[r] = th
    if not tmpls:
        raise FileNotFoundError(f"No templates found in {folder}.")
    return tmpls

def find_cards(image_bgr):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cards = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        area = cv2.contourArea(approx)
        if len(approx)==4 and area > 8000:
            cards.append(approx)
    return cards

def order_corners(pts):
    pts = pts.reshape(4,2)
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1).ravel()
    ordered = np.zeros((4,2), dtype="float32")
    ordered[0] = pts[np.argmin(s)]
    ordered[2] = pts[np.argmax(s)]
    ordered[1] = pts[np.argmin(diff)]
    ordered[3] = pts[np.argmax(diff)]
    return ordered

def warp_card(image_bgr, quad, w=300, h=420):
    rect = order_corners(quad)
    dst = np.array([[0,0],[w-1,0],[w-1,h-1],[0,h-1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image_bgr, M, (w,h))

def detect_rank_from_corner(card_bgr, templates):
    H, W = card_bgr.shape[:2]
    corner = card_bgr[0:int(H*0.28), 0:int(W*0.28)]
    gray = cv2.cvtColor(corner, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    best_r, best_score = None, -1.0
    for r, tmpl in templates.items():
        res = cv2.matchTemplate(th, tmpl, cv2.TM_CCOEFF_NORMED)
        if res.size > 0:
            score = res.max()
            if score > best_score:
                best_score = score
                best_r = r
    return best_r, best_score

def annotate(image_bgr, cards, ranks):
    out = image_bgr.copy()
    for quad, (r, score) in zip(cards, ranks):
        quad = quad.reshape(-1,2)
        cv2.polylines(out, [quad.astype(int)], True, (0,255,0), 2)
        cx, cy = quad.mean(axis=0).astype(int)
        label = f"{r if r else '?'} ({score:.2f})" if r else "?"
        cv2.putText(out, label, (cx-30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50,50,255), 2)
    return out
