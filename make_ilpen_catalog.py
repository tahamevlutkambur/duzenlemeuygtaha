import os
import json
import glob

base_dir = r"C:\Users\Taha\Pictures\kolonya"

# Load catalog data
with open(os.path.join(base_dir, "products_catalog.json"), "r", encoding="utf-8") as f:
    products = json.load(f)

# Helper to find user mockup or fallback
def get_product_visual(code, fallback_mockup, fallback_crop):
    user_file_png = os.path.join(base_dir, "kullanici_mockuplari", f"{code}.png")
    user_file_jpg = os.path.join(base_dir, "kullanici_mockuplari", f"{code}.jpg")
    fam_png = os.path.join(base_dir, "kullanici_mockuplari", f"{code[:-1]}.png")
    fam_jpg = os.path.join(base_dir, "kullanici_mockuplari", f"{code[:-1]}.jpg")
    
    if os.path.exists(user_file_png):
        return f"kullanici_mockuplari/{code}.png", True
    elif os.path.exists(user_file_jpg):
        return f"kullanici_mockuplari/{code}.jpg", True
    elif os.path.exists(fam_png):
        return f"kullanici_mockuplari/{code[:-1]}.png", True
    elif os.path.exists(fam_jpg):
        return f"kullanici_mockuplari/{code[:-1]}.jpg", True
    elif os.path.exists(os.path.join(base_dir, fallback_mockup)):
        return fallback_mockup, False
    else:
        return fallback_crop, False

# Group products into families
# We want 2 products per page (like İlpen page 120/121)
# Each family can have 1 or 2 variants (F and S, or D and S)
families = [
    # PET SERİSİ
    {
        "id": "30P01",
        "title": "30 ML YUVARLAK PET KOLONYA",
        "category": "PET Serisi",
        "volume": "30 ml",
        "box_qty": "200 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Kompakt ergonomik form, çanta ve cep kullanımına uygun sızdırmaz seyahat boyu tasarım.",
        "primary_code": "30P01",
        "variants": [
            {"code": "30P01F", "cap_name": "FLİP-TOP (F)", "sub": "Açılır-Kapanır Kapak", "photo": "seffaf_png/DSCF0320.png", "cap_crop": "assets/cap_crops/cap_30P01F.png", "mockup": "assets/cropped_mockups/crop_30P01F_mock.png", "crop": "assets/cropped_products/crop_30P01F_orig.png"},
            {"code": "30P01S", "cap_name": "SPREY (S)", "sub": "Mikro Sis Püskürtme", "photo": "seffaf_png/DSCF0322.png", "cap_crop": "assets/cap_crops/cap_30P01S.png", "mockup": "assets/cropped_mockups/crop_30P01S_mock.png", "crop": "assets/cropped_products/crop_30P01S_orig.png"}
        ]
    },
    {
        "id": "45P01",
        "title": "45 ML YASSI PET KOLONYA",
        "category": "PET Serisi",
        "volume": "45 ml",
        "box_qty": "150 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Yassı zarif gövde yapısı, geniş etiket baskı alanı ile kurumsal logonuzu maksimum görünürlükle sunar.",
        "primary_code": "45P01",
        "variants": [
            {"code": "45P01F", "cap_name": "FLİP-TOP (F)", "sub": "Sızdırmaz Açılır Kapak", "photo": "seffaf_png/DSCF0360.png", "cap_crop": "assets/cap_crops/cap_45P01F.png", "mockup": "assets/cropped_mockups/crop_45P01F_mock.png", "crop": "assets/cropped_products/crop_45P01F_orig.png"}
        ]
    },
    {
        "id": "50P01",
        "title": "50 ML YUVARLAK PET KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "box_qty": "150 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Klasik silindirik şişe formu, zengin koku esansları ve pratik kullanım opsiyonları ile ideal kurumsal hediye.",
        "primary_code": "50P01",
        "variants": [
            {"code": "50P01F", "cap_name": "FLİP-TOP (F)", "sub": "Dökme Açılır Kapak", "photo": "seffaf_png/DSCF0324.png", "cap_crop": "assets/cap_crops/cap_50P01F.png", "mockup": "assets/cropped_mockups/crop_50P01F_mock.png", "crop": "assets/cropped_products/crop_50P01F_orig.png"},
            {"code": "50P01S", "cap_name": "SPREY (S)", "sub": "Mikro Sis Başlık", "photo": "seffaf_png/DSCF0326.png", "cap_crop": "assets/cap_crops/cap_50P01S.png", "mockup": "assets/cropped_mockups/crop_50P01S_mock.png", "crop": "assets/cropped_products/crop_50P01S_orig.png"}
        ]
    },
    {
        "id": "50P02",
        "title": "50 ML KAVİSLİ PET KOLONYA",
        "category": "PET Serisi",
        "volume": "50 ml",
        "box_qty": "150 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Modern kavisli estetik hatlar, ele oturan konforlu kavrama ve şık masaüstü promosyon duruşu.",
        "primary_code": "50P02",
        "variants": [
            {"code": "50P02S", "cap_name": "SPREY (S)", "sub": "Püskürtme Mekanizması", "photo": "seffaf_png/DSCF0332.png", "cap_crop": "assets/cap_crops/cap_50P02S.png", "mockup": "assets/cropped_mockups/crop_50P02S_mock.png", "crop": "assets/cropped_products/crop_50P02S_orig.png"},
            {"code": "50P02F", "cap_name": "FLİP-TOP (F)", "sub": "Açılır Kapanır Kapak", "photo": "seffaf_png/DSCF0333.png", "cap_crop": "assets/cap_crops/cap_50P02F.png", "mockup": "assets/cropped_mockups/crop_50P02F_mock.png", "crop": "assets/cropped_products/crop_50P02F_orig.png"}
        ]
    },
    {
        "id": "70P01",
        "title": "70 ML PRİZMA PET KOLONYA",
        "category": "PET Serisi",
        "volume": "70 ml",
        "box_qty": "120 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Özel köşeli prizmatik tasarım, yüksek berraklıkta gövde ve hem sprey hem flip-top kapak uyumu.",
        "primary_code": "70P01",
        "variants": [
            {"code": "70P01F", "cap_name": "FLİP-TOP (F)", "sub": "Pratik Açılır Kapak", "photo": "seffaf_png/DSCF0328.png", "cap_crop": "assets/cap_crops/cap_70P01F.png", "mockup": "assets/cropped_mockups/crop_70P01F_mock.png", "crop": "assets/cropped_products/crop_70P01F_orig.png"},
            {"code": "70P01S", "cap_name": "SPREY (S)", "sub": "Korumalı Sis Sprey", "photo": "seffaf_png/DSCF0330.png", "cap_crop": "assets/cap_crops/cap_70P01S.png", "mockup": "assets/cropped_mockups/crop_70P01S_mock.png", "crop": "assets/cropped_products/crop_70P01S_orig.png"}
        ]
    },
    {
        "id": "100P1",
        "title": "100 ML YUVARLAK PET KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "box_qty": "100 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Standart promosyonun lider modeli; ofis, mağaza ve etkinlikler için optimum gramaj ve uzun ömürlü kullanım.",
        "primary_code": "100P1",
        "variants": [
            {"code": "100P1S", "cap_name": "SPREY (S)", "sub": "Yüksek Verimli Püskürtme", "photo": "seffaf_png/DSCF0338.png", "cap_crop": "assets/cap_crops/cap_100P1S.png", "mockup": "assets/cropped_mockups/crop_100P1S_mock.png", "crop": "assets/cropped_products/crop_100P1S_orig.png"},
            {"code": "100P1F", "cap_name": "FLİP-TOP (F)", "sub": "Açılır Dökme Kapak", "photo": "seffaf_png/DSCF0340.png", "cap_crop": "assets/cap_crops/cap_100P1F.png", "mockup": "assets/cropped_mockups/crop_100P1F_mock.png", "crop": "assets/cropped_products/crop_100P1F_orig.png"}
        ]
    },
    {
        "id": "100P2",
        "title": "100 ML YASSI PET KOLONYA",
        "category": "PET Serisi",
        "volume": "100 ml",
        "box_qty": "100 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Geniş ön yüzeyiyle çift taraflı etiketleme imkanı sağlayan zarif yassı masaüstü ve vitrin boyu.",
        "primary_code": "100P2",
        "variants": [
            {"code": "100P2F", "cap_name": "FLİP-TOP (F)", "sub": "Geniş Açılır Kapak", "photo": "seffaf_png/DSCF0417.png", "cap_crop": "assets/cap_crops/cap_100P2F.png", "mockup": "assets/cropped_mockups/crop_100P2F_mock.png", "crop": "assets/cropped_products/crop_100P2F_orig.png"},
            {"code": "100P2S", "cap_name": "SPREY (S)", "sub": "Sis Püskürtme Başlığı", "photo": "seffaf_png/DSCF0420.png", "cap_crop": "assets/cap_crops/cap_100P2S.png", "mockup": "assets/cropped_mockups/crop_100P2S_mock.png", "crop": "assets/cropped_products/crop_100P2S_orig.png"}
        ]
    },
    {
        "id": "150P1",
        "title": "150 ML YUVARLAK PET KOLONYA",
        "category": "PET Serisi",
        "volume": "150 ml",
        "box_qty": "80 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Geniş hacimli ferahlatıcı kurumsal sunum. Karşılama bankoları ve toplantı salonları için vazgeçilmez.",
        "primary_code": "150P1",
        "variants": [
            {"code": "150P1F", "cap_name": "FLİP-TOP (F)", "sub": "Dökme Kapak", "photo": "seffaf_png/DSCF0423.png", "cap_crop": "assets/cap_crops/cap_150P1F.png", "mockup": "assets/cropped_mockups/crop_150P1F_mock.png", "crop": "assets/cropped_products/crop_150P1F_orig.png"},
            {"code": "150P1S", "cap_name": "SPREY (S)", "sub": "Geniş Açılı Sprey", "photo": "seffaf_png/DSCF0342.png", "cap_crop": "assets/cap_crops/cap_150P1S.png", "mockup": "assets/cropped_mockups/crop_150P1S_mock.png", "crop": "assets/cropped_products/crop_150P1S_orig.png"}
        ]
    },
    {
        "id": "200P1",
        "title": "200 ML YUVARLAK PET KOLONYA",
        "category": "PET Serisi",
        "volume": "200 ml",
        "box_qty": "60 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Klasik Türk kolonyası boyutunda, yüksek kapasiteli ve kalıcı kokulu prestij promosyonu.",
        "primary_code": "200P1",
        "variants": [
            {"code": "200P1F", "cap_name": "FLİP-TOP (F)", "sub": "Klasik Açılır Kapak", "photo": "seffaf_png/DSCF0436.png", "cap_crop": "assets/cap_crops/cap_200P1F.png", "mockup": "assets/cropped_mockups/crop_200P1F_mock.png", "crop": "assets/cropped_products/crop_200P1F_orig.png"},
            {"code": "200P1S", "cap_name": "SPREY (S)", "sub": "Püskürtme Başlığı", "photo": "seffaf_png/DSCF0432.png", "cap_crop": "assets/cap_crops/cap_200P1S.png", "mockup": "assets/cropped_mockups/crop_200P1S_mock.png", "crop": "assets/cropped_products/crop_200P1S_orig.png"}
        ]
    },
    {
        "id": "400P1",
        "title": "400 ML DİKDÖRTGEN PET KOLONYA",
        "category": "PET Serisi",
        "volume": "400 ml",
        "box_qty": "36 Adet",
        "material": "PET Plastik Gövde",
        "desc": "Maksimum hacim ve köşeli kurumsal mimari form. Otel lobileri, restoranlar ve kurumsal binalar için.",
        "primary_code": "400P1",
        "variants": [
            {"code": "400P1F", "cap_name": "FLİP-TOP (F)", "sub": "Büyük Boy Açılır Kapak", "photo": "seffaf_png/DSCF0442.png", "cap_crop": "assets/cap_crops/cap_400P1F.png", "mockup": "assets/cropped_mockups/crop_400P1F_mock.png", "crop": "assets/cropped_products/crop_400P1F_orig.png"}
        ]
    },

    # SLİM & CEP SERİSİ
    {
        "id": "20K01",
        "title": "20 ML SLİM KLASİK KART KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "20 ml",
        "box_qty": "250 Adet",
        "material": "Mat Siyah Polimer",
        "desc": "Kredi kartı ebatında ultra ince tasarım. Ceket cebinde, cüzdanda ve el çantasında taşınabilir.",
        "primary_code": "20K01",
        "variants": [
            {"code": "20K01S", "cap_name": "GÖMME SPREY (S)", "sub": "Entegre Püskürtme", "photo": "seffaf_png/DSCF0451.png", "cap_crop": "assets/cap_crops/cap_20K01S.png", "mockup": "assets/cropped_mockups/crop_20K01S_mock.png", "crop": "assets/cropped_products/crop_20K01S_orig.png"}
        ]
    },
    {
        "id": "20K02",
        "title": "20 ML SLİM KLİPSLİ CEP KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "20 ml",
        "box_qty": "250 Adet",
        "material": "Mat Siyah Polimer",
        "desc": "Gövdeye entegre koruyucu kapak ve asma klipsi mekanizması ile fuar ve kurumsal etkinlik favorisi.",
        "primary_code": "20K02",
        "variants": [
            {"code": "20K02S", "cap_name": "KORUMALI SPREY (S)", "sub": "Klipsli Emniyet Başlığı", "photo": "seffaf_png/DSCF0458.png", "cap_crop": "assets/cap_crops/cap_20K02S.png", "mockup": "assets/cropped_mockups/crop_20K02S_mock.png", "crop": "assets/cropped_products/crop_20K02S_orig.png"}
        ]
    },
    {
        "id": "25K01",
        "title": "25 ML SLİM ÜÇGEN CEP KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "25 ml",
        "box_qty": "200 Adet",
        "material": "Polimer Gövde",
        "desc": "Özgün üçgen prizma geometri; dinamik, genç ve inovatif marka imajınızı pekiştiren modern form.",
        "primary_code": "25K01",
        "variants": [
            {"code": "25K01S", "cap_name": "SPREY (S)", "sub": "Hassas Dozajlı Başlık", "photo": "seffaf_png/DSCF0480.png", "cap_crop": "assets/cap_crops/cap_25K01S.png", "mockup": "assets/cropped_mockups/crop_25K01S_mock.png", "crop": "assets/cropped_products/crop_25K01S_orig.png"}
        ]
    },
    {
        "id": "45K01",
        "title": "45 ML SLİM MEDIUM CEP KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "45 ml",
        "box_qty": "150 Adet",
        "material": "Mat Siyah Polimer",
        "desc": "Orta boy yassı kart formatı; hem geniş baskı alanı hem de uzun süreli hijyen sağlayan ideal hacim.",
        "primary_code": "45K01",
        "variants": [
            {"code": "45K01S", "cap_name": "SPREY (S)", "sub": "Entegre Geniş Başlık", "photo": "seffaf_png/DSCF0488.png", "cap_crop": "assets/cap_crops/cap_45K01S.png", "mockup": "assets/cropped_mockups/crop_45K01S_mock.png", "crop": "assets/cropped_products/crop_45K01S_orig.png"}
        ]
    },
    {
        "id": "50K01",
        "title": "50 ML SLİM MAXİ CEP KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "50 ml",
        "box_qty": "120 Adet",
        "material": "Mat Siyah Polimer",
        "desc": "Slim serisinin en yüksek kapasiteli amiral gemisi; mat siyah kadife dokulu yüzey üzerine altın yaldız baskı uyumlu.",
        "primary_code": "50K01",
        "variants": [
            {"code": "50K01S", "cap_name": "SPREY (S)", "sub": "Mikro Sis Püskürtme", "photo": "seffaf_png/DSCF0491.png", "cap_crop": "assets/cap_crops/cap_50K01S.png", "mockup": "assets/cropped_mockups/crop_50K01S_mock.png", "crop": "assets/cropped_products/crop_50K01S_orig.png"}
        ]
    },

    # KRİSTAL & LÜKS CAM SERİSİ
    {
        "id": "10C01",
        "title": "10 ML PEN MİNİ CAM SPREY",
        "category": "Kristal Cam Serisi",
        "volume": "10 ml",
        "box_qty": "300 Adet",
        "material": "Şeffaf Tip-1 Cam Gövde",
        "desc": "Kalem formunda ince cam tüp, metalik sprey başlığı ve şık cep boyutuyla VIP etkinlik esansı.",
        "primary_code": "10C01",
        "variants": [
            {"code": "10C01S", "cap_name": "SPREY (S)", "sub": "Metalik Sis Başlık", "photo": "seffaf_png/DSCF0497.png", "cap_crop": "assets/cap_crops/cap_10C01S.png", "mockup": "assets/cropped_mockups/crop_10C01S_mock.png", "crop": "assets/cropped_products/crop_10C01S_orig.png"}
        ]
    },
    {
        "id": "50C01",
        "title": "50 ML LINEA CAM SPREY",
        "category": "Kristal Cam Serisi",
        "volume": "50 ml",
        "box_qty": "100 Adet",
        "material": "Kristal Berrak Cam",
        "desc": "Zarif dikey silindirik form, kristal cam ağırlığı ve parfümeri kalitesinde lüks püskürtme başlığı.",
        "primary_code": "50C01",
        "variants": [
            {"code": "50C01S", "cap_name": "SPREY (S)", "sub": "Lüks Parfüm Valfi", "photo": "seffaf_png/DSCF0500.png", "cap_crop": "assets/cap_crops/cap_50C01S.png", "mockup": "assets/cropped_mockups/crop_50C01S_mock.png", "crop": "assets/cropped_products/crop_50C01S_orig.png"}
        ]
    },
    {
        "id": "100C1",
        "title": "100 ML DIAMOND CAM KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "100 ml",
        "box_qty": "80 Adet",
        "material": "Ağır Tabanlı Kristal Cam",
        "desc": "Elmas kesim ışıltılı cam gövde; hem dökme tıpalı hem de sprey valfli seçenekleriyle üst düzey yönetici hediyesi.",
        "primary_code": "100C1",
        "variants": [
            {"code": "100C1S", "cap_name": "SPREY (S)", "sub": "Kristal Sis Başlık", "photo": "seffaf_png/DSCF0503.png", "cap_crop": "assets/cap_crops/cap_100C1S.png", "mockup": "assets/cropped_mockups/crop_100C1S_mock.png", "crop": "assets/cropped_products/crop_100C1S_orig.png"},
            {"code": "100C1D", "cap_name": "DİKME / TIPA (D)", "sub": "Geleneksel Tıpalı Kapak", "photo": "seffaf_png/DSCF0511.png", "cap_crop": "assets/cap_crops/cap_100C1D.png", "mockup": "assets/cropped_mockups/crop_100C1D_mock.png", "crop": "assets/cropped_products/crop_100C1D_orig.png"}
        ]
    },
    {
        "id": "100C2",
        "title": "100 ML RIGA CAM SPREY",
        "category": "Kristal Cam Serisi",
        "volume": "100 ml",
        "box_qty": "80 Adet",
        "material": "Kristal Cam",
        "desc": "Klasik Avrupa esintili yivli gövde mimarisi, yüksek cam berraklığı ve özel koku serileri için ideal platform.",
        "primary_code": "100C2",
        "variants": [
            {"code": "100C2S", "cap_name": "SPREY (S)", "sub": "Mikro Sis Püskürtme", "photo": "seffaf_png/DSCF0518.png", "cap_crop": "assets/cap_crops/cap_100C2S.png", "mockup": "assets/cropped_mockups/crop_100C2S_mock.png", "crop": "assets/cropped_products/crop_100C2S_orig.png"}
        ]
    },
    {
        "id": "200C1",
        "title": "200 ML DIAMOND CAM DÖKME",
        "category": "Kristal Cam Serisi",
        "volume": "200 ml",
        "box_qty": "48 Adet",
        "material": "Ağır Taban Kristal Cam",
        "desc": "Geleneksel Türk konukseverliğinin sembolü; 200 ml kristal cam şişede kalıcı 80° koku seramonisi.",
        "primary_code": "200C1",
        "variants": [
            {"code": "200C1D", "cap_name": "DİKME / TIPA (D)", "sub": "Sızdırmaz Tıpalı Başlık", "photo": "seffaf_png/DSCF0506.png", "cap_crop": "assets/cap_crops/cap_200C1D.png", "mockup": "assets/cropped_mockups/crop_200C1D_mock.png", "crop": "assets/cropped_products/crop_200C1D_orig.png"}
        ]
    },
    {
        "id": "200C2",
        "title": "200 ML RIGA CAM DÖKME",
        "category": "Kristal Cam Serisi",
        "volume": "200 ml",
        "box_qty": "48 Adet",
        "material": "Kristal Cam",
        "desc": "Riga koleksiyonunun 200 ml dökme versiyonu; asil duruşuyla makam masalarında ve lüks hediye kutularında parlar.",
        "primary_code": "200C2",
        "variants": [
            {"code": "200C2D", "cap_name": "DİKME / TIPA (D)", "sub": "Altın/Gümüş Tıpalı Kapak", "photo": "seffaf_png/DSCF0515.png", "cap_crop": "assets/cap_crops/cap_200C2D.png", "mockup": "assets/cropped_mockups/crop_200C2D_mock.png", "crop": "assets/cropped_products/crop_200C2D_orig.png"}
        ]
    },
    {
        "id": "200C3",
        "title": "200 ML PRİZMA CAM DÖKME",
        "category": "Kristal Cam Serisi",
        "volume": "200 ml",
        "box_qty": "48 Adet",
        "material": "Kristal Cam Gövde",
        "desc": "Köşeli prizmatik kristal gövde, ışığı yansıtan özel cam kesimi ve prestijli kurumsal duruş.",
        "primary_code": "200C3",
        "variants": [
            {"code": "200C3D", "cap_name": "DİKME / TIPA (D)", "sub": "Özel Akıtıcı Tıpa", "photo": "seffaf_png/DSCF0521.png", "cap_crop": "assets/cap_crops/cap_200C3D.png", "mockup": "assets/cropped_mockups/crop_200C3D_mock.png", "crop": "assets/cropped_products/crop_200C3D_orig.png"}
        ]
    },
    {
        "id": "250C1",
        "title": "250 ML SIGNATURE CAM DÖKME",
        "category": "Kristal Cam Serisi",
        "volume": "250 ml",
        "box_qty": "36 Adet",
        "material": "Lüks Kristal Cam Gövde",
        "desc": "Promkol kristal serisinin en heybetli tasarımı. Özel ahşap veya kadife kutulu VIP kurumsal setlere mükemmel uyum.",
        "primary_code": "250C1",
        "variants": [
            {"code": "250C1D", "cap_name": "DİKME / TIPA (D)", "sub": "Lüks Tıpalı Kapak", "photo": "seffaf_png/DSCF0524.png", "cap_crop": "assets/cap_crops/cap_250C1D.png", "mockup": "assets/cropped_mockups/crop_250C1D_mock.png", "crop": "assets/cropped_products/crop_250C1D_orig.png"}
        ]
    }
]

print(f"Total structured families: {len(families)}")
