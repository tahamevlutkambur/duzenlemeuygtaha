import json
import os
import glob

with open('products_catalog.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products in catalog: {len(products)}")
for i, p in enumerate(products):
    print(f"{i+1:02d}. Code: {p['code']} | Name: {p['name']} | Vol: {p['volume']} | Cap: {p['cap_type']} | Best: {p['best_photo']}")
