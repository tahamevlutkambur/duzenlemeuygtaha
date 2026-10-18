import glob, os
from PIL import Image

files = sorted(glob.glob('ürünler/*.jpg'))

# We want to identify which file belongs to which product code
# Let's inspect the files in detail
print("Mapping files in ürünler/:")
for f in files:
    name = os.path.basename(f)
    print(name)
