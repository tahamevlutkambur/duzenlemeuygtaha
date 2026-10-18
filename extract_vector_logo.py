import os
from PIL import Image
import numpy as np

base_dir = r"C:\Users\Taha\Pictures\kolonya"
guide_img = Image.open(os.path.join(base_dir, "assets", "brand_guide_35x.png"))
w, h = guide_img.size

# In brand_guide_35x.png:
# Box 2 is SLOGANLI KOYU RENK ZEMİN KULLANIMI
# Let's crop it tightly around the dark navy rectangle
crop_y1 = int(h * 0.615)
crop_y2 = int(h * 0.745)
crop_x1 = int(w * 0.222)
crop_x2 = int(w * 0.478)

box_crop = guide_img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
box_crop.save(os.path.join(base_dir, "assets", "box2_tight.png"))
print("Saved box2_tight.png, size:", box_crop.size)

# The background color is Promkol Navy (approx RGB 29, 41, 65)
arr = np.array(box_crop)
# Find pixels that are NOT the navy background
# Background color:
bg_r, bg_g, bg_b = arr[10, 10, 0], arr[10, 10, 1], arr[10, 10, 2]
print(f"Detected background color: RGB({bg_r}, {bg_g}, {bg_b})")

# Calculate color distance from the background
diff = np.sqrt(
    (arr[:, :, 0].astype(float) - bg_r)**2 +
    (arr[:, :, 1].astype(float) - bg_g)**2 +
    (arr[:, :, 2].astype(float) - bg_b)**2
)

# Any pixel with diff > 18 is part of the logo/slogan
mask = diff > 18
# Bounding box of content
y_indices, x_indices = np.where(mask)
min_y, max_y = y_indices.min(), y_indices.max()
min_x, max_x = x_indices.min(), x_indices.max()

pad = 10
min_y = max(0, min_y - pad)
max_y = min(arr.shape[0], max_y + pad)
min_x = max(0, min_x - pad)
max_x = min(arr.shape[1], max_x + pad)

content_arr = arr[min_y:max_y, min_x:max_x]
content_diff = diff[min_y:max_y, min_x:max_x]

# Create transparent RGBA image
rgba = np.zeros((content_arr.shape[0], content_arr.shape[1], 4), dtype=np.uint8)
# Colors
rgba[:, :, 0] = content_arr[:, :, 0]
rgba[:, :, 1] = content_arr[:, :, 1]
rgba[:, :, 2] = content_arr[:, :, 2]

# Smooth alpha transition
alpha = np.clip((content_diff - 12) * (255.0 / 25.0), 0, 255).astype(np.uint8)
rgba[:, :, 3] = alpha

logo_transparent = Image.fromarray(rgba, "RGBA")
out_logo_path = os.path.join(base_dir, "assets", "promkol_logo_vector_transparent.png")
logo_transparent.save(out_logo_path)
print(f"Saved transparent logo: {out_logo_path}, size: {logo_transparent.size}")
