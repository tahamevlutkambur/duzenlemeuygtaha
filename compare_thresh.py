import json, os
from PIL import Image
import numpy as np

with open('products_catalog.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    im = Image.open(p['photo_png'])
    a = np.array(im)[:, :, 3]
    y10, x10 = np.where(a > 10)
    y25, x25 = np.where(a > 25)
    w10, h10 = (x10.max()-x10.min(), y10.max()-y10.min()) if len(y10) else (0,0)
    w25, h25 = (x25.max()-x25.min(), y25.max()-y25.min()) if len(y25) else (0,0)
    if abs(w10 - w25) > 100 or abs(h10 - h25) > 100:
        print(f"{p['code']:10} DIFFERENCE: thresh10=({w10},{h10}) vs thresh25=({w25},{h25})")
