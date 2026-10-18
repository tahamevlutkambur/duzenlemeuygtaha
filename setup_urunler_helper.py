import os
import json

base_dir = r"C:\Users\Taha\Pictures\kolonya"

# Variant-level mapping of all 28 uploaded Gemini dual-mockups
variant_mockups = {
    # PET SERİSİ
    "30P01F": "ürünler/Gemini_Generated_Image_86yzz386yzz386yz.jpg",     # 30 ml Flip-top
    "30P01S": "ürünler/Gemini_Generated_Image_z60n3dz60n3dz60n.jpg",     # 30 ml Sprey
    "45P01F": "ürünler/Gemini_Generated_Image_5me3v25me3v25me3.jpg",     # 45 ml Yassı Flip-top
    "50P01S": "ürünler/Gemini_Generated_Image_6n0dw16n0dw16n0d.jpg",     # 50 ml Yuvarlak Sprey
    "50P01F": "ürünler/Gemini_Generated_Image_86yzz386yzz386yz.jpg",     # 50 ml Yuvarlak Flip-top alternatif
    "50P02F": "ürünler/Gemini_Generated_Image_3xoiuh3xoiuh3xoi.jpg",     # 50 ml Kavisli Flip-top
    "50P02S": "ürünler/Gemini_Generated_Image_3xoiuh3xoiuh3xoi (3).jpg", # 50 ml Kavisli Sprey
    "70P01F": "ürünler/Gemini_Generated_Image_3xoiuh3xoiuh3xoi (1).jpg", # 70 ml Prizma Flip-top
    "70P01S": "ürünler/Gemini_Generated_Image_3xoiuh3xoiuh3xoi (3).jpg", # 70 ml Prizma Sprey
    "100P1F": "ürünler/Gemini_Generated_Image_t640x9t640x9t640.jpg",     # 100 ml Yuvarlak Flip-top
    "100P1S": "ürünler/Gemini_Generated_Image_t640x9t640x9t640 (1).jpg", # 100 ml Yuvarlak Sprey
    "100P2S": "ürünler/Gemini_Generated_Image_mb3jhdmb3jhdmb3j.jpg",     # 100 ml Yassı Sprey
    "100P2F": "ürünler/Gemini_Generated_Image_5me3v25me3v25me3.jpg",     # 100 ml Yassı Flip-top
    "150P1S": "ürünler/Gemini_Generated_Image_86yzz386yzz386yz (1).jpg", # 150 ml Yuvarlak Sprey
    "150P1F": "ürünler/Gemini_Generated_Image_t640x9t640x9t640.jpg",     # 150 ml Yuvarlak Flip-top
    "200P1F": "ürünler/Gemini_Generated_Image_3xoiuh3xoiuh3xoi (2).jpg", # 200 ml Yuvarlak Flip-top
    "200P1S": "ürünler/Gemini_Generated_Image_mb3jhdmb3jhdmb3j (3).jpg", # 200 ml Yuvarlak Sprey
    "400P1F": "ürünler/Gemini_Generated_Image_3xoiuh3xoiuh3xoi (3).jpg", # 400 ml Dikdörtgen Flip-top

    # SLİM CEP SERİSİ
    "20K01S": "ürünler/Gemini_Generated_Image_qyoaqvqyoaqvqyoa.jpg",     # 20 ml Slim Klasik Kart
    "20K02S": "ürünler/Gemini_Generated_Image_ab5yiiab5yiiab5y.jpg",     # 20 ml Slim Klipsli Kart
    "25K01S": "ürünler/Gemini_Generated_Image_ab5yiiab5yiiab5y (1).jpg", # 25 ml Slim Üçgen
    "45K01S": "ürünler/Gemini_Generated_Image_mb3jhdmb3jhdmb3j (1).jpg", # 45 ml Slim Medium
    "50K01S": "ürünler/Gemini_Generated_Image_mb3jhdmb3jhdmb3j (2).jpg", # 50 ml Slim Maxi

    # KRİSTAL CAM SERİSİ
    "10C01S": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp.jpg",     # 10 ml Pen Cam Sprey
    "50C01S": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (1).jpg", # 50 ml Linea Cam Sprey
    "100C1S": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (2).jpg", # 100 ml Linea Cam Altın Sprey
    "100C1D": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (3).jpg", # 100 ml Diamond Cam Altın Dökme
    "200C1D": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (4).jpg", # 200 ml Diamond Cam Dökme
    "200C1D_ALT": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (5).jpg", # Diamond Cam alternatif
    "100C2S": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (6).jpg", # 100 ml Riga Cam Siyah Sprey
    "200C2D": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (7).jpg", # 200 ml Riga Cam Altın Dökme
    "200C3D": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (8).jpg", # 200 ml Prizma Cam Dökme
    "250C1D": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (9).jpg", # 250 ml Signature Cam Altın Kapak
}

# Family-level fallback map
family_mockup_map = {
    "30P01": "ürünler/Gemini_Generated_Image_86yzz386yzz386yz.jpg",
    "45P01": "ürünler/Gemini_Generated_Image_5me3v25me3v25me3.jpg",
    "50P01": "ürünler/Gemini_Generated_Image_6n0dw16n0dw16n0d.jpg",
    "50P02": "ürünler/Gemini_Generated_Image_3xoiuh3xoiuh3xoi.jpg",
    "70P01": "ürünler/Gemini_Generated_Image_3xoiuh3xoiuh3xoi (1).jpg",
    "100P1": "ürünler/Gemini_Generated_Image_t640x9t640x9t640.jpg",
    "100P2": "ürünler/Gemini_Generated_Image_mb3jhdmb3jhdmb3j.jpg",
    "150P1": "ürünler/Gemini_Generated_Image_86yzz386yzz386yz (1).jpg",
    "200P1": "ürünler/Gemini_Generated_Image_mb3jhdmb3jhdmb3j (3).jpg",
    "400P1": "ürünler/Gemini_Generated_Image_3xoiuh3xoiuh3xoi (3).jpg",
    "20K01": "ürünler/Gemini_Generated_Image_qyoaqvqyoaqvqyoa.jpg",
    "20K02": "ürünler/Gemini_Generated_Image_ab5yiiab5yiiab5y.jpg",
    "25K01": "ürünler/Gemini_Generated_Image_ab5yiiab5yiiab5y (1).jpg",
    "45K01": "ürünler/Gemini_Generated_Image_mb3jhdmb3jhdmb3j (1).jpg",
    "50K01": "ürünler/Gemini_Generated_Image_mb3jhdmb3jhdmb3j (2).jpg",
    "10C01": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp.jpg",
    "50C01": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (1).jpg",
    "100C1": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (2).jpg",
    "100C2": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (6).jpg",
    "200C1": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (4).jpg",
    "200C2": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (7).jpg",
    "200C3": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (8).jpg",
    "250C1": "ürünler/Gemini_Generated_Image_ydfpdfydfpdfydfp (9).jpg",
}

# Color palettes per cap / body type
cap_color_options = {
    "flip_top": [
        {"name": "Siyah", "hex": "#1E293B"},
        {"name": "Beyaz", "hex": "#FFFFFF", "border": True},
        {"name": "Şeffaf", "hex": "#CBD5E1"},
        {"name": "Kırmızı", "hex": "#DC2626"},
        {"name": "Lacivert", "hex": "#1E3A8A"}
    ],
    "sprey": [
        {"name": "Siyah Başlık", "hex": "#1E293B"},
        {"name": "Beyaz Başlık", "hex": "#FFFFFF", "border": True},
        {"name": "Şeffaf Başlık", "hex": "#CBD5E1"}
    ],
    "slim": [
        {"name": "Mat Siyah", "hex": "#1E293B"},
        {"name": "Opak Beyaz", "hex": "#FFFFFF", "border": True},
        {"name": "Buzlu Şeffaf", "hex": "#94A3B8"}
    ],
    "cam_sprey": [
        {"name": "Parlak Gold (Altın)", "hex": "#D4AF37"},
        {"name": "Gümüş (Krom)", "hex": "#CBD5E1"},
        {"name": "Mat Siyah", "hex": "#1E293B"}
    ],
    "cam_dokme": [
        {"name": "Lüks Altın Kapak", "hex": "#D4AF37"},
        {"name": "Gümüş Kapak", "hex": "#CBD5E1"}
    ]
}

def get_cap_colors_for_variant(var_code, cat):
    if "K" in var_code:
        return cap_color_options["slim"]
    elif "C" in var_code:
        if "D" in var_code:
            return cap_color_options["cam_dokme"]
        return cap_color_options["cam_sprey"]
    elif "F" in var_code:
        return cap_color_options["flip_top"]
    else:
        return cap_color_options["sprey"]

def get_visual_for_variant(var_code, fam_id):
    # 1. User mockup
    for ext in ['.png', '.jpg']:
        u1 = os.path.join(base_dir, "kullanici_mockuplari", f"{var_code}{ext}")
        if os.path.exists(u1):
            return f"kullanici_mockuplari/{var_code}{ext}", True
            
    # 2. Variant uploaded mockup
    if var_code in variant_mockups and os.path.exists(os.path.join(base_dir, variant_mockups[var_code])):
        return variant_mockups[var_code], False
        
    # 3. Family uploaded mockup
    if fam_id in family_mockup_map and os.path.exists(os.path.join(base_dir, family_mockup_map[fam_id])):
        return family_mockup_map[fam_id], False
        
    # 4. Fallback crop
    fallback = f"assets/cropped_mockups/crop_{var_code}_mock.png"
    if os.path.exists(os.path.join(base_dir, fallback)):
        return fallback, False
    return f"assets/cropped_products/crop_{var_code}_orig.png", False

print("Setup helper updated with all 28 mockups and color variety support.")
