import os
import glob
from PIL import Image

# Let's inspect the text/note on each note image
# Let's print out what files exist in assets/note_crops
crops = sorted(glob.glob('assets/note_crops/*.JPG'))
print(f"Total note crop files: {len(crops)}")

# Let's make an overview contact sheet of all notes so we can view them easily
img_w, img_h = 300, 200
cols = 5
rows = (len(crops) + cols - 1) // cols

sheet = Image.new('RGB', (cols * img_w, rows * img_h), (240, 240, 240))

from PIL import ImageDraw, ImageFont
draw = ImageDraw.Draw(sheet)

for idx, cp in enumerate(crops):
    try:
        im = Image.open(cp)
        im.thumbnail((img_w - 20, img_h - 40))
        r = idx // cols
        c = idx % cols
        x = c * img_w + 10
        y = r * img_h + 30
        sheet.paste(im, (x, y))
        draw.text((c * img_w + 10, r * img_h + 5), os.path.basename(cp), fill=(0, 0, 0))
    except Exception as e:
        print(f"Error {cp}: {e}")

sheet.save('assets/all_notes_contact_sheet.jpg', quality=85)
print("Saved assets/all_notes_contact_sheet.jpg")
