import os
import json
import subprocess
import shutil

base_dir = r"C:\Users\Taha\Pictures\kolonya"

from setup_technical_data import products_data, render_product_card

# Verify 32 products
print(f"Total products to render: {len(products_data)}")

# Group products into pairs of 2 for 16 pages
def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

product_pairs = list(chunk(products_data, 2))
print(f"Total product pages: {len(product_pairs)}") # 16 pages

# Master comparison table rows for Page 19
table_rows_html = ""
for i, p in enumerate(products_data, 1):
    table_rows_html += f"""
    <tr>
        <td class="tc-num">{i:02d}</td>
        <td class="tc-code"><strong>{p['code']}</strong></td>
        <td class="tc-name">{p['name']}</td>
        <td class="tc-cat">{p['category']}</td>
        <td class="tc-vol">{p['volume']}</td>
        <td class="tc-cap">{p['cap_name']}</td>
        <td class="tc-neck"><strong>{p['neck_size']}</strong></td>
        <td class="tc-dims">{p['dims']}</td>
        <td class="tc-label"><span class="table-lbl-pill">{p['label_area']}</span></td>
        <td class="tc-box">{p['box_qty']}</td>
        <td class="tc-weight">{p['box_weight']}</td>
        <td class="tc-refill"><span class="badge-yes">✓ Evet</span></td>
    </tr>
    """

# Build all product pages HTML (Pages 3 to 18)
product_pages_html = ""
for page_idx, pair in enumerate(product_pairs, start=3):
    # Determine category for header
    cat_title = pair[0]["category"].upper()
    if len(pair) > 1 and pair[0]["category"] != pair[1]["category"]:
        cat_title = f"{pair[0]['category'].upper()} &bull; {pair[1]['category'].upper()}"
        
    card_1_html = render_product_card(pair[0])
    card_2_html = render_product_card(pair[1]) if len(pair) > 1 else ""
    
    product_pages_html += f"""
    <!-- SAYFA {page_idx:02d}: {pair[0]['code']} & {pair[1]['code'] if len(pair) > 1 else ''} -->
    <div class="page product-page" id="page-{page_idx:02d}">
        <div class="page-top-bar">
            <div class="bar-left">
                <span class="bar-brand">PROMKOL</span>
                <span class="bar-sep">|</span>
                <span class="bar-cat">{cat_title}</span>
                <span class="bar-desc">TEKNİK ŞARTNAME & KAPAK ÇEŞİTLERİ</span>
            </div>
            <div class="bar-right">
                <span class="bar-std">80° KOZMETİK BİLDİRİMLİ</span>
                <span class="bar-page-num">SAYFA {page_idx:02d} / 20</span>
            </div>
        </div>
        <div class="bar-accent-line"></div>

        <div class="cards-grid">
            {card_1_html}
            {card_2_html}
        </div>

        <div class="page-bottom-bar">
            <div class="foot-left">
                <strong>PROMKOL KOLONYA VE AMBALAJ SAN. TİC.</strong> &bull; Miss gibi promosyon
            </div>
            <div class="foot-center">
                <span>www.promkol.com</span> &bull; <span>info@promkol.com</span> &bull; <span>0 212 445 45 66</span>
            </div>
            <div class="foot-right">
                <span>Teknik Şartname &bull; 2027 Kataloğu</span>
            </div>
        </div>
    </div>
    """

# Complete HTML Document
html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Promkol 2027 Teknik Şartname & Kapak Çeşitleri Kataloğu (32 Ürün)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --pk-navy: #1E2B45;
            --pk-navy-dark: #101826;
            --pk-navy-light: #2A3C5E;
            --pk-lime: #91CE17;
            --pk-lime-dark: #74A612;
            --pk-lime-light: #A6E823;
            --pk-gold: #D4AF37;
            --pk-gold-dark: #B8860B;
            --pk-slate-bg: #F8FAFC;
            --pk-card-bg: #FFFFFF;
            --pk-border: #E2E8F0;
            --pk-border-dark: #CBD5E1;
            --pk-text-main: #0F172A;
            --pk-text-muted: #64748B;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}

        @page {{
            size: 297mm 210mm; /* A4 Landscape */
            margin: 0;
        }}

        body {{
            background: #0B111E;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--pk-text-main);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 24px;
            padding: 24px 0;
        }}

        @media print {{
            body {{
                background: none;
                padding: 0;
                gap: 0;
            }}
            .page {{
                margin: 0;
                box-shadow: none !important;
                border-radius: 0 !important;
                page-break-after: always;
                page-break-inside: avoid;
            }}
        }}

        /* Standard Page Container (A4 Landscape: 297 x 210 mm) */
        .page {{
            width: 297mm;
            height: 210mm;
            background: #FFFFFF;
            position: relative;
            overflow: hidden;
            box-shadow: 0 16px 40px rgba(0,0,0,0.4);
            border-radius: 4px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        /* ----------------------------------------------------
           PAGE 1: ULTRA-PREMIUM FRONT COVER
        ---------------------------------------------------- */
        .cover-page {{
            background: var(--pk-navy-dark);
            color: #FFFFFF;
            padding: 0;
        }}

        .cover-bg-wrap {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }}

        .cover-bg-wrap img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: brightness(0.65) contrast(1.1);
        }}

        .cover-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(16,24,38,0.95) 0%, rgba(30,43,69,0.78) 50%, rgba(16,24,38,0.92) 100%);
            z-index: 2;
        }}

        .cover-content {{
            position: relative;
            z-index: 3;
            height: 100%;
            padding: 16mm 20mm;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .cover-top-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .cover-brand-pill {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.15);
            padding: 8px 18px;
            border-radius: 40px;
        }}

        .brand-logo-text {{
            font-family: 'Outfit', sans-serif;
            font-size: 26px;
            font-weight: 900;
            letter-spacing: 2px;
            color: #FFFFFF;
        }}

        .brand-logo-accent {{
            color: var(--pk-lime);
        }}

        .brand-slogan {{
            font-size: 11px;
            color: #94A3B8;
            letter-spacing: 1px;
            border-left: 1px solid rgba(255,255,255,0.2);
            padding-left: 12px;
        }}

        .cover-year-badge {{
            font-family: 'Outfit', sans-serif;
            font-size: 14px;
            font-weight: 800;
            color: var(--pk-navy-dark);
            background: var(--pk-lime);
            padding: 6px 16px;
            border-radius: 20px;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(145,206,23,0.4);
        }}

        .cover-center-box {{
            max-width: 220mm;
        }}

        .cover-eyebrow {{
            display: inline-block;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 3px;
            color: var(--pk-lime);
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .cover-main-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 42px;
            font-weight: 900;
            line-height: 1.1;
            color: #FFFFFF;
            letter-spacing: -0.5px;
            margin-bottom: 14px;
        }}

        .cover-sub-title {{
            font-size: 14px;
            line-height: 1.5;
            color: #CBD5E1;
            font-weight: 400;
            max-width: 190mm;
            margin-bottom: 20px;
        }}

        .cover-features-pills {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .c-pill {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 30px;
            padding: 6px 14px;
            font-size: 10.5px;
            color: #E2E8F0;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .c-pill span.dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--pk-lime);
        }}

        .cover-bottom-bar {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-top: 1px solid rgba(255,255,255,0.12);
            padding-top: 12px;
        }}

        .cover-stats {{
            display: flex;
            gap: 30px;
        }}

        .c-stat-box {{
            display: flex;
            flex-direction: column;
        }}

        .c-stat-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 24px;
            font-weight: 800;
            color: var(--pk-lime);
        }}

        .c-stat-lbl {{
            font-size: 9.5px;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .cover-contact {{
            text-align: right;
            font-size: 10px;
            color: #CBD5E1;
            line-height: 1.6;
        }}

        /* ----------------------------------------------------
           PAGE 2: MASTER CAP GUIDE (KAPAK SİSTEMLERİ REHBERİ)
        ---------------------------------------------------- */
        .guide-page {{
            padding: 8mm 12mm;
            background: #F8FAFC;
        }}

        .guide-header {{
            margin-bottom: 6mm;
        }}

        .guide-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: var(--pk-navy);
            letter-spacing: -0.3px;
        }}

        .guide-sub {{
            font-size: 11px;
            color: var(--pk-text-muted);
            margin-top: 2px;
        }}

        .guide-grid-4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8mm;
            height: 155mm;
        }}

        .guide-cap-card {{
            background: #FFFFFF;
            border: 1.5px solid var(--pk-border);
            border-radius: 8px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        }}

        .gcc-badge {{
            display: inline-block;
            font-size: 8.5px;
            font-weight: 800;
            letter-spacing: 1px;
            padding: 3px 8px;
            border-radius: 12px;
            background: var(--pk-navy);
            color: #FFF;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}

        .gcc-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 800;
            color: var(--pk-navy);
            line-height: 1.2;
            margin-bottom: 6px;
        }}

        .gcc-img-box {{
            height: 48mm;
            background: radial-gradient(circle at 50% 50%, #F8FAFC 0%, #EDF2F7 100%);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--pk-border);
            margin-bottom: 8px;
        }}

        .gcc-img-box img {{
            max-height: 44mm;
            max-width: 90%;
            object-fit: contain;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
        }}

        .gcc-specs-list {{
            list-style: none;
            font-size: 8.5px;
            color: #334155;
            line-height: 1.5;
            margin-bottom: 8px;
        }}

        .gcc-specs-list li {{
            padding: 2.5px 0;
            border-bottom: 1px solid #F1F5F9;
        }}

        .gcc-specs-list strong {{
            color: var(--pk-navy);
        }}

        .gcc-colors-title {{
            font-size: 8.5px;
            font-weight: 700;
            color: var(--pk-navy);
            margin-bottom: 4px;
        }}

        .gcc-colors-dots {{
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }}

        .gcc-dot {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
        }}

        /* ----------------------------------------------------
           PAGES 3-18: 32 PRODUCT CARDS (2 PRODUCTS PER PAGE)
        ---------------------------------------------------- */
        .product-page {{
            padding: 6mm 10mm;
            background: #F8FAFC;
        }}

        .page-top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 9px;
            color: var(--pk-text-muted);
            padding-bottom: 3px;
        }}

        .bar-brand {{
            font-family: 'Outfit', sans-serif;
            font-weight: 900;
            font-size: 12px;
            color: var(--pk-navy);
            letter-spacing: 1px;
        }}

        .bar-sep {{
            margin: 0 6px;
            color: #CBD5E1;
        }}

        .bar-cat {{
            font-weight: 700;
            color: var(--pk-lime-dark);
            letter-spacing: 0.5px;
        }}

        .bar-desc {{
            margin-left: 6px;
            color: #64748B;
        }}

        .bar-std {{
            font-weight: 700;
            color: var(--pk-navy);
            background: #E2E8F0;
            padding: 2px 8px;
            border-radius: 10px;
            margin-right: 10px;
            font-size: 8px;
        }}

        .bar-page-num {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            color: var(--pk-navy);
            font-size: 10px;
        }}

        .bar-accent-line {{
            height: 2px;
            background: linear-gradient(90deg, var(--pk-lime) 0%, var(--pk-navy) 40%, rgba(30,43,69,0.2) 100%);
            margin-bottom: 4mm;
        }}

        .cards-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8mm;
            height: 180mm;
        }}

        /* INDIVIDUAL TECHNICAL PRODUCT CARD */
        .tech-card {{
            background: #FFFFFF;
            border: 1.5px solid var(--pk-border);
            border-radius: 8px;
            padding: 8px 10px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 14px rgba(0,0,0,0.03);
            position: relative;
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding-bottom: 6px;
            border-bottom: 1.5px solid #F1F5F9;
            margin-bottom: 6px;
        }}

        .code-and-title {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}

        .tech-code-badge {{
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 900;
            color: #FFFFFF;
            background: var(--pk-navy);
            padding: 4px 10px;
            border-radius: 6px;
            letter-spacing: 0.8px;
            border-left: 3px solid var(--pk-lime);
        }}

        .header-titles {{
            display: flex;
            flex-direction: column;
        }}

        .prod-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 11px;
            font-weight: 800;
            color: var(--pk-navy);
            line-height: 1.2;
            letter-spacing: -0.2px;
        }}

        .prod-meta {{
            display: flex;
            gap: 6px;
            align-items: center;
            font-size: 8px;
            color: #64748B;
            margin-top: 2px;
        }}

        .meta-cat {{
            color: #FFF;
            padding: 1px 6px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 7.5px;
        }}

        .meta-vol {{
            font-weight: 700;
            color: var(--pk-navy);
        }}

        .header-badges {{
            display: flex;
            gap: 4px;
        }}

        .feat-pill {{
            font-size: 7.5px;
            font-weight: 700;
            color: #166534;
            background: #DCFCE7;
            padding: 2px 6px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            gap: 2px;
        }}

        /* CARD BODY (SPLIT INTO VISUAL & SPECS COLUMNS) */
        .card-body {{
            display: grid;
            grid-template-columns: 54mm 1fr;
            gap: 10px;
            flex: 1;
            align-content: space-between;
        }}

        /* VISUAL COLUMN */
        .visual-col {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .studio-podium {{
            height: 72mm;
            background: radial-gradient(circle at 50% 35%, #FFFFFF 0%, #F1F5F9 100%);
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }}

        .podium-badge {{
            position: absolute;
            top: 5px;
            left: 5px;
            font-size: 6.5px;
            font-weight: 800;
            background: var(--pk-navy);
            color: #FFFFFF;
            padding: 2px 6px;
            border-radius: 4px;
            letter-spacing: 0.5px;
        }}

        .studio-img {{
            max-height: 64mm;
            max-width: 90%;
            object-fit: contain;
            filter: drop-shadow(0 6px 12px rgba(0,0,0,0.14));
            z-index: 2;
        }}

        .podium-shadow {{
            position: absolute;
            bottom: 4px;
            width: 70%;
            height: 6px;
            background: radial-gradient(ellipse at center, rgba(0,0,0,0.18) 0%, rgba(0,0,0,0) 70%);
            z-index: 1;
        }}

        /* CAP MACRO BOX */
        .cap-macro-box {{
            display: flex;
            gap: 7px;
            align-items: center;
            background: #F8FAFC;
            border: 1px solid var(--pk-border);
            border-radius: 6px;
            padding: 5px;
        }}

        .cap-macro-thumb {{
            width: 36px;
            height: 36px;
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 4px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .cap-macro-thumb img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}

        .zoom-indicator {{
            position: absolute;
            bottom: 0px;
            right: 0px;
            background: var(--pk-lime-dark);
            color: #FFF;
            font-size: 5.5px;
            font-weight: 800;
            padding: 1px 3px;
            border-radius: 2px 0 0 0;
        }}

        .cap-macro-info {{
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}

        .cap-code-tag {{
            font-size: 8.5px;
            font-weight: 800;
            color: var(--pk-navy);
            line-height: 1.15;
        }}

        .cap-mech-text {{
            font-size: 7.8px;
            font-weight: 700;
            color: var(--pk-lime-dark);
            line-height: 1.2;
        }}

        .cap-spec-sub {{
            font-size: 7.2px;
            color: #64748B;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* CAP COLORS BLOCK */
        .cap-colors-block {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 5px;
            padding: 5px 6px;
        }}

        .colors-headline {{
            display: block;
            font-size: 7.2px;
            font-weight: 800;
            color: var(--pk-navy);
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 3px;
        }}

        .swatches-wrap {{
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
        }}

        .swatch-item {{
            display: inline-flex;
            align-items: center;
            gap: 3px;
            background: #F1F5F9;
            padding: 1.5px 5px;
            border-radius: 4px;
        }}

        .swatch-circle {{
            width: 9px;
            height: 9px;
            border-radius: 50%;
            display: inline-block;
        }}

        .swatch-name {{
            font-size: 6.8px;
            font-weight: 600;
            color: #334155;
        }}

        /* SIBLING CAP BOX */
        .sibling-cap-box {{
            display: flex;
            gap: 7px;
            align-items: center;
            background: #EFF6FF;
            border: 1px dashed #60A5FA;
            border-radius: 5px;
            padding: 4px 6px;
        }}

        .sibling-thumb {{
            width: 26px;
            height: 26px;
            background: #FFF;
            border: 1px solid #93C5FD;
            border-radius: 3px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .sibling-thumb img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}

        .sibling-text {{
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}

        .sib-badge {{
            font-size: 6.2px;
            font-weight: 800;
            color: #1E40AF;
            letter-spacing: 0.4px;
        }}

        .sib-title {{
            font-size: 7.5px;
            font-weight: 700;
            color: #1E3A8A;
            line-height: 1.15;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* SPECS COLUMN */
        .specs-col {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .specs-table-title {{
            font-size: 8px;
            font-weight: 800;
            color: var(--pk-navy);
            letter-spacing: 0.6px;
            text-transform: uppercase;
            padding-bottom: 2.5px;
            border-bottom: 1.5px solid var(--pk-lime);
            margin-bottom: 4px;
        }}

        .tech-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 8.2px;
        }}

        .tech-table tr {{
            border-bottom: 1px solid #F1F5F9;
        }}

        .tech-table tr:nth-child(even) {{
            background: #F8FAFC;
        }}

        .t-key {{
            padding: 3.5px 5px;
            font-weight: 700;
            color: #475569;
            width: 36%;
            vertical-align: middle;
        }}

        .t-val {{
            padding: 3.5px 5px;
            color: #0F172A;
            vertical-align: middle;
        }}

        .highlight-neck {{
            font-weight: 800;
            color: var(--pk-navy);
            background: #FEF08A;
            padding: 1px 5px;
            border-radius: 3px;
        }}

        .highlight-label {{
            font-weight: 800;
            color: #1E40AF;
            background: #DBEAFE;
            padding: 1px 5px;
            border-radius: 3px;
        }}

        .tech-note-box {{
            background: #F1F5F9;
            border-left: 3px solid var(--pk-lime-dark);
            padding: 5px 8px;
            border-radius: 0 4px 4px 0;
            margin-top: 5px;
        }}

        .note-label {{
            display: block;
            font-size: 7px;
            font-weight: 800;
            color: var(--pk-navy);
            letter-spacing: 0.4px;
            margin-bottom: 1px;
        }}

        .note-desc {{
            font-size: 7.5px;
            color: #334155;
            line-height: 1.3;
        }}

        .compatibility-bar {{
            display: flex;
            gap: 5px;
            margin-top: 5px;
            flex-wrap: wrap;
        }}

        .compat-tag {{
            font-size: 7px;
            font-weight: 700;
            color: var(--pk-navy);
            background: #E2E8F0;
            padding: 2px 6px;
            border-radius: 4px;
        }}

        /* BOTTOM BAR FOR PRODUCT PAGES */
        .page-bottom-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 8px;
            color: #64748B;
            border-top: 1px solid #E2E8F0;
            padding-top: 3px;
            margin-top: 2mm;
        }}

        .foot-left strong {{
            color: var(--pk-navy);
        }}

        /* ----------------------------------------------------
           PAGE 19: MASTER COMPARISON MATRIX TABLE
        ---------------------------------------------------- */
        .matrix-page {{
            padding: 5mm 7mm;
            background: #FFFFFF;
        }}

        .matrix-title-bar {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 2mm;
            border-bottom: 2px solid var(--pk-navy);
            padding-bottom: 2px;
        }}

        .matrix-h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 900;
            color: var(--pk-navy);
        }}

        .matrix-sub {{
            font-size: 8.5px;
            color: #64748B;
        }}

        .master-table-wrap {{
            overflow: hidden;
            border: 1px solid var(--pk-border);
            border-radius: 5px;
        }}

        .master-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 6.2px;
            text-align: left;
            line-height: 1.15;
        }}

        .master-table th {{
            background: var(--pk-navy);
            color: #FFFFFF;
            padding: 3px 4px;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 6.8px;
            letter-spacing: 0.2px;
            border-right: 1px solid rgba(255,255,255,0.1);
        }}

        .master-table td {{
            padding: 1.5px 4px;
            border-bottom: 1px solid #F1F5F9;
            border-right: 1px solid #F1F5F9;
            color: #1E293B;
            vertical-align: middle;
        }}

        .master-table tr:nth-child(even) {{
            background: #F8FAFC;
        }}

        .master-table tr:hover {{
            background: #F1F5F9;
        }}

        .tc-num {{ font-weight: 700; color: #64748B; width: 12px; text-align: center; }}
        .tc-code {{ font-weight: 800; color: var(--pk-navy); }}
        .tc-neck {{ color: #B45309; }}
        .table-lbl-pill {{
            background: #EFF6FF;
            color: #1E40AF;
            font-weight: 700;
            padding: 0.5px 3px;
            border-radius: 2px;
            display: inline-block;
        }}
        .badge-yes {{
            color: #166534;
            font-weight: 800;
        }}

        /* ----------------------------------------------------
           PAGE 20: CORPORATE BACK COVER
        ---------------------------------------------------- */
        .back-cover-page {{
            background: var(--pk-navy-dark);
            color: #FFFFFF;
            padding: 16mm 20mm;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        }}

        .back-bg-art {{
            position: absolute;
            top: 0;
            right: 0;
            width: 45%;
            height: 100%;
            opacity: 0.15;
            background: radial-gradient(circle at 70% 30%, var(--pk-lime) 0%, transparent 70%);
        }}

        .back-top-brand {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .back-logo-text {{
            font-family: 'Outfit', sans-serif;
            font-size: 36px;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: 2px;
        }}

        .back-center-info {{
            max-width: 180mm;
            z-index: 2;
        }}

        .back-h2 {{
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 12px;
            line-height: 1.2;
        }}

        .back-lead {{
            font-size: 13px;
            color: #CBD5E1;
            line-height: 1.6;
            margin-bottom: 24px;
        }}

        .back-certs-row {{
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
        }}

        .cert-box {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 8px;
            padding: 10px 16px;
        }}

        .cert-name {{
            font-family: 'Outfit', sans-serif;
            font-size: 14px;
            font-weight: 800;
            color: var(--pk-lime);
        }}

        .cert-desc {{
            font-size: 9px;
            color: #94A3B8;
            margin-top: 2px;
        }}

        .back-contact-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            border-top: 1px solid rgba(255,255,255,0.15);
            padding-top: 16px;
            z-index: 2;
        }}

        .contact-col-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 12px;
            font-weight: 800;
            color: var(--pk-lime);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }}

        .contact-col-text {{
            font-size: 11px;
            color: #CBD5E1;
            line-height: 1.6;
        }}

        .back-copyright {{
            display: flex;
            justify-content: space-between;
            font-size: 9px;
            color: #64748B;
            border-top: 1px solid rgba(255,255,255,0.08);
            padding-top: 8px;
            z-index: 2;
        }}
    </style>
</head>
<body>

    <!-- ====================================================
         SAYFA 01: ULTRA-PRESTİJLİ TEKNİK ŞARTNAME KAPAĞI
    ==================================================== -->
    <div class="page cover-page" id="page-01">
        <div class="cover-bg-wrap">
            <img src="assets/promkol_cover_main.jpg" alt="Promkol Corporate Background">
        </div>
        <div class="cover-overlay"></div>
        <div class="cover-content">
            <div class="cover-top-row">
                <div class="cover-brand-pill">
                    <span class="brand-logo-text">PROM<span class="brand-logo-accent">KOL</span></span>
                    <span class="brand-slogan">Miss gibi promosyon &bull; Ambalaj & Dolum Sanayi</span>
                </div>
                <div class="cover-year-badge">2027 TEKNİK ŞARTNAME</div>
            </div>

            <div class="cover-center-box">
                <span class="cover-eyebrow">PROFESYONEL PROMOSYON AMBALAJ ÇÖZÜMLERİ</span>
                <h1 class="cover-main-title">ÜRÜN ÖZELLİKLERİ &<br>KAPAK ÇEŞİTLERİ KATALOĞU</h1>
                <p class="cover-sub-title">
                    32 Model Kolonya Şişesi, Standart Boğaz Çapları (18/410 - 28/410), Flip-Top & Mikro Sis Sprey Mekanizmaları, 
                    Lüks Kristal Cam Tıpalar, Etiket Ölçü Kılavuzu ve Detaylı Teknik Şartname Rehberi.
                </p>

                <div class="cover-features-pills">
                    <div class="c-pill"><span class="dot"></span> 32 Farklı Ürün ve Kapak Varyantı</div>
                    <div class="c-pill"><span class="dot"></span> Flip-Top & Mikro Sprey & Dikme Tıpalar</div>
                    <div class="c-pill"><span class="dot"></span> 10 ml - 400 ml Geniş Hacim Yelpazesi</div>
                    <div class="c-pill"><span class="dot"></span> Kuşe & Şeffaf UV Çift Baskı Uyumu</div>
                    <div class="c-pill"><span class="dot"></span> Sağlık Bakanlığı Kozmetik Bildirimli (80°)</div>
                </div>
            </div>

            <div class="cover-bottom-bar">
                <div class="cover-stats">
                    <div class="c-stat-box">
                        <span class="c-stat-val">32</span>
                        <span class="c-stat-lbl">Şişe & Kapak Modeli</span>
                    </div>
                    <div class="c-stat-box">
                        <span class="c-stat-val">80°</span>
                        <span class="c-stat-lbl">Etil Alkol Derecesi</span>
                    </div>
                    <div class="c-stat-box">
                        <span class="c-stat-val">100%</span>
                        <span class="c-stat-lbl">Yerli Üretim & Dolum</span>
                    </div>
                    <div class="c-stat-box">
                        <span class="c-stat-val">ISO</span>
                        <span class="c-stat-lbl">22716 GMP Sertifikalı</span>
                    </div>
                </div>
                <div class="cover-contact">
                    <strong>PROMKOL KOLONYA VE AMBALAJ SAN. TİC.</strong><br>
                    www.promkol.com &bull; info@promkol.com &bull; 0 212 445 45 66 &bull; 0 532 464 18 21
                </div>
            </div>
        </div>
    </div>

    <!-- ====================================================
         SAYFA 02: KAPAK SİSTEMLERİ VE MEKANİZMA REHBERİ
    ==================================================== -->
    <div class="page guide-page" id="page-02">
        <div class="guide-header">
            <h2 class="guide-title">PROMKOL KAPAK SİSTEMLERİ VE MEKANİZMA REHBERİ</h2>
            <p class="guide-sub">Kolonya ambalajlarımızda kullanılan 4 temel kapak ailesi, teknik kilit sistemleri, dozajlama özellikleri ve renk opsiyonları.</p>
        </div>

        <div class="guide-grid-4">
            <!-- Kapak Tipi 1: Flip-Top -->
            <div class="guide-cap-card">
                <div>
                    <span class="gcc-badge">DÖKME SİSTEMİ</span>
                    <h3 class="gcc-title">Flip-Top Açılır Kapak (F)</h3>
                    <div class="gcc-img-box">
                        <img src="assets/cap_crops/cap_100P1F.png" alt="Flip-Top Kapak">
                    </div>
                    <ul class="gcc-specs-list">
                        <li><strong>Boğaz Çapları:</strong> 18/410, 20/410, 24/410, 28/410</li>
                        <li><strong>Malzeme:</strong> Yüksek Dayanımlı Polipropilen (PP)</li>
                        <li><strong>Kapanış:</strong> Çift emniyetli klik tırnak kilidi</li>
                        <li><strong>Akış Tipi:</strong> Damlatıcı ve sızdırmaz dökme ağzı</li>
                        <li><strong>Özellik:</strong> Tek elle pratik açılıp kapanır</li>
                    </ul>
                </div>
                <div>
                    <div class="gcc-colors-title">Mevcut Gövde / Kapak Renkleri:</div>
                    <div class="gcc-colors-dots">
                        <span class="gcc-dot" style="background: #1E293B;" title="Siyah"></span>
                        <span class="gcc-dot" style="background: #FFFFFF; border: 1px solid #CBD5E1;" title="Beyaz"></span>
                        <span class="gcc-dot" style="background: #CBD5E1;" title="Şeffaf"></span>
                        <span class="gcc-dot" style="background: #DC2626;" title="Kırmızı"></span>
                        <span class="gcc-dot" style="background: #1E3A8A;" title="Lacivert"></span>
                        <span class="gcc-dot" style="background: #16A34A;" title="Yeşil"></span>
                    </div>
                </div>
            </div>

            <!-- Kapak Tipi 2: Mikro Sis Sprey -->
            <div class="guide-cap-card">
                <div>
                    <span class="gcc-badge" style="background: var(--pk-lime-dark);">PÜSKÜRTME SİSTEMİ</span>
                    <h3 class="gcc-title">Mikro Sis Sprey Valfi (S)</h3>
                    <div class="gcc-img-box">
                        <img src="assets/cap_crops/cap_100P1S.png" alt="Sprey Valf">
                    </div>
                    <ul class="gcc-specs-list">
                        <li><strong>Boğaz Çapları:</strong> 18/410, 20/410, 24/410</li>
                        <li><strong>Dozajlama:</strong> 0.12 - 0.14 ml / basım</li>
                        <li><strong>Mekanizma:</strong> Paslanmaz çelik yay, PE boru</li>
                        <li><strong>Koruma:</strong> Şeffaf koruyucu dış başlık kapağı</li>
                        <li><strong>Avantaj:</strong> Temassız hijyenik ve ekonomik kullanım</li>
                    </ul>
                </div>
                <div>
                    <div class="gcc-colors-title">Mevcut Başlık Renkleri:</div>
                    <div class="gcc-colors-dots">
                        <span class="gcc-dot" style="background: #1E293B;" title="Siyah Başlık"></span>
                        <span class="gcc-dot" style="background: #FFFFFF; border: 1px solid #CBD5E1;" title="Beyaz Başlık"></span>
                        <span class="gcc-dot" style="background: #CBD5E1;" title="Şeffaf Başlık"></span>
                    </div>
                </div>
            </div>

            <!-- Kapak Tipi 3: Slim & Kart Entegre Atomizör -->
            <div class="guide-cap-card">
                <div>
                    <span class="gcc-badge" style="background: #334155;">ENTEGRE CEP SİSTEMİ</span>
                    <h3 class="gcc-title">Slim Entegre Kart Sprey (S)</h3>
                    <div class="gcc-img-box">
                        <img src="assets/cap_crops/cap_20K01S.png" alt="Slim Sprey">
                    </div>
                    <ul class="gcc-specs-list">
                        <li><strong>Form Ebadı:</strong> 11 - 15 mm ultra ince kart yapısı</li>
                        <li><strong>Gövde:</strong> Ultrasonik kaynaklı Polietilen</li>
                        <li><strong>Kilit / Koruma:</strong> Gövdeye gömme veya klipsli valf</li>
                        <li><strong>Doldurma:</strong> Sökülebilir sızdırmaz dolum tıpası</li>
                        <li><strong>Taşıma:</strong> Cüzdan, ceket cebi ve çanta uyumlu</li>
                    </ul>
                </div>
                <div>
                    <div class="gcc-colors-title">Mevcut Gövde Renkleri:</div>
                    <div class="gcc-colors-dots">
                        <span class="gcc-dot" style="background: #1E293B;" title="Mat Siyah Soft Touch"></span>
                        <span class="gcc-dot" style="background: #FFFFFF; border: 1px solid #CBD5E1;" title="Opak Beyaz"></span>
                        <span class="gcc-dot" style="background: #94A3B8;" title="Buzlu Yarı Şeffaf"></span>
                    </div>
                </div>
            </div>

            <!-- Kapak Tipi 4: Kristal Cam Lüks Kapaklar -->
            <div class="guide-cap-card">
                <div>
                    <span class="gcc-badge" style="background: #B45309;">VIP LÜKS SERİ</span>
                    <h3 class="gcc-title">Kristal Cam Sprey & Tıpa (S/D)</h3>
                    <div class="gcc-img-box">
                        <img src="assets/cap_crops/cap_200C1D.png" alt="Kristal Lüks Kapak">
                    </div>
                    <ul class="gcc-specs-list">
                        <li><strong>Sprey Valf:</strong> Alüminyum metalize altın / krom valf</li>
                        <li><strong>Dökme Tıpa:</strong> Kristal iç akıtıcı tıpa + masif kapak</li>
                        <li><strong>Boğaz Çapı:</strong> 18/415 mm ve 24/410 mm lüks boğaz</li>
                        <li><strong>Sızdırmazlık:</strong> Özel polietilen conta ile %100 emniyet</li>
                        <li><strong>Kullanım:</strong> Makam, VIP hediye ve lüks ikramlar</li>
                    </ul>
                </div>
                <div>
                    <div class="gcc-colors-title">Mevcut Metalik Renkler:</div>
                    <div class="gcc-colors-dots">
                        <span class="gcc-dot" style="background: #D4AF37;" title="Parlak Gold Altın"></span>
                        <span class="gcc-dot" style="background: #E2E8F0; border: 1px solid #94A3B8;" title="Parlak Krom Gümüş"></span>
                        <span class="gcc-dot" style="background: #1E293B;" title="Lüks Mat Siyah"></span>
                    </div>
                </div>
            </div>
        </div>

        <div class="page-bottom-bar" style="margin-top: 4mm;">
            <div class="foot-left">
                <strong>PROMKOL KOLONYA VE AMBALAJ SAN. TİC.</strong> &bull; Kapak Standartları Rehberi
            </div>
            <div class="foot-center">
                <span>www.promkol.com</span> &bull; <span>info@promkol.com</span> &bull; <span>0 212 445 45 66</span>
            </div>
            <div class="foot-right">
                <span>Sayfa 02 / 20</span>
            </div>
        </div>
    </div>

    <!-- ====================================================
         SAYFALAR 03 - 18: 32 ÜRÜN TEKNİK ŞARTNAME KARTLARI
    ==================================================== -->
    {product_pages_html}

    <!-- ====================================================
         SAYFA 19: 32 MODEL KAPSAMLI TEKNİK KARŞILAŞTIRMA MATRİSİ
    ==================================================== -->
    <div class="page matrix-page" id="page-19">
        <div class="matrix-title-bar">
            <div>
                <h2 class="matrix-h1">32 ÜRÜN KAPSAMLI TEKNİK ŞARTNAME & LOJİSTİK MATRİSİ</h2>
                <span class="matrix-sub">Tüm şişe modellerinin boğaz çapları, dış ebatları, etiketleme baskı alanları ve koli paketleme verileri.</span>
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 11px; font-weight: 800; color: var(--pk-navy);">
                SAYFA 19 / 20
            </div>
        </div>

        <div class="master-table-wrap">
            <table class="master-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>KOD</th>
                        <th>ÜRÜN ADI</th>
                        <th>SERİ</th>
                        <th>HACİM</th>
                        <th>KAPAK MODELİ</th>
                        <th>BOĞAZ ÇAPI</th>
                        <th>DIŞ EBATLAR (mm)</th>
                        <th>ETİKET ALANI (mm)</th>
                        <th>KOLİ İÇİ</th>
                        <th>BRÜT KG</th>
                        <th>REFILL</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
        </div>

        <div class="page-bottom-bar" style="margin-top: 3mm;">
            <div class="foot-left">
                <strong>PROMKOL LOJİSTİK VE TEKNİK TABLO</strong> &bull; Tüm ürünler 80° etil alkollü ve Sağlık Bakanlığı Kozmetik Bildirimlidir.
            </div>
            <div class="foot-center">
                <span>Standart Koli İçi Paketleme ve Palet Dağıtım Kılavuzu</span>
            </div>
            <div class="foot-right">
                <span>Sayfa 19 / 20</span>
            </div>
        </div>
    </div>

    <!-- ====================================================
         SAYFA 20: KURUMSAL ARKA KAPAK & SERTİFİKALAR
    ==================================================== -->
    <div class="page back-cover-page" id="page-20">
        <div class="back-bg-art"></div>

        <div class="back-top-brand">
            <span class="back-logo-text">PROM<span style="color: var(--pk-lime);">KOL</span></span>
            <span style="font-size: 13px; color: #94A3B8; letter-spacing: 1px; border-left: 1px solid rgba(255,255,255,0.2); padding-left: 14px;">
                Miss gibi promosyon &bull; Türkiye'nin Lider Kolonya Ambalaj Üreticisi
            </span>
        </div>

        <div class="back-center-info">
            <h2 class="back-h2">KURUMSAL KALİTE, SIZDIRMAZ EMNİYET VE KALICI ESANSLAR</h2>
            <p class="back-lead">
                Promkol, yüksek standartlı PET, mat polimer ve kristal cam ambalajlarını; sızdırmaz tırnaklı flip-top kapaklar, 
                mikro sis sprey valfleri ve lüks metalize akıtıcı tıpalar ile buluşturur. 
                Modern otomatik dolum tesislerimizde üretilen tüm kolonyalarımız, T.C. Sağlık Bakanlığı Kozmetik Yönetmeliğine 
                tam uyumlu olarak 80° etil alkol ve ferahlatıcı doğal esanslar ile hazırlanmaktadır.
            </p>

            <div class="back-certs-row">
                <div class="cert-box">
                    <div class="cert-name">ISO 22716:2007</div>
                    <div class="cert-desc">Kozmetik İyi Üretim Uygulamaları (GMP)</div>
                </div>
                <div class="cert-box">
                    <div class="cert-name">ISO 9001:2015</div>
                    <div class="cert-desc">Kalite Yönetim Sistemi Standardı</div>
                </div>
                <div class="cert-box">
                    <div class="cert-name">80° ETİL ALKOL</div>
                    <div class="cert-desc">Kalıcı Hijyen & Sağlık Bakanlığı Bildirimli</div>
                </div>
                <div class="cert-box">
                    <div class="cert-name">%100 SIZDIRMAZLIK</div>
                    <div class="cert-desc">Hassas Diş ve Conta Test Güvencesi</div>
                </div>
            </div>
        </div>

        <div class="back-contact-grid">
            <div class="contact-col">
                <div class="contact-col-title">İLETİŞİM BİLGİLERİ</div>
                <div class="contact-col-text">
                    <strong>Santral:</strong> 0 212 445 45 66<br>
                    <strong>GSM / WhatsApp:</strong> 0 532 464 18 21<br>
                    <strong>E-Posta:</strong> info@promkol.com<br>
                    <strong>Web:</strong> www.promkol.com
                </div>
            </div>
            <div class="contact-col">
                <div class="contact-col-title">FABRİKA & DOLUM TESİSİ</div>
                <div class="contact-col-text">
                    Promkol Kolonya ve Ambalaj Sanayi Ticaret<br>
                    İkitelli Organize Sanayi Bölgesi<br>
                    Başakşehir / İstanbul / TÜRKİYE
                </div>
            </div>
            <div class="contact-col">
                <div class="contact-col-title">GRAFİK & BASKI HİZMETİ</div>
                <div class="contact-col-text">
                    Ücretsiz Şişe Simülasyonu & Tasarım Onayı<br>
                    Kuşe Etiket &bull; Şeffaf PP Etiket &bull; UV Dijital Baskı<br>
                    Tam Tur Serigrafi &bull; Altın Varlık Baskı
                </div>
            </div>
        </div>

        <div class="back-copyright">
            <span>&copy; 2027 Promkol Kolonya ve Ambalaj San. Tic. Tüm hakları saklıdır.</span>
            <span>Sayfa 20 / 20 &bull; Teknik Şartname & Kapak Kataloğu</span>
        </div>
    </div>

</body>
</html>
"""

# Save HTML file
html_path = os.path.join(base_dir, "katalog_teknik_ozellikler.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML successfully: {html_path} ({len(html_content)} bytes)")
