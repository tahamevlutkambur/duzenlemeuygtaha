import os
import json

base_dir = r"C:\Users\Taha\Pictures\kolonya"

with open(os.path.join(base_dir, "products_catalog.json"), "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"Total products in catalog: {len(products)}")
for i, p in enumerate(products, 1):
    code = p['code']
    name = p['name']
    cat = p.get('category', '')
    vol = p.get('volume', '')
    cap = p.get('cap_type', '')
    white = p.get('photo_white', '')
    png = p.get('photo_png', '')
    crop_orig = p.get('crop_orig', '')
    cap_crop = f"assets/cap_crops/cap_{code}.png"
    
    white_ok = os.path.exists(os.path.join(base_dir, white)) if white else False
    png_ok = os.path.exists(os.path.join(base_dir, png)) if png else False
    cap_crop_ok = os.path.exists(os.path.join(base_dir, cap_crop))
    
    print(f"{i:02d}. {code} | {vol} | {cap} | White: {white_ok} | PNG: {png_ok} | CapCrop: {cap_crop_ok}")
