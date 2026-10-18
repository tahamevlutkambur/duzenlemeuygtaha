import glob, os
from PIL import Image, ImageDraw, ImageFont

files = sorted(glob.glob('ürünler/*.jpg'))

# Create contact sheets
cols = 4
rows = (len(files) + cols - 1) // cols
cell_w, cell_h = 400, 300
sheet = Image.new('RGB', (cols * cell_w, rows * cell_h), (240, 240, 240))
draw = ImageDraw.Draw(sheet)

for idx, f in enumerate(files):
    img = Image.open(f)
    img.thumbnail((cell_w - 20, cell_h - 40))
    c = idx % cols
    r = idx // cols
    x = c * cell_w + (cell_w - img.width) // 2
    y = r * cell_h + 10 + (cell_h - 40 - img.height) // 2
    sheet.paste(img, (x, y))
    
    name = os.path.basename(f)[:25]
    draw.text((c * cell_w + 10, (r + 1) * cell_h - 25), f"{idx+1}. {name}", fill=(20, 20, 20))

sheet.save('assets/urunler_contact_sheet.jpg', quality=85)
print('Saved assets/urunler_contact_sheet.jpg')
