import os
import json

base_dir = r"C:\Users\Taha\Pictures\kolonya"

manifest = {
    'urunler': [],
    'mockups': [],
    'assets': [],
    'seffaf_png': [],
    'beyaz_arka_plan': [],
    'kullanici': []
}

def scan_dir(folder, key, clean_rel=None):
    p = os.path.join(base_dir, folder)
    if not os.path.exists(p): return
    for f in sorted(os.listdir(p)):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.svg')):
            rel = f"{clean_rel or folder}/{f}"
            manifest[key].append({
                'name': f,
                'path': rel,
                'category': key
            })

scan_dir('ürünler', 'urunler')
scan_dir('mockups', 'mockups')
scan_dir('assets', 'assets')
scan_dir('assets/seffaf_web', 'seffaf_png')
scan_dir('assets/beyaz_web', 'beyaz_arka_plan')
scan_dir('assets/kullanici', 'kullanici')

out_p = os.path.join(base_dir, 'assets_manifest.json')
with open(out_p, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("Updated assets_manifest.json successfully!")
for k, v in manifest.items():
    print(f"  {k}: {len(v)} items")
