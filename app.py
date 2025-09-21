import cv2
import argparse
from src.cv_card_counter import find_cards, warp_card, load_rank_templates, detect_rank_from_corner, annotate
from src.count_utils import update_running_count

def process_frame(frame, templates, running_count):
    cards = find_cards(frame)
    ranks = []
    for quad in cards:
        card = warp_card(frame, quad)
        r, score = detect_rank_from_corner(card, templates)
        ranks.append((r, score if score else 0.0))
    detected = [r for r, _ in ranks if r]
    running_count = update_running_count(detected, running_count)
    vis = annotate(frame, cards, ranks)
    cv2.putText(vis, f"Running count: {running_count}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0), 3)
    cv2.putText(vis, f"Running count: {running_count}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 1)
    return vis, running_count, detected

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", help="Path to video file. If omitted, uses webcam 0.")
    ap.add_argument("--templates", default="templates", help="Folder with rank templates")
    args = ap.parse_args()

    templates = load_rank_templates(args.templates)
    cap = cv2.VideoCapture(args.video if args.video else 0)
    running_count = 0

    while True:
        ret, frame = cap.read()
        if not ret: break
        vis, running_count, detected = process_frame(frame, templates, running_count)
        cv2.imshow("Card Counter", vis)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        if key == ord('r'): running_count = 0
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
