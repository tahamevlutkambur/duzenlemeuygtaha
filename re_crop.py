import os
import json
from PIL import Image
import numpy as np

base_dir = r"C:\Users\Taha\Pictures\kolonya"
json_path = os.path.join(base_dir, "products_catalog.json")

with open(json_path, "r", encoding="utf-8") as f:
    products = json.load(f)

crop_prod_dir = os.path.join(base_dir, "assets", "cropped_products")
crop_mock_dir = os.path.join(base_dir, "assets", "cropped_mockups")
os.makedirs(crop_prod_dir, exist_ok=True)
os.makedirs(crop_mock_dir, exist_ok=True)

def crop_tight(img_path, out_path, margin_ratio=0.04, thresh=25):
    with Image.open(img_path) as img:
        img_rgba = img.convert("RGBA")
        alpha = np.array(img_rgba)[:, :, 3]
        y_indices, x_indices = np.where(alpha > thresh)
        if len(y_indices) == 0:
            img.save(out_path)
            return
        x_min, x_max = x_indices.min(), x_indices.max()
        y_min, y_max = y_indices.min(), y_indices.max()
        
        w = x_max - x_min
        h = y_max - y_min
        
        mx = int(w * margin_ratio)
        my = int(h * margin_ratio)
        
        x1 = max(0, x_min - mx)
        y1 = max(0, y_min - my)
        x2 = min(img.width, x_max + mx)
        y2 = min(img.height, y_max + my)
        
        cropped = img_rgba.crop((x1, y1, x2, y2))
        cropped.save(out_path, format="PNG")

print("Cropping all 32 products and mockups tightly with thresh=25...")
for p in products:
    code = p["code"]
    orig_rel = p["photo_png"]
    mock_rel = p["mockup_png"]
    
    orig_full = os.path.join(base_dir, orig_rel)
    mock_full = os.path.join(base_dir, mock_rel)
    
    out_orig = os.path.join(crop_prod_dir, f"crop_{code}_orig.png")
    out_mock = os.path.join(crop_mock_dir, f"crop_{code}_mock.png")
    
    if os.path.exists(orig_full):
        crop_tight(orig_full, out_orig)
    if os.path.exists(mock_full):
        crop_tight(mock_full, out_mock)
        
    p["crop_orig"] = f"assets/cropped_products/crop_{code}_orig.png"
    p["crop_mock"] = f"assets/cropped_mockups/crop_{code}_mock.png"
    print(f"Cropped tightly: {code}")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("Done tight cropping!")
