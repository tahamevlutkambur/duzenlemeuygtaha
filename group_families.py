import os, json, glob
from PIL import Image

# Let's inspect the products and their cap photos
with open('products_catalog.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Group products by bottle model / family (e.g. 30P01, 50P01, 50P02, 70P01, 100P1, 100P2, 150P1, 200P1, etc.)
families = {}
for p in products:
    # Family is code without F/S/D
    fam_code = p['code'][:-1]
    if fam_code not in families:
        families[fam_code] = {
            'fam_code': fam_code,
            'name': p['name'].replace('FLİPTOP ', '').replace('SPREY ', '').replace('DİKME ', '').replace('FLPTOP ', '').replace('DKME ', ''),
            'volume': p['volume'],
            'category': p['category'],
            'material': p['material'],
            'variants': []
        }
    families[fam_code]['variants'].append(p)

print(f"Total bottle families: {len(families)}")
for fam_code, data in families.items():
    print(f"\n=== {fam_code} ({data['volume']} - {data['name']}) ===")
    for v in data['variants']:
        print(f"  Variant [{v['code']}] - Cap: {v['cap_type']} -> Photo: {v['best_photo']} (in seffaf_png/{v['best_photo']})")
