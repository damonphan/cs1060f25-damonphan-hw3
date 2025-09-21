import cv2
import argparse
from src.cv_card_counter import find_cards, warp_card, load_rank_templates, detect_rank_from_corner, annotate
from src.count_utils import update_running_count

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="Path to image file")
    ap.add_argument("--templates", default="templates", help="Folder with rank templates")
    args = ap.parse_args()

    templates = load_rank_templates(args.templates)
    img = cv2.imread(args.image)
    cards = find_cards(img)
    ranks = []
    for quad in cards:
        card = warp_card(img, quad)
        r, score = detect_rank_from_corner(card, templates)
        ranks.append((r, score if score else 0.0))

    vis = annotate(img, cards, ranks)
    detected = [r for r, _ in ranks if r]
    rc = update_running_count(detected, 0)
    cv2.putText(vis, f"Running count: {rc}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0), 3)
    cv2.putText(vis, f"Running count: {rc}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 1)
    cv2.imwrite("out_annotated.jpg", vis)
    print("Detected ranks:", detected)
    print("Running count:", rc)
    print("Wrote out_annotated.jpg")

if __name__ == "__main__":
    main()
