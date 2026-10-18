import os, glob
from PIL import Image, ImageDraw, ImageFont

crops = sorted(glob.glob('assets/note_crops/*.JPG'))
batch_size = 10

for b in range(0, len(crops), batch_size):
    batch = crops[b:b+batch_size]
    w = 1200
    h = 600
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 2 rows of 5
    for i, cp in enumerate(batch):
        im = Image.open(cp)
        im.thumbnail((220, 240))
        col = i % 5
        row = i // 5
        x = col * 240 + 10
        y = row * 290 + 35
        img.paste(im, (x, y))
        draw.text((x, y - 25), os.path.basename(cp), fill=(0, 0, 0))
    
    batch_num = b // batch_size + 1
    out_name = f'assets/note_batch_{batch_num}.jpg'
    img.save(out_name)
    print(f'Saved {out_name}')
