import os, json, glob
from PIL import Image

with open('products_catalog.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Intervals definition
intervals = [
    ('30P01', ['DSCF0319', 'DSCF0320', 'DSCF0321', 'DSCF0322'], 'DSCF0323'),
    ('50P01', ['DSCF0324', 'DSCF0325', 'DSCF0326'], 'DSCF0327'),
    ('70P01', ['DSCF0328', 'DSCF0329', 'DSCF0330'], 'DSCF0331'),
    ('50P02', ['DSCF0332', 'DSCF0333', 'DSCF0334', 'DSCF0335', 'DSCF0336'], 'DSCF0337'),
    ('100P1_S', ['DSCF0338'], 'DSCF0339'),
    ('100P1_F', ['DSCF0340'], 'DSCF0341'),
    ('150P1_S', ['DSCF0342', 'DSCF0343', 'DSCF0344'], 'DSCF0345'),
    ('45P01', ['DSCF0360'], 'DSCF0361'),
    ('100P2_F', ['DSCF0416', 'DSCF0417', 'DSCF0418'], 'DSCF0419'),
    ('100P2_S', ['DSCF0420', 'DSCF0421'], 'DSCF0422'),
    ('150P1_F', ['DSCF0423', 'DSCF0424', 'DSCF0425', 'DSCF0426', 'DSCF0427'], 'DSCF0428'),
    ('200P1_S', ['DSCF0432', 'DSCF0433', 'DSCF0434'], 'DSCF0435'),
    ('200P1_F', ['DSCF0436', 'DSCF0437', 'DSCF0438', 'DSCF0439', 'DSCF0440'], 'DSCF0441'),
    ('400P1', ['DSCF0442', 'DSCF0443', 'DSCF0444'], 'DSCF0445'),
    ('20K01', ['DSCF0449', 'DSCF0450', 'DSCF0451', 'DSCF0452', 'DSCF0453', 'DSCF0454', 'DSCF0455'], 'DSCF0456'),
    ('20K02', ['DSCF0457', 'DSCF0458', 'DSCF0459', 'DSCF0460', 'DSCF0461', 'DSCF0462', 'DSCF0463', 'DSCF0464'], 'DSCF0465'),
    ('25K01', ['DSCF0480', 'DSCF0481', 'DSCF0482', 'DSCF0483', 'DSCF0484', 'DSCF0485', 'DSCF0486'], 'DSCF0487'),
    ('45K_50K', ['DSCF0488', 'DSCF0489', 'DSCF0490', 'DSCF0491', 'DSCF0492', 'DSCF0493'], 'DSCF0494'),
    ('10C01', ['DSCF0497', 'DSCF0498'], 'DSCF0499'),
    ('50C01', ['DSCF0500', 'DSCF0501'], 'DSCF0502'),
    ('100C1S', ['DSCF0503', 'DSCF0504'], 'DSCF0505'),
    ('200C1D', ['DSCF0506', 'DSCF0507', 'DSCF0508'], 'DSCF0510'),
    ('100C1D', ['DSCF0511', 'DSCF0512', 'DSCF0513'], 'DSCF0514'),
    ('200C2D', ['DSCF0515', 'DSCF0516'], 'DSCF0517'),
    ('100C2S', ['DSCF0518', 'DSCF0519'], 'DSCF0520'),
    ('200C3D', ['DSCF0521', 'DSCF0522'], 'DSCF0523'),
    ('250C1D', ['DSCF0524', 'DSCF0525', 'DSCF0526', 'DSCF0527', 'DSCF0528', 'DSCF0529', 'DSCF0530'], 'DSCF0531'),
]

out = []
for p in products:
    code = p['code']
    best = p['best_photo'].replace('.png', '')
    cap = p['cap_type']
    vol = p['volume']
    name = p['name']
    
    # find interval
    int_match = None
    for item in intervals:
        if best in item[1]:
            int_match = item
            break
            
    all_photos = int_match[1] if int_match else [best]
    note = int_match[2] if int_match else 'N/A'
    
    out.append({
        'code': code,
        'name': name,
        'volume': vol,
        'cap': cap,
        'best_photo': p['best_photo'],
        'photo_file_png': f"seffaf_png/{p['best_photo']}",
        'photo_file_jpg': f"beyaz_arka_plan/{best}.jpg",
        'all_photos_in_batch': [f"{x}.png" for x in all_photos],
        'note_card': f"{note}.JPG"
    })

with open('user_mockup_guide.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"Generated guide for {len(out)} products.")
