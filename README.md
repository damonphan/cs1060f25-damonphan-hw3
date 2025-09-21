Author: Damon Phan
github: damonphan
https://cs1060.netlify.app/

https://drive.google.com/drive/folders/1OpmhWMKdeagoG6_jR4c339zDFFPjZL95?dmr=1&ec=wgc-drive-hero-goto

pwd
ls -1

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python3 src/generate_templates.py

python3 demo_image.py path/to/cards.jpg --templates templates

python3 app.py --templates templates

