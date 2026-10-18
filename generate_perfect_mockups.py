import os
import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

base_dir = r"C:\Users\Taha\Pictures\kolonya"
logo_navy_path = os.path.join(base_dir, "assets", "clean_extracted_logo.png")
logo_white_path = os.path.join(base_dir, "assets", "clean_logo_white.png")
logo_gold_path = os.path.join(base_dir, "assets", "clean_logo_gold.png")

logo_navy = Image.open(logo_navy_path).convert("RGBA")
logo_white = Image.open(logo_white_path).convert("RGBA")
logo_gold = Image.open(logo_gold_path).convert("RGBA")

# 32 Products Definition with precise photo matching & mockup styling
products_data = [
    # --- PET SERİSİ ---
    {
        "code": "30P01F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "30 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "Ergonomik açılır-kapanır flip-top kapak, dökme kullanım için sızdırmaz cep boyu tasarım.",
        "best_photo": "DSCF0320.png",
        "style": "white_label",
        "label_y_ratio": (0.45, 0.78),
        "logo_w_ratio": 0.48
    },
    {
        "code": "30P01S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "30 ml",
        "cap_type": "Sprey (S)",
        "material": "PET Plastik",
        "description": "Kompakt silindirik gövde, pratik cep boyu sprey mekanizması ile her an yanınızda.",
        "best_photo": "DSCF0322.png",
        "style": "white_label",
        "label_y_ratio": (0.47, 0.80),
        "logo_w_ratio": 0.48
    },
    {
        "code": "45P01F",
        "name": "YASSI FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "45 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "Yassı zarif şişe formu, geniş etiket baskı yüzeyi ile kurumsal logonuzu öne çıkarır.",
        "best_photo": "DSCF0360.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.40, 0.75),
        "logo_w_ratio": 0.55
    },
    {
        "code": "50P01F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "Klasik silindirik form, pratik açılır kapak ve zengin esans seçenekleriyle ideal promosyon.",
        "best_photo": "DSCF0324.png",
        "style": "white_label",
        "label_y_ratio": (0.43, 0.76),
        "logo_w_ratio": 0.48
    },
    {
        "code": "50P01S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "cap_type": "Sprey (S)",
        "material": "PET Plastik",
        "description": "Yüksek püskürtme performanslı mikro sprey başlık, şık ve kullanışlı 50 ml silindirik şişe.",
        "best_photo": "DSCF0326.png",
        "style": "white_label",
        "label_y_ratio": (0.45, 0.78),
        "logo_w_ratio": 0.48
    },
    {
        "code": "50P02F",
        "name": "KAVİSLİ FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "Özel bombeli kavisli şişe tasarımı, elde rahat tutuş ve modern estetik görünüm.",
        "best_photo": "DSCF0333.png",
        "style": "white_label",
        "label_y_ratio": (0.42, 0.75),
        "logo_w_ratio": 0.48
    },
    {
        "code": "50P02S",
        "name": "KAVİSLİ SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "cap_type": "Sprey (S)",
        "material": "PET Plastik",
        "description": "Dinamik kavisli hatlar, ince sisleme sprey başlığı ve uzun ömürlü kullanım imkanı.",
        "best_photo": "DSCF0332.png",
        "style": "white_label",
        "label_y_ratio": (0.44, 0.77),
        "logo_w_ratio": 0.48
    },
    {
        "code": "70P01F",
        "name": "PRİZMA FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "70 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "Göz alıcı prizmatik gövde yapısı, dökme flip-top kapak ile araç ve ofis için ideal.",
        "best_photo": "DSCF0328.png",
        "style": "white_label",
        "label_y_ratio": (0.42, 0.76),
        "logo_w_ratio": 0.48
    },
    {
        "code": "70P01S",
        "name": "PRİZMA SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "70 ml",
        "cap_type": "Sprey (S)",
        "material": "PET Plastik",
        "description": "Prizma geometrik şişe, homojen dağılım sağlayan sprey mekanizması ve geniş etiket alanı.",
        "best_photo": "DSCF0330.png",
        "style": "white_label",
        "label_y_ratio": (0.44, 0.78),
        "logo_w_ratio": 0.48
    },
    {
        "code": "100P1F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "100 ml geniş hacim, sızdırmaz conta mekanizmalı flip-top kapak, yüksek marka görünürlüğü.",
        "best_photo": "DSCF0340.png",
        "style": "white_label",
        "label_y_ratio": (0.40, 0.75),
        "logo_w_ratio": 0.48
    },
    {
        "code": "100P1S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "cap_type": "Sprey (S)",
        "material": "PET Plastik",
        "description": "Geniş hacimli silindirik 100 ml sprey şişe, ferahlatıcı kullanım ve ekonomik promosyon çözümü.",
        "best_photo": "DSCF0338.png",
        "style": "white_label",
        "label_y_ratio": (0.42, 0.77),
        "logo_w_ratio": 0.48
    },
    {
        "code": "100P2F",
        "name": "YASSI FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "İnce yassı gövde mimarisi, çanta ve cepte taşımaya uygun ergonomik form.",
        "best_photo": "DSCF0417.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.38, 0.72),
        "logo_w_ratio": 0.55
    },
    {
        "code": "100P2S",
        "name": "YASSI SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "cap_type": "Sprey (S)",
        "material": "PET Plastik",
        "description": "Yassı formda 100 ml sprey çözümü, geniş ön baskı yüzeyiyle logonuz için maksimum prestij.",
        "best_photo": "DSCF0420.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.40, 0.74),
        "logo_w_ratio": 0.55
    },
    {
        "code": "150P1F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "150 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "Ofis masaları ve karşılama bankoları için ideal 150 ml boyut, uzun süreli reklam etkisi.",
        "best_photo": "DSCF0423.png",
        "style": "white_label",
        "label_y_ratio": (0.38, 0.72),
        "logo_w_ratio": 0.48
    },
    {
        "code": "150P1S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "150 ml",
        "cap_type": "Sprey (S)",
        "material": "PET Plastik",
        "description": "Yüksek debili sprey başlığı, şeffaf gövdede ferah esans rengi, güçlü kurumsal etki.",
        "best_photo": "DSCF0342.png",
        "style": "white_label",
        "label_y_ratio": (0.40, 0.74),
        "logo_w_ratio": 0.48
    },
    {
        "code": "200P1S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "200 ml",
        "cap_type": "Sprey (S)",
        "material": "PET Plastik",
        "description": "200 ml büyük boy sprey, kurumsal etkinlikler ve VIP hediye paketleri için zengin içerik.",
        "best_photo": "DSCF0432.png",
        "style": "white_label",
        "label_y_ratio": (0.38, 0.72),
        "logo_w_ratio": 0.48
    },
    {
        "code": "200P1F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "200 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "Ekonomik ve dayanıklı 200 ml gövde, açılır kapak ve geniş renkli etiket alanı.",
        "best_photo": "DSCF0436.png",
        "style": "white_label",
        "label_y_ratio": (0.38, 0.72),
        "logo_w_ratio": 0.48
    },
    {
        "code": "400P1F",
        "name": "DİKDÖRTGEN FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "400 ml",
        "cap_type": "Flip-Top (F)",
        "material": "PET Plastik",
        "description": "Maksimum hacim, sağlam dikdörtgen taban, mağaza ve showroom karşılama alanları için.",
        "best_photo": "DSCF0442.png",
        "style": "white_label",
        "label_y_ratio": (0.35, 0.70),
        "logo_w_ratio": 0.60
    },

    # --- SLİM & KART SERİSİ ---
    {
        "code": "20K01S",
        "name": "SLİM KLASİK SPREY KOLONYA",
        "category": "Slim & Kart Serisi",
        "volume": "20 ml",
        "cap_type": "Sprey (S)",
        "material": "Polietilen Kredi Kartı Formu",
        "description": "Cep ve cüzdan boyu kredi kartı formatı, çift taraflı tam alan UV baskıya uygun.",
        "best_photo": "DSCF0451.png",
        "style": "card_white_print",
        "label_y_ratio": (0.42, 0.85),
        "logo_w_ratio": 0.65
    },
    {
        "code": "20K02S",
        "name": "SLİM KAPAKLI SPREY KOLONYA",
        "category": "Slim & Kart Serisi",
        "volume": "20 ml",
        "cap_type": "Sprey (S)",
        "material": "Polietilen Slim",
        "description": "Kapaklı zarif tasarım, çanta içi sızdırmazlık güvenliği ve tekrar doldurulabilir gövde.",
        "best_photo": "DSCF0458.png",
        "style": "card_white_print",
        "label_y_ratio": (0.42, 0.85),
        "logo_w_ratio": 0.65
    },
    {
        "code": "25K01S",
        "name": "SLİM ÜÇGEN SPREY KOLONYA",
        "category": "Slim & Kart Serisi",
        "volume": "25 ml",
        "cap_type": "Sprey (S)",
        "material": "Polietilen Slim",
        "description": "Dinamik kavisli renkli başlık detayları, ergonomik cep tasarımı ve canlı renk seçenekleri.",
        "best_photo": "DSCF0480.png",
        "style": "card_navy_print",
        "label_y_ratio": (0.45, 0.85),
        "logo_w_ratio": 0.60
    },
    {
        "code": "45K01S",
        "name": "SLİM MEDİUM SPREY KOLONYA",
        "category": "Slim & Kart Serisi",
        "volume": "45 ml",
        "cap_type": "Sprey (S)",
        "material": "Polietilen Slim",
        "description": "Genişletilmiş 45 ml ince profil, dayanıklı klipsli başlık ve modern kurumsal stil.",
        "best_photo": "DSCF0488.png",
        "style": "card_navy_print",
        "label_y_ratio": (0.40, 0.82),
        "logo_w_ratio": 0.65
    },
    {
        "code": "50K01S",
        "name": "SLİM MAXİ SPREY KOLONYA",
        "category": "Slim & Kart Serisi",
        "volume": "50 ml",
        "cap_type": "Sprey (S)",
        "material": "Polietilen Slim",
        "description": "50 ml kapasiteli cep boyu devrim, şık kavisli mat gövde, premium promosyon prestiji.",
        "best_photo": "DSCF0491.png",
        "style": "card_white_print",
        "label_y_ratio": (0.42, 0.85),
        "logo_w_ratio": 0.65
    },

    # --- KRİSTAL CAM SERİSİ ---
    {
        "code": "10C01S",
        "name": "PEN MİNİ CAM SPREY",
        "category": "Kristal Cam Serisi",
        "volume": "10 ml",
        "cap_type": "Sprey (S)",
        "material": "Kristal Cam & Metal Klips",
        "description": "Kalem tipi mini cam tüp, metal klipsli kapak, toplantı ve etkinlikler için lüks hediye.",
        "best_photo": "DSCF0497.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.35, 0.75),
        "logo_w_ratio": 0.70
    },
    {
        "code": "50C01S",
        "name": "LINEA 50 CAM SPREY",
        "category": "Kristal Cam Serisi",
        "volume": "50 ml",
        "cap_type": "Sprey (S)",
        "material": "Kristal Cam & Altın Başlık",
        "description": "Zarif dikey çizgili kalın cam taban, altın metalik sprey başlığı ile üst düzey şıklık.",
        "best_photo": "DSCF0500.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.38, 0.72),
        "logo_w_ratio": 0.55
    },
    {
        "code": "100C1S",
        "name": "LINEA 100 CAM SPREY",
        "category": "Kristal Cam Serisi",
        "volume": "100 ml",
        "cap_type": "Sprey (S)",
        "material": "Kristal Cam",
        "description": "100 ml ağır kristal cam gövde, premium esans dolumu, kalıcı ve unutulmaz bir jest.",
        "best_photo": "DSCF0503.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.38, 0.72),
        "logo_w_ratio": 0.55
    },
    {
        "code": "200C1D",
        "name": "DIAMOND 200 CAM DİKME",
        "category": "Kristal Cam Serisi",
        "volume": "200 ml",
        "cap_type": "Dökme / Dikme (D)",
        "material": "Kristal Cam",
        "description": "Göz alıcı elmas kesim 200 ml kristal cam şişe, salon ve makam odalarında vitrin ürünü.",
        "best_photo": "DSCF0506.png",
        "style": "glass_luxury_label",
        "label_y_ratio": (0.42, 0.74),
        "logo_w_ratio": 0.50
    },
    {
        "code": "100C1D",
        "name": "DIAMOND 100 CAM DİKME",
        "category": "Kristal Cam Serisi",
        "volume": "100 ml",
        "cap_type": "Dökme / Dikme (D)",
        "material": "Kristal Cam",
        "description": "Elmas kesim fasetli cam gövde, geleneksel Türk kolonyası dökme ritüeli için özel tıpa.",
        "best_photo": "DSCF0511.png",
        "style": "glass_luxury_label",
        "label_y_ratio": (0.42, 0.74),
        "logo_w_ratio": 0.50
    },
    {
        "code": "200C2D",
        "name": "RIGA 200 CAM DİKME",
        "category": "Kristal Cam Serisi",
        "volume": "200 ml",
        "cap_type": "Dökme / Dikme (D)",
        "material": "Kristal Cam",
        "description": "İskandinav Riga çizgileri, düz dikey hatlar ve modern cam işçiliği ile minimalist zarafet.",
        "best_photo": "DSCF0515.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.40, 0.72),
        "logo_w_ratio": 0.55
    },
    {
        "code": "100C2S",
        "name": "RIGA 100 CAM SPREY",
        "category": "Kristal Cam Serisi",
        "volume": "100 ml",
        "cap_type": "Sprey (S)",
        "material": "Kristal Cam",
        "description": "100 ml dikey çizgili silindirik cam sprey, modern mimari çizgiler ve kaliteli esans.",
        "best_photo": "DSCF0518.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.42, 0.74),
        "logo_w_ratio": 0.55
    },
    {
        "code": "200C3D",
        "name": "PRİZMA 200 CAM DİKME",
        "category": "Kristal Cam Serisi",
        "volume": "200 ml",
        "cap_type": "Dökme / Dikme (D)",
        "material": "Kristal Cam",
        "description": "Ağır piramit kristal cam taban, makam masalarında ağırlığını hissettiren hediye kolonya.",
        "best_photo": "DSCF0521.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.42, 0.74),
        "logo_w_ratio": 0.55
    },
    {
        "code": "250C1D",
        "name": "SIGNATURE 250 CAM DİKME",
        "category": "Kristal Cam Serisi",
        "volume": "250 ml",
        "cap_type": "Dökme / Dikme (D)",
        "material": "Kristal Cam",
        "description": "Koleksiyonun amiral gemisi, 250 ml anıt cam form, prestij ve kurumsal gücün simgesi.",
        "best_photo": "DSCF0524.png",
        "style": "transparent_navy",
        "label_y_ratio": (0.40, 0.72),
        "logo_w_ratio": 0.50
    }
]

print(f"Total products mapped: {len(products_data)}")

mock_dir = os.path.join(base_dir, "mockups")
os.makedirs(mock_dir, exist_ok=True)

# Generate mockups with high realism
for p in products_data:
    code = p["code"]
    photo_file = p["best_photo"]
    style = p["style"]
    
    in_path = os.path.join(base_dir, "seffaf_png", photo_file)
    if not os.path.exists(in_path):
        print(f"Error: {in_path} missing!")
        continue
        
    bottle = Image.open(in_path).convert("RGBA")
    b_arr = np.array(bottle)
    alpha = b_arr[:, :, 3]
    y_idx, x_idx = np.where(alpha > 25)
    if len(y_idx) == 0:
        continue
    y_min, y_max = y_idx.min(), y_idx.max()
    x_min, x_max = x_idx.min(), x_idx.max()
    
    bw = x_max - x_min
    bh = y_max - y_min
    
    y1_ratio, y2_ratio = p["label_y_ratio"]
    lbl_y1 = int(y_min + bh * y1_ratio)
    lbl_y2 = int(y_min + bh * y2_ratio)
    lbl_h = lbl_y2 - lbl_y1
    
    mockup = bottle.copy()
    
    if style == "white_label":
        # White wrap-around label like örnekbaskı.jpeg
        lbl_x1 = int(x_min + bw * 0.05)
        lbl_x2 = int(x_max - bw * 0.05)
        lbl_w = lbl_x2 - lbl_x1
        
        lbl_arr = np.zeros((lbl_h, lbl_w, 4), dtype=np.uint8)
        x_coords = np.linspace(-1, 1, lbl_w)
        cyl = np.sqrt(np.maximum(0, 1 - 0.65 * (x_coords ** 2)))
        
        for col in range(lbl_w):
            f = cyl[col]
            lbl_arr[:, col, 0] = int(246 * f)
            lbl_arr[:, col, 1] = int(248 * f)
            lbl_arr[:, col, 2] = int(248 * f)
            lbl_arr[:, col, 3] = 252 # opaque
            
        label_surf = Image.fromarray(lbl_arr)
        
        # Place logo
        lw = int(lbl_w * p["logo_w_ratio"])
        lh = int(logo_navy.height * (lw / logo_navy.width))
        logo_res = logo_navy.resize((lw, lh), Image.Resampling.LANCZOS)
        
        lx = (lbl_w - lw) // 2
        ly = (lbl_h - lh) // 2
        label_surf.alpha_composite(logo_res, (lx, ly))
        
        # Composite onto bottle
        # Mask by bottle alpha to perfectly hug contours
        temp_layer = Image.new("RGBA", bottle.size, (0, 0, 0, 0))
        temp_layer.paste(label_surf, (lbl_x1, lbl_y1))
        
        # Apply bottle alpha mask
        t_arr = np.array(temp_layer)
        t_arr[:, :, 3] = np.minimum(t_arr[:, :, 3], (alpha > 50).astype(np.uint8) * 255)
        masked_label = Image.fromarray(t_arr)
        
        mockup.alpha_composite(masked_label)
        
    elif style == "card_white_print":
        # Pure crisp white print on dark cards
        lw = int(bw * p["logo_w_ratio"])
        lh = int(logo_white.height * (lw / logo_white.width))
        logo_res = logo_white.resize((lw, lh), Image.Resampling.LANCZOS)
        
        lx = x_min + (bw - lw) // 2
        ly = lbl_y1 + (lbl_h - lh) // 2
        mockup.alpha_composite(logo_res, (lx, ly))
        
    elif style == "card_navy_print":
        # Crisp navy print on light/white cards
        lw = int(bw * p["logo_w_ratio"])
        lh = int(logo_navy.height * (lw / logo_navy.width))
        logo_res = logo_navy.resize((lw, lh), Image.Resampling.LANCZOS)
        
        lx = x_min + (bw - lw) // 2
        ly = lbl_y1 + (lbl_h - lh) // 2
        mockup.alpha_composite(logo_res, (lx, ly))
        
    elif style == "glass_luxury_label":
        # Diamond bottles with recessed glass pane: place crisp navy logo with subtle soft frosted white backing
        lw = int(bw * p["logo_w_ratio"])
        lh = int(logo_navy.height * (lw / logo_navy.width))
        
        # Frosted glass backplate
        pad_x, pad_y = int(lw * 0.15), int(lh * 0.15)
        pane_w, pane_h = lw + 2 * pad_x, lh + 2 * pad_y
        pane = Image.new("RGBA", (pane_w, pane_h), (255, 255, 255, 175))
        
        logo_res = logo_navy.resize((lw, lh), Image.Resampling.LANCZOS)
        pane.alpha_composite(logo_res, (pad_x, pad_y))
        
        lx = x_min + (bw - pane_w) // 2
        ly = lbl_y1 + (lbl_h - pane_h) // 2
        mockup.alpha_composite(pane, (lx, ly))
        
    else: # transparent_navy
        lw = int(bw * p["logo_w_ratio"])
        lh = int(logo_navy.height * (lw / logo_navy.width))
        logo_res = logo_navy.resize((lw, lh), Image.Resampling.LANCZOS)
        
        lx = x_min + (bw - lw) // 2
        ly = lbl_y1 + (lbl_h - lh) // 2
        mockup.alpha_composite(logo_res, (lx, ly))
        
    out_png = os.path.join(mock_dir, f"mock_{code}.png")
    mockup.save(out_png, format="PNG")
    
    # Also save white jpg
    white_bg = Image.new("RGB", mockup.size, (255, 255, 255))
    white_bg.paste(mockup, mask=mockup.split()[3])
    white_bg.save(os.path.join(mock_dir, f"mock_{code}.jpg"), quality=95)
    
    p["photo_png"] = f"seffaf_png/{photo_file}"
    p["photo_white"] = f"beyaz_arka_plan/{photo_file.replace('.png', '.jpg')}"
    p["mockup_png"] = f"mockups/mock_{code}.png"
    p["mockup_jpg"] = f"mockups/mock_{code}.jpg"
    print(f"Generated realistic mockup for {code} ({style})")

with open(os.path.join(base_dir, "products_catalog.json"), "w", encoding="utf-8") as f:
    json.dump(products_data, f, ensure_ascii=False, indent=2)

print("All 32 realistic mockups generated and catalog JSON updated!")
