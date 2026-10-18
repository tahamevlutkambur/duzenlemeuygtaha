import os
import json
from PIL import Image, ImageDraw, ImageOps
import numpy as np

# Directory paths
base_dir = r"C:\Users\Taha\Pictures\kolonya"
seffaf_dir = os.path.join(base_dir, "seffaf_png")
mockups_dir = os.path.join(base_dir, "mockups")
os.makedirs(mockups_dir, exist_ok=True)

# Load logos
logo_navy_path = os.path.join(base_dir, "assets", "logo_transparent_navy.png")
logo_white_path = os.path.join(base_dir, "assets", "logo_transparent_white.png")

logo_navy = Image.open(logo_navy_path).convert("RGBA")
logo_white = Image.open(logo_white_path).convert("RGBA")

# Complete Product Dictionary: 32 Products
products_meta = [
    # --- PET SERİSİ ---
    {
        "code": "30P01S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "30 ml",
        "cap_type": "Sprey Başlık (S)",
        "material": "PET Plastik",
        "description": "Kompakt silindirik gövde, pratik cep boyu sprey mekanizması ile her an yanınızda.",
        "best_photo": "DSCF0374.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.45
    },
    {
        "code": "30P01F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "30 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "Ergonomik açılır-kapanır flip-top kapak, dökme kullanım için ideal sızdırmaz tasarım.",
        "best_photo": "DSCF0320.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.48
    },
    {
        "code": "45P01F",
        "name": "YASSI FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "45 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "Yassı zarif şişe formu, geniş etiket baskı yüzeyi ile kurumsal logonuzu öne çıkarır.",
        "best_photo": "DSCF0380.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.50
    },
    {
        "code": "50P01F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "Popüler 50 ml silindirik form, pratik flip-top kapak ile ekonomik ve şık promosyon hediyesi.",
        "best_photo": "DSCF0383.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.48
    },
    {
        "code": "50P01S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "cap_type": "Sprey Başlık (S)",
        "material": "PET Plastik",
        "description": "Yüksek performanslı sprey pompası ve şeffaf koruyucu kapağı ile ferahlatıcı kullanım.",
        "best_photo": "DSCF0387.png",
        "is_dark": False,
        "logo_y_ratio": 0.62,
        "logo_w_ratio": 0.46
    },
    {
        "code": "50P02F",
        "name": "KAVİSLİ FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "Modern kavisli omuz hattı, ele oturan ergonomik gövde ve sızdırmaz kapak mekanizması.",
        "best_photo": "DSCF0333.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.50
    },
    {
        "code": "50P02S",
        "name": "KAVİSLİ SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "cap_type": "Sprey Başlık (S)",
        "material": "PET Plastik",
        "description": "Zarif kavisli tasarım, ince sis püskürtme özellikli kaliteli sprey mekanizması.",
        "best_photo": "DSCF0391.png",
        "is_dark": False,
        "logo_y_ratio": 0.62,
        "logo_w_ratio": 0.48
    },
    {
        "code": "70P01F",
        "name": "PRİZMA FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "70 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "Geometrik prizmatik form, düz yüzeyleri sayesinde etiket ve serigrafi baskıda kusursuz netlik.",
        "best_photo": "DSCF0401.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.52
    },
    {
        "code": "70P01S",
        "name": "PRİZMA SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "70 ml",
        "cap_type": "Sprey Başlık (S)",
        "material": "PET Plastik",
        "description": "Köşeli modern gövde yapısı ve kaliteli sprey başlığı ile prestijli görünüm.",
        "best_photo": "DSCF0405.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.50
    },
    {
        "code": "100P1F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "Geniş hacimli silindirik gövde, masaüstü ve ofis kullanımı için en çok tercih edilen boyut.",
        "best_photo": "DSCF0410.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.50
    },
    {
        "code": "100P1S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "cap_type": "Sprey Başlık (S)",
        "material": "PET Plastik",
        "description": "100 ml kapasiteli güçlü sprey başlık, uzun ömürlü ve bereketli kurumsal hediye.",
        "best_photo": "DSCF0413.png",
        "is_dark": False,
        "logo_y_ratio": 0.62,
        "logo_w_ratio": 0.48
    },
    {
        "code": "100P2F",
        "name": "YASSI FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "Geniş ön yüzeyli yassı tasarım, logonuzun ve kurumsal mesajınızın en net sergilendiği model.",
        "best_photo": "DSCF0417.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.52
    },
    {
        "code": "100P2S",
        "name": "YASSI SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "cap_type": "Sprey Başlık (S)",
        "material": "PET Plastik",
        "description": "Yassı estetik hatlar, sprey başlık konforu ile premium promosyon etkisi yaratır.",
        "best_photo": "DSCF0420.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.50
    },
    {
        "code": "150P1F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "150 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "150 ml dolgun hacim, şık yuvarlak form ve dayanıklı kapak yapısı.",
        "best_photo": "DSCF0425.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.50
    },
    {
        "code": "150P1S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "150 ml",
        "cap_type": "Sprey Başlık (S)",
        "material": "PET Plastik",
        "description": "Geniş hacim, güçlü atomizer sprey püskürtme ile ferahlığın kalıcı temsilcisi.",
        "best_photo": "DSCF0429.png",
        "is_dark": False,
        "logo_y_ratio": 0.62,
        "logo_w_ratio": 0.48
    },
    {
        "code": "200P1S",
        "name": "YUVARLAK SPREY KOLONYA",
        "category": "PET Serisi",
        "volume": "200 ml",
        "cap_type": "Sprey Başlık (S)",
        "material": "PET Plastik",
        "description": "200 ml yüksek kapasite, ev ve iş yeri kullanımına uygun heybetli sprey modeli.",
        "best_photo": "DSCF0433.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.48
    },
    {
        "code": "200P1F",
        "name": "YUVARLAK FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "200 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "200 ml klasik dökme kolonya şişesi, flip-top kapak pratikliği ile buluştu.",
        "best_photo": "DSCF0438.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.48
    },
    {
        "code": "400P1F",
        "name": "DİKDÖRTGEN FLİPTOP KOLONYA",
        "category": "PET Serisi",
        "volume": "400 ml",
        "cap_type": "Flip-Top Kapak (F)",
        "material": "PET Plastik",
        "description": "400 ml mega hacim, kurumsal ofis ve karşılama bankoları için prestijli dikdörtgen form.",
        "best_photo": "DSCF0443.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.52
    },

    # --- SLİM SERİSİ ---
    {
        "code": "20K01S",
        "name": "SLİM KLASİK SPREY KOLONYA",
        "category": "Slim Serisi",
        "volume": "20 ml",
        "cap_type": "Entegre Sprey (S)",
        "material": "Polietilen Kredi Kartı Formu",
        "description": "Cep ve cüzdan boyu kredi kartı formatı, çift taraflı tam alan UV baskıya uygun.",
        "best_photo": "DSCF0451.png",
        "is_dark": True, # Dark bottle / navy body
        "logo_y_ratio": 0.55,
        "logo_w_ratio": 0.58
    },
    {
        "code": "20K02S",
        "name": "SLİM KAPAKLI SPREY KOLONYA",
        "category": "Slim Serisi",
        "volume": "20 ml",
        "cap_type": "Kapaklı Sprey (S)",
        "material": "Polietilen Slim",
        "description": "Kapaklı zarif tasarım, çanta içi sızdırmazlık güvenliği ve tekrar doldurulabilir gövde.",
        "best_photo": "DSCF0459.png",
        "is_dark": False,
        "logo_y_ratio": 0.55,
        "logo_w_ratio": 0.52
    },
    {
        "code": "25K01S",
        "name": "SLİM ÜÇGEN SPREY KOLONYA",
        "category": "Slim Serisi",
        "volume": "25 ml",
        "cap_type": "Renkli Başlık Sprey (S)",
        "material": "Polietilen Slim",
        "description": "Dinamik kavisli renkli başlık detayları, ergonomik cep tasarımı ve canlı renk seçenekleri.",
        "best_photo": "DSCF0482.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.54
    },
    {
        "code": "45K01S",
        "name": "SLİM MEDİUM SPREY KOLONYA",
        "category": "Slim Serisi",
        "volume": "45 ml",
        "cap_type": "Entegre Sprey (S)",
        "material": "Polietilen Slim",
        "description": "Orta boy slim sprey, geniş eliptik yüzeyiyle dikkat çekici kurumsal marka alanı sağlar.",
        "best_photo": "DSCF0485.png",
        "is_dark": False,
        "logo_y_ratio": 0.56,
        "logo_w_ratio": 0.52
    },
    {
        "code": "50K01S",
        "name": "SLİM MAXİ SPREY KOLONYA",
        "category": "Slim Serisi",
        "volume": "50 ml",
        "cap_type": "Entegre Sprey (S)",
        "material": "Polietilen Slim",
        "description": "50 ml yüksek kapasiteli ince tasarım, taşınabilirliği maksimum hacimle birleştirir.",
        "best_photo": "DSCF0490.png",
        "is_dark": True, # Dark/blue finish
        "logo_y_ratio": 0.55,
        "logo_w_ratio": 0.55
    },

    # --- CAM SERİSİ ---
    {
        "code": "10C01S",
        "name": "PEN MİNİ CAM SPREY",
        "category": "Cam Serisi",
        "volume": "10 ml",
        "cap_type": "Metalize Kalem Sprey (S)",
        "material": "Cam Şişe",
        "description": "İnce kalem formunda şeffaf cam tüp, gümüş metalize sprey başlığı ile üst düzey zarafet.",
        "best_photo": "DSCF0498.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.60
    },
    {
        "code": "50C01S",
        "name": "LİNEA 50 CAM SPREY",
        "category": "Cam Serisi",
        "volume": "50 ml",
        "cap_type": "Metalize Sprey Başlık (S)",
        "material": "Kristal Cam",
        "description": "Kristal parlaklığında kalın tabanlı cam, lüks krom sprey kapağı ile VIP hediye seçeneği.",
        "best_photo": "DSCF0500.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.48
    },
    {
        "code": "100C1S",
        "name": "LİNEA 100 CAM SPREY",
        "category": "Cam Serisi",
        "volume": "100 ml",
        "cap_type": "Metalize Sprey Başlık (S)",
        "material": "Kristal Cam",
        "description": "100 ml heybetli cam prizma, parlak metal kapağı ve asil duruşuyla üst yönetim hediyesi.",
        "best_photo": "DSCF0503.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.48
    },
    {
        "code": "100C1D",
        "name": "DIAMOND 100 CAM DİKME",
        "category": "Cam Serisi",
        "volume": "100 ml",
        "cap_type": "Tıpalı Dökme Kapak (D)",
        "material": "Kristal Cam",
        "description": "Elmas kesim fasetli cam gövde, geleneksel Türk kolonyası dökme ritüeli için özel tıpa.",
        "best_photo": "DSCF0512.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.50
    },
    {
        "code": "200C1D",
        "name": "DIAMOND 200 CAM DİKME",
        "category": "Cam Serisi",
        "volume": "200 ml",
        "cap_type": "Tıpalı Dökme Kapak (D)",
        "material": "Kristal Cam",
        "description": "Göz alıcı elmas kesim 200 ml kristal cam şişe, salon ve makam odalarında vitrin ürünü.",
        "best_photo": "DSCF0507.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.50
    },
    {
        "code": "100C2S",
        "name": "RIGA 100 CAM SPREY",
        "category": "Cam Serisi",
        "volume": "100 ml",
        "cap_type": "Metalize Sprey Başlık (S)",
        "material": "Kristal Cam",
        "description": "İskandinav Riga çizgileri, düz dikey hatlar ve modern cam işçiliği ile minimalist zarafet.",
        "best_photo": "DSCF0518.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.48
    },
    {
        "code": "200C2D",
        "name": "RIGA 200 CAM DİKME",
        "category": "Cam Serisi",
        "volume": "200 ml",
        "cap_type": "Tıpalı Dökme Kapak (D)",
        "material": "Kristal Cam",
        "description": "200 ml ağır tabanlı Riga camı, dökme kullanım için zarif tıpalı kapak sistemi.",
        "best_photo": "DSCF0515.png",
        "is_dark": False,
        "logo_y_ratio": 0.60,
        "logo_w_ratio": 0.48
    },
    {
        "code": "200C3D",
        "name": "PRİZMA 200 CAM DİKME",
        "category": "Cam Serisi",
        "volume": "200 ml",
        "cap_type": "Tıpalı Dökme Kapak (D)",
        "material": "Kristal Cam",
        "description": "Dörtgen keskin cam hatları, masif cam tabanı ile zamansız klasik dökme şişe.",
        "best_photo": "DSCF0521.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.50
    },
    {
        "code": "250C1D",
        "name": "SIGNATURE 250 CAM DİKME",
        "category": "Cam Serisi",
        "volume": "250 ml",
        "cap_type": "Tıpalı Dökme Kapak (D)",
        "material": "Kristal Cam",
        "description": "Koleksiyonun en prestijli modeli, 250 ml ihtişamlı cam kütlesi ve kusursuz optik berraklık.",
        "best_photo": "DSCF0527.png",
        "is_dark": False,
        "logo_y_ratio": 0.58,
        "logo_w_ratio": 0.50
    }
]

# Generate mockup for each product
for prod in products_meta:
    code = prod["code"]
    photo_file = prod["best_photo"]
    photo_path = os.path.join(seffaf_dir, photo_file)
    
    if not os.path.exists(photo_path):
        print(f"Warning: {photo_path} does not exist!")
        continue
        
    bottle = Image.open(photo_path).convert("RGBA")
    
    # Calculate bounding box of the bottle
    alpha = np.array(bottle)[:, :, 3]
    y_indices, x_indices = np.where(alpha > 15)
    if len(y_indices) == 0:
        continue
    x_min, x_max = x_indices.min(), x_indices.max()
    y_min, y_max = y_indices.min(), y_indices.max()
    
    bottle_w = x_max - x_min
    bottle_h = y_max - y_min
    center_x = (x_min + x_max) // 2
    center_y = y_min + int(bottle_h * prod["logo_y_ratio"])
    
    # Choose logo
    selected_logo = logo_white if prod["is_dark"] else logo_navy
    
    # Scale logo
    logo_w = int(bottle_w * prod["logo_w_ratio"])
    logo_h = int(logo_w * (selected_logo.height / selected_logo.width))
    logo_scaled = selected_logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    
    # Paste logo onto bottle
    pos_x = center_x - logo_w // 2
    pos_y = center_y - logo_h // 2
    
    mockup_img = bottle.copy()
    mockup_img.paste(logo_scaled, (pos_x, pos_y), mask=logo_scaled)
    
    # Save transparent PNG mockup
    mock_png_path = os.path.join(mockups_dir, f"mock_{code}.png")
    mockup_img.save(mock_png_path, format="PNG")
    
    # Also save clean white background mockup for catalog use
    white_bg = Image.new("RGB", mockup_img.size, (255, 255, 255))
    white_bg.paste(mockup_img, mask=mockup_img.split()[3])
    mock_jpg_path = os.path.join(mockups_dir, f"mock_{code}.jpg")
    white_bg.save(mock_jpg_path, format="JPEG", quality=95)
    
    # Update metadata with output paths
    prod["mockup_png"] = f"mockups/mock_{code}.png"
    prod["mockup_jpg"] = f"mockups/mock_{code}.jpg"
    prod["photo_png"] = f"seffaf_png/{photo_file}"
    prod["photo_white"] = f"beyaz_arka_plan/{photo_file.replace('.png', '.jpg')}"
    
    print(f"Generated mockup for [{code}] -> {mock_png_path}")

# Save products metadata JSON for easy customization
json_path = os.path.join(base_dir, "products_catalog.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(products_meta, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully generated mockups for {len(products_meta)} products!")
print(f"Metadata saved to: {json_path}")
