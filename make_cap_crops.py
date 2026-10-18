import os, glob
from PIL import Image

os.makedirs('assets/cap_crops', exist_ok=True)

# Generate tight close-up crops of the caps from cropped_products
orig_crops = glob.glob('assets/cropped_products/*_orig.png')

for path in orig_crops:
    fname = os.path.basename(path) # e.g. crop_30P01F_orig.png
    code = fname.replace('crop_', '').replace('_orig.png', '')
    
    img = Image.open(path)
    w, h = img.size
    
    # Cap is typically in top 30% of the bottle
    cap_h = int(h * 0.32)
    # Center horizontally
    cap_crop = img.crop((0, 0, w, cap_h))
    
    # Make it a clean square with subtle padding
    side = max(cap_crop.width, cap_crop.height) + 40
    sq = Image.new('RGBA', (side, side), (255, 255, 255, 0))
    px = (side - cap_crop.width) // 2
    py = (side - cap_crop.height) // 2
    sq.paste(cap_crop, (px, py), cap_crop)
    
    # Resize to standard 240x240
    sq_thumb = sq.resize((240, 240), Image.Resampling.LANCZOS)
    sq_thumb.save(f'assets/cap_crops/cap_{code}.png')

print(f"Generated {len(orig_crops)} cap close-up crops in assets/cap_crops/")
