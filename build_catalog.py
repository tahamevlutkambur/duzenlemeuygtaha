import os
import json

base_dir = r"C:\Users\Taha\Pictures\kolonya"
json_path = os.path.join(base_dir, "products_catalog.json")

with open(json_path, "r", encoding="utf-8") as f:
    products = json.load(f)

# Group products
pet_prods = [p for p in products if "PET" in p.get("category", "")]
slim_prods = [p for p in products if "Slim" in p.get("category", "")]
cam_prods = [p for p in products if "Cam" in p.get("category", "")]

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

pet_pages = list(chunk_list(pet_prods, 3))
slim_pages = list(chunk_list(slim_prods, 3))
cam_pages = list(chunk_list(cam_prods, 3))

# HTML Template starts
html_head = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROMKOL 2027 | Kurumsal Promosyon Kolonyaları Kataloğu</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --pk-navy: #1E2B45;
            --pk-navy-dark: #121B2D;
            --pk-navy-light: #2A3B5E;
            --pk-lime: #91CE17;
            --pk-lime-dark: #7DB213;
            --pk-lime-soft: #F2F9E6;
            --pk-gray-bg: #F8FAFC;
            --pk-border: #E2E8F0;
            --pk-text: #1E293B;
            --pk-muted: #64748B;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #0F172A;
            color: var(--pk-text);
            -webkit-font-smoothing: antialiased;
        }

        /* Top Control Bar */
        .catalog-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 64px;
            background: rgba(18, 27, 45, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            z-index: 1000;
            color: #FFFFFF;
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .nav-logo {
            height: 38px;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        }

        .nav-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: #FFFFFF;
        }

        .nav-tagline {
            font-size: 11px;
            color: var(--pk-lime);
            font-weight: 500;
        }

        .nav-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .nav-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.1);
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .nav-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
        }

        .nav-btn.primary {
            background: var(--pk-lime);
            color: #121B2D;
            border-color: var(--pk-lime);
        }

        .nav-btn.primary:hover {
            background: #A2E21B;
            box-shadow: 0 4px 12px rgba(145, 206, 23, 0.3);
        }

        /* Mode Switcher */
        .mode-pill {
            display: flex;
            background: rgba(0, 0, 0, 0.3);
            padding: 4px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .mode-btn {
            background: transparent;
            border: none;
            color: #94A3B8;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .mode-btn.active {
            background: #FFFFFF;
            color: #121B2D;
        }

        /* Catalog Main Canvas */
        .catalog-container {
            padding-top: 84px;
            padding-bottom: 60px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
        }

        /* A4 Page Specifications (210mm x 297mm @ 96DPI is ~794px x 1123px) */
        .a4-page {
            width: 794px;
            min-height: 1123px;
            max-height: 1123px;
            background: #FFFFFF;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05);
            border-radius: 2px;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* Page Layout Styles */
        .page-header {
            height: 72px;
            padding: 0 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--pk-border);
            background: #FFFFFF;
        }

        .ph-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .ph-logo {
            height: 30px;
        }

        .ph-badge {
            background: var(--pk-lime-soft);
            color: var(--pk-lime-dark);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .ph-right {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 12px;
            font-weight: 600;
            color: var(--pk-muted);
        }

        .page-footer {
            height: 52px;
            padding: 0 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid var(--pk-border);
            font-size: 11px;
            color: var(--pk-muted);
            background: #FFFFFF;
            margin-top: auto;
        }

        .pf-brand {
            font-weight: 600;
            color: var(--pk-navy);
        }

        .pf-slogan {
            font-family: 'Caveat', cursive;
            font-size: 16px;
            color: var(--pk-lime-dark);
        }

        .pf-num {
            font-weight: 700;
            color: var(--pk-navy);
            background: var(--pk-gray-bg);
            padding: 4px 10px;
            border-radius: 4px;
        }

        /* Product Grid (3 items per page) */
        .products-grid-3 {
            flex: 1;
            padding: 24px 36px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            justify-content: space-between;
        }

        .product-card {
            background: #FFFFFF;
            border: 1px solid var(--pk-border);
            border-radius: 12px;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            gap: 24px;
            height: 290px;
            position: relative;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .product-card:hover {
            border-color: var(--pk-lime);
            box-shadow: 0 8px 24px -8px rgba(30, 43, 69, 0.12);
        }

        /* Dual Visual Presentation */
        .prod-visuals {
            display: flex;
            align-items: center;
            gap: 14px;
            width: 320px;
            height: 100%;
            flex-shrink: 0;
        }

        .visual-box {
            flex: 1;
            height: 100%;
            background: var(--pk-gray-bg);
            border-radius: 8px;
            border: 1px solid rgba(0, 0, 0, 0.04);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            padding: 10px;
            overflow: hidden;
        }

        .visual-box img {
            max-width: 100%;
            max-height: 215px;
            object-fit: contain;
            filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.08));
            transition: transform 0.2s ease;
        }

        .product-card:hover .visual-box img {
            transform: scale(1.03);
        }

        .visual-badge {
            position: absolute;
            bottom: 8px;
            left: 8px;
            right: 8px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(0, 0, 0, 0.06);
            padding: 4px;
            border-radius: 4px;
            font-size: 9px;
            font-weight: 700;
            text-align: center;
            color: var(--pk-navy);
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }

        .visual-badge.brand-badge {
            background: var(--pk-navy);
            color: var(--pk-lime);
            border: none;
        }

        /* Product Details Info */
        .prod-info {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 10px;
        }

        .prod-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .prod-code-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--pk-navy);
            color: #FFFFFF;
            padding: 6px 14px;
            border-radius: 6px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 15px;
            letter-spacing: 0.5px;
        }

        .prod-code-badge .code-accent {
            color: var(--pk-lime);
        }

        .prod-volume-badge {
            background: var(--pk-lime-soft);
            color: var(--pk-lime-dark);
            font-weight: 700;
            font-size: 12px;
            padding: 4px 10px;
            border-radius: 20px;
        }

        .prod-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 16px;
            font-weight: 800;
            color: var(--pk-navy);
            line-height: 1.3;
        }

        .prod-desc {
            font-size: 11.5px;
            color: var(--pk-muted);
            line-height: 1.45;
        }

        .spec-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
            background: var(--pk-gray-bg);
            border-radius: 6px;
            overflow: hidden;
        }

        .spec-table td {
            padding: 5px 8px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.04);
        }

        .spec-table tr:last-child td {
            border-bottom: none;
        }

        .spec-label {
            font-weight: 600;
            color: var(--pk-muted);
            width: 38%;
        }

        .spec-val {
            font-weight: 700;
            color: var(--pk-navy);
        }

        /* COVER PAGE STYLES */
        .cover-page {
            background: linear-gradient(135deg, var(--pk-navy-dark) 0%, var(--pk-navy) 60%, #152238 100%);
            color: #FFFFFF;
            padding: 60px 50px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .cover-decor {
            position: absolute;
            top: -100px;
            right: -100px;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(145, 206, 23, 0.15) 0%, rgba(30, 43, 69, 0) 70%);
            pointer-events: none;
        }

        .cover-decor-bottom {
            position: absolute;
            bottom: -150px;
            left: -150px;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(145, 206, 23, 0.08) 0%, rgba(30, 43, 69, 0) 70%);
            pointer-events: none;
        }

        .cover-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 2;
        }

        .cover-logo {
            height: 64px;
            filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
        }

        .cover-year {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: var(--pk-lime);
            letter-spacing: 2px;
            border: 2px solid var(--pk-lime);
            padding: 6px 18px;
            border-radius: 8px;
        }

        .cover-body {
            z-index: 2;
            margin: 40px 0;
        }

        .cover-pill {
            display: inline-block;
            background: rgba(145, 206, 23, 0.15);
            border: 1px solid var(--pk-lime);
            color: var(--pk-lime);
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            padding: 6px 16px;
            border-radius: 30px;
            margin-bottom: 24px;
        }

        .cover-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 46px;
            font-weight: 900;
            line-height: 1.15;
            letter-spacing: -0.5px;
            color: #FFFFFF;
            margin-bottom: 20px;
        }

        .cover-title span {
            color: var(--pk-lime);
        }

        .cover-slogan {
            font-family: 'Caveat', cursive;
            font-size: 38px;
            color: #E2E8F0;
            margin-bottom: 30px;
        }

        .cover-hero-img {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
            z-index: 2;
        }

        .hero-bottle {
            height: 380px;
            object-fit: contain;
            filter: drop-shadow(0 20px 30px rgba(0, 0, 0, 0.5));
            transform: translateY(0);
            transition: transform 0.3s;
        }

        .hero-bottle:hover {
            transform: translateY(-8px);
        }

        .cover-footer {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            padding-top: 24px;
            z-index: 2;
        }

        .cover-footer-left {
            font-size: 12px;
            color: #94A3B8;
            line-height: 1.6;
        }

        .cover-footer-left strong {
            color: #FFFFFF;
        }

        .cover-footer-right {
            text-align: right;
            font-size: 12px;
            color: var(--pk-lime);
            font-weight: 600;
        }

        /* ABOUT / CORPORATE PAGE */
        .editorial-page {
            padding: 44px 44px;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .section-eyebrow {
            color: var(--pk-lime-dark);
            font-weight: 800;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        .section-heading {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 28px;
            font-weight: 800;
            color: var(--pk-navy);
            line-height: 1.25;
            margin-top: 4px;
        }

        .editorial-text {
            font-size: 13.5px;
            color: #334155;
            line-height: 1.75;
        }

        .pillars-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 10px;
        }

        .pillar-card {
            background: var(--pk-gray-bg);
            border: 1px solid var(--pk-border);
            border-radius: 10px;
            padding: 20px;
        }

        .pillar-icon {
            font-size: 26px;
            margin-bottom: 12px;
        }

        .pillar-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: var(--pk-navy);
            margin-bottom: 8px;
        }

        .pillar-desc {
            font-size: 11.5px;
            color: var(--pk-muted);
            line-height: 1.5;
        }

        .quote-box {
            background: linear-gradient(135deg, var(--pk-navy) 0%, var(--pk-navy-light) 100%);
            border-radius: 12px;
            padding: 24px 30px;
            color: #FFFFFF;
            position: relative;
        }

        .quote-text {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 17px;
            font-weight: 700;
            line-height: 1.5;
            color: #FFFFFF;
        }

        .quote-text span {
            color: var(--pk-lime);
        }

        .quote-author {
            font-family: 'Caveat', cursive;
            font-size: 22px;
            color: var(--pk-lime);
            margin-top: 10px;
        }

        /* SCENTS & BRANDING PAGE */
        .scents-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
        }

        .scent-item {
            display: flex;
            align-items: center;
            gap: 14px;
            background: var(--pk-gray-bg);
            border: 1px solid var(--pk-border);
            padding: 14px;
            border-radius: 10px;
        }

        .scent-bullet {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: #FFFFFF;
            border: 2px solid var(--pk-lime);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }

        .scent-name {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 14px;
            font-weight: 800;
            color: var(--pk-navy);
        }

        .scent-notes {
            font-size: 11px;
            color: var(--pk-muted);
            margin-top: 2px;
        }

        /* BACK COVER */
        .back-cover {
            background: linear-gradient(135deg, var(--pk-navy-dark) 0%, var(--pk-navy) 100%);
            color: #FFFFFF;
            padding: 60px 50px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            text-align: center;
        }

        .bc-logo {
            height: 90px;
            margin-bottom: 16px;
        }

        .bc-slogan {
            font-family: 'Caveat', cursive;
            font-size: 42px;
            color: var(--pk-lime);
            margin-bottom: 30px;
        }

        .contact-card-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            width: 100%;
            max-width: 600px;
            margin: 40px 0;
        }

        .contact-box {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            text-align: left;
        }

        .contact-box h4 {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--pk-lime);
            letter-spacing: 1px;
            margin-bottom: 6px;
        }

        .contact-box p {
            font-size: 14px;
            font-weight: 600;
            color: #FFFFFF;
        }

        /* Live Code Editor Drawer */
        .editor-drawer {
            position: fixed;
            top: 0;
            right: -480px;
            width: 460px;
            height: 100vh;
            background: #FFFFFF;
            box-shadow: -10px 0 30px rgba(0, 0, 0, 0.3);
            z-index: 2000;
            transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
        }

        .editor-drawer.open {
            right: 0;
        }

        .editor-header {
            padding: 20px;
            background: var(--pk-navy);
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .editor-body {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .editor-item {
            background: var(--pk-gray-bg);
            border: 1px solid var(--pk-border);
            border-radius: 8px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .editor-item label {
            font-size: 11px;
            font-weight: 700;
            color: var(--pk-muted);
            text-transform: uppercase;
        }

        .editor-item input, .editor-item textarea {
            width: 100%;
            padding: 8px 10px;
            border: 1px solid var(--pk-border);
            border-radius: 6px;
            font-size: 13px;
            font-family: inherit;
        }

        .editor-footer {
            padding: 16px 20px;
            border-top: 1px solid var(--pk-border);
            display: flex;
            gap: 10px;
        }

        /* PRINT STYLES FOR PERFECT A4 EXPORT */
        @media print {
            body {
                background: #FFFFFF !important;
                color: #000000 !important;
            }

            .catalog-nav, .editor-drawer, .nav-btn, .mode-pill {
                display: none !important;
            }

            .catalog-container {
                padding: 0 !important;
                margin: 0 !important;
                display: block !important;
            }

            .a4-page {
                width: 210mm !important;
                height: 297mm !important;
                min-height: 297mm !important;
                max-height: 297mm !important;
                page-break-after: always !important;
                page-break-inside: avoid !important;
                box-shadow: none !important;
                border-radius: 0 !important;
                margin: 0 !important;
                overflow: hidden !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }

            @page {
                size: A4 portrait;
                margin: 0;
            }
        }
    </style>
</head>
<body>

    <!-- TOP CONTROL NAVIGATION -->
    <nav class="catalog-nav">
        <div class="nav-brand">
            <img src="assets/promkol_logo_hires_dark.png" alt="PROMKOL" class="nav-logo">
            <div>
                <div class="nav-title">PROMKOL 2027 E-KATALOG</div>
                <div class="nav-tagline">Miss gibi promosyon • Kurumsal Promosyon Kolonyaları</div>
            </div>
        </div>

        <div class="nav-actions">
            <div class="mode-pill">
                <button class="mode-btn active" id="btnAllPages" onclick="setViewMode('grid')">Tüm Sayfalar</button>
                <button class="mode-btn" id="btnSlider" onclick="setViewMode('slider')">Sayfa Sayfa</button>
            </div>
            <button class="nav-btn" onclick="toggleEditor()">
                ✏️ Kod & Ürün Düzenleyici
            </button>
            <button class="nav-btn primary" onclick="window.print()">
                🖨️ PDF İndir / Yazdır (A4)
            </button>
        </div>
    </nav>

    <!-- LIVE CODE EDITOR DRAWER -->
    <div class="editor-drawer" id="editorDrawer">
        <div class="editor-header">
            <div>
                <h3 style="font-size: 16px; font-weight: 800;">Ürün Kodu & Bilgi Düzenleyici</h3>
                <p style="font-size: 12px; color: var(--pk-lime);">Değişiklikler kataloğa anında yansır</p>
            </div>
            <button onclick="toggleEditor()" style="background: transparent; border: none; color: white; font-size: 22px; cursor: pointer;">&times;</button>
        </div>
        <div style="padding: 12px 20px; border-bottom: 1px solid var(--pk-border);">
            <input type="text" id="codeSearch" placeholder="Ürün kodu ara (Örn: 30P01F, 20K01S)..." onkeyup="filterEditor(this.value)" style="width: 100%; padding: 8px 12px; border: 1px solid var(--pk-border); border-radius: 6px; font-size: 13px;">
        </div>
        <div class="editor-body" id="editorList">
            <!-- Dynamically populated -->
        </div>
        <div class="editor-footer">
            <button class="nav-btn primary" style="flex: 1;" onclick="applyEdits()">Kataloğu Güncelle</button>
            <button class="nav-btn" style="flex: 1; color: var(--pk-navy); border-color: var(--pk-border);" onclick="downloadUpdatedJSON()">JSON İndir</button>
        </div>
    </div>

    <!-- MAIN CATALOG CONTAINER -->
    <main class="catalog-container" id="catalogCanvas">
"""

# Helper to build a product card
def build_product_card(p):
    code = p["code"]
    name = p["name"]
    vol = p["volume"]
    cap = p["cap_type"]
    mat = p["material"]
    desc = p["description"]
    photo = p.get("crop_orig", p["photo_png"])
    mockup = p.get("crop_mock", p["mockup_png"])
    
    # Cap badge color logic
    cap_short = "Sprey (S)" if "(S)" in cap else ("Flip-Top (F)" if "(F)" in cap else "Dökme / Dikme (D)")
    
    # Specific print types based on bottle material/style
    style = p.get("style", "white_label")
    if "white_label" in style:
        baski_val = "Beyaz Kuşe Etiket / Şeffaf Serigrafi"
    elif "card" in style:
        baski_val = "Çift Taraflı Tam Alan UV Baskı"
    elif "glass" in style:
        baski_val = "Lüks Serigrafi / Altın Varak Baskı"
    else:
        baski_val = "Şeffaf Serigrafi / Doğrudan UV Baskı"

    return f"""
        <div class="product-card" id="card-{code}">
            <div class="prod-visuals">
                <div class="visual-box">
                    <img src="{photo}" alt="{code} Orijinal Şişe" loading="lazy">
                    <div class="visual-badge">Orijinal Şişe</div>
                </div>
                <div class="visual-box">
                    <img src="{mockup}" alt="{code} Sizin Markanız" loading="lazy">
                    <div class="visual-badge brand-badge">Sizin Markanız</div>
                </div>
            </div>
            <div class="prod-info">
                <div class="prod-top">
                    <div class="prod-code-badge">
                        <span>KOD:</span>
                        <span class="code-accent" id="badge-code-{code}">{code}</span>
                    </div>
                    <div class="prod-volume-badge">{vol}</div>
                </div>
                <h3 class="prod-title" id="title-{code}">{name}</h3>
                <p class="prod-desc" id="desc-{code}">{desc}</p>
                <table class="spec-table">
                    <tr>
                        <td class="spec-label">Hacim:</td>
                        <td class="spec-val">{vol}</td>
                    </tr>
                    <tr>
                        <td class="spec-label">Kapak Tipi:</td>
                        <td class="spec-val">{cap_short}</td>
                    </tr>
                    <tr>
                        <td class="spec-label">Şişe Materyali:</td>
                        <td class="spec-val">{mat}</td>
                    </tr>
                    <tr>
                        <td class="spec-label">Baskı Türü:</td>
                        <td class="spec-val">{baski_val}</td>
                    </tr>
                    <tr>
                        <td class="spec-label">Esans / Dolum:</td>
                        <td class="spec-val">80° Doğal Kolonya (Limon, Ice, Kaşmir vb.)</td>
                    </tr>
                </table>
            </div>
        </div>
    """

# Build Pages
pages_html = []
current_page_num = 1

# --- PAGE 1: COVER ---
cover_html = f"""
    <section class="a4-page cover-page" id="page-{current_page_num}">
        <div class="cover-decor"></div>
        <div class="cover-decor-bottom"></div>
        <div class="cover-header">
            <img src="assets/promkol_logo_hires_dark.png" alt="PROMKOL Logo" class="cover-logo">
            <div class="cover-year">2027 KOLEKSİYONU</div>
        </div>
        <div class="cover-body">
            <div class="cover-pill">Kurumsal Promosyon Kolonyaları</div>
            <h1 class="cover-title">Markanız Her Yerde<br><span>Taze ve Kalıcı</span></h1>
            <div class="cover-slogan">"Miss gibi promosyon"</div>
            <div class="cover-hero-img">
                <img src="assets/cropped_mockups/crop_50P01F_mock.png" alt="Hero Bottle 1" class="hero-bottle" style="height: 320px;">
                <img src="assets/cropped_mockups/crop_100C1S_mock.png" alt="Hero Bottle 2" class="hero-bottle" style="height: 380px;">
                <img src="assets/cropped_mockups/crop_20K01S_mock.png" alt="Hero Bottle 3" class="hero-bottle" style="height: 300px;">
            </div>
        </div>
        <div class="cover-footer">
            <div class="cover-footer-left">
                <p><strong>PROMKOL PROMOSYON SAN. VE TİC. LTD. ŞTİ.</strong></p>
                <p>PET Serisi • Slim Serisi • Kristal Cam Serisi • Özel Koku Formülleri</p>
            </div>
            <div class="cover-footer-right">
                <p>www.promkol.com</p>
                <p style="color: #FFFFFF; font-weight: 400; font-size: 11px;">Kurumsal Ürün Kataloğu</p>
            </div>
        </div>
    </section>
"""
pages_html.append(cover_html)
current_page_num += 1

# --- PAGE 2: CORPORATE / ABOUT US ---
about_html = f"""
    <section class="a4-page" id="page-{current_page_num}">
        <div class="page-header">
            <div class="ph-left">
                <img src="assets/promkol_logo_hires_light.png" alt="PROMKOL" class="ph-logo">
                <span class="ph-badge">Kurumsal Profil</span>
            </div>
            <div class="ph-right">BİZ KİMİZ?</div>
        </div>
        <div class="editorial-page">
            <div>
                <div class="section-eyebrow">Biz Kimiz & Ne Yapıyoruz?</div>
                <h2 class="section-heading">Kolonya Üzerinden Markaların Reklamını Yapıyoruz</h2>
            </div>
            <p class="editorial-text">
                <strong>PROMKOL</strong>, kurumsal firmalara özel promosyon kolonyası hazırlayan, bu alanda uzmanlaşmış yenilikçi bir markadır. 
                Biz her türlü promosyon ürününü satan klasik bir toptancı değiliz; bilinçli olarak tek bir alana odaklandık: <strong>Promosyon Kolonyası.</strong>
            </p>
            <p class="editorial-text">
                Bizim işimiz yalnızca şişelere kolonya doldurup satmak değil. Asıl yaptığımız şey, firmaların kendi markalarını taşıyan, müşterilerine ve iş ortaklarına gönül rahatlığıyla hediye edebilecekleri, kullanışlı, şık ve kaliteli bir tanıtım ürünü ortaya çıkarmaktır.
                Bir otomobil firması, banka, otel, hastane veya kurumsal işletme müşterisine kendi logosunu taşıyan bir kolonya hediye ettiğinde, o kolonya arabada, çantada, ofiste ve evde aylarca yer edinir. <strong>Her kullanımda firmanızın logosuyla yeniden karşılaşılır.</strong>
            </p>

            <div class="pillars-grid">
                <div class="pillar-card">
                    <div class="pillar-icon">🎯</div>
                    <h3 class="pillar-title">Odaklanmış Uzmanlık</h3>
                    <p class="pillar-desc">Sadece promosyon kolonyasında derinleşerek şişe kalitesi, sızdırmazlık ve baskı teknolojisinde liderlik sunuyoruz.</p>
                </div>
                <div class="pillar-card">
                    <div class="pillar-icon">💎</div>
                    <h3 class="pillar-title">Müşteri Markası Ön Planda</h3>
                    <p class="pillar-desc">Biz arka plandaki profesyoneliz. Şişenin üzerindeki asıl yıldız müşterimizin logosu ve kurumsal kimliğidir.</p>
                </div>
                <div class="pillar-card">
                    <div class="pillar-icon">🌿</div>
                    <h3 class="pillar-title">Yüksek Esans Kalitesi</h3>
                    <p class="pillar-desc">80 derece saf alkol, doğal bitkisel esanslar ve uzun süre kalıcı ferahlık veren özel koku reçeteleri.</p>
                </div>
            </div>

            <div class="quote-box">
                <p class="quote-text">
                    "Küçücük bir kolonya şişesini, üzerinde firmanızın kimliğini gururla taşıyan <span>prestijli bir kurumsal tanıtım ürününe</span> dönüştürüyoruz."
                </p>
                <div class="quote-author">PROMKOL • "Miss gibi promosyon"</div>
            </div>
        </div>
        <div class="page-footer">
            <span class="pf-brand">PROMKOL 2027</span>
            <span class="pf-slogan">Miss gibi promosyon</span>
            <span class="pf-num">0{current_page_num}</span>
        </div>
    </section>
"""
pages_html.append(about_html)
current_page_num += 1

# --- PAGE 3: SCENTS & BRANDING OPTIONS ---
scents_html = f"""
    <section class="a4-page" id="page-{current_page_num}">
        <div class="page-header">
            <div class="ph-left">
                <img src="assets/promkol_logo_hires_light.png" alt="PROMKOL" class="ph-logo">
                <span class="ph-badge">Koku & Baskı Rehberi</span>
            </div>
            <div class="ph-right">KİŞİSELLEŞTİRME</div>
        </div>
        <div class="editorial-page">
            <div>
                <div class="section-eyebrow">Duyulara Hitap Eden Çözümler</div>
                <h2 class="section-heading">Özel Koku Koleksiyonu & Baskı Standartları</h2>
            </div>
            
            <p class="editorial-text">
                Koku bizim için çok önemli. Ürünlerimizin yalnızca güzel görünmesini değil, kullanıldığında akılda kalıcı zarif bir izlenim bırakmasını önemsiyoruz. Kurumsal kimliğinize en uygun koku notasını seçebilirsiniz:
            </p>

            <div class="scents-grid">
                <div class="scent-item">
                    <div class="scent-bullet">🍋</div>
                    <div>
                        <div class="scent-name">Çeşme Limonu (80°)</div>
                        <div class="scent-notes">Geleneksel Türk misafirperverliği, canlandırıcı taze narenciye.</div>
                    </div>
                </div>
                <div class="scent-item">
                    <div class="scent-bullet">❄️</div>
                    <div>
                        <div class="scent-name">Ice Cool Breeze</div>
                        <div class="scent-notes">Buz ferahlığı, mentol ve odunsu maskülen alt notalar.</div>
                    </div>
                </div>
                <div class="scent-item">
                    <div class="scent-bullet">🌸</div>
                    <div>
                        <div class="scent-name">Japon Kiraz Çiçeği</div>
                        <div class="scent-notes">Zarif çiçeksi esintiler, baharın enerjisini taşıyan yumuşak koku.</div>
                    </div>
                </div>
                <div class="scent-item">
                    <div class="scent-bullet">🍃</div>
                    <div>
                        <div class="scent-name">Yeşil Çay & Bambu</div>
                        <div class="scent-notes">Modern ofis ortamları için dingin, tazeleyici ve ferahlatıcı etki.</div>
                    </div>
                </div>
                <div class="scent-item">
                    <div class="scent-bullet">🧶</div>
                    <div>
                        <div class="scent-name">Kaşmir & Beyaz Çiçekler</div>
                        <div class="scent-notes">Sıcak, pudralı ve lüks otel lobilerini andıran sofistike dokunuş.</div>
                    </div>
                </div>
                <div class="scent-item">
                    <div class="scent-bullet">🍊</div>
                    <div>
                        <div class="scent-name">Bodrum Mandalinası</div>
                        <div class="scent-notes">Güneşli Ege bahçelerinin tatlı ve enerjik narenciye aroması.</div>
                    </div>
                </div>
            </div>

            <div style="background: var(--pk-gray-bg); border: 1px solid var(--pk-border); border-radius: 12px; padding: 20px; margin-top: 6px;">
                <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 800; color: var(--pk-navy); margin-bottom: 12px;">
                    ✨ Şişe Üzeri Baskı & Etiketleme Seçeneklerimiz
                </h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; font-size: 11.5px;">
                    <div>
                        <strong style="color: var(--pk-navy); display: block; margin-bottom: 4px;">1. Şeffaf Serigrafi / UV:</strong>
                        Şişe üzerine doğrudan yapılan, zeminsiz şeffaf baskı. Şişenin içindeki kolonyayı gösteren modern lüks görünüm.
                    </div>
                    <div>
                        <strong style="color: var(--pk-navy); display: block; margin-bottom: 4px;">2. Beyaz Opak Kuşe Etiket:</strong>
                        Suya ve neme dayanıklı özel kuşe etiket. Canlı kurumsal renkler, logonuz ve QR kod için maksimum okunurluk.
                    </div>
                    <div>
                        <strong style="color: var(--pk-navy); display: block; margin-bottom: 4px;">3. Kapak & Sprey Çeşitleri:</strong>
                        Flip-Top (F), Atomizer Sprey (S) veya Tıpalı Dikme (D) seçenekleri; beyaz, siyah veya şeffaf kapak renkleri.
                    </div>
                </div>
            </div>
        </div>
        <div class="page-footer">
            <span class="pf-brand">PROMKOL 2027</span>
            <span class="pf-slogan">Miss gibi promosyon</span>
            <span class="pf-num">0{current_page_num}</span>
        </div>
    </section>
"""
pages_html.append(scents_html)
current_page_num += 1

# --- PAGE 4: TABLE OF CONTENTS ---
toc_html = f"""
    <section class="a4-page" id="page-{current_page_num}">
        <div class="page-header">
            <div class="ph-left">
                <img src="assets/promkol_logo_hires_light.png" alt="PROMKOL" class="ph-logo">
                <span class="ph-badge">Koleksiyon Dizini</span>
            </div>
            <div class="ph-right">İÇİNDEKİLER</div>
        </div>
        <div class="editorial-page" style="justify-content: space-between;">
            <div>
                <div class="section-eyebrow">Ürün Koleksiyonumuz</div>
                <h2 class="section-heading">Kategori ve Model Rehberi</h2>
                <p class="editorial-text" style="margin-top: 8px;">
                    Tüm promosyon kolonyası modellerimiz 3 ana koleksiyonda toplanmıştır. İhtiyacınıza, dağıtım alanınıza ve bütçenize uygun seriyi seçebilirsiniz:
                </p>
            </div>

            <div style="display: flex; flex-direction: column; gap: 16px;">
                <!-- Category 1 -->
                <div style="background: var(--pk-gray-bg); border-left: 6px solid var(--pk-navy); border-radius: 8px; padding: 20px 24px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span style="font-size: 11px; font-weight: 800; color: var(--pk-lime-dark); letter-spacing: 1px;">01. BÖLÜM</span>
                        <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 19px; font-weight: 800; color: var(--pk-navy);">PET SERİSİ KOLONYALAR</h3>
                        <p style="font-size: 12px; color: var(--pk-muted); margin-top: 4px;">30 ml'den 400 ml'ye kadar silindirik, yassı, kavisli ve prizmatik ekonomik çözümler (18 Model)</p>
                    </div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 800; color: var(--pk-navy);">
                        S. 05 - 10
                    </div>
                </div>

                <!-- Category 2 -->
                <div style="background: var(--pk-gray-bg); border-left: 6px solid var(--pk-lime); border-radius: 8px; padding: 20px 24px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span style="font-size: 11px; font-weight: 800; color: var(--pk-lime-dark); letter-spacing: 1px;">02. BÖLÜM</span>
                        <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 19px; font-weight: 800; color: var(--pk-navy);">SLİM & KART SPREY SERİSİ</h3>
                        <p style="font-size: 12px; color: var(--pk-muted); margin-top: 4px;">Cep, çanta ve cüzdan boyu kredi kartı formatında ultra taşınabilir zarif spreyler (5 Model)</p>
                    </div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 800; color: var(--pk-navy);">
                        S. 11 - 12
                    </div>
                </div>

                <!-- Category 3 -->
                <div style="background: var(--pk-gray-bg); border-left: 6px solid #C084FC; border-radius: 8px; padding: 20px 24px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span style="font-size: 11px; font-weight: 800; color: #9333EA; letter-spacing: 1px;">03. BÖLÜM</span>
                        <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 19px; font-weight: 800; color: var(--pk-navy);">KRİSTAL CAM SERİSİ</h3>
                        <p style="font-size: 12px; color: var(--pk-muted); margin-top: 4px;">Diamond, Riga, Linea ve Signature modelleri; VIP hediye ve üst yönetim prestiji (9 Model)</p>
                    </div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 800; color: var(--pk-navy);">
                        S. 13 - 15
                    </div>
                </div>

                <!-- Category 4 -->
                <div style="background: var(--pk-gray-bg); border-left: 6px solid #64748B; border-radius: 8px; padding: 20px 24px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span style="font-size: 11px; font-weight: 800; color: var(--pk-muted); letter-spacing: 1px;">04. BÖLÜM</span>
                        <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 19px; font-weight: 800; color: var(--pk-navy);">SİPARİŞ SÜRECİ & KOD İNDEKSİ</h3>
                        <p style="font-size: 12px; color: var(--pk-muted); margin-top: 4px;">Numune onayı, teslimat koşulları ve 32 modelin tam kod karşılaştırma cetveli</p>
                    </div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 800; color: var(--pk-navy);">
                        S. 16 - 17
                    </div>
                </div>
            </div>

            <div style="text-align: center; font-size: 11.5px; color: var(--pk-muted); padding-top: 10px;">
                Tüm modellerimizde <strong>Flip-Top (F)</strong> ve <strong>Sprey (S)</strong> seçenekleri ihtiyaca göre uyarlanabilmektedir.
            </div>
        </div>
        <div class="page-footer">
            <span class="pf-brand">PROMKOL 2027</span>
            <span class="pf-slogan">Miss gibi promosyon</span>
            <span class="pf-num">0{current_page_num}</span>
        </div>
    </section>
"""
pages_html.append(toc_html)
current_page_num += 1

# --- PAGES 5 - 10: PET SERİSİ (6 Pages) ---
for idx, page_prods in enumerate(pet_pages, 1):
    cards_html = "".join([build_product_card(p) for p in page_prods])
    pet_html = f"""
        <section class="a4-page" id="page-{current_page_num}">
            <div class="page-header">
                <div class="ph-left">
                    <img src="assets/promkol_logo_hires_light.png" alt="PROMKOL" class="ph-logo">
                    <span class="ph-badge">PET Serisi • {idx}/6</span>
                </div>
                <div class="ph-right">EKONOMİK & PRATİK ÇÖZÜMLER</div>
            </div>
            <div class="products-grid-3">
                {cards_html}
            </div>
            <div class="page-footer">
                <span class="pf-brand">PROMKOL 2027 • PET Serisi</span>
                <span class="pf-slogan">Miss gibi promosyon</span>
                <span class="pf-num">{current_page_num:02d}</span>
            </div>
        </section>
    """
    pages_html.append(pet_html)
    current_page_num += 1

# --- PAGES 11 - 12: SLİM SERİSİ (2 Pages) ---
for idx, page_prods in enumerate(slim_pages, 1):
    cards_html = "".join([build_product_card(p) for p in page_prods])
    slim_html = f"""
        <section class="a4-page" id="page-{current_page_num}">
            <div class="page-header">
                <div class="ph-left">
                    <img src="assets/promkol_logo_hires_light.png" alt="PROMKOL" class="ph-logo">
                    <span class="ph-badge" style="background: #EBF8FF; color: #0284C7;">Slim & Kart Serisi • {idx}/2</span>
                </div>
                <div class="ph-right">CEP & ÇANTA BOYU ZARAFET</div>
            </div>
            <div class="products-grid-3">
                {cards_html}
            </div>
            <div class="page-footer">
                <span class="pf-brand">PROMKOL 2027 • Slim Serisi</span>
                <span class="pf-slogan">Miss gibi promosyon</span>
                <span class="pf-num">{current_page_num:02d}</span>
            </div>
        </section>
    """
    pages_html.append(slim_html)
    current_page_num += 1

# --- PAGES 13 - 15: CAM SERİSİ (3 Pages) ---
for idx, page_prods in enumerate(cam_pages, 1):
    cards_html = "".join([build_product_card(p) for p in page_prods])
    cam_html = f"""
        <section class="a4-page" id="page-{current_page_num}">
            <div class="page-header">
                <div class="ph-left">
                    <img src="assets/promkol_logo_hires_light.png" alt="PROMKOL" class="ph-logo">
                    <span class="ph-badge" style="background: #FAF5FF; color: #9333EA;">Kristal Cam Serisi • {idx}/3</span>
                </div>
                <div class="ph-right">PRESTİJ & VIP HEDİYE</div>
            </div>
            <div class="products-grid-3">
                {cards_html}
            </div>
            <div class="page-footer">
                <span class="pf-brand">PROMKOL 2027 • Cam Serisi</span>
                <span class="pf-slogan">Miss gibi promosyon</span>
                <span class="pf-num">{current_page_num:02d}</span>
            </div>
        </section>
    """
    pages_html.append(cam_html)
    current_page_num += 1

# --- PAGE 16: ORDERING & PRODUCTION PROCESS ---
process_html = f"""
    <section class="a4-page" id="page-{current_page_num}">
        <div class="page-header">
            <div class="ph-left">
                <img src="assets/promkol_logo_hires_light.png" alt="PROMKOL" class="ph-logo">
                <span class="ph-badge">Hizmet Standartları</span>
            </div>
            <div class="ph-right">SİPARİŞ SÜRECİ</div>
        </div>
        <div class="editorial-page" style="justify-content: space-between;">
            <div>
                <div class="section-eyebrow">Nasıl Çalışıyoruz?</div>
                <h2 class="section-heading">4 Adımda Markanıza Özel Üretim</h2>
                <p class="editorial-text" style="margin-top: 8px;">
                    Kurumsal siparişlerinizin her aşamasında onayınız alınır, numune ve dijital prova ile sıfır hata garantisi sağlanır:
                </p>
            </div>

            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                <div style="background: var(--pk-gray-bg); border: 1px solid var(--pk-border); border-radius: 12px; padding: 24px;">
                    <div style="font-size: 32px; margin-bottom: 12px;">1️⃣</div>
                    <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 800; color: var(--pk-navy); margin-bottom: 8px;">Model & Hacim Seçimi</h3>
                    <p style="font-size: 12px; color: var(--pk-muted); line-height: 1.6;">
                        PET, Slim veya Kristal Cam serilerimizden bütçenize ve hedef kitlenize uygun şişe formunu ve kapak tipini (Fliptop / Sprey) belirlersiniz.
                    </p>
                </div>
                <div style="background: var(--pk-gray-bg); border: 1px solid var(--pk-border); border-radius: 12px; padding: 24px;">
                    <div style="font-size: 32px; margin-bottom: 12px;">2️⃣</div>
                    <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 800; color: var(--pk-navy); margin-bottom: 8px;">Grafik & Mockup Onayı</h3>
                    <p style="font-size: 12px; color: var(--pk-muted); line-height: 1.6;">
                        Vektörel logonuz şişe üzerine 3D mockup olarak yerleştirilir. Şeffaf serigrafi veya opak kuşe etiket baskı provası dijital olarak onayınıza sunulur.
                    </p>
                </div>
                <div style="background: var(--pk-gray-bg); border: 1px solid var(--pk-border); border-radius: 12px; padding: 24px;">
                    <div style="font-size: 32px; margin-bottom: 12px;">3️⃣</div>
                    <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 800; color: var(--pk-navy); margin-bottom: 8px;">Koku & Dolum Aşaması</h3>
                    <p style="font-size: 12px; color: var(--pk-muted); line-height: 1.6;">
                        Çeşme Limonu, Ice, Kaşmir veya Kiraz Çiçeği esanslarımız 80° hijyenik koşullarda el değmeden otomatik dolum hatlarında şişelenir.
                    </p>
                </div>
                <div style="background: var(--pk-gray-bg); border: 1px solid var(--pk-border); border-radius: 12px; padding: 24px;">
                    <div style="font-size: 32px; margin-bottom: 12px;">4️⃣</div>
                    <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 800; color: var(--pk-navy); margin-bottom: 8px;">Güvenli Paketleme & Sevkiyat</h3>
                    <p style="font-size: 12px; color: var(--pk-muted); line-height: 1.6;">
                        Sızdırmazlık testlerinden geçen ürünler kurumsal kolilerde güvenle ambalajlanarak deponuza veya doğrudan fuar/etkinlik adresinize teslim edilir.
                    </p>
                </div>
            </div>

            <div style="background: var(--pk-lime-soft); border: 1px solid var(--pk-lime); border-radius: 12px; padding: 20px 24px; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h4 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 800; color: var(--pk-navy);">Kurumsal Numune Talep Edin</h4>
                    <p style="font-size: 12px; color: #475569; margin-top: 2px;">Şişe kalitesini ve kokularımızı sipariş öncesi yerinde inceleyin.</p>
                </div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 800; color: var(--pk-navy);">
                    📞 0 212 445 45 66
                </div>
            </div>
        </div>
        <div class="page-footer">
            <span class="pf-brand">PROMKOL 2027</span>
            <span class="pf-slogan">Miss gibi promosyon</span>
            <span class="pf-num">{current_page_num:02d}</span>
        </div>
    </section>
"""
pages_html.append(process_html)
current_page_num += 1

# --- PAGE 17: FULL CODE & SPEC INDEX TABLE ---
rows_html = "".join([
    f"<tr>"
    f"<td style='font-weight: 800; color: var(--pk-navy);'>{p['code']}</td>"
    f"<td>{p['name']}</td>"
    f"<td><span style='background: var(--pk-gray-bg); padding: 2px 6px; border-radius: 4px; font-weight: 600;'>{p['category']}</span></td>"
    f"<td>{p['volume']}</td>"
    f"<td>{'Sprey' if '(S)' in p['cap_type'] else ('Flip-Top' if '(F)' in p['cap_type'] else 'Dökme')}</td>"
    f"<td style='color: var(--pk-muted);'>{p['material']}</td>"
    f"</tr>"
    for p in products
])

index_html = f"""
    <section class="a4-page" id="page-{current_page_num}">
        <div class="page-header">
            <div class="ph-left">
                <img src="assets/promkol_logo_hires_light.png" alt="PROMKOL" class="ph-logo">
                <span class="ph-badge">Hızlı Referans Cetveli</span>
            </div>
            <div class="ph-right">KOD İNDEKSİ</div>
        </div>
        <div class="editorial-page" style="padding-top: 24px; padding-bottom: 24px;">
            <div>
                <div class="section-eyebrow">Tüm Modeller Bir Arada</div>
                <h2 class="section-heading" style="font-size: 22px;">32 Ürünlük Tam Karşılaştırma Listesi</h2>
            </div>
            
            <div style="overflow: hidden; border: 1px solid var(--pk-border); border-radius: 8px;">
                <table style="width: 100%; border-collapse: collapse; font-size: 9.5px; text-align: left;">
                    <thead>
                        <tr style="background: var(--pk-navy); color: #FFFFFF;">
                            <th style="padding: 6px 8px;">ÜRÜN KODU</th>
                            <th style="padding: 6px 8px;">MODEL ADI</th>
                            <th style="padding: 6px 8px;">SERİ</th>
                            <th style="padding: 6px 8px;">HACİM</th>
                            <th style="padding: 6px 8px;">KAPAK</th>
                            <th style="padding: 6px 8px;">MATERYAL</th>
                        </tr>
                    </thead>
                    <tbody style="line-height: 1.35;">
                        {rows_html}
                    </tbody>
                </table>
            </div>

            <div style="font-size: 10.5px; color: var(--pk-muted); text-align: center;">
                * Ürün kodlarının sonundaki <strong>F</strong> harfi Flip-Top kapaklı modelleri, <strong>S</strong> harfi Sprey başlıklı modelleri, <strong>D</strong> harfi ise Dökme/Dikme tıpaları ifade eder.
            </div>
        </div>
        <div class="page-footer">
            <span class="pf-brand">PROMKOL 2027</span>
            <span class="pf-slogan">Miss gibi promosyon</span>
            <span class="pf-num">{current_page_num:02d}</span>
        </div>
    </section>
"""
pages_html.append(index_html)
current_page_num += 1

# --- PAGE 18: BACK COVER ---
back_html = f"""
    <section class="a4-page back-cover" id="page-{current_page_num}">
        <div class="cover-decor"></div>
        <div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 2px; color: var(--pk-lime); text-transform: uppercase; margin-bottom: 12px;">
                PROMOSYON KOLONYASINDA GÜVEN VE KALİTE
            </div>
            <img src="assets/promkol_logo_hires_dark.png" alt="PROMKOL" class="bc-logo">
            <div class="bc-slogan">"Miss gibi promosyon"</div>
        </div>

        <div class="contact-card-grid">
            <div class="contact-box">
                <h4>WEB SİTESİ</h4>
                <p>www.promkol.com</p>
            </div>
            <div class="contact-box">
                <h4>E-POSTA</h4>
                <p>info@promkol.com</p>
            </div>
            <div class="contact-box">
                <h4>SANTRAL TELEFON</h4>
                <p>0 212 445 45 66</p>
            </div>
            <div class="contact-box">
                <h4>GSM / WHATSAPP</h4>
                <p>0 532 464 18 21</p>
            </div>
        </div>

        <div style="max-width: 540px; border-top: 1px solid rgba(255, 255, 255, 0.15); padding-top: 24px;">
            <p style="font-size: 12px; color: #94A3B8; line-height: 1.6;">
                PROMKOL, kurumsal promosyon kolonyası üretiminde Türkiye'nin öncü uzman markasıdır.
                Tüm şişe modellerimiz gıdaya ve kozmetiğe uygun sertifikalı hammaddelerden üretilmektedir.
            </p>
            <p style="font-size: 11px; color: var(--pk-lime); margin-top: 10px; font-weight: 700;">
                © 2027 PROMKOL • Tüm Hakları Saklıdır.
            </p>
        </div>
    </section>
"""
pages_html.append(back_html)

# HTML Script for interactivity and live code editor
html_script = """
    </main>

    <script>
        // Load initial products data
        let catalogProducts = """ + json.dumps(products, ensure_ascii=False) + """;

        function setViewMode(mode) {
            const canvas = document.getElementById('catalogCanvas');
            const btnAll = document.getElementById('btnAllPages');
            const btnSlider = document.getElementById('btnSlider');
            
            if (mode === 'grid') {
                btnAll.classList.add('active');
                btnSlider.classList.remove('active');
                document.querySelectorAll('.a4-page').forEach(p => p.style.display = 'flex');
            } else {
                btnAll.classList.remove('active');
                btnSlider.classList.add('active');
                // Slider presentation: show 1 page at a time with buttons
                currentIdx = 0;
                showSliderPage(currentIdx);
            }
        }

        let currentIdx = 0;
        function showSliderPage(idx) {
            const pages = document.querySelectorAll('.a4-page');
            pages.forEach((p, i) => {
                p.style.display = (i === idx) ? 'flex' : 'none';
            });
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Keyboard arrow navigation
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('btnSlider').classList.contains('active')) {
                const pages = document.querySelectorAll('.a4-page');
                if (e.key === 'ArrowRight' || e.key === 'PageDown') {
                    if (currentIdx < pages.length - 1) {
                        currentIdx++;
                        showSliderPage(currentIdx);
                    }
                } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
                    if (currentIdx > 0) {
                        currentIdx--;
                        showSliderPage(currentIdx);
                    }
                }
            }
        });

        // Toggle Live Code Editor
        function toggleEditor() {
            const drawer = document.getElementById('editorDrawer');
            drawer.classList.toggle('open');
            if (drawer.classList.contains('open')) {
                renderEditorList();
            }
        }

        function renderEditorList(filterText = '') {
            const container = document.getElementById('editorList');
            container.innerHTML = '';
            
            catalogProducts.forEach((p, idx) => {
                if (filterText && !p.code.toLowerCase().includes(filterText.toLowerCase()) && !p.name.toLowerCase().includes(filterText.toLowerCase())) {
                    return;
                }
                
                const item = document.createElement('div');
                item.className = 'editor-item';
                item.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 800; color: var(--pk-navy); font-size: 13px;">${p.name}</span>
                        <span style="font-size: 11px; background: var(--pk-lime-soft); color: var(--pk-lime-dark); padding: 2px 8px; border-radius: 4px; font-weight: 700;">${p.volume}</span>
                    </div>
                    <div>
                        <label>Ürün Kodu:</label>
                        <input type="text" id="edit-code-${idx}" value="${p.code}" style="font-weight: 700; color: var(--pk-navy);">
                    </div>
                    <div>
                        <label>Ürün Adı:</label>
                        <input type="text" id="edit-name-${idx}" value="${p.name}">
                    </div>
                    <div>
                        <label>Açıklama:</label>
                        <textarea id="edit-desc-${idx}" rows="2">${p.description}</textarea>
                    </div>
                `;
                container.appendChild(item);
            });
        }

        function filterEditor(val) {
            renderEditorList(val);
        }

        // Apply edits live on screen
        function applyEdits() {
            catalogProducts.forEach((p, idx) => {
                const codeInput = document.getElementById(`edit-code-${idx}`);
                const nameInput = document.getElementById(`edit-name-${idx}`);
                const descInput = document.getElementById(`edit-desc-${idx}`);
                
                if (codeInput && nameInput && descInput) {
                    const oldCode = p.code;
                    p.code = codeInput.value.trim();
                    p.name = nameInput.value.trim();
                    p.description = descInput.value.trim();
                    
                    // Update DOM elements on page
                    const badge = document.getElementById(`badge-code-${oldCode}`);
                    if (badge) {
                        badge.textContent = p.code;
                        badge.id = `badge-code-${p.code}`;
                    }
                    const title = document.getElementById(`title-${oldCode}`);
                    if (title) {
                        title.textContent = p.name;
                        title.id = `title-${p.code}`;
                    }
                    const desc = document.getElementById(`desc-${oldCode}`);
                    if (desc) {
                        desc.textContent = p.description;
                        desc.id = `desc-${p.code}`;
                    }
                }
            });
            alert('Ürün kodları ve bilgileri katalog üzerinde canlı olarak güncellendi!');
        }

        // Export updated JSON
        function downloadUpdatedJSON() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(catalogProducts, null, 2));
            const dlAnchorElem = document.createElement('a');
            dlAnchorElem.setAttribute("href", dataStr);
            dlAnchorElem.setAttribute("download", "products_catalog.json");
            dlAnchorElem.click();
        }
    </script>
</body>
</html>
"""

full_html = html_head + "".join(pages_html) + html_script

out_html_path = os.path.join(base_dir, "katalog.html")
with open(out_html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Catalog HTML successfully built! Total pages: {len(pages_html)}")
print(f"Saved to: {out_html_path}")
