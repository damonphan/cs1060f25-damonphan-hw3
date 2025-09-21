from PIL import Image, ImageDraw, ImageFont
import os

RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

def generate_templates(out_dir="templates", size=(80,120)):
    os.makedirs(out_dir, exist_ok=True)
    try:
        font = ImageFont.truetype("arial.ttf", 72)
    except:
        font = ImageFont.load_default()
    for r in RANKS:
        img = Image.new("L", size, color=255)
        d = ImageDraw.Draw(img)
        w, h = d.textbbox((0,0), r, font=font)[2:]
        d.text(((size[0]-w)//2, (size[1]-h)//2), r, fill=0, font=font)
        path = os.path.join(out_dir, f"{r}.png")
        img.save(path)
        print("wrote", path)

if __name__ == "__main__":
    generate_templates()
