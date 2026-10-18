import os, glob
from PIL import Image

files = sorted(glob.glob('drive-download-20261018T133157Z-1-001/*.JPG'))
print(f"Total raw photos: {len(files)}")

# Let's save a 150x100 thumbnail of EVERY single photo into assets/all_thumbs/
os.makedirs('assets/all_thumbs', exist_ok=True)

for f in files:
    name = os.path.basename(f)
    out_p = os.path.join('assets/all_thumbs', name)
    if not os.path.exists(out_p):
        im = Image.open(f)
        im.thumbnail((160, 110))
        im.save(out_p)

print("All thumbs created.")
