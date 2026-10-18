import os
import json
import subprocess
import shutil

base_dir = r"C:\Users\Taha\Pictures\kolonya"

# 32 Products comprehensive technical dataset
products_data = [
    # --- PET SERİSİ (18 Products) ---
    {
        "code": "30P01F",
        "name": "30 ML YUVARLAK FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "30 ml (1.01 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Yuvarlak Şişe",
        "neck_size": "18/410 mm Standart Diş",
        "dims": "Yükseklik: 84 mm | Taban Çapı: Ø 29 mm",
        "label_area": "75 x 35 mm (Tam Tur veya Ön-Arka)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "Vidalı Boğaz, Tek Elle Açılır Klik Kapanış, Sızdırmaz Tırnak",
        "cap_flow": "Dökme / Kontrollü Akış Ağzı",
        "box_qty": "200 Adet / Koli",
        "box_weight": "8.2 kg (Brüt Koli Ağırlığı)",
        "desc": "Kompakt cep ve çanta boyutu. Sızdırmaz emniyetli flip-top kapağıyla dökülme yapmaz.",
        "studio_photo": "assets/cropped_products/crop_30P01F_orig.png",
        "cap_crop": "assets/cap_crops/cap_30P01F.png",
        "sibling_code": "30P01S",
        "sibling_name": "Sprey Sis Başlık Seçeneği (30P01S)",
        "sibling_crop": "assets/cap_crops/cap_30P01S.png"
    },
    {
        "code": "30P01S",
        "name": "30 ML YUVARLAK SPREY KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "30 ml (1.01 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Yuvarlak Şişe",
        "neck_size": "18/410 mm Standart Diş",
        "dims": "Yükseklik: 92 mm | Taban Çapı: Ø 29 mm",
        "label_area": "75 x 35 mm (Tam Tur veya Ön-Arka)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "MİKRO SİS SPREY VALFİ (S)",
        "cap_group": "sprey",
        "cap_mechanic": "0.13 ml Dozajlı Atomizör Valf, Şeffaf Koruyucu Başlık Kapağı",
        "cap_flow": "Homojen Geniş Açılı Sis Püskürtme",
        "box_qty": "200 Adet / Koli",
        "box_weight": "8.4 kg (Brüt Koli Ağırlığı)",
        "desc": "Temas etmeden hijyen sağlayan mikro sis sprey valfi. Seyahat ve kişisel hijyen için ideal.",
        "studio_photo": "assets/cropped_products/crop_30P01S_orig.png",
        "cap_crop": "assets/cap_crops/cap_30P01S.png",
        "sibling_code": "30P01F",
        "sibling_name": "Flip-Top Dökme Kapak Seçeneği (30P01F)",
        "sibling_crop": "assets/cap_crops/cap_30P01F.png"
    },
    {
        "code": "45P01F",
        "name": "45 ML YASSI FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "45 ml (1.52 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Yassı Düz Form Şişe",
        "neck_size": "20/410 mm Standart Diş",
        "dims": "Y: 102 mm | Genişlik: 34 mm | Derinlik: 22 mm",
        "label_area": "28 x 65 mm (Geniş Ön & Arka Düz Yüzey)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "Geniş Açılır Sızdırmaz Kapak, Emniyet Klik Kilidi",
        "cap_flow": "Dökme / Hassas Akış Kontrolü",
        "box_qty": "150 Adet / Koli",
        "box_weight": "8.5 kg (Brüt Koli Ağırlığı)",
        "desc": "Zarif yassı form, cebe ve çantaya düz oturur. Geniş ön etiket yüzeyi ile yüksek marka görünürlüğü sağlar.",
        "studio_photo": "assets/cropped_products/crop_45P01F_orig.png",
        "cap_crop": "assets/cap_crops/cap_45P01F.png",
        "sibling_code": None,
        "sibling_name": "Vidalı Düz Kapak & Sprey Uyumlu Boğaz",
        "sibling_crop": "assets/cap_crops/cap_50P01S.png"
    },
    {
        "code": "50P01F",
        "name": "50 ML YUVARLAK FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "50 ml (1.69 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Klasik Yuvarlak",
        "neck_size": "20/410 mm Standart Diş",
        "dims": "Yükseklik: 105 mm | Taban Çapı: Ø 32 mm",
        "label_area": "85 x 45 mm (Geniş Tam Tur Etiket Alanı)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "Vidalı Montaj, Çift Kilitli Sızdırmaz Klik Tırnak",
        "cap_flow": "Dökme / Damlatıcı Ağız",
        "box_qty": "150 Adet / Koli",
        "box_weight": "9.4 kg (Brüt Koli Ağırlığı)",
        "desc": "Klasik Türk kolonyası ergonomisinde en çok tercih edilen 50 ml silindirik şişe formu.",
        "studio_photo": "assets/cropped_products/crop_50P01F_orig.png",
        "cap_crop": "assets/cap_crops/cap_50P01F.png",
        "sibling_code": "50P01S",
        "sibling_name": "Sprey Sis Başlık Seçeneği (50P01S)",
        "sibling_crop": "assets/cap_crops/cap_50P01S.png"
    },
    {
        "code": "50P01S",
        "name": "50 ML YUVARLAK SPREY KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "50 ml (1.69 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Klasik Yuvarlak",
        "neck_size": "20/410 mm Standart Diş",
        "dims": "Yükseklik: 112 mm | Taban Çapı: Ø 32 mm",
        "label_area": "85 x 45 mm (Geniş Tam Tur Etiket Alanı)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "MİKRO SİS SPREY VALFİ (S)",
        "cap_group": "sprey",
        "cap_mechanic": "0.14 ml Dozajlı Paslanmaz Yaylı Valf + Koruma Kapağı",
        "cap_flow": "Mikro Sis Atomizasyon",
        "box_qty": "150 Adet / Koli",
        "box_weight": "9.6 kg (Brüt Koli Ağırlığı)",
        "desc": "50 ml yuvarlak şişenin sprey versiyonu. Eşit püskürtme ile uzun ömürlü ve ekonomik kullanım.",
        "studio_photo": "assets/cropped_products/crop_50P01S_orig.png",
        "cap_crop": "assets/cap_crops/cap_50P01S.png",
        "sibling_code": "50P01F",
        "sibling_name": "Flip-Top Dökme Kapak Seçeneği (50P01F)",
        "sibling_crop": "assets/cap_crops/cap_50P01F.png"
    },
    {
        "code": "50P02F",
        "name": "50 ML KAVİSLİ FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "50 ml (1.69 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Kavisli Ergonomik Gövde",
        "neck_size": "20/410 mm Standart Diş",
        "dims": "Y: 108 mm | Genişlik: 36 mm | Derinlik: 26 mm",
        "label_area": "30 x 60 mm (Ön ve Arka Etiket)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "Tek Elle Açılır Kavisli Kapak, Sızdırmaz Conta",
        "cap_flow": "Dökme / Akış Kontrollü",
        "box_qty": "150 Adet / Koli",
        "box_weight": "9.6 kg (Brüt Koli Ağırlığı)",
        "desc": "Ele tam oturan kavisli ergonomik bel yapısı. Masada ve tezgahlarda modern dinamik duruş.",
        "studio_photo": "assets/cropped_products/crop_50P02F_orig.png",
        "cap_crop": "assets/cap_crops/cap_50P02F.png",
        "sibling_code": "50P02S",
        "sibling_name": "Sprey Başlık Seçeneği (50P02S)",
        "sibling_crop": "assets/cap_crops/cap_50P02S.png"
    },
    {
        "code": "50P02S",
        "name": "50 ML KAVİSLİ SPREY KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "50 ml (1.69 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Kavisli Ergonomik Gövde",
        "neck_size": "20/410 mm Standart Diş",
        "dims": "Y: 115 mm | Genişlik: 36 mm | Derinlik: 26 mm",
        "label_area": "30 x 60 mm (Ön ve Arka Etiket)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "MİKRO SİS SPREY VALFİ (S)",
        "cap_group": "sprey",
        "cap_mechanic": "0.13 ml Püskürtme Valfi, Korumalı Şeffaf Başlık",
        "cap_flow": "İnce Sis Püskürtme",
        "box_qty": "150 Adet / Koli",
        "box_weight": "9.7 kg (Brüt Koli Ağırlığı)",
        "desc": "Kavisli şişe formu üzerine mikro sprey entegrasyonu. Estetik ve fonksiyonelliği bir araya getirir.",
        "studio_photo": "assets/cropped_products/crop_50P02S_orig.png",
        "cap_crop": "assets/cap_crops/cap_50P02S.png",
        "sibling_code": "50P02F",
        "sibling_name": "Flip-Top Dökme Kapak Seçeneği (50P02F)",
        "sibling_crop": "assets/cap_crops/cap_50P02F.png"
    },
    {
        "code": "70P01F",
        "name": "70 ML PRİZMA FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "70 ml (2.36 fl oz)",
        "material": "PET Plastik Gövde (Yüksek Berraklık)",
        "body_type": "Kare Prizma Şişe",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Y: 118 mm | En: 35 mm | Boy: 35 mm",
        "label_area": "28 x 75 mm (Düz 4 Kenar Yüzeyi)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "24 mm Geniş Boğaz Vidalı Kapak, Sızdırmaz Klik",
        "cap_flow": "Dökme / Akış Kontrolü",
        "box_qty": "120 Adet / Koli",
        "box_weight": "10.2 kg (Brüt Koli Ağırlığı)",
        "desc": "Köşeli prizmatik tasarım; 4 düz cephesiyle logo ve kurumsal mesajlar için mükemmel bir vitrin oluşturur.",
        "studio_photo": "assets/cropped_products/crop_70P01F_orig.png",
        "cap_crop": "assets/cap_crops/cap_70P01F.png",
        "sibling_code": "70P01S",
        "sibling_name": "Prizma Sprey Seçeneği (70P01S)",
        "sibling_crop": "assets/cap_crops/cap_70P01S.png"
    },
    {
        "code": "70P01S",
        "name": "70 ML PRİZMA SPREY KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "70 ml (2.36 fl oz)",
        "material": "PET Plastik Gövde (Yüksek Berraklık)",
        "body_type": "Kare Prizma Şişe",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Y: 125 mm | En: 35 mm | Boy: 35 mm",
        "label_area": "28 x 75 mm (Düz 4 Kenar Yüzeyi)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "MİKRO SİS SPREY VALFİ (S)",
        "cap_group": "sprey",
        "cap_mechanic": "24/410 Geniş Valf Mekanizması, Koruyucu Dış Kapak",
        "cap_flow": "0.14 ml Mikro Sis Püskürtme",
        "box_qty": "120 Adet / Koli",
        "box_weight": "10.4 kg (Brüt Koli Ağırlığı)",
        "desc": "Köşeli prizma şişede sprey ferahlığı. Modern ofisler ve masaüstü promosyonlar için premium tercih.",
        "studio_photo": "assets/cropped_products/crop_70P01S_orig.png",
        "cap_crop": "assets/cap_crops/cap_70P01S.png",
        "sibling_code": "70P01F",
        "sibling_name": "Prizma Flip-Top Seçeneği (70P01F)",
        "sibling_crop": "assets/cap_crops/cap_70P01F.png"
    },
    {
        "code": "100P1F",
        "name": "100 ML YUVARLAK FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "100 ml (3.38 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Yuvarlak Şişe",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Yükseklik: 126 mm | Taban Çapı: Ø 39 mm",
        "label_area": "105 x 65 mm (Geniş Tam Tur Etiket)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "24/410 Vidalı Emniyetli Flip-Top, İç Sızdırmaz Tırnak",
        "cap_flow": "Dökme / Akış Kontrollü",
        "box_qty": "100 Adet / Koli",
        "box_weight": "11.8 kg (Brüt Koli Ağırlığı)",
        "desc": "Promosyon sektörünün 1 numaralı standart boyu. Optimum gramaj, uzun ömürlü kullanım.",
        "studio_photo": "assets/cropped_products/crop_100P1F_orig.png",
        "cap_crop": "assets/cap_crops/cap_100P1F.png",
        "sibling_code": "100P1S",
        "sibling_name": "100 ml Yuvarlak Sprey Seçeneği (100P1S)",
        "sibling_crop": "assets/cap_crops/cap_100P1S.png"
    },
    {
        "code": "100P1S",
        "name": "100 ML YUVARLAK SPREY KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "100 ml (3.38 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Yuvarlak Şişe",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Yükseklik: 135 mm | Taban Çapı: Ø 39 mm",
        "label_area": "105 x 65 mm (Geniş Tam Tur Etiket)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "MİKRO SİS SPREY VALFİ (S)",
        "cap_group": "sprey",
        "cap_mechanic": "24/410 Yüksek Verimli Püskürtme Valfi, Şeffaf Başlık",
        "cap_flow": "0.14 ml Mikro Sis Dağılımı",
        "box_qty": "100 Adet / Koli",
        "box_weight": "12.0 kg (Brüt Koli Ağırlığı)",
        "desc": "100 ml silindirik şişede mikro sis sprey. Mağaza girişleri, resepsiyon ve etkinlikler için ideal.",
        "studio_photo": "assets/cropped_products/crop_100P1S_orig.png",
        "cap_crop": "assets/cap_crops/cap_100P1S.png",
        "sibling_code": "100P1F",
        "sibling_name": "100 ml Yuvarlak Flip-Top Seçeneği (100P1F)",
        "sibling_crop": "assets/cap_crops/cap_100P1F.png"
    },
    {
        "code": "100P2F",
        "name": "100 ML YASSI FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "100 ml (3.38 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Yassı Elips Form Şişe",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Y: 128 mm | Genişlik: 52 mm | Derinlik: 28 mm",
        "label_area": "44 x 78 mm (Geniş Ön/Arka Düz Yüzey)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "Geniş Boyunlu Vidalı Flip-Top, Sızdırmaz Tırnak Kilit",
        "cap_flow": "Dökme / Kontrollü Akış",
        "box_qty": "100 Adet / Koli",
        "box_weight": "12.0 kg (Brüt Koli Ağırlığı)",
        "desc": "Geniş ön yüzeyiyle çift taraflı etiketleme imkanı sunan zarif yassı masaüstü ve vitrin boyu.",
        "studio_photo": "assets/cropped_products/crop_100P2F_orig.png",
        "cap_crop": "assets/cap_crops/cap_100P2F.png",
        "sibling_code": "100P2S",
        "sibling_name": "100 ml Yassı Sprey Seçeneği (100P2S)",
        "sibling_crop": "assets/cap_crops/cap_100P2S.png"
    },
    {
        "code": "100P2S",
        "name": "100 ML YASSI SPREY KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "100 ml (3.38 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Yassı Elips Form Şişe",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Y: 136 mm | Genişlik: 52 mm | Derinlik: 28 mm",
        "label_area": "44 x 78 mm (Geniş Ön/Arka Düz Yüzey)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "MİKRO SİS SPREY VALFİ (S)",
        "cap_group": "sprey",
        "cap_mechanic": "24/410 Sprey Mekanizması, Şeffaf Koruma Başlığı",
        "cap_flow": "0.14 ml Mikro Sis Püskürtme",
        "box_qty": "100 Adet / Koli",
        "box_weight": "12.2 kg (Brüt Koli Ağırlığı)",
        "desc": "Yassı şişe formunda yüksek performanslı sprey. Estetik raf duruşu ve geniş marka alanı sunar.",
        "studio_photo": "assets/cropped_products/crop_100P2S_orig.png",
        "cap_crop": "assets/cap_crops/cap_100P2S.png",
        "sibling_code": "100P2F",
        "sibling_name": "100 ml Yassı Flip-Top Seçeneği (100P2F)",
        "sibling_crop": "assets/cap_crops/cap_100P2F.png"
    },
    {
        "code": "150P1F",
        "name": "150 ML YUVARLAK FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "150 ml (5.07 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Yuvarlak Şişe",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Yükseklik: 142 mm | Taban Çapı: Ø 45 mm",
        "label_area": "125 x 82 mm (Tam Tur Geniş Alan)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "24 mm Vidalı Ağır Hizmet Tipi Flip-Top Kapak",
        "cap_flow": "Dökme / Akış Kontrollü",
        "box_qty": "80 Adet / Koli",
        "box_weight": "13.5 kg (Brüt Koli Ağırlığı)",
        "desc": "Geniş hacimli ferahlatıcı kurumsal sunum. Karşılama bankoları ve toplantı salonları için vazgeçilmez.",
        "studio_photo": "assets/cropped_products/crop_150P1F_orig.png",
        "cap_crop": "assets/cap_crops/cap_150P1F.png",
        "sibling_code": "150P1S",
        "sibling_name": "150 ml Yuvarlak Sprey Seçeneği (150P1S)",
        "sibling_crop": "assets/cap_crops/cap_150P1S.png"
    },
    {
        "code": "150P1S",
        "name": "150 ML YUVARLAK SPREY KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "150 ml (5.07 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Yuvarlak Şişe",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Yükseklik: 150 mm | Taban Çapı: Ø 45 mm",
        "label_area": "125 x 82 mm (Tam Tur Geniş Alan)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "MİKRO SİS SPREY VALFİ (S)",
        "cap_group": "sprey",
        "cap_mechanic": "24/410 Geniş Açılı Sis Valfi, Emniyetli Başlık",
        "cap_flow": "0.15 ml Geniş Alan Püskürtme",
        "box_qty": "80 Adet / Koli",
        "box_weight": "13.7 kg (Brüt Koli Ağırlığı)",
        "desc": "150 ml yüksek hacimde mikro sis konforu. Yoğun sirkülasyonlu işletmeler için ideal hijyen çözümü.",
        "studio_photo": "assets/cropped_products/crop_150P1S_orig.png",
        "cap_crop": "assets/cap_crops/cap_150P1S.png",
        "sibling_code": "150P1F",
        "sibling_name": "150 ml Yuvarlak Flip-Top Seçeneği (150P1F)",
        "sibling_crop": "assets/cap_crops/cap_150P1F.png"
    },
    {
        "code": "200P1S",
        "name": "200 ML YUVARLAK SPREY KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "200 ml (6.76 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Klasik Yuvarlak",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Yükseklik: 170 mm | Taban Çapı: Ø 48 mm",
        "label_area": "135 x 95 mm (Büyük Boy Tam Tur Alan)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "MİKRO SİS SPREY VALFİ (S)",
        "cap_group": "sprey",
        "cap_mechanic": "24/410 Yüksek Kapasiteli Püskürtme Valfi",
        "cap_flow": "0.15 ml Homojen Sis Dağılımı",
        "box_qty": "60 Adet / Koli",
        "box_weight": "13.8 kg (Brüt Koli Ağırlığı)",
        "desc": "200 ml büyük boy şişede püskürtme başlığı. Kurumsal ofisler ve karşılama noktalarında prestijli sunum.",
        "studio_photo": "assets/cropped_products/crop_200P1S_orig.png",
        "cap_crop": "assets/cap_crops/cap_200P1S.png",
        "sibling_code": "200P1F",
        "sibling_name": "200 ml Yuvarlak Flip-Top Seçeneği (200P1F)",
        "sibling_crop": "assets/cap_crops/cap_200P1F.png"
    },
    {
        "code": "200P1F",
        "name": "200 ML YUVARLAK FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "200 ml (6.76 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Silindirik Klasik Yuvarlak",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Yükseklik: 162 mm | Taban Çapı: Ø 48 mm",
        "label_area": "135 x 95 mm (Büyük Boy Tam Tur Alan)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "24 mm Vidalı Klasik Dökme Kapak, Sızdırmaz Klik",
        "cap_flow": "Dökme / Serbest ve Kontrollü Akış",
        "box_qty": "60 Adet / Koli",
        "box_weight": "13.6 kg (Brüt Koli Ağırlığı)",
        "desc": "Geleneksel Türk kolonyası hacminde, yüksek kapasiteli ve kalıcı kokulu standart promosyon devi.",
        "studio_photo": "assets/cropped_products/crop_200P1F_orig.png",
        "cap_crop": "assets/cap_crops/cap_200P1F.png",
        "sibling_code": "200P1S",
        "sibling_name": "200 ml Yuvarlak Sprey Seçeneği (200P1S)",
        "sibling_crop": "assets/cap_crops/cap_200P1S.png"
    },
    {
        "code": "400P1F",
        "name": "400 ML DİKDÖRTGEN FLİP-TOP KOLONYA ŞİŞESİ",
        "category": "PET Serisi",
        "volume": "400 ml (13.52 fl oz)",
        "material": "PET Plastik Gövde (Polietilen Tereftalat)",
        "body_type": "Köşeli Dikdörtgen Blok Gövde",
        "neck_size": "28/410 mm Geniş Boğaz",
        "dims": "Y: 185 mm | Genişlik: 65 mm | Derinlik: 42 mm",
        "label_area": "55 x 115 mm (Geniş Dikdörtgen Ön Etiket)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "FLİP-TOP DÖKME KAPAK (F)",
        "cap_group": "flip_top",
        "cap_mechanic": "28/410 Ağır Hizmet Flip-Top Kapak, Pompa Dispenser Uyumlu",
        "cap_flow": "Geniş Ağız Dökme Akışı",
        "box_qty": "36 Adet / Koli",
        "box_weight": "16.2 kg (Brüt Koli Ağırlığı)",
        "desc": "Maksimum hacim ve mimari form. Otel lobileri, restoranlar ve kurumsal binalar için amiral gemisi.",
        "studio_photo": "assets/cropped_products/crop_400P1F_orig.png",
        "cap_crop": "assets/cap_crops/cap_400P1F.png",
        "sibling_code": None,
        "sibling_name": "Pompalı Sıvı Dispenser Başlığı Uyumlu (28/410)",
        "sibling_crop": "assets/cap_crops/cap_200P1F.png"
    },

    # --- SLİM & CEP SERİSİ (5 Products) ---
    {
        "code": "20K01S",
        "name": "20 ML SLİM KLASİK KART KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "20 ml (0.68 fl oz)",
        "material": "Mat Siyah Polimer (Soft Touch Gövde)",
        "body_type": "Kredi Kartı Formu Ultra İnce",
        "neck_size": "Entegre Ultrasonik Valf Sistemi",
        "dims": "Y: 86 mm | En: 56 mm | Kalınlık: 11 mm",
        "label_area": "50 x 80 mm (Çift Taraflı Geniş Baskı)",
        "print_methods": "Tam Renkli UV Baskı, Sıcak Varlık Altın Yaldız, Etiket",
        "cap_name": "GÖMME SPREY BAŞLIĞI (S)",
        "cap_group": "slim",
        "cap_mechanic": "Gövdeye Entegre Atomizör Valf, Cepte Kazara Basılmayı Önler",
        "cap_flow": "0.10 ml Hassas Sis Püskürtme (~300 Basım)",
        "box_qty": "250 Adet / Koli",
        "box_weight": "7.5 kg (Brüt Koli Ağırlığı)",
        "desc": "Kredi kartı ebatında ultra ince tasarım. Ceket cebinde, cüzdanda ve el çantasında taşınabilir.",
        "studio_photo": "assets/cropped_products/crop_20K01S_orig.png",
        "cap_crop": "assets/cap_crops/cap_20K01S.png",
        "sibling_code": "20K02S",
        "sibling_name": "Klipsli Koruma Başlığı Versiyonu (20K02S)",
        "sibling_crop": "assets/cap_crops/cap_20K02S.png"
    },
    {
        "code": "20K02S",
        "name": "20 ML SLİM KLİPSLİ CEP KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "20 ml (0.68 fl oz)",
        "material": "Mat Siyah Polimer (Soft Touch)",
        "body_type": "Korumalı Klipsli Kart Gövde",
        "neck_size": "Entegre Valf + Tekrar Doldurma Tıpası",
        "dims": "Y: 88 mm | En: 58 mm | Kalınlık: 12 mm",
        "label_area": "52 x 75 mm (Ön ve Arka Yüzey)",
        "print_methods": "Tam Renkli UV Baskı, Sıcak Varlık Altın Yaldız, Etiket",
        "cap_name": "KORUMALI KLİPS SPREY (S)",
        "cap_group": "slim",
        "cap_mechanic": "Entegre Asma Klipsi ve Koruyucu Emniyet Kapağı",
        "cap_flow": "0.10 ml Mikro Sis Püskürtme",
        "box_qty": "250 Adet / Koli",
        "box_weight": "8.0 kg (Brüt Koli Ağırlığı)",
        "desc": "Gövdeye entegre koruyucu kapak ve asma klipsi. Ceket cebine, yaka kartına veya çantaya takılabilir.",
        "studio_photo": "assets/cropped_products/crop_20K02S_orig.png",
        "cap_crop": "assets/cap_crops/cap_20K02S.png",
        "sibling_code": "20K01S",
        "sibling_name": "Klasik Düz Kart Versiyonu (20K01S)",
        "sibling_crop": "assets/cap_crops/cap_20K01S.png"
    },
    {
        "code": "25K01S",
        "name": "25 ML SLİM ÜÇGEN SPREY KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "25 ml (0.85 fl oz)",
        "material": "Polimer Gövde (Darbe Emici)",
        "body_type": "Üçgen Prizma Cep Gövdesi",
        "neck_size": "Entegre Atomizör Kartuşu",
        "dims": "Y: 95 mm | Taban Kenarı: 38 x 38 x 38 mm",
        "label_area": "30 x 70 mm (3 Ayrı Düz Panel)",
        "print_methods": "Tam Renkli UV Baskı, Sıcak Varlık, Etiket",
        "cap_name": "ERGONOMİK AÇILI SPREY (S)",
        "cap_group": "slim",
        "cap_mechanic": "Prizma Tepesine Entegre Açılı Sis Valfi",
        "cap_flow": "0.11 ml Dozajlı Atomizasyon",
        "box_qty": "200 Adet / Koli",
        "box_weight": "7.2 kg (Brüt Koli Ağırlığı)",
        "desc": "Özgün üçgen prizma geometri. Dinamik, genç ve inovatif marka algısı yaratan futuristik form.",
        "studio_photo": "assets/cropped_products/crop_25K01S_orig.png",
        "cap_crop": "assets/cap_crops/cap_25K01S.png",
        "sibling_code": None,
        "sibling_name": "Gömme Valf & Koruyucu Kapaklı Tasarım",
        "sibling_crop": "assets/cap_crops/cap_20K01S.png"
    },
    {
        "code": "45K01S",
        "name": "45 ML SLİM MEDIUM SPREY KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "45 ml (1.52 fl oz)",
        "material": "Mat Siyah Polimer (Soft Touch Gövde)",
        "body_type": "Medium Dikdörtgen Kart Gövde",
        "neck_size": "Geniş Entegre Valf + Refill Tıpası",
        "dims": "Y: 98 mm | En: 68 mm | Kalınlık: 14 mm",
        "label_area": "60 x 85 mm (Çift Taraflı Geniş Alan)",
        "print_methods": "Tam Renkli UV Baskı, Sıcak Varlık Altın Yaldız, Etiket",
        "cap_name": "GENİŞ BUTONLU SPREY (S)",
        "cap_group": "slim",
        "cap_mechanic": "Geniş Parmak Butonu, Yüksek Basınçlı Sis Valfi",
        "cap_flow": "0.12 ml Mikro Sis Püskürtme",
        "box_qty": "150 Adet / Koli",
        "box_weight": "8.8 kg (Brüt Koli Ağırlığı)",
        "desc": "Orta boy yassı kart formatı; hem geniş reklam alanı hem de 45 ml uzun süreli hijyen sunar.",
        "studio_photo": "assets/cropped_products/crop_45K01S_orig.png",
        "cap_crop": "assets/cap_crops/cap_45K01S.png",
        "sibling_code": "50K01S",
        "sibling_name": "50 ml Slim Maxi Versiyonu (50K01S)",
        "sibling_crop": "assets/cap_crops/cap_50K01S.png"
    },
    {
        "code": "50K01S",
        "name": "50 ML SLİM MAXİ SPREY KOLONYA",
        "category": "Slim & Cep Serisi",
        "volume": "50 ml (1.69 fl oz)",
        "material": "Mat Siyah Polimer (Soft Touch Lüks)",
        "body_type": "Maxi Boy Yassı Kart Gövde",
        "neck_size": "Entegre Valf + Alttan Dolum Portu",
        "dims": "Y: 105 mm | En: 72 mm | Kalınlık: 15 mm",
        "label_area": "65 x 92 mm (Maksimum Reklam Alanı)",
        "print_methods": "Tam Renkli UV Baskı, Altın Yaldız Sıcak Baskı, Etiket",
        "cap_name": "YÜKSEK DOZAJLI SPREY (S)",
        "cap_group": "slim",
        "cap_mechanic": "Entegre Mikro Püskürtme, Sızdırmaz Ultrasonik Gövde",
        "cap_flow": "0.12 ml Sis Püskürtme (~450 Basım)",
        "box_qty": "120 Adet / Koli",
        "box_weight": "8.5 kg (Brüt Koli Ağırlığı)",
        "desc": "Slim serisinin amiral gemisi; mat siyah kadife dokulu yüzey üzerine altın yaldız baskıyla lüks duruş.",
        "studio_photo": "assets/cropped_products/crop_50K01S_orig.png",
        "cap_crop": "assets/cap_crops/cap_50K01S.png",
        "sibling_code": "45K01S",
        "sibling_name": "45 ml Slim Medium Seçeneği (45K01S)",
        "sibling_crop": "assets/cap_crops/cap_45K01S.png"
    },

    # --- KRİSTAL & LÜKS CAM SERİSİ (9 Products) ---
    {
        "code": "10C01S",
        "name": "10 ML PEN MİNİ CAM SPREY KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "10 ml (0.34 fl oz)",
        "material": "Şeffaf Tip-1 Cam Gövde (Borosilikat)",
        "body_type": "Kalem Tipi Silindirik Cam Tüp",
        "neck_size": "12/410 mm Metalik Boğaz",
        "dims": "Yükseklik: 115 mm | Dış Çap: Ø 14 mm",
        "label_area": "35 x 65 mm (Tam Tur veya Şeffaf Etiket)",
        "print_methods": "Şeffaf PP Etiket, UV Dijital Baskı, Sıcak Varlık",
        "cap_name": "METALİK ALÜMİNYUM SPREY (S)",
        "cap_group": "cam_sprey",
        "cap_mechanic": "Alüminyum Metalize Parfüm Valfi, Geçmeli Koruyucu Kapak",
        "cap_flow": "0.08 ml Ultra İnce Parfüm Sisi",
        "box_qty": "300 Adet / Koli",
        "box_weight": "9.0 kg (Brüt Koli Ağırlığı)",
        "desc": "Kalem formunda ince cam tüp, metalik valfi ve şık cep boyutuyla VIP kurumsal etkinlik esansı.",
        "studio_photo": "assets/cropped_products/crop_10C01S_orig.png",
        "cap_crop": "assets/cap_crops/cap_10C01S.png",
        "sibling_code": None,
        "sibling_name": "Parlak Gold & Krom Gümüş Valf Seçenekleri",
        "sibling_crop": "assets/cap_crops/cap_50C01S.png"
    },
    {
        "code": "50C01S",
        "name": "50 ML LINEA CAM SPREY KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "50 ml (1.69 fl oz)",
        "material": "Kristal Berrak Cam (Ağır Taban)",
        "body_type": "Dikey Silindirik Lüks Cam",
        "neck_size": "18/415 mm Parfüm Boğazı",
        "dims": "Yükseklik: 112 mm | Taban Çapı: Ø 38 mm",
        "label_area": "95 x 52 mm (Geniş Etiket & Serigrafi Alanı)",
        "print_methods": "Şeffaf PP Etiket, UV Dijital Baskı, Altın Varlık Serigrafi",
        "cap_name": "LÜKS PARFÜM VALFİ (S)",
        "cap_group": "cam_sprey",
        "cap_mechanic": "Metalize Gold/Gümüş Pompa, Şeffaf Akrilik Dış Kapak",
        "cap_flow": "0.12 ml Mikro Parfüm Atomizasyonu",
        "box_qty": "100 Adet / Koli",
        "box_weight": "14.5 kg (Brüt Koli Ağırlığı)",
        "desc": "Zarif dikey silindirik form, kristal cam ağırlığı ve parfümeri kalitesinde altın sprey başlığı.",
        "studio_photo": "assets/cropped_products/crop_50C01S_orig.png",
        "cap_crop": "assets/cap_crops/cap_50C01S.png",
        "sibling_code": None,
        "sibling_name": "Krom Gümüş & Mat Siyah Valf Opsiyonları",
        "sibling_crop": "assets/cap_crops/cap_100C1S.png"
    },
    {
        "code": "100C1S",
        "name": "100 ML DIAMOND CAM SPREY KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "100 ml (3.38 fl oz)",
        "material": "Ağır Tabanlı Elmas Kesim Kristal Cam",
        "body_type": "Çok Yüzeyli Fasetalı Cam Şişe",
        "neck_size": "20/410 mm Metalik Boğaz",
        "dims": "Yükseklik: 135 mm | Taban Çapı: Ø 48 mm",
        "label_area": "110 x 60 mm (Fasetalı Ön Panel Alanı)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Baskı, Altın Varlık",
        "cap_name": "KRİSTAL PARFÜM SPREY VALFİ (S)",
        "cap_group": "cam_sprey",
        "cap_mechanic": "Lüks Altın/Gümüş Metalize Valf, Akrilik Emniyet Kapağı",
        "cap_flow": "0.13 ml İnce Sis Atomizasyonu",
        "box_qty": "80 Adet / Koli",
        "box_weight": "18.5 kg (Brüt Koli Ağırlığı)",
        "desc": "Elmas kesim ışıltılı cam gövde. Işığı kıran geometrik fasetalarıyla üst düzey yönetici hediyesi.",
        "studio_photo": "assets/cropped_products/crop_100C1S_orig.png",
        "cap_crop": "assets/cap_crops/cap_100C1S.png",
        "sibling_code": "100C1D",
        "sibling_name": "Geleneksel Dökme Tıpa Seçeneği (100C1D)",
        "sibling_crop": "assets/cap_crops/cap_100C1D.png"
    },
    {
        "code": "100C1D",
        "name": "100 ML DIAMOND CAM DÖKME KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "100 ml (3.38 fl oz)",
        "material": "Ağır Tabanlı Elmas Kesim Kristal Cam",
        "body_type": "Çok Yüzeyli Fasetalı Cam Şişe",
        "neck_size": "20/410 mm Akıtıcı Boğaz",
        "dims": "Yükseklik: 130 mm | Taban Çapı: Ø 48 mm",
        "label_area": "110 x 60 mm (Fasetalı Ön Panel Alanı)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "DİKME / AKITICI TIPA KAPAK (D)",
        "cap_group": "cam_dokme",
        "cap_mechanic": "İç Sızdırmaz Damlatıcı Tıpa, Masif Altın Metalize Dış Kapak",
        "cap_flow": "Dökme / Kontrollü Geleneksel Akış",
        "box_qty": "80 Adet / Koli",
        "box_weight": "18.5 kg (Brüt Koli Ağırlığı)",
        "desc": "Geleneksel Türk dökme kolonyası ikram seramonisini lüks kristal elmas cam şişeyle buluşturur.",
        "studio_photo": "assets/cropped_products/crop_100C1D_orig.png",
        "cap_crop": "assets/cap_crops/cap_100C1D.png",
        "sibling_code": "100C1S",
        "sibling_name": "Kristal Sprey Valf Seçeneği (100C1S)",
        "sibling_crop": "assets/cap_crops/cap_100C1S.png"
    },
    {
        "code": "200C1D",
        "name": "200 ML DIAMOND CAM DÖKME KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "200 ml (6.76 fl oz)",
        "material": "Ağır Tabanlı Masif Kristal Cam",
        "body_type": "Geniş Elmas Kesim Fasetalı Gövde",
        "neck_size": "24/410 mm Lüks Akıtıcı Boğaz",
        "dims": "Yükseklik: 158 mm | Taban Çapı: Ø 58 mm",
        "label_area": "130 x 75 mm (Geniş Prestij Etiket Alanı)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, Sıcak Varlık Serigrafi",
        "cap_name": "LÜKS ALTIN TIPA KAPAK (D)",
        "cap_group": "cam_dokme",
        "cap_mechanic": "Vidalı Masif Metalize Dış Kapak, İç Sızdırmaz Damlatıcı Conta",
        "cap_flow": "Geleneksel İkram Akışı (Dökme)",
        "box_qty": "48 Adet / Koli",
        "box_weight": "19.5 kg (Brüt Koli Ağırlığı)",
        "desc": "200 ml kristal cam şişede kalıcı 80° koku seramonisi. Ağır tabanıyla makam masalarının asil simgesi.",
        "studio_photo": "assets/cropped_products/crop_200C1D_orig.png",
        "cap_crop": "assets/cap_crops/cap_200C1D.png",
        "sibling_code": None,
        "sibling_name": "Altın & Krom Gümüş Kapak Çeşitleri",
        "sibling_crop": "assets/cap_crops/cap_100C1D.png"
    },
    {
        "code": "100C2S",
        "name": "100 ML RIGA CAM SPREY KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "100 ml (3.38 fl oz)",
        "material": "Kristal Cam Gövde (Dikey Yivli)",
        "body_type": "Yivli Mimarili Silindirik Cam",
        "neck_size": "20/410 mm Parfüm Boğazı",
        "dims": "Yükseklik: 138 mm | Taban Çapı: Ø 46 mm",
        "label_area": "105 x 62 mm (Merkez Etiket Kuşağı)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "MAT SİYAH / ALTIN SPREY VALF (S)",
        "cap_group": "cam_sprey",
        "cap_mechanic": "Metalik Valf Püskürtme Mekanizması, Koruyucu Başlık",
        "cap_flow": "0.13 ml Mikro Sis Dağılımı",
        "box_qty": "80 Adet / Koli",
        "box_weight": "19.0 kg (Brüt Koli Ağırlığı)",
        "desc": "Klasik Avrupa esintili dikey yivli gövde mimarisi. Mat siyah valfi ile modern lüksü temsil eder.",
        "studio_photo": "assets/cropped_products/crop_100C2S_orig.png",
        "cap_crop": "assets/cap_crops/cap_100C2S.png",
        "sibling_code": "200C2D",
        "sibling_name": "Riga 200 ml Dökme Versiyonu (200C2D)",
        "sibling_crop": "assets/cap_crops/cap_200C2D.png"
    },
    {
        "code": "200C2D",
        "name": "200 ML RIGA CAM DÖKME KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "200 ml (6.76 fl oz)",
        "material": "Kristal Cam Gövde (Dikey Yivli Ağır Taban)",
        "body_type": "Yivli Mimarili Lüks Cam Şişe",
        "neck_size": "24/410 mm Metalize Akıtıcı Boğaz",
        "dims": "Yükseklik: 162 mm | Taban Çapı: Ø 56 mm",
        "label_area": "125 x 80 mm (Geniş Etiket Kuşağı)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, Sıcak Varlık",
        "cap_name": "ALTIN TIPA KAPAK (D)",
        "cap_group": "cam_dokme",
        "cap_mechanic": "Metalize Ağır Kapak, Akıtıcı İç Tıpa, Sızdırmaz Kapanış",
        "cap_flow": "Dökme / Damlatıcı Ağız",
        "box_qty": "48 Adet / Koli",
        "box_weight": "20.2 kg (Brüt Koli Ağırlığı)",
        "desc": "Riga koleksiyonunun 200 ml dökme versiyonu; asil duruşuyla özel hediye kutularında parlar.",
        "studio_photo": "assets/cropped_products/crop_200C2D_orig.png",
        "cap_crop": "assets/cap_crops/cap_200C2D.png",
        "sibling_code": "100C2S",
        "sibling_name": "Riga 100 ml Sprey Seçeneği (100C2S)",
        "sibling_crop": "assets/cap_crops/cap_100C2S.png"
    },
    {
        "code": "200C3D",
        "name": "200 ML PRİZMA CAM DÖKME KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "200 ml (6.76 fl oz)",
        "material": "Lüks Kristal Cam Gövde (Ağır Blok Taban)",
        "body_type": "Kare Kesitli Blok Cam Prizma",
        "neck_size": "24/410 mm Standart Diş",
        "dims": "Y: 160 mm | En: 52 mm | Boy: 52 mm",
        "label_area": "42 x 85 mm (Geniş Düz Panel Alanı)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Dijital Baskı",
        "cap_name": "KÖŞELİ ALTIN TIPA KAPAK (D)",
        "cap_group": "cam_dokme",
        "cap_mechanic": "Özel Akıtıcı İç Tıpa + Parlak Altın Vidalı Dış Kapak",
        "cap_flow": "Dökme / Kontrollü Akış",
        "box_qty": "48 Adet / Koli",
        "box_weight": "21.0 kg (Brüt Koli Ağırlığı)",
        "desc": "Köşeli prizmatik kristal gövde, ışığı yansıtan özel cam kesimi ve prestijli kurumsal duruş.",
        "studio_photo": "assets/cropped_products/crop_200C3D_orig.png",
        "cap_crop": "assets/cap_crops/cap_200C3D.png",
        "sibling_code": None,
        "sibling_name": "Altın & Krom Gümüş Tıpalı Kapak Seçenekleri",
        "sibling_crop": "assets/cap_crops/cap_250C1D.png"
    },
    {
        "code": "250C1D",
        "name": "250 ML SIGNATURE CAM DÖKME KOLONYA",
        "category": "Kristal Cam Serisi",
        "volume": "250 ml (8.45 fl oz)",
        "material": "Lüks Masif Kristal Cam (Ekstra Ağır Taban)",
        "body_type": "Kare Kaideli Anıtsal Gövde",
        "neck_size": "24/410 mm Lüks Akıtıcı Boğaz",
        "dims": "Y: 172 mm | En: 62 mm | Boy: 62 mm",
        "label_area": "50 x 95 mm (Geniş Düz Ön Vitrin)",
        "print_methods": "Kuşe Etiket, Şeffaf PP Etiket, UV Baskı, Sıcak Varlık",
        "cap_name": "VIP MASİF ALTIN TIPA KAPAK (D)",
        "cap_group": "cam_dokme",
        "cap_mechanic": "Masif Parlak Altın Kapak, Kristal Akıtıcı Tıpa, Sızdırmaz",
        "cap_flow": "Geleneksel Lüks İkram Akışı",
        "box_qty": "36 Adet / Koli",
        "box_weight": "18.8 kg (Brüt Koli Ağırlığı)",
        "desc": "Promkol kristal serisinin en heybetli tasarımı. Masif ağırlığı ile VIP kurumsal setlere mükemmel uyum.",
        "studio_photo": "assets/cropped_products/crop_250C1D_orig.png",
        "cap_crop": "assets/cap_crops/cap_250C1D.png",
        "sibling_code": None,
        "sibling_name": "Masif Altın & Krom Gümüş Metalize Başlıklar",
        "sibling_crop": "assets/cap_crops/cap_200C3D.png"
    }
]

# Cap color swatches definitions
cap_color_palettes = {
    "flip_top": [
        {"name": "Siyah", "hex": "#1E293B"},
        {"name": "Opak Beyaz", "hex": "#FFFFFF", "border": True},
        {"name": "Şeffaf / Buzlu", "hex": "#CBD5E1"},
        {"name": "Bayrak Kırmızı", "hex": "#DC2626"},
        {"name": "Kurumsal Lacivert", "hex": "#1E3A8A"},
        {"name": "Orman Yeşili", "hex": "#16A34A"}
    ],
    "sprey": [
        {"name": "Siyah Başlık", "hex": "#1E293B"},
        {"name": "Opak Beyaz Başlık", "hex": "#FFFFFF", "border": True},
        {"name": "Şeffaf Başlık", "hex": "#CBD5E1"}
    ],
    "slim": [
        {"name": "Mat Siyah (Soft Touch)", "hex": "#1E293B"},
        {"name": "Opak Kar Beyaz", "hex": "#FFFFFF", "border": True},
        {"name": "Buzlu Yarı Şeffaf", "hex": "#94A3B8"}
    ],
    "cam_sprey": [
        {"name": "Parlak Gold (Altın)", "hex": "#D4AF37"},
        {"name": "Parlak Krom (Gümüş)", "hex": "#E2E8F0", "border": True},
        {"name": "Mat Siyah Lüks", "hex": "#1E293B"}
    ],
    "cam_dokme": [
        {"name": "Lüks Masif Altın", "hex": "#D4AF37"},
        {"name": "Parlak Krom / Gümüş", "hex": "#E2E8F0", "border": True},
        {"name": "Siyah Metalize", "hex": "#1E293B"}
    ]
}

def render_color_swatches(group):
    colors = cap_color_palettes.get(group, cap_color_palettes["flip_top"])
    html = ""
    for c in colors:
        border_style = "border: 1px solid #94A3B8;" if c.get("border") else ""
        html += f"""
        <div class="swatch-item" title="{c['name']}">
            <span class="swatch-circle" style="background: {c['hex']}; {border_style}"></span>
            <span class="swatch-name">{c['name']}</span>
        </div>
        """
    return html

def render_product_card(p):
    # Sibling alternative cap section
    sibling_html = ""
    if p.get("sibling_name"):
        sib_crop = p.get("sibling_crop")
        sibling_html = f"""
        <div class="sibling-cap-box">
            <div class="sibling-thumb">
                <img src="{sib_crop}" alt="{p['sibling_name']}">
            </div>
            <div class="sibling-text">
                <span class="sib-badge">ALTERNATİF KAPAK OPSİYONU</span>
                <span class="sib-title">{p['sibling_name']}</span>
            </div>
        </div>
        """
        
    color_swatches_html = render_color_swatches(p["cap_group"])
    
    # Category tag styling
    cat_badge_color = "var(--pk-navy)"
    if "Slim" in p["category"]:
        cat_badge_color = "#334155"
    elif "Cam" in p["category"]:
        cat_badge_color = "#B45309"

    return f"""
    <div class="tech-card" id="card-{p['code']}">
        <!-- Kart Başlığı -->
        <div class="card-header">
            <div class="code-and-title">
                <div class="tech-code-badge">{p['code']}</div>
                <div class="header-titles">
                    <h3 class="prod-title">{p['name']}</h3>
                    <div class="prod-meta">
                        <span class="meta-cat" style="background: {cat_badge_color};">{p['category']}</span>
                        <span class="meta-vol">{p['volume']}</span>
                        <span class="meta-type">{p['body_type']}</span>
                    </div>
                </div>
            </div>
            <div class="header-badges">
                <span class="feat-pill"><i class="icon-check">✓</i> Doldurulabilir</span>
                <span class="feat-pill"><i class="icon-check">✓</i> 80° Alkol</span>
            </div>
        </div>

        <!-- Kart Gövdesi: 2 Kolon (Sol: Görsel & Kapak, Sağ: Teknik Şartname) -->
        <div class="card-body">
            <!-- Sol Kolon: Stüdyo Çekim Fotoğrafı & Kapak Detayı -->
            <div class="visual-col">
                <!-- Stüdyo Çekilen Ürün Fotoğrafı Podyumu -->
                <div class="studio-podium" title="Çekilen Orijinal Stüdyo Ürün Fotoğrafı: {p['code']}">
                    <div class="podium-badge">ORİJİNAL ÇEKİM</div>
                    <img class="studio-img" src="{p['studio_photo']}" alt="{p['name']}">
                    <div class="podium-shadow"></div>
                </div>

                <!-- Kapak Yakın Çekim Detay Kutusu -->
                <div class="cap-macro-box">
                    <div class="cap-macro-thumb">
                        <img src="{p['cap_crop']}" alt="{p['cap_name']}">
                        <span class="zoom-indicator">DETAY</span>
                    </div>
                    <div class="cap-macro-info">
                        <div class="cap-code-tag">{p['cap_name']}</div>
                        <div class="cap-mech-text">{p['cap_flow']}</div>
                        <div class="cap-spec-sub">{p['cap_mechanic']}</div>
                    </div>
                </div>

                <!-- Kapak Renk Çeşitleri -->
                <div class="cap-colors-block">
                    <span class="colors-headline">Mevcut Kapak Renkleri:</span>
                    <div class="swatches-wrap">
                        {color_swatches_html}
                    </div>
                </div>

                <!-- Alternatif / Kardeş Kapak Seçeneği -->
                {sibling_html}
            </div>

            <!-- Sağ Kolon: Teknik Şartname & Ölçü Tablosu -->
            <div class="specs-col">
                <div class="specs-table-title">TEKNİK ŞARTNAME & ÜRÜN ÖLÇÜLERİ</div>
                
                <table class="tech-table">
                    <tbody>
                        <tr>
                            <td class="t-key">Ürün Kodu & Hacim</td>
                            <td class="t-val"><strong style="color: var(--pk-navy);">{p['code']}</strong> &bull; {p['volume']}</td>
                        </tr>
                        <tr>
                            <td class="t-key">Gövde Malzemesi</td>
                            <td class="t-val">{p['material']}</td>
                        </tr>
                        <tr>
                            <td class="t-key">Boğaz / Ağız Çapı</td>
                            <td class="t-val"><span class="highlight-neck">{p['neck_size']}</span></td>
                        </tr>
                        <tr>
                            <td class="t-key">Şişe Dış Ebatları</td>
                            <td class="t-val">{p['dims']}</td>
                        </tr>
                        <tr>
                            <td class="t-key">Etiket & Baskı Alanı</td>
                            <td class="t-val"><span class="highlight-label">{p['label_area']}</span></td>
                        </tr>
                        <tr>
                            <td class="t-key">Uyumlu Baskı Türleri</td>
                            <td class="t-val">{p['print_methods']}</td>
                        </tr>
                        <tr>
                            <td class="t-key">Kapak Tipi & Montaj</td>
                            <td class="t-val"><strong>{p['cap_name']}</strong> &bull; {p['cap_mechanic']}</td>
                        </tr>
                        <tr>
                            <td class="t-key">Koli İçi Adet & Ağırlık</td>
                            <td class="t-val">{p['box_qty']} &bull; {p['box_weight']}</td>
                        </tr>
                        <tr>
                            <td class="t-key">Alkol & Esans Güvencesi</td>
                            <td class="t-val">80° Etil Alkol, Kalıcı Esans, Gliserinli Formül</td>
                        </tr>
                        <tr>
                            <td class="t-key">Yasal Mevzuat & Kalite</td>
                            <td class="t-val">Sağlık Bakanlığı Kozmetik Bildirimli &bull; ISO 22716 GMP</td>
                        </tr>
                    </tbody>
                </table>

                <!-- Kullanım ve Teknik Açıklama Notu -->
                <div class="tech-note-box">
                    <span class="note-label">TEKNİK AVANTAJ:</span>
                    <p class="note-desc">{p['desc']}</p>
                </div>

                <!-- Baskı Uyumluluk Rozetleri -->
                <div class="compatibility-bar">
                    <span class="compat-tag">✓ Kuşe Etiket</span>
                    <span class="compat-tag">✓ Şeffaf PP Etiket</span>
                    <span class="compat-tag">✓ UV Dijital Baskı</span>
                    <span class="compat-tag">✓ Sıcak Varlık</span>
                </div>
            </div>
        </div>
    </div>
    """

print(f"Loaded {len(products_data)} products successfully.")
