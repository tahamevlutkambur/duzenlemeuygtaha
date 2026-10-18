import json

with open('user_mockup_guide.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("KOD      | HACİM  | ÜRÜN ADI                     | KAPAK TÜRÜ       | SEFFAF PNG DOSYASI    | BEYAZ JPG DOSYASI")
print("-" * 105)
for x in data:
    print(f"{x['code']:<8} | {x['volume']:<6} | {x['name']:<28} | {x['cap']:<16} | {x['photo_file_png']:<22} | {x['photo_file_jpg']}")
