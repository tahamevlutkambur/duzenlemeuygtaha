import os, glob
from PIL import Image, ImageDraw, ImageFont

thumbs = sorted(glob.glob('assets/all_thumbs/*.JPG'))
print(f"Total thumbs: {len(thumbs)}")

chunk_size = 48
for sheet_idx in range(0, len(thumbs), chunk_size):
    chunk = thumbs[sheet_idx:sheet_idx+chunk_size]
    cols = 6
    rows = (len(chunk) + cols - 1) // cols
    
    cell_w = 200
    cell_h = 160
    
    sheet = Image.new('RGB', (cols * cell_w, rows * cell_h), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    
    for i, t in enumerate(chunk):
        im = Image.open(t)
        c = i % cols
        r = i // cols
        x = c * cell_w + 10
        y = r * cell_h + 30
        sheet.paste(im, (x, y))
        name = os.path.basename(t).replace('.JPG', '')
        draw.text((x, y - 20), name, fill=(0, 0, 0))
    
    out_name = f'assets/sheet_{sheet_idx // chunk_size + 1}.jpg'
    sheet.save(out_name)
    print(f"Saved {out_name}")
