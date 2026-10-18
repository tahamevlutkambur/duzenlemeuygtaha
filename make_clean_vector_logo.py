from PIL import Image
import numpy as np

img = Image.open('assets/navy_box2_perfect.png')
arr = np.array(img).astype(float)

navy = np.array([30.0, 43.0, 69.0])
# Distance from navy
diff = np.sqrt(np.sum((arr - navy)**2, axis=2))

# Logo pixels are clearly different from navy (diff > 15)
# Also exclude pure white border outside the navy rectangle if any
# The navy rectangle itself is where distance from navy is small (< 10)
# Content inside the navy rectangle:
is_navy_area = (diff < 20) | (diff > 25) # inside the box
# Content pixels:
content_mask = (diff > 25) & ~(arr[:,:,0]>240) # exclude top/outside white border if any

# Let's find content inside the navy box:
# Just take pixels where diff from navy is significant, but not the external white background:
# External white has arr[:,:,0]>240 & arr[:,:,1]>240 & arr[:,:,2]>240
is_ext_white = (arr[:,:,0] > 250) & (arr[:,:,1] > 250) & (arr[:,:,2] > 250)
logo_mask = (diff > 25) & ~is_ext_white

y_idx, x_idx = np.where(logo_mask)
min_x, max_x = x_idx.min(), x_idx.max()
min_y, max_y = y_idx.min(), y_idx.max()
print("Content bbox:", min_x, min_y, max_x, max_y)

# Crop with 15px padding
p = 15
crop_x1 = max(0, min_x - p)
crop_x2 = min(arr.shape[1], max_x + p)
crop_y1 = max(0, min_y - p)
crop_y2 = min(arr.shape[0], max_y + p)

cropped = arr[crop_y1:crop_y2, crop_x1:crop_x2]
c_diff = diff[crop_y1:crop_y2, crop_x1:crop_x2]

# Create transparent RGBA
rgba = np.zeros((cropped.shape[0], cropped.shape[1], 4), dtype=np.uint8)
rgba[:, :, 0] = np.clip(cropped[:, :, 0], 0, 255).astype(np.uint8)
rgba[:, :, 1] = np.clip(cropped[:, :, 1], 0, 255).astype(np.uint8)
rgba[:, :, 2] = np.clip(cropped[:, :, 2], 0, 255).astype(np.uint8)

# Smooth alpha calculation
# When diff < 8 -> alpha 0
# When diff > 30 -> alpha 255
alpha = np.clip((c_diff - 8) * (255.0 / 24.0), 0, 255).astype(np.uint8)
rgba[:, :, 3] = alpha

out_img = Image.fromarray(rgba, 'RGBA')
out_path = 'assets/promkol_logo_vector_transparent.png'
out_img.save(out_path)
print(f"Saved {out_path}, size: {out_img.size}")
