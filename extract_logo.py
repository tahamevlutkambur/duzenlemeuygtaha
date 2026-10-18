import os
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

# Load kullancağın foto.jpeg
logo_src = Image.open('örnek sizin markanız/kullancağın foto.jpeg')
# Extract logo bounding box
arr = np.array(logo_src)
gray = 0.299 * arr[:,:,0] + 0.587 * arr[:,:,1] + 0.114 * arr[:,:,2]
mask = gray < 240
y, x = np.where(mask)
logo_crop = logo_src.crop((x.min()-10, y.min()-10, x.max()+10, y.max()+10))

# Make logo transparent (white background -> transparent)
logo_rgba = logo_crop.convert("RGBA")
l_data = np.array(logo_rgba)
# Distance from white
dist = np.maximum(np.maximum(255 - l_data[:,:,0], 255 - l_data[:,:,1]), 255 - l_data[:,:,2])
# Alpha is proportional to darkness
alpha = np.clip(dist * 2.5, 0, 255).astype(np.uint8)
# Keep original navy color
navy_logo = np.zeros_like(l_data)
navy_logo[:,:,0] = 28
navy_logo[:,:,1] = 39
navy_logo[:,:,2] = 59
navy_logo[:,:,3] = alpha
clean_logo_img = Image.fromarray(navy_logo)
clean_logo_img.save('assets/clean_extracted_logo.png')
print("Clean logo extracted and saved!")
