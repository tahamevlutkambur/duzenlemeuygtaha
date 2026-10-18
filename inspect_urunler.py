import glob, os
from PIL import Image

files = sorted(glob.glob('ürünler/*.jpg'))
print(f"Total files in ürünler: {len(files)}")

# Let's inspect the files
for i, f in enumerate(files):
    img = Image.open(f)
    print(f"{i+1:02d}. {os.path.basename(f)} - Size: {img.size}")
