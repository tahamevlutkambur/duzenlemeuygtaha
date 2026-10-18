import os
import sys
import json

base_dir = r"C:\Users\Taha\Pictures\kolonya"

from make_ilpen_catalog import families
from setup_urunler_helper import get_visual_for_variant, get_cap_colors_for_variant

# Ensure manifest exists
manifest_path = os.path.join(base_dir, "assets_manifest.json")
if not os.path.exists(manifest_path):
    import update_manifest

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest_data = json.load(f)

# Group products
pet_fams = [f for f in families if f["category"] == "PET Serisi"]
slim_fams = [f for f in families if "Slim" in f["category"]]
cam_fams = [f for f in families if "Cam" in f["category"]]

def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

pet_pairs = list(chunk(pet_fams, 2))
slim_pairs = list(chunk(slim_fams[:4], 2))
slim_single = [slim_fams[4]]
cam_pairs = list(chunk(cam_fams, 2))

# Helper to render product card with full studio editing tools, scaling, spec items, and color dot editors
def render_product_card(fam):
    variants = fam["variants"]
    caps_html = ""
    variant_visuals = []
    
    for v in variants:
        cap_img = v["cap_crop"]
        v_img, is_user = get_visual_for_variant(v["code"], fam["id"])
        variant_visuals.append({
            "code": v["code"],
            "cap_name": v["cap_name"],
            "sub": v["sub"],
            "img": v_img,
            "is_user": is_user
        })
        
        color_list = get_cap_colors_for_variant(v["code"], fam["category"])
        color_dots_html = "".join([
            f'<span class="color-dot" style="background:{c["hex"]};{"border:1px solid #CBD5E1;" if c.get("border") else ""}" title="{c["name"]} (Rengi değiştirmek için tıkla)" onclick="editColorDot(this)" oncontextmenu="deleteColorDot(event, this)"></span>'
            for c in color_list
        ])
        
        caps_html += f"""
        <div class="ilpen-cap-badge" title="{v['cap_name']} ({v['code']})">
            <div class="cap-badge-actions">
                <button class="cap-act-btn clone" onclick="duplicateCapBadge(this.closest('.ilpen-cap-badge'))" title="Kapağı Çoğalt">📋</button>
                <button class="cap-act-btn del" onclick="deleteCapBadge(this.closest('.ilpen-cap-badge'))" title="Kapağı Sil">×</button>
            </div>
            <div class="cap-thumb-box editable-img-box" data-label="Kapak ({v['code']})">
                <img src="{cap_img}" alt="{v['cap_name']}" class="studio-img resizable-img" data-scale="1.0">
                <div class="img-quick-tools">
                    <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))" title="Fotoğraf Seç">🔄</button>
                    <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)" title="Küçült">🔍 -</button>
                    <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)" title="Büyüt">🔍 +</button>
                    <button class="img-tool-btn del" onclick="clearImageSrc(this.closest('.editable-img-box').querySelector('img'))" title="Kaldır">🗑️</button>
                </div>
            </div>
            <div class="cap-info">
                <div class="cap-header-line">
                    <span class="cap-code" contenteditable="true" spellcheck="false">{v['code']}</span>
                    <span class="cap-title" contenteditable="true" spellcheck="false">{v['cap_name']}</span>
                </div>
                <span class="cap-sub" contenteditable="true" spellcheck="false">{v['sub']}</span>
                <div class="cap-colors-row">
                    <span class="colors-label">Renkler:</span>
                    <div class="colors-dots-container">
                        {color_dots_html}
                    </div>
                    <button class="btn-add-color-dot" onclick="addColorDot(this.previousElementSibling)" title="Yeni Renk Ekle">+</button>
                </div>
            </div>
        </div>
        """
    
    # Visual Column with Scale & Resize Handles
    if len(variant_visuals) >= 2 and variant_visuals[0]["img"] != variant_visuals[1]["img"]:
        visual_col_html = f"""
        <div class="ilpen-dual-podium-wrap">
            <div class="dual-podium-col">
                <div class="podium-cap-header">
                    <span class="podium-cap-code" contenteditable="true" spellcheck="false">{variant_visuals[0]['code']}</span>
                    <span class="podium-cap-title" contenteditable="true" spellcheck="false">{variant_visuals[0]['cap_name']}</span>
                </div>
                <div class="ilpen-bottle-podium-mini editable-img-box resizable-container" data-label="{variant_visuals[0]['code']} Görseli">
                    <img class="ilpen-bottle-img studio-img resizable-img" src="{variant_visuals[0]['img']}" alt="{variant_visuals[0]['code']}" data-scale="1.0">
                    <div class="img-quick-tools">
                        <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))" title="Fotoğraf Seç">🔄 Değiştir</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)" title="Küçült">🔍 -</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)" title="Büyüt">🔍 +</button>
                        <button class="img-tool-btn reset-scale" onclick="resetImgScale(this.closest('.editable-img-box').querySelector('img'))" title="Sıfırla">↺ %100</button>
                        <button class="img-tool-btn del" onclick="clearImageSrc(this.closest('.editable-img-box').querySelector('img'))" title="Kaldır">🗑️</button>
                    </div>
                    <div class="resize-corner-handle" onmousedown="initDragResize(event, this.previousElementSibling.previousElementSibling)" title="Boyutu değiştirmek için sürükleyin"></div>
                </div>
                <div class="mini-tag-bar">
                    <span class="mini-tag" style="background: var(--pk-navy);">KUŞE</span>
                    <span class="mini-tag" style="background: var(--pk-lime-dark);">ŞEFFAF UV</span>
                </div>
            </div>
            <div class="dual-podium-col">
                <div class="podium-cap-header">
                    <span class="podium-cap-code" contenteditable="true" spellcheck="false">{variant_visuals[1]['code']}</span>
                    <span class="podium-cap-title" contenteditable="true" spellcheck="false">{variant_visuals[1]['cap_name']}</span>
                </div>
                <div class="ilpen-bottle-podium-mini editable-img-box resizable-container" data-label="{variant_visuals[1]['code']} Görseli">
                    <img class="ilpen-bottle-img studio-img resizable-img" src="{variant_visuals[1]['img']}" alt="{variant_visuals[1]['code']}" data-scale="1.0">
                    <div class="img-quick-tools">
                        <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))" title="Fotoğraf Seç">🔄 Değiştir</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)" title="Küçült">🔍 -</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)" title="Büyüt">🔍 +</button>
                        <button class="img-tool-btn reset-scale" onclick="resetImgScale(this.closest('.editable-img-box').querySelector('img'))" title="Sıfırla">↺ %100</button>
                        <button class="img-tool-btn del" onclick="clearImageSrc(this.closest('.editable-img-box').querySelector('img'))" title="Kaldır">🗑️</button>
                    </div>
                    <div class="resize-corner-handle" onmousedown="initDragResize(event, this.previousElementSibling.previousElementSibling)" title="Boyutu değiştirmek için sürükleyin"></div>
                </div>
                <div class="mini-tag-bar">
                    <span class="mini-tag" style="background: var(--pk-navy);">KUŞE</span>
                    <span class="mini-tag" style="background: var(--pk-lime-dark);">ŞEFFAF UV</span>
                </div>
            </div>
        </div>
        <div class="visual-tag-bar" style="justify-content: center; margin-top: 6px;">
            <span class="tag-brand" style="background: var(--pk-lime-dark); font-size: 8.5px;" contenteditable="true" spellcheck="false">İKİ AYRI KAPAK MODELİ &bull; KUŞE & ŞEFFAF ÇİFT BASKI</span>
        </div>
        """
    else:
        hero_img = variant_visuals[0]["img"]
        visual_col_html = f"""
        <div class="ilpen-bottle-podium editable-img-box resizable-container" data-label="{fam['title']} Ana Görsel">
            <img class="ilpen-bottle-img studio-img resizable-img" src="{hero_img}" alt="{fam['title']}" data-scale="1.0">
            <div class="img-quick-tools">
                <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))" title="Fotoğraf Seç">🔄 Fotoğraf Değiştir</button>
                <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)" title="Küçült">🔍 -</button>
                <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)" title="Büyüt">🔍 +</button>
                <button class="img-tool-btn reset-scale" onclick="resetImgScale(this.closest('.editable-img-box').querySelector('img'))" title="Sıfırla">↺ %100</button>
                <button class="img-tool-btn del" onclick="clearImageSrc(this.closest('.editable-img-box').querySelector('img'))" title="Kaldır">🗑️</button>
            </div>
            <div class="resize-corner-handle" onmousedown="initDragResize(event, this.previousElementSibling.previousElementSibling)" title="Boyutu değiştirmek için sürükleyin"></div>
        </div>
        <div class="visual-tag-bar">
            <span class="tag-brand" style="background: var(--pk-navy);" contenteditable="true" spellcheck="false">KUŞE ETİKET</span>
            <span class="tag-brand" style="background: var(--pk-lime-dark);" contenteditable="true" spellcheck="false">ŞEFFAF / UV BASKI</span>
            <span class="tag-res" contenteditable="true" spellcheck="false">Çift Uygulama Simülasyonu</span>
        </div>
        """
        
    return f"""
    <div class="ilpen-product-row" id="prod-{fam['id']}">
        <!-- Floating Row Actions Toolbar -->
        <div class="row-actions-bar">
            <span class="row-badge-code">{fam['primary_code']}</span>
            <button class="row-action-btn" onclick="moveRowUp(this.closest('.ilpen-product-row'))" title="Yukarı Taşı">▲</button>
            <button class="row-action-btn" onclick="moveRowDown(this.closest('.ilpen-product-row'))" title="Aşağı Taşı">▼</button>
            <button class="row-action-btn" onclick="duplicateRow(this.closest('.ilpen-product-row'))" title="Ürünü Kopyala (Çoğalt)">📋 Çoğalt</button>
            <button class="row-action-btn delete" onclick="deleteRow(this.closest('.ilpen-product-row'))" title="Bu Ürünü Sil">🗑️ Sil</button>
        </div>

        <!-- Sol: Ürün Bilgi & Teknik Özellik Kolonu -->
        <div class="ilpen-info-col">
            <div class="ilpen-code-badge" contenteditable="true" spellcheck="false">{fam['primary_code']}</div>
            <h2 class="ilpen-prod-title" contenteditable="true" spellcheck="false">{fam['title']}</h2>
            <div class="ilpen-prod-sub" contenteditable="true" spellcheck="false">{fam['category']} &bull; {fam['material']}</div>
            <div class="ilpen-accent-line"></div>
            
            <p class="ilpen-desc" contenteditable="true" spellcheck="false">{fam['desc']}</p>
            
            <!-- Teknik Özellikler Kutusu (Buraları da düzenlenebilir) -->
            <div class="ilpen-specs-grid">
                <div class="spec-item editable-spec-item" title="Tıkla ve düzenle">
                    <div class="spec-icon" onclick="cycleSpecIcon(this)" title="İkon Değiştir">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                    </div>
                    <div class="spec-texts">
                        <span class="spec-val" contenteditable="true" spellcheck="false">80° Etil Alkol</span>
                        <span class="spec-lbl" contenteditable="true" spellcheck="false">Kalıcı ferahlatıcı esans</span>
                    </div>
                    <button class="spec-del-btn" onclick="deleteSpecItem(this.closest('.spec-item'))" title="Bu Özelliği Sil">×</button>
                </div>

                <div class="spec-item editable-spec-item" title="Tıkla ve düzenle">
                    <div class="spec-icon" onclick="cycleSpecIcon(this)" title="İkon Değiştir">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
                    </div>
                    <div class="spec-texts">
                        <span class="spec-val" contenteditable="true" spellcheck="false">{fam['volume']}</span>
                        <span class="spec-lbl" contenteditable="true" spellcheck="false">Koli: {fam['box_qty']}</span>
                    </div>
                    <button class="spec-del-btn" onclick="deleteSpecItem(this.closest('.spec-item'))" title="Bu Özelliği Sil">×</button>
                </div>

                <div class="spec-item editable-spec-item" title="Tıkla ve düzenle">
                    <div class="spec-icon" onclick="cycleSpecIcon(this)" title="İkon Değiştir">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
                    </div>
                    <div class="spec-texts">
                        <span class="spec-val" contenteditable="true" spellcheck="false">Baskı Türleri</span>
                        <span class="spec-lbl" contenteditable="true" spellcheck="false">Kuşe Etiket, UV, Yaldız</span>
                    </div>
                    <button class="spec-del-btn" onclick="deleteSpecItem(this.closest('.spec-item'))" title="Bu Özelliği Sil">×</button>
                </div>

                <button class="btn-add-spec" onclick="addNewSpecItem(this.closest('.ilpen-specs-grid'))" title="Yeni Özellik Ekle">+ Özellik Ekle</button>
            </div>
            
            <!-- Kapak & Renk Varyasyon Kutusu (Altındaki yerler de düzenlenebilir) -->
            <div class="ilpen-caps-section">
                <div class="caps-header-wrap">
                    <span class="caps-header-lbl" contenteditable="true" spellcheck="false">KAPAK & RENK SEÇENEKLERİ</span>
                    <button class="btn-add-cap-badge" onclick="addNewCapBadge(this.closest('.ilpen-caps-section').querySelector('.ilpen-caps-flex'))" title="Yeni Kapak Modeli Ekle">+ Kapak Ekle</button>
                </div>
                <div class="ilpen-caps-flex">
                    {caps_html}
                </div>
            </div>
        </div>

        <!-- Sağ: Ana Ürün Görseli (Kuşe Etiket & Şeffaf Baskı Çift Vitrin) -->
        <div class="ilpen-visual-col">
            {visual_col_html}
        </div>
    </div>
    """

# Helper to render page header with editable & resizable logo
def render_page_header(cat_title):
    return f"""
    <div class="page-header">
        <div class="header-left">
            <div class="header-logo-box editable-img-box" data-label="Sayfa Başlık Logosu">
                <img class="header-logo studio-img resizable-img" src="assets/promkol_logo_hires_dark.png" alt="PROMKOL" data-scale="1.0">
                <div class="img-quick-tools">
                    <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))" title="Logo Değiştir">🔄 Logo</button>
                    <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)" title="Küçült">🔍 -</button>
                    <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)" title="Büyüt">🔍 +</button>
                    <button class="img-tool-btn reset-scale" onclick="resetImgScale(this.closest('.editable-img-box').querySelector('img'))" title="Sıfırla">↺</button>
                    <button class="img-tool-btn del" onclick="clearImageSrc(this.closest('.editable-img-box').querySelector('img'))" title="Kaldır">🗑️</button>
                </div>
            </div>
            <span class="header-cat-pill" contenteditable="true" spellcheck="false">{cat_title}</span>
        </div>
        <div class="header-slogan" contenteditable="true" spellcheck="false">Miss gibi promosyon</div>
    </div>
    """

# Build Full Studio HTML
html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>PROMKOL 2027 | Katalog Stüdyosu & Canlı Düzenleyici</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --pk-navy: #1E2B45;
            --pk-navy-dark: #121B2D;
            --pk-navy-deep: #0B1320;
            --pk-lime: #91CE17;
            --pk-lime-dark: #7DB213;
            --pk-lime-soft: #F4FAE8;
            --pk-accent: #E05A47;
            --pk-bg: #FFFFFF;
            --pk-gray-50: #F8FAFC;
            --pk-gray-100: #F1F5F9;
            --pk-gray-200: #E2E8F0;
            --pk-gray-300: #CBD5E1;
            --pk-text: #1E293B;
            --pk-muted: #64748B;
            --studio-sidebar-w: 390px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #070D18;
            color: var(--pk-text);
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden;
        }}

        /* STUDIO TOP COMMAND BAR */
        .catalog-topbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 64px;
            background: rgba(11, 19, 32, 0.96);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 100000;
            color: #FFFFFF;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }}

        .topbar-left {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .topbar-logo-img {{
            height: 38px;
            cursor: pointer;
        }}

        .topbar-title-wrap {{
            display: flex;
            flex-direction: column;
        }}

        .topbar-main-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 15px;
            font-weight: 800;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .badge-live {{
            background: rgba(145, 206, 23, 0.2);
            color: var(--pk-lime);
            border: 1px solid var(--pk-lime);
            padding: 2px 7px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}

        .topbar-sub {{
            font-size: 11px;
            color: #94A3B8;
        }}

        .topbar-center {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.06);
            padding: 4px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .topbar-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 7px 14px;
            border-radius: 7px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            border: none;
            background: transparent;
            color: #CBD5E1;
            transition: all 0.2s ease;
        }}

        .topbar-btn:hover {{
            background: rgba(255, 255, 255, 0.1);
            color: #FFFFFF;
        }}

        .topbar-btn.active {{
            background: var(--pk-lime);
            color: var(--pk-navy-deep);
            box-shadow: 0 2px 10px rgba(145, 206, 23, 0.35);
        }}

        .topbar-right {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .btn-action-studio {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s ease;
        }}

        .btn-sidebar-toggle {{
            background: rgba(145, 206, 23, 0.15);
            color: var(--pk-lime);
            border-color: rgba(145, 206, 23, 0.35);
        }}

        .btn-sidebar-toggle:hover {{
            background: var(--pk-lime);
            color: var(--pk-navy-deep);
        }}

        .btn-undo-redo {{
            background: rgba(255, 255, 255, 0.08);
            color: #FFFFFF;
            padding: 7px 10px;
            border-color: rgba(255, 255, 255, 0.15);
        }}

        .btn-undo-redo:hover {{
            background: rgba(255, 255, 255, 0.18);
        }}

        .btn-save-disk {{
            background: #2563EB;
            color: #FFFFFF;
            box-shadow: 0 2px 10px rgba(37, 99, 235, 0.3);
        }}

        .btn-save-disk:hover {{
            background: #1D4ED8;
            transform: translateY(-1px);
        }}

        .btn-download-html {{
            background: rgba(255, 255, 255, 0.08);
            color: #E2E8F0;
            border-color: rgba(255, 255, 255, 0.2);
        }}

        .btn-download-html:hover {{
            background: rgba(255, 255, 255, 0.18);
            color: #FFFFFF;
        }}

        .btn-reset-catalog {{
            background: rgba(220, 38, 38, 0.15);
            color: #F87171;
            border-color: rgba(220, 38, 38, 0.3);
        }}

        .btn-reset-catalog:hover {{
            background: #DC2626;
            color: #FFFFFF;
        }}

        .btn-print-pdf {{
            background: var(--pk-lime);
            color: var(--pk-navy-dark);
            box-shadow: 0 2px 12px rgba(145, 206, 23, 0.4);
        }}

        .btn-print-pdf:hover {{
            background: #A2E51A;
            transform: translateY(-1px);
        }}

        /* STUDIO LEFT MEDIA SIDEBAR */
        .media-sidebar {{
            position: fixed;
            top: 64px;
            left: 0;
            bottom: 0;
            width: var(--studio-sidebar-w);
            background: rgba(15, 23, 42, 0.98);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.12);
            z-index: 99990;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 10px 0 30px rgba(0,0,0,0.5);
            color: #FFFFFF;
        }}

        .media-sidebar.collapsed {{
            transform: translateX(-100%);
        }}

        .sidebar-header {{
            padding: 16px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .sidebar-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 15px;
            font-weight: 800;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .sidebar-close-btn {{
            background: transparent;
            border: none;
            color: #94A3B8;
            font-size: 20px;
            cursor: pointer;
            padding: 4px;
            border-radius: 6px;
        }}

        .sidebar-close-btn:hover {{
            color: #FFFFFF;
            background: rgba(255, 255, 255, 0.1);
        }}

        /* Target Indicator Box in Sidebar */
        .target-indicator-box {{
            margin: 12px 16px 8px 16px;
            padding: 12px 14px;
            background: rgba(145, 206, 23, 0.12);
            border: 1px dashed var(--pk-lime);
            border-radius: 10px;
            font-size: 12px;
            line-height: 1.4;
        }}

        .target-indicator-title {{
            font-weight: 800;
            color: var(--pk-lime);
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 4px;
        }}

        .target-indicator-desc {{
            color: #E2E8F0;
            font-size: 11px;
        }}

        /* Search & Filter */
        .sidebar-search-wrap {{
            padding: 8px 16px 12px 16px;
        }}

        .sidebar-search-input {{
            width: 100%;
            padding: 10px 14px;
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            color: #FFFFFF;
            font-size: 13px;
            outline: none;
            transition: border-color 0.2s ease;
        }}

        .sidebar-search-input:focus {{
            border-color: var(--pk-lime);
            background: rgba(255, 255, 255, 0.12);
        }}

        /* Category Tabs */
        .sidebar-tabs {{
            display: flex;
            gap: 6px;
            padding: 0 16px 10px 16px;
            overflow-x: auto;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            scrollbar-width: none;
        }}

        .sidebar-tabs::-webkit-scrollbar {{
            display: none;
        }}

        .sidebar-tab-btn {{
            padding: 6px 12px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #94A3B8;
            font-size: 11px;
            font-weight: 700;
            border-radius: 20px;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s ease;
        }}

        .sidebar-tab-btn:hover {{
            background: rgba(255, 255, 255, 0.12);
            color: #FFFFFF;
        }}

        .sidebar-tab-btn.active {{
            background: var(--pk-lime);
            color: var(--pk-navy-deep);
            border-color: var(--pk-lime);
        }}

        /* Media Gallery Grid */
        .sidebar-gallery {{
            flex: 1;
            overflow-y: auto;
            padding: 14px 16px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}

        .gallery-card {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px;
            display: flex;
            flex-direction: column;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }}

        .gallery-card:hover {{
            background: rgba(255, 255, 255, 0.12);
            border-color: var(--pk-lime);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.4);
        }}

        .gallery-thumb-wrap {{
            width: 100%;
            height: 110px;
            background: rgba(255, 255, 255, 0.04);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            margin-bottom: 6px;
        }}

        .gallery-thumb-img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            transition: transform 0.2s ease;
        }}

        .gallery-card:hover .gallery-thumb-img {{
            transform: scale(1.08);
        }}

        .gallery-name {{
            font-size: 10px;
            font-weight: 700;
            color: #CBD5E1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .gallery-btn-use {{
            margin-top: 4px;
            padding: 4px 6px;
            background: rgba(145, 206, 23, 0.2);
            color: var(--pk-lime);
            border: 1px solid rgba(145, 206, 23, 0.4);
            border-radius: 4px;
            font-size: 10px;
            font-weight: 800;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .gallery-card:hover .gallery-btn-use {{
            background: var(--pk-lime);
            color: var(--pk-navy-deep);
        }}

        /* Upload Tab Dropzone */
        .upload-dropzone {{
            grid-column: 1 / -1;
            border: 2px dashed rgba(145, 206, 23, 0.5);
            background: rgba(145, 206, 23, 0.05);
            border-radius: 12px;
            padding: 24px 16px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .upload-dropzone:hover {{
            background: rgba(145, 206, 23, 0.12);
            border-color: var(--pk-lime);
        }}

        /* CATALOG CANVAS & EDITING STYLES */
        .catalog-container {{
            margin-top: 64px;
            padding: 40px 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
            transition: margin-left 0.3s ease;
        }}

        body.sidebar-open .catalog-container {{
            margin-left: calc(var(--studio-sidebar-w) / 2);
        }}

        /* A4 Page Definition */
        .a4-page {{
            width: 210mm;
            height: 297mm;
            min-height: 297mm;
            background: #FFFFFF;
            position: relative;
            box-shadow: 0 24px 50px rgba(0, 0, 0, 0.5);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            page-break-after: always;
            page-break-inside: avoid;
            transition: box-shadow 0.2s ease;
        }}

        /* PAGE ACTIONS TOOLBAR (Appears above each A4 page) */
        .page-actions-bar {{
            position: absolute;
            top: 8px;
            right: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 4px 10px;
            border-radius: 8px;
            z-index: 100;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            opacity: 0.15;
            transition: opacity 0.2s ease;
        }}

        .a4-page:hover .page-actions-bar {{
            opacity: 1;
        }}

        .page-badge-lbl {{
            font-size: 11px;
            font-weight: 800;
            color: var(--pk-lime);
            margin-right: 4px;
        }}

        .page-action-btn {{
            padding: 3px 8px;
            font-size: 11px;
            font-weight: 700;
            border-radius: 5px;
            border: none;
            background: rgba(255, 255, 255, 0.12);
            color: #FFFFFF;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .page-action-btn:hover {{
            background: rgba(255, 255, 255, 0.25);
        }}

        .page-action-btn.del:hover {{
            background: #DC2626;
            color: #FFFFFF;
        }}

        /* PRODUCT ROW CONTROLS */
        .ilpen-product-row {{
            position: relative;
            transition: all 0.25s ease;
        }}

        .ilpen-product-row:hover {{
            outline: 2px dashed rgba(145, 206, 23, 0.35);
            outline-offset: 4px;
            border-radius: 8px;
        }}

        .row-actions-bar {{
            position: absolute;
            top: 4px;
            right: 4px;
            display: flex;
            align-items: center;
            gap: 4px;
            background: rgba(18, 27, 45, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 3px 8px;
            border-radius: 6px;
            z-index: 90;
            opacity: 0;
            transform: translateY(-4px);
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
        }}

        .ilpen-product-row:hover .row-actions-bar {{
            opacity: 1;
            transform: translateY(0);
        }}

        .row-badge-code {{
            font-size: 10px;
            font-weight: 800;
            color: var(--pk-lime);
            margin-right: 4px;
        }}

        .row-action-btn {{
            padding: 3px 7px;
            font-size: 11px;
            font-weight: 700;
            border-radius: 4px;
            border: none;
            background: rgba(255, 255, 255, 0.1);
            color: #FFFFFF;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .row-action-btn:hover {{
            background: rgba(255, 255, 255, 0.22);
        }}

        .row-action-btn.delete {{
            background: rgba(220, 38, 38, 0.25);
            color: #F87171;
            border: 1px solid rgba(220, 38, 38, 0.4);
        }}

        .row-action-btn.delete:hover {{
            background: #DC2626;
            color: #FFFFFF;
        }}

        /* IMAGE EDITING OVERLAYS, SCALING & RESIZE HANDLES */
        .editable-img-box {{
            position: relative;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .editable-img-box:hover {{
            outline: 2px dashed var(--pk-lime);
            outline-offset: 2px;
            border-radius: 6px;
        }}

        .studio-img {{
            transition: transform 0.15s ease;
            transform-origin: center center;
        }}

        /* Selected Active Image Glow */
        .studio-img.editor-active-img {{
            outline: 3px solid #91CE17 !important;
            outline-offset: 3px !important;
            box-shadow: 0 0 25px rgba(145, 206, 23, 0.75) !important;
            border-radius: 6px;
            animation: pulse-glow 1.5s infinite alternate;
        }}

        @keyframes pulse-glow {{
            0% {{ box-shadow: 0 0 15px rgba(145, 206, 23, 0.5); }}
            100% {{ box-shadow: 0 0 30px rgba(145, 206, 23, 0.95); }}
        }}

        .img-quick-tools {{
            position: absolute;
            bottom: 6px;
            left: 50%;
            transform: translateX(-50%) translateY(6px);
            display: flex;
            align-items: center;
            gap: 3px;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 3px 6px;
            border-radius: 6px;
            opacity: 0;
            pointer-events: none;
            transition: all 0.2s ease;
            z-index: 50;
            box-shadow: 0 4px 16px rgba(0,0,0,0.5);
            white-space: nowrap;
        }}

        .editable-img-box:hover .img-quick-tools {{
            opacity: 1;
            pointer-events: auto;
            transform: translateX(-50%) translateY(0);
        }}

        .img-tool-btn {{
            background: rgba(255, 255, 255, 0.12);
            color: #FFFFFF;
            border: none;
            padding: 3px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .img-tool-btn:hover {{
            background: var(--pk-lime);
            color: var(--pk-navy-deep);
        }}

        .img-tool-btn.scale-btn {{
            background: rgba(145, 206, 23, 0.2);
            color: var(--pk-lime);
            font-weight: 800;
        }}

        .img-tool-btn.del:hover {{
            background: #DC2626;
            color: #FFFFFF;
        }}

        /* Resize Corner Drag Handle */
        .resize-corner-handle {{
            position: absolute;
            right: 2px;
            bottom: 2px;
            width: 14px;
            height: 14px;
            background: linear-gradient(135deg, transparent 50%, var(--pk-lime) 50%);
            cursor: nwse-resize;
            opacity: 0;
            transition: opacity 0.2s ease;
            border-bottom-right-radius: 4px;
            z-index: 45;
        }}

        .editable-img-box:hover .resize-corner-handle {{
            opacity: 0.9;
        }}

        /* CONTENTEDITABLE HIGHLIGHTS */
        [contenteditable="true"] {{
            outline: none;
            transition: background 0.2s ease, border-color 0.2s ease;
            border-radius: 3px;
        }}

        [contenteditable="true"]:hover {{
            background: rgba(145, 206, 23, 0.08);
            cursor: text;
        }}

        [contenteditable="true"]:focus {{
            background: rgba(145, 206, 23, 0.15);
            box-shadow: 0 0 0 2px var(--pk-lime);
        }}

        /* SPECS GRID EDITING (Buraları da) */
        .editable-spec-item {{
            position: relative;
            transition: all 0.2s ease;
        }}

        .editable-spec-item:hover {{
            background: rgba(145, 206, 23, 0.1);
            border-radius: 6px;
        }}

        .spec-icon {{
            cursor: pointer;
            transition: transform 0.2s ease;
        }}

        .spec-icon:hover {{
            transform: scale(1.15);
            color: var(--pk-lime);
        }}

        .spec-del-btn {{
            position: absolute;
            top: -5px;
            right: -5px;
            width: 16px;
            height: 16px;
            background: #DC2626;
            color: #FFFFFF;
            border: none;
            border-radius: 50%;
            font-size: 11px;
            line-height: 14px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0;
            transition: all 0.2s ease;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
            z-index: 10;
        }}

        .editable-spec-item:hover .spec-del-btn {{
            opacity: 1;
        }}

        .btn-add-spec {{
            grid-column: 1 / -1;
            padding: 4px 8px;
            background: transparent;
            border: 1px dashed var(--pk-gray-300);
            color: var(--pk-muted);
            font-size: 10px;
            font-weight: 700;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .btn-add-spec:hover {{
            background: rgba(145, 206, 23, 0.15);
            border-color: var(--pk-lime-dark);
            color: var(--pk-navy);
        }}

        /* CAPS & COLORS SECTION (Altındaki yerler de) */
        .caps-header-wrap {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .btn-add-cap-badge {{
            padding: 2px 7px;
            font-size: 9px;
            font-weight: 800;
            color: var(--pk-lime-dark);
            background: var(--pk-lime-soft);
            border: 1px solid rgba(145, 206, 23, 0.4);
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .btn-add-cap-badge:hover {{
            background: var(--pk-lime);
            color: var(--pk-navy-deep);
        }}

        .cap-badge-actions {{
            position: absolute;
            top: 2px;
            right: 2px;
            display: flex;
            gap: 2px;
            opacity: 0;
            transition: opacity 0.2s ease;
            z-index: 15;
        }}

        .ilpen-cap-badge {{
            position: relative;
        }}

        .ilpen-cap-badge:hover .cap-badge-actions {{
            opacity: 1;
        }}

        .cap-act-btn {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: none;
            font-size: 9px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            background: rgba(15, 23, 42, 0.8);
            color: #FFFFFF;
        }}

        .cap-act-btn.del:hover {{
            background: #DC2626;
        }}

        .cap-act-btn.clone:hover {{
            background: var(--pk-navy);
        }}

        .color-dot {{
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .color-dot:hover {{
            transform: scale(1.3);
            box-shadow: 0 0 6px rgba(0,0,0,0.3);
        }}

        .btn-add-color-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #E2E8F0;
            border: 1px dashed #94A3B8;
            color: #475569;
            font-size: 9px;
            font-weight: 900;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            line-height: 1;
            padding: 0;
            margin-left: 2px;
        }}

        .btn-add-color-dot:hover {{
            background: var(--pk-lime);
            color: var(--pk-navy-deep);
            border-color: var(--pk-lime);
        }}

        /* PREVIEW MODE (Hides all editor outlines, toolbars, sidebars) */
        body.preview-mode .catalog-topbar .mode-edit-only {{
            display: none !important;
        }}

        body.preview-mode .media-sidebar {{
            display: none !important;
        }}

        body.preview-mode .row-actions-bar,
        body.preview-mode .page-actions-bar,
        body.preview-mode .img-quick-tools,
        body.preview-mode .resize-corner-handle,
        body.preview-mode .spec-del-btn,
        body.preview-mode .btn-add-spec,
        body.preview-mode .btn-add-cap-badge,
        body.preview-mode .cap-badge-actions,
        body.preview-mode .btn-add-color-dot {{
            display: none !important;
        }}

        body.preview-mode .ilpen-product-row:hover,
        body.preview-mode .editable-img-box:hover,
        body.preview-mode .editable-spec-item:hover {{
            outline: none !important;
            background: transparent !important;
        }}

        body.preview-mode .studio-img.editor-active-img {{
            outline: none !important;
            box-shadow: none !important;
            animation: none !important;
        }}

        body.preview-mode [contenteditable="true"]:hover,
        body.preview-mode [contenteditable="true"]:focus {{
            background: transparent !important;
            box-shadow: none !important;
        }}

        /* TOAST NOTIFICATION */
        .toast-container {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 200000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            pointer-events: none;
        }}

        .toast-msg {{
            background: rgba(15, 23, 42, 0.96);
            backdrop-filter: blur(12px);
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-left: 4px solid var(--pk-lime);
            padding: 12px 18px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            gap: 10px;
            pointer-events: auto;
            animation: toast-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes toast-in {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}

        /* ================= MOBILE RESPONSIVE ENGINE (Akıllı Telefon ve Tablet Uyumu) ================= */
        @media screen and (max-width: 900px) {{
            /* General Reset & Fluid Mobile Canvas */
            body {{
                overflow-x: hidden !important;
                padding-bottom: 75px !important;
                -webkit-tap-highlight-color: transparent;
            }}

            /* Mobile Top Command Bar */
            .catalog-topbar {{
                height: 54px !important;
                padding: 0 10px !important;
            }}

            .topbar-sub {{
                display: none !important;
            }}

            .topbar-main-title {{
                font-size: 13px !important;
                letter-spacing: 0 !important;
            }}

            .badge-live {{
                display: none !important;
            }}

            .topbar-logo-img {{
                height: 28px !important;
            }}

            .topbar-center {{
                padding: 2px !important;
                gap: 2px !important;
            }}

            .topbar-btn {{
                padding: 4px 8px !important;
                font-size: 11px !important;
            }}

            .topbar-right .btn-action-studio {{
                display: none !important;
            }}

            .topbar-right .btn-save-disk,
            .topbar-right .btn-sidebar-toggle {{
                display: inline-flex !important;
                padding: 5px 9px !important;
                font-size: 11px !important;
            }}

            /* Canvas Container on Mobile */
            .catalog-container {{
                margin-top: 54px !important;
                margin-left: 0 !important;
                padding: 10px 8px 30px 8px !important;
                gap: 16px !important;
                width: 100% !important;
                max-width: 100vw !important;
                box-sizing: border-box !important;
            }}

            body.sidebar-open .catalog-container {{
                margin-left: 0 !important;
            }}

            /* A4 Page Transforms into Fluid Mobile Card */
            .a4-page {{
                width: 100% !important;
                max-width: 100% !important;
                height: auto !important;
                min-height: auto !important;
                border-radius: 14px !important;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
                overflow: visible !important;
                margin: 0 0 16px 0 !important;
            }}

            /* Page Actions Bar (Always Visible on Mobile) */
            .page-actions-bar {{
                position: static !important;
                opacity: 1 !important;
                width: 100% !important;
                border-radius: 12px 12px 0 0 !important;
                background: rgba(15, 23, 42, 0.95) !important;
                padding: 8px 10px !important;
                display: flex !important;
                justify-content: space-between !important;
                box-sizing: border-box !important;
            }}

            .page-action-btn {{
                padding: 5px 9px !important;
                font-size: 11px !important;
            }}

            /* Page Header & Footer */
            .page-header {{
                height: auto !important;
                padding: 10px 12px !important;
                flex-wrap: wrap !important;
                gap: 6px !important;
            }}

            .header-slogan {{
                font-size: 14px !important;
            }}

            .page-body {{
                padding: 12px 10px !important;
                height: auto !important;
                gap: 16px !important;
                display: flex !important;
                flex-direction: column !important;
            }}

            .page-footer {{
                height: auto !important;
                padding: 8px 12px !important;
                font-size: 10px !important;
                flex-wrap: wrap !important;
                gap: 4px !important;
            }}

            /* Product Row Layout: Vertical Responsive Stack */
            .ilpen-product-row {{
                display: flex !important;
                flex-direction: column !important;
                height: auto !important;
                gap: 12px !important;
                padding: 10px 0 16px 0 !important;
                border-bottom: 2px dashed var(--pk-gray-300) !important;
            }}

            /* Product Row Actions Bar (Always Visible on Touch) */
            .row-actions-bar {{
                position: static !important;
                opacity: 1 !important;
                transform: none !important;
                width: 100% !important;
                display: flex !important;
                justify-content: space-between !important;
                background: #0F172A !important;
                border-radius: 8px !important;
                padding: 6px 10px !important;
                margin-bottom: 8px !important;
                box-sizing: border-box !important;
            }}

            .row-action-btn {{
                padding: 5px 9px !important;
                font-size: 11px !important;
            }}

            /* Visual Column on Mobile */
            .ilpen-visual-col {{
                width: 100% !important;
                box-sizing: border-box !important;
                padding: 12px 6px !important;
            }}

            .ilpen-bottle-podium {{
                height: 220px !important;
                width: 100% !important;
            }}

            .ilpen-dual-podium-wrap {{
                height: 180px !important;
                gap: 6px !important;
            }}

            .visual-tag-bar {{
                flex-wrap: wrap !important;
                justify-content: center !important;
                gap: 4px !important;
            }}

            /* Image Quick Tools: Always Accessible on Touch */
            .img-quick-tools {{
                position: static !important;
                opacity: 1 !important;
                pointer-events: auto !important;
                transform: none !important;
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
                gap: 4px !important;
                margin-top: 8px !important;
                padding: 6px 8px !important;
                border-radius: 8px !important;
                background: rgba(15, 23, 42, 0.95) !important;
                box-sizing: border-box !important;
                flex-wrap: wrap !important;
            }}

            .img-tool-btn {{
                padding: 6px 9px !important;
                font-size: 11px !important;
            }}

            .resize-corner-handle {{
                display: none !important;
            }}

            /* Typography & Inputs */
            .ilpen-prod-title {{
                font-size: 18px !important;
            }}

            .ilpen-desc {{
                font-size: 12px !important;
                line-height: 1.45 !important;
            }}

            /* Specs Grid: 2 Columns on Mobile */
            .ilpen-specs-grid {{
                grid-template-columns: 1fr 1fr !important;
                gap: 6px !important;
                padding: 8px !important;
            }}

            .spec-del-btn {{
                opacity: 1 !important;
                width: 20px !important;
                height: 20px !important;
                font-size: 13px !important;
            }}

            .btn-add-spec {{
                padding: 6px 10px !important;
                font-size: 11px !important;
            }}

            /* Cap Badges on Mobile */
            .ilpen-caps-flex {{
                display: flex !important;
                flex-direction: column !important;
                gap: 8px !important;
            }}

            .ilpen-cap-badge {{
                width: 100% !important;
                min-width: 0 !important;
                padding: 8px !important;
                box-sizing: border-box !important;
            }}

            .cap-badge-actions {{
                opacity: 1 !important;
            }}

            .cap-act-btn {{
                width: 22px !important;
                height: 22px !important;
                font-size: 11px !important;
            }}

            .color-dot {{
                width: 15px !important;
                height: 15px !important;
            }}

            .btn-add-color-dot {{
                width: 16px !important;
                height: 16px !important;
                font-size: 11px !important;
            }}

            /* Cover Page Mobile Styling */
            .divider-page {{
                height: auto !important;
                min-height: 520px !important;
                padding: 24px 16px !important;
                box-sizing: border-box !important;
            }}

            .divider-header {{
                flex-direction: column !important;
                align-items: flex-start !important;
                gap: 8px !important;
                margin-bottom: 20px !important;
            }}

            .divider-logo {{
                height: 50px !important;
            }}

            .divider-slogan {{
                font-size: 24px !important;
            }}

            .divider-num {{
                font-size: 54px !important;
            }}

            .divider-title {{
                font-size: 24px !important;
                line-height: 1.15 !important;
            }}

            .divider-desc {{
                font-size: 13px !important;
            }}

            .cover-hero-tagline {{
                font-size: 16px !important;
            }}

            .cover-sub-slogan {{
                font-size: 20px !important;
            }}

            .cover-usp-badges {{
                flex-direction: column !important;
                gap: 6px !important;
            }}

            .divider-footer {{
                flex-direction: column !important;
                align-items: flex-start !important;
                gap: 6px !important;
                padding-top: 16px !important;
            }}

            /* TOC Page Mobile Styling */
            .toc-page {{
                padding: 20px 14px !important;
                height: auto !important;
                box-sizing: border-box !important;
            }}

            .toc-brand-bar {{
                margin-bottom: 16px !important;
            }}

            .toc-hero-num {{
                font-size: 34px !important;
            }}

            .toc-hero-title {{
                font-size: 18px !important;
            }}

            .toc-hero-line {{
                margin: 8px 0 16px 0 !important;
            }}

            .toc-grid {{
                grid-template-columns: 1fr !important;
                gap: 12px !important;
                margin-bottom: 16px !important;
            }}

            .toc-about-box {{
                margin-top: 16px !important;
                padding: 14px !important;
            }}

            /* SLIDE-UP BOTTOM SHEET FOR MEDIA GALLERY */
            .media-sidebar {{
                top: auto !important;
                left: 0 !important;
                right: 0 !important;
                bottom: 0 !important;
                width: 100% !important;
                max-width: 100% !important;
                height: 82vh !important;
                max-height: 82vh !important;
                border-radius: 20px 20px 0 0 !important;
                border-right: none !important;
                border-top: 2px solid var(--pk-lime) !important;
                transform: translateY(100%) !important;
                z-index: 100001 !important;
                box-shadow: 0 -10px 40px rgba(0,0,0,0.8) !important;
            }}

            .media-sidebar:not(.collapsed) {{
                transform: translateY(0) !important;
            }}

            .sheet-pull-bar {{
                width: 44px;
                height: 5px;
                background: rgba(255, 255, 255, 0.35);
                border-radius: 3px;
                margin: 8px auto 4px auto;
            }}

            .sidebar-header {{
                padding: 8px 16px !important;
            }}

            .sidebar-search-input {{
                font-size: 16px !important; /* Prevents iOS auto-zoom */
            }}

            /* Backdrop Overlay */
            .sidebar-backdrop {{
                display: none;
                position: fixed;
                inset: 0;
                background: rgba(0, 0, 0, 0.65);
                backdrop-filter: blur(4px);
                z-index: 100000;
            }}

            .sidebar-backdrop.active {{
                display: block;
            }}

            /* STICKY MOBILE BOTTOM BAR */
            .mobile-bottom-bar {{
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                height: 60px;
                background: rgba(11, 19, 32, 0.98);
                backdrop-filter: blur(16px);
                border-top: 1px solid rgba(255, 255, 255, 0.15);
                display: flex !important;
                align-items: center;
                justify-content: space-around;
                z-index: 99990;
                padding: 0 4px;
                padding-bottom: max(0px, env(safe-area-inset-bottom));
                box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.5);
            }}

            .mob-nav-btn {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background: transparent;
                border: none;
                color: #CBD5E1;
                font-size: 10px;
                font-weight: 700;
                gap: 3px;
                padding: 6px 10px;
                cursor: pointer;
                border-radius: 8px;
                touch-action: manipulation;
                transition: all 0.2s ease;
                min-width: 60px;
            }}

            .mob-nav-btn:active {{
                transform: scale(0.92);
                color: #FFFFFF;
                background: rgba(255, 255, 255, 0.1);
            }}

            .mob-nav-btn.primary {{
                background: #2563EB;
                color: #FFFFFF;
                box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4);
            }}

            .mob-nav-icon {{
                font-size: 17px;
                line-height: 1;
            }}
        }}

        @media screen and (min-width: 901px) {{
            .mobile-bottom-bar {{
                display: none !important;
            }}
            .sidebar-backdrop {{
                display: none !important;
            }}
            .sheet-pull-bar {{
                display: none !important;
            }}
        }}

        /* PRINT MEDIA STYLES - ZERO MARGIN, 100% PURE A4 */
        @media print {{
            body {{
                background: transparent !important;
                padding-bottom: 0 !important;
            }}
            .catalog-topbar,
            .media-sidebar,
            .mobile-bottom-bar,
            .sidebar-backdrop,
            .sheet-pull-bar,
            .row-actions-bar,
            .page-actions-bar,
            .img-quick-tools,
            .resize-corner-handle,
            .spec-del-btn,
            .btn-add-spec,
            .btn-add-cap-badge,
            .cap-badge-actions,
            .btn-add-color-dot,
            .toast-container {{
                display: none !important;
            }}
            .catalog-container {{
                margin-top: 0 !important;
                padding: 0 !important;
                gap: 0 !important;
                margin-left: 0 !important;
            }}
            .a4-page {{
                width: 210mm !important;
                height: 297mm !important;
                min-height: 297mm !important;
                margin: 0 !important;
                box-shadow: none !important;
                border-radius: 0 !important;
                page-break-after: always !important;
                break-after: page !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            .ilpen-product-row {{
                display: grid !important;
                grid-template-columns: 1.15fr 0.85fr !important;
                height: calc((297mm - 145px) / 2) !important;
                padding: 12px 0 !important;
                border-bottom: 1px dashed var(--pk-gray-200) !important;
            }}
            .ilpen-specs-grid {{
                grid-template-columns: repeat(3, 1fr) !important;
                display: grid !important;
            }}
            .ilpen-caps-flex {{
                display: flex !important;
                flex-direction: row !important;
            }}
            .ilpen-cap-badge {{
                flex: 1 !important;
                min-width: 130px !important;
            }}
            .page-header {{
                height: 65px !important;
                padding: 0 40px !important;
            }}
            .page-body {{
                padding: 24px 40px !important;
                height: calc(297mm - 105px) !important;
            }}
            .page-footer {{
                height: 40px !important;
                padding: 0 40px !important;
            }}
            .divider-page {{
                height: 297mm !important;
                min-height: 297mm !important;
                padding: 60px !important;
            }}
            .toc-page {{
                height: 297mm !important;
                min-height: 297mm !important;
                padding: 50px !important;
            }}
            .toc-grid {{
                grid-template-columns: 1fr 1fr !important;
            }}
        }}

        @page {{
            size: A4 portrait;
            margin: 0;
        }}

        /* ================= ORIGINAL CATALOG DESIGN CSS ================= */
        .page-header {{
            height: 65px;
            padding: 0 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--pk-gray-200);
            background: #FFFFFF;
            flex-shrink: 0;
        }}

        .header-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .header-logo-box {{
            display: flex;
            align-items: center;
        }}

        .header-logo {{
            height: 30px;
            object-fit: contain;
        }}

        .header-cat-pill {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: var(--pk-navy);
            background: var(--pk-gray-100);
            padding: 4px 10px;
            border-radius: 4px;
        }}

        .header-slogan {{
            font-family: 'Caveat', cursive;
            font-size: 18px;
            color: var(--pk-lime-dark);
            font-weight: 700;
        }}

        .page-body {{
            flex: 1;
            padding: 24px 40px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: #FFFFFF;
        }}

        .ilpen-product-row {{
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            height: calc((297mm - 145px) / 2);
            padding: 12px 0;
            border-bottom: 1px dashed var(--pk-gray-200);
        }}

        .ilpen-product-row:last-child {{
            border-bottom: none;
        }}

        .ilpen-info-col {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .ilpen-code-badge {{
            display: inline-block;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 11px;
            font-weight: 800;
            color: #FFFFFF;
            background: var(--pk-navy);
            padding: 3px 10px;
            border-radius: 4px;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
            width: fit-content;
        }}

        .ilpen-prod-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 19px;
            font-weight: 800;
            color: var(--pk-navy);
            line-height: 1.15;
            margin-bottom: 4px;
        }}

        .ilpen-prod-sub {{
            font-size: 11px;
            color: var(--pk-muted);
            margin-bottom: 8px;
            font-weight: 500;
        }}

        .ilpen-accent-line {{
            width: 36px;
            height: 3px;
            background: var(--pk-lime);
            border-radius: 2px;
            margin-bottom: 10px;
        }}

        .ilpen-desc {{
            font-size: 11.5px;
            line-height: 1.45;
            color: #475569;
            margin-bottom: 12px;
        }}

        .ilpen-specs-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            background: var(--pk-gray-50);
            border: 1px solid var(--pk-gray-200);
            border-radius: 8px;
            padding: 8px 10px;
            margin-bottom: 12px;
        }}

        .spec-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .spec-icon {{
            color: var(--pk-lime-dark);
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .spec-texts {{
            display: flex;
            flex-direction: column;
        }}

        .spec-val {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 11px;
            font-weight: 700;
            color: var(--pk-navy);
            line-height: 1.1;
        }}

        .spec-lbl {{
            font-size: 9px;
            color: var(--pk-muted);
        }}

        .ilpen-caps-section {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .caps-header-lbl {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: var(--pk-navy);
            text-transform: uppercase;
        }}

        .ilpen-caps-flex {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .ilpen-cap-badge {{
            flex: 1;
            min-width: 130px;
            display: flex;
            align-items: center;
            gap: 8px;
            background: #FFFFFF;
            border: 1px solid var(--pk-gray-200);
            border-radius: 6px;
            padding: 6px;
        }}

        .cap-thumb-box {{
            width: 36px;
            height: 36px;
            border-radius: 4px;
            background: var(--pk-gray-100);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            flex-shrink: 0;
        }}

        .cap-thumb-box img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}

        .cap-info {{
            display: flex;
            flex-direction: column;
            overflow: hidden;
            width: 100%;
        }}

        .cap-header-line {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .cap-code {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 10.5px;
            font-weight: 800;
            color: var(--pk-navy);
        }}

        .cap-title {{
            font-size: 10px;
            font-weight: 600;
            color: #334155;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .cap-sub {{
            font-size: 8.5px;
            color: var(--pk-muted);
            line-height: 1.1;
        }}

        .cap-colors-row {{
            display: flex;
            align-items: center;
            gap: 4px;
            margin-top: 2px;
            flex-wrap: wrap;
        }}

        .colors-label {{
            font-size: 8px;
            font-weight: 700;
            color: var(--pk-muted);
        }}

        .colors-dots-container {{
            display: flex;
            align-items: center;
            gap: 3px;
        }}

        .color-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
        }}

        .ilpen-visual-col {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle at center, #F8FAFC 0%, #EDF2F7 100%);
            border-radius: 12px;
            padding: 12px;
            position: relative;
            border: 1px solid var(--pk-gray-200);
        }}

        .ilpen-bottle-podium {{
            width: 100%;
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}

        .ilpen-bottle-img {{
            max-width: 95%;
            max-height: 95%;
            object-fit: contain;
            filter: drop-shadow(0 14px 20px rgba(0, 0, 0, 0.16));
        }}

        .ilpen-dual-podium-wrap {{
            width: 100%;
            height: 190px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}

        .dual-podium-col {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 8px;
            padding: 6px;
            border: 1px solid rgba(226, 232, 240, 0.8);
        }}

        .podium-cap-header {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .podium-cap-code {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 10px;
            font-weight: 800;
            color: var(--pk-navy);
            background: #E2E8F0;
            padding: 1px 4px;
            border-radius: 3px;
        }}

        .podium-cap-title {{
            font-size: 9px;
            font-weight: 700;
            color: var(--pk-muted);
        }}

        .ilpen-bottle-podium-mini {{
            flex: 1;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}

        .mini-tag-bar {{
            display: flex;
            gap: 4px;
        }}

        .mini-tag {{
            font-size: 7.5px;
            font-weight: 800;
            color: #FFFFFF;
            padding: 1px 5px;
            border-radius: 2px;
            letter-spacing: 0.3px;
        }}

        .visual-tag-bar {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-top: 8px;
        }}

        .tag-brand {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 9px;
            font-weight: 800;
            color: #FFFFFF;
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.5px;
        }}

        .tag-res {{
            font-size: 9.5px;
            color: var(--pk-muted);
            font-weight: 600;
        }}

        .page-footer {{
            height: 40px;
            padding: 0 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid var(--pk-gray-200);
            font-size: 11px;
            color: var(--pk-muted);
            background: #FFFFFF;
            flex-shrink: 0;
        }}

        .footer-brand {{
            font-weight: 600;
            letter-spacing: 0.5px;
        }}

        .footer-page-num {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 13px;
            color: var(--pk-navy);
        }}

        /* Full Bleed Divider Covers */
        .divider-page {{
            position: relative;
            background-size: cover;
            background-position: center;
            color: #FFFFFF;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 60px;
        }}

        .divider-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(11, 19, 32, 0.75) 0%, rgba(18, 27, 45, 0.45) 50%, rgba(11, 19, 32, 0.85) 100%);
            z-index: 1;
        }}

        .divider-content {{
            position: relative;
            z-index: 2;
        }}

        .divider-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .divider-logo {{
            height: 68px;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.35));
        }}

        .divider-slogan {{
            font-family: 'Caveat', cursive;
            font-size: 36px;
            font-weight: 700;
            color: var(--pk-lime);
            text-shadow: 0 2px 10px rgba(145,206,23,0.35);
            letter-spacing: 0.5px;
        }}

        .divider-body {{
            position: relative;
            z-index: 2;
            margin-top: auto;
            margin-bottom: 60px;
        }}

        .divider-num {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 80px;
            font-weight: 900;
            color: var(--pk-lime);
            line-height: 1;
            margin-bottom: 12px;
            opacity: 0.95;
        }}

        .divider-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 38px;
            font-weight: 900;
            letter-spacing: 1px;
            text-transform: uppercase;
            line-height: 1.1;
            margin-bottom: 16px;
        }}

        .divider-line {{
            width: 80px;
            height: 5px;
            background: var(--pk-lime);
            border-radius: 3px;
            margin-bottom: 20px;
        }}

        .divider-desc {{
            font-size: 15px;
            line-height: 1.6;
            max-width: 480px;
            color: #E2E8F0;
        }}

        .divider-footer {{
            position: relative;
            z-index: 2;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 13px;
            color: #CBD5E1;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            padding-top: 24px;
        }}

        /* Table of Contents (TOC) */
        .toc-page {{
            padding: 50px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: #FFFFFF;
        }}

        .toc-top {{
            display: flex;
            flex-direction: column;
        }}

        .toc-brand-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 40px;
        }}

        .toc-hero-num {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 48px;
            font-weight: 900;
            color: var(--pk-navy);
            line-height: 1;
        }}

        .toc-hero-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 26px;
            font-weight: 800;
            color: var(--pk-navy);
            margin-top: 4px;
            letter-spacing: -0.5px;
        }}

        .toc-hero-line {{
            width: 60px;
            height: 4px;
            background: var(--pk-lime);
            border-radius: 2px;
            margin: 12px 0 32px 0;
        }}

        .toc-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 30px;
        }}

        .toc-item {{
            border-left: 3px solid var(--pk-navy);
            padding-left: 14px;
            display: flex;
            flex-direction: column;
        }}

        .toc-item:nth-child(2) {{ border-left-color: var(--pk-lime); }}
        .toc-item:nth-child(3) {{ border-left-color: var(--pk-navy-dark); }}
        .toc-item:nth-child(4) {{ border-left-color: var(--pk-muted); }}

        .toc-item-num {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            font-weight: 800;
            color: var(--pk-lime-dark);
            margin-bottom: 2px;
        }}

        .toc-item-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 16px;
            font-weight: 800;
            color: var(--pk-navy);
            margin-bottom: 4px;
        }}

        .toc-item-sub {{
            font-size: 11px;
            color: #64748B;
            line-height: 1.4;
            margin-bottom: 6px;
        }}

        .toc-item-pages {{
            font-size: 11px;
            font-weight: 700;
            color: var(--pk-navy);
        }}

        .toc-about-box {{
            background: var(--pk-gray-50);
            border: 1px solid var(--pk-gray-200);
            border-radius: 12px;
            padding: 24px;
            margin-top: auto;
        }}

        .toc-about-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 14px;
            font-weight: 800;
            color: var(--pk-navy);
            margin-bottom: 8px;
        }}

        .toc-about-text {{
            font-size: 12px;
            line-height: 1.6;
            color: #475569;
        }}
    </style>
</head>
<body class="sidebar-open">
    <!-- Backdrop Overlay for Mobile Bottom Sheet -->
    <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="closeSidebar()"></div>

    <!-- STUDIO TOP COMMAND BAR -->
    <header class="catalog-topbar">
        <div class="topbar-left">
            <img class="topbar-logo-img" src="assets/promkol_logo_vector_clean.png" alt="PROMKOL" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
            <div class="topbar-title-wrap">
                <div class="topbar-main-title">
                    KATALOG STÜDYOSU <span class="badge-live">CANLI EDİTÖR</span>
                </div>
                <div class="topbar-sub">Her şeyi tıklayıp düzenleyin &bull; Fotoğraf & logo seçin &bull; Büyütün & silin</div>
            </div>
        </div>

        <div class="topbar-center">
            <button class="topbar-btn active" id="btnModeEdit" onclick="setStudioMode('edit')">
                ✏️ Düzenleme Modu
            </button>
            <button class="topbar-btn" id="btnModePreview" onclick="setStudioMode('preview')">
                👁️ Baskı Önizlemesi
            </button>
        </div>

        <div class="topbar-right">
            <button class="btn-action-studio btn-sidebar-toggle" id="btnToggleSidebar" onclick="toggleSidebar()">
                🖼️ Fotoğraf Seçici
            </button>

            <button class="btn-action-studio btn-undo-redo mode-edit-only" onclick="studioUndo()" title="Geri Al (Ctrl+Z)">
                ↩️ Geri
            </button>
            <button class="btn-action-studio btn-undo-redo mode-edit-only" onclick="studioRedo()" title="İleri Al (Ctrl+Y)">
                ↪️ İleri
            </button>

            <button class="btn-action-studio btn-save-disk mode-edit-only" onclick="saveCatalogToDisk()" title="Değişiklikleri Kaydet">
                💾 Kaydet
            </button>

            <button class="btn-action-studio btn-download-html mode-edit-only" onclick="downloadCurrentCatalogHtml()" title="HTML Dosyası İndir">
                📥 İndir
            </button>

            <button class="btn-action-studio btn-reset-catalog mode-edit-only" onclick="resetCatalogToInitial()" title="İlk Orijinal Haline Sıfırla">
                🔄 Sıfırla
            </button>

            <button class="btn-action-studio btn-print-pdf" onclick="triggerPrint()">
                🖨️ PDF İndir (A4)
            </button>
        </div>
    </header>

    <!-- STUDIO LEFT MEDIA SIDEBAR (Desktop Drawer / Mobile Slide-up Bottom Sheet) -->
    <aside class="media-sidebar" id="mediaSidebar">
        <div class="sheet-pull-bar"></div>
        <div class="sidebar-header">
            <div class="sidebar-title">
                <span>📸 Fotoğraf & Mockup Kütüphanesi</span>
            </div>
            <button class="sidebar-close-btn" onclick="toggleSidebar()" title="Paneli Kapat">&times;</button>
        </div>

        <!-- Target Indicator -->
        <div class="target-indicator-box" id="targetIndicatorBox">
            <div class="target-indicator-title">
                <span>🎯 Seçili Alan:</span> <span id="targetLabelText">Henüz seçilmedi</span>
            </div>
            <div class="target-indicator-desc" id="targetDescText">
                Katalogdaki herhangi bir şişe, logo veya fotoğrafa tıklayın, ardından buradaki bir görsele tıklayarak anında değiştirin!
            </div>
        </div>

        <!-- Search Bar -->
        <div class="sidebar-search-wrap">
            <input type="text" class="sidebar-search-input" id="sidebarSearchInput" placeholder="Fotoğraf veya kod ara (Örn: 30P, Cam, Gemini)..." onkeyup="filterSidebarGallery(this.value)">
        </div>

        <!-- Tabs -->
        <div class="sidebar-tabs">
            <button class="sidebar-tab-btn active" onclick="switchSidebarTab('urunler', this)">🌟 Gemini Ürünler</button>
            <button class="sidebar-tab-btn" onclick="switchSidebarTab('mockups', this)">🧴 Şişe Mockupları</button>
            <button class="sidebar-tab-btn" onclick="switchSidebarTab('seffaf_png', this)">📦 Dekupe Şeffaf</button>
            <button class="sidebar-tab-btn" onclick="switchSidebarTab('beyaz_arka_plan', this)">🤍 Beyaz Zemin</button>
            <button class="sidebar-tab-btn" onclick="switchSidebarTab('assets', this)">🎨 Kapak & Logo</button>
            <button class="sidebar-tab-btn" onclick="switchSidebarTab('upload', this)">📤 Bilgisayardan Yükle</button>
        </div>

        <!-- Gallery Grid -->
        <div class="sidebar-gallery" id="sidebarGallery">
            <!-- Dynamically populated -->
        </div>

        <!-- Hidden Inputs for Custom Upload & Color Picking -->
        <input type="file" id="customImgFileInput" accept="image/*" style="display: none;" onchange="handleCustomFileUpload(event)">
        <input type="color" id="universalColorPicker" style="display: none;" onchange="onColorPicked(event)">
    </aside>

    <!-- TOAST CONTAINER -->
    <div class="toast-container" id="toastContainer"></div>

    <!-- MAIN CATALOG CONTAINER -->
    <main class="catalog-container" id="catalogContainer">
"""

# ----------------- SAYFA 1: KAPAK (Cover) -----------------
html += f"""
        <!-- SAYFA 1: KAPAK -->
        <div class="a4-page divider-page" style="background-image: url('assets/promkol_cover_main.jpg');" id="page-1">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa 01 (Kapak)</span>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            <div class="divider-overlay" style="background: linear-gradient(135deg, rgba(11, 19, 32, 0.75) 0%, rgba(18, 27, 45, 0.45) 50%, rgba(11, 19, 32, 0.85) 100%);"></div>
            
            <div class="divider-header divider-content">
                <div class="editable-img-box resizable-container" data-label="Kapak Logosu">
                    <img class="divider-logo studio-img resizable-img" src="assets/promkol_logo_vector_clean.png" alt="PROMKOL" style="height: 68px;" data-scale="1.0">
                    <div class="img-quick-tools">
                        <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))">🔄 Logo Seç</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)" title="Küçült">🔍 -</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)" title="Büyüt">🔍 +</button>
                        <button class="img-tool-btn reset-scale" onclick="resetImgScale(this.closest('.editable-img-box').querySelector('img'))" title="Sıfırla">↺</button>
                    </div>
                </div>
                <div class="divider-slogan" contenteditable="true" spellcheck="false">Miss gibi promosyon</div>
            </div>

            <div class="divider-body">
                <div class="divider-num" style="font-size: 96px; letter-spacing: -2px;" contenteditable="true" spellcheck="false">2027</div>
                <div class="divider-title" style="font-size: 40px; max-width: 520px; margin-bottom: 14px;" contenteditable="true" spellcheck="false">KURUMSAL PROMOSYON KOLONYA KOLEKSİYONU</div>
                <div class="divider-line" style="width: 120px; height: 6px; margin-bottom: 16px;"></div>
                
                <div class="cover-hero-tagline" style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin-bottom: 10px; letter-spacing: -0.2px;" contenteditable="true" spellcheck="false">
                    Güzel kokular hafızada, markanız akılda kalır.
                </div>
                <div class="divider-desc" style="font-size: 15px; line-height: 1.65; max-width: 540px; color: #E2E8F0; margin-bottom: 14px;" contenteditable="true" spellcheck="false">
                    Her kullanımda markanızı hatırlatan, müşterilerinizin severek kullanacağı özel bir hediye. Türkiye’nin lider kurumsal kolonya üreticisi PROMKOL güvencesiyle, markanıza özel tasarlanmış promosyon kolonyaları.
                </div>
                <div class="cover-sub-slogan" style="font-family: 'Caveat', cursive; font-size: 26px; font-weight: 700; color: var(--pk-lime); margin-bottom: 16px; text-shadow: 0 2px 8px rgba(145,206,23,0.3);" contenteditable="true" spellcheck="false">
                    Miss gibi promosyon
                </div>

                <div class="cover-usp-badges" style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <span style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.18); backdrop-filter: blur(8px); padding: 5px 14px; border-radius: 20px; font-size: 11px; font-weight: 700; color: #F8FAFC;" contenteditable="true" spellcheck="false">
                        <span style="color: var(--pk-lime); font-weight: 800;">✓</span> Markanızın Kurumsal Renk & Logo Uyumu
                    </span>
                    <span style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.18); backdrop-filter: blur(8px); padding: 5px 14px; border-radius: 20px; font-size: 11px; font-weight: 700; color: #F8FAFC;" contenteditable="true" spellcheck="false">
                        <span style="color: var(--pk-lime); font-weight: 800;">✓</span> Bütçenize & Etkinliğinize Özel Zengin Çeşitlilik
                    </span>
                </div>
            </div>

            <div class="divider-footer" style="letter-spacing: 0.8px; font-weight: 700;">
                <div style="color: #FFFFFF; font-size: 13.5px;" contenteditable="true" spellcheck="false">MARKANIZA ÖZEL ETİKET &bull; ZENGİN ÜRÜN ÇEŞİTLİLİĞİ</div>
                <div style="color: var(--pk-lime); font-size: 13.5px;" contenteditable="true" spellcheck="false">www.promkol.com.tr</div>
            </div>
        </div>
"""

# ----------------- SAYFA 2: İÇİNDEKİLER (TOC) -----------------
html += f"""
        <!-- SAYFA 2: İÇİNDEKİLER & BİZ KİMİZ -->
        <div class="a4-page toc-page" id="page-2">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa 02 (İçindekiler)</span>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            <div class="toc-top">
                <div class="toc-brand-bar">
                    <div class="header-logo-box editable-img-box" data-label="TOC Logosu">
                        <img src="assets/promkol_logo_hires_dark.png" alt="PROMKOL" class="studio-img resizable-img" style="height: 36px;" data-scale="1.0">
                        <div class="img-quick-tools">
                            <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))">🔄 Logo</button>
                            <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)">🔍 -</button>
                            <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)">🔍 +</button>
                        </div>
                    </div>
                    <span style="font-family: 'Caveat', cursive; font-size: 22px; color: var(--pk-lime-dark); font-weight: 700;" contenteditable="true" spellcheck="false">Miss gibi promosyon</span>
                </div>

                <div class="toc-hero-num" contenteditable="true" spellcheck="false">2027</div>
                <div class="toc-hero-title" contenteditable="true" spellcheck="false">ÜRÜN KOLEKSİYONU VE İÇİNDEKİLER</div>
                <div class="toc-hero-line"></div>

                <div class="toc-grid">
                    <div class="toc-item">
                        <span class="toc-item-num">01</span>
                        <span class="toc-item-title" contenteditable="true" spellcheck="false">PET ŞİŞE KOLONYA SERİSİ</span>
                        <span class="toc-item-sub" contenteditable="true" spellcheck="false">30 ml - 400 ml Ergonomik Şişeler &bull; Flip-Top ve Sprey</span>
                        <span class="toc-item-pages" contenteditable="true" spellcheck="false">Sayfa 03 - 08</span>
                    </div>

                    <div class="toc-item">
                        <span class="toc-item-num">02</span>
                        <span class="toc-item-title" contenteditable="true" spellcheck="false">SLİM & CEP KOLONYALARI SERİSİ</span>
                        <span class="toc-item-sub" contenteditable="true" spellcheck="false">20 ml - 50 ml Kredi Kartı Boyu & Modern Klipsli</span>
                        <span class="toc-item-pages" contenteditable="true" spellcheck="false">Sayfa 09 - 12</span>
                    </div>

                    <div class="toc-item">
                        <span class="toc-item-num">03</span>
                        <span class="toc-item-title" contenteditable="true" spellcheck="false">KRİSTAL & LÜKS CAM SERİSİ</span>
                        <span class="toc-item-sub" contenteditable="true" spellcheck="false">10 ml - 250 ml Ağır Taban Kristal Cam & Metalik Başlık</span>
                        <span class="toc-item-pages" contenteditable="true" spellcheck="false">Sayfa 13 - 17</span>
                    </div>

                    <div class="toc-item">
                        <span class="toc-item-num">04</span>
                        <span class="toc-item-title" contenteditable="true" spellcheck="false">ESANS, BASKI VE TEKNİK REHBER</span>
                        <span class="toc-item-sub" contenteditable="true" spellcheck="false">80° Koku Çeşitleri, Özel Etiketleme ve Koli Standartları</span>
                        <span class="toc-item-pages" contenteditable="true" spellcheck="false">Sayfa 18 - 19</span>
                    </div>
                </div>
            </div>

            <div class="toc-about-box">
                <div class="toc-about-title" contenteditable="true" spellcheck="false">BİZ KİMİZ? &bull; PROMKOL HAKKINDA</div>
                <div class="toc-about-text" contenteditable="true" spellcheck="false">
                    Promkol olarak, kurumsal promosyon ve kişisel bakım sektöründe yenilikçi bakış açımız, yüksek üretim standartlarımız ve koşulsuz müşteri memnuniyeti ilkemizle hizmet vermekteyiz. 80 derece etil alkol ile hazırlanan formüllerimiz, Sağlık Bakanlığı bildirimli olup uluslararası hijyen ve GMP normlarına tam uyumludur. Markanızın prestijini kokunuzla buluşturuyoruz.
                </div>
            </div>

            <div class="page-footer" style="padding: 0; border: none;">
                <span class="footer-brand" contenteditable="true" spellcheck="false">PROMKOL KURUMSAL PROMOSYON</span>
                <span class="footer-page-num">02</span>
            </div>
        </div>
"""

cur_page = 3

# ----------------- BÖLÜM 1: PET SERİSİ -----------------
# Bölüm Kapağı
html += f"""
        <!-- SAYFA {cur_page}: BÖLÜM 1 KAPAĞI -->
        <div class="a4-page divider-page" style="background-image: url('assets/promkol_cover_pet.jpg');" id="page-{cur_page}">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa {cur_page:02d} (Bölüm 1 Kapağı)</span>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            <div class="divider-overlay"></div>
            
            <div class="divider-header divider-content">
                <div class="editable-img-box resizable-container" data-label="Bölüm Logosu">
                    <img class="divider-logo studio-img resizable-img" src="assets/promkol_logo_vector_clean.png" alt="PROMKOL" style="height: 68px;" data-scale="1.0">
                    <div class="img-quick-tools">
                        <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))">🔄 Logo</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)">🔍 -</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)">🔍 +</button>
                    </div>
                </div>
                <div class="divider-slogan" contenteditable="true" spellcheck="false">Miss gibi promosyon</div>
            </div>

            <div class="divider-body">
                <div class="divider-num" contenteditable="true" spellcheck="false">01</div>
                <div class="divider-title" contenteditable="true" spellcheck="false">PET ŞİŞE KOLONYA SERİSİ</div>
                <div class="divider-line"></div>
                <div class="divider-desc" contenteditable="true" spellcheck="false">
                    30 ml'den 400 ml'ye kadar geniş hacim seçenekleri, yüksek berraklıkta kırılmaz gövde yapısı, sızdırmaz Flip-Top ve mikro sis Sprey kapak opsiyonlarıyla kurumsal promosyonun en çok tercih edilen koleksiyonu.
                </div>
            </div>

            <div class="divider-footer">
                <div contenteditable="true" spellcheck="false">YUVARLAK &bull; YASSI &bull; KAVİSLİ &bull; PRİZMA FORMLAR</div>
                <div>Sayfa {cur_page:02d}</div>
            </div>
        </div>
"""
cur_page += 1

# PET Product Pages
for pair in pet_pairs:
    html += f"""
        <!-- SAYFA {cur_page}: PET ÜRÜNLERİ -->
        <div class="a4-page" id="page-{cur_page}">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa {cur_page:02d}</span>
                <button class="page-action-btn" onclick="addNewProductRowToPage(this.closest('.a4-page'))">➕ Ürün Ekle</button>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            {render_page_header("01 • PET ŞİŞE SERİSİ")}

            <div class="page-body">
                {render_product_card(pair[0])}
                {render_product_card(pair[1]) if len(pair) > 1 else ''}
            </div>

            <div class="page-footer">
                <span class="footer-brand">PROMKOL &bull; www.promkol.com.tr</span>
                <span class="footer-page-num">{cur_page:02d}</span>
            </div>
        </div>
    """
    cur_page += 1

# ----------------- BÖLÜM 2: SLİM CEP SERİSİ -----------------
# Bölüm Kapağı
html += f"""
        <!-- SAYFA {cur_page}: BÖLÜM 2 KAPAĞI -->
        <div class="a4-page divider-page" style="background-image: url('assets/promkol_cover_slim.jpg');" id="page-{cur_page}">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa {cur_page:02d} (Bölüm 2 Kapağı)</span>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            <div class="divider-overlay"></div>
            
            <div class="divider-header divider-content">
                <div class="editable-img-box resizable-container" data-label="Bölüm Logosu">
                    <img class="divider-logo studio-img resizable-img" src="assets/promkol_logo_vector_clean.png" alt="PROMKOL" style="height: 68px;" data-scale="1.0">
                    <div class="img-quick-tools">
                        <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))">🔄 Logo</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)">🔍 -</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)">🔍 +</button>
                    </div>
                </div>
                <div class="divider-slogan" contenteditable="true" spellcheck="false">Miss gibi promosyon</div>
            </div>

            <div class="divider-body">
                <div class="divider-num" contenteditable="true" spellcheck="false">02</div>
                <div class="divider-title" contenteditable="true" spellcheck="false">SLİM & CEP KOLONYALARI SERİSİ</div>
                <div class="divider-line"></div>
                <div class="divider-desc" contenteditable="true" spellcheck="false">
                    Mat siyah ve dinamik renk alternatifleriyle cepte, cüzdanda ve çantada her an yanınızda taşınabilen ultra modern kredi kartı ve klipsli mekanizmalı promosyon serisi.
                </div>
            </div>

            <div class="divider-footer">
                <div contenteditable="true" spellcheck="false">20 ML &bull; 25 ML &bull; 45 ML &bull; 50 ML FORM ÇEŞİTLERİ</div>
                <div>Sayfa {cur_page:02d}</div>
            </div>
        </div>
"""
cur_page += 1

# Slim Product Pages
for pair in slim_pairs:
    html += f"""
        <!-- SAYFA {cur_page}: SLİM ÜRÜNLERİ -->
        <div class="a4-page" id="page-{cur_page}">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa {cur_page:02d}</span>
                <button class="page-action-btn" onclick="addNewProductRowToPage(this.closest('.a4-page'))">➕ Ürün Ekle</button>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            {render_page_header("02 • SLİM & CEP SERİSİ")}

            <div class="page-body">
                {render_product_card(pair[0])}
                {render_product_card(pair[1]) if len(pair) > 1 else ''}
            </div>

            <div class="page-footer">
                <span class="footer-brand">PROMKOL &bull; www.promkol.com.tr</span>
                <span class="footer-page-num">{cur_page:02d}</span>
            </div>
        </div>
    """
    cur_page += 1

# Slim Showcase (50K01 + Series Display)
html += f"""
        <!-- SAYFA {cur_page}: SLİM 50K01 SHOWCASE -->
        <div class="a4-page" id="page-{cur_page}">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa {cur_page:02d} (Vitrin)</span>
                <button class="page-action-btn" onclick="addNewProductRowToPage(this.closest('.a4-page'))">➕ Ürün Ekle</button>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            {render_page_header("02 • SLİM & CEP SERİSİ")}

            <div class="page-body">
                {render_product_card(slim_single[0])}
                
                <!-- Alt: Slim Serisi Aile Vitrini -->
                <div style="flex: 0.9; background: var(--pk-gray-50); border: 1px solid var(--pk-gray-200); border-radius: 12px; padding: 20px; display: flex; align-items: center; justify-content: space-between; gap: 24px;">
                    <div style="flex: 1.2;">
                        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; font-weight: 800; color: var(--pk-lime-dark); letter-spacing: 1px;">SLİM SERİSİ AVANTAJLARI</span>
                        <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 800; color: var(--pk-navy); margin: 4px 0 8px 0;" contenteditable="true" spellcheck="false">HER AN YANINIZDA &bull; MAKSİMUM MARKA ETKİSİ</h3>
                        <p style="font-size: 12px; line-height: 1.5; color: #475569;" contenteditable="true" spellcheck="false">
                            Kredi kartı ebatlarındaki slim kolonyalar, müşterilerinizin gün boyu cebinde veya çantasında taşıdığı, sürekli kullanılan ve markanızı her kullanımda hatırlatan en etkili promosyon ürünüdür.
                        </p>
                    </div>
                    <div style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 12px;">
                        <div class="editable-img-box resizable-container" data-label="20K01 Vitrin Görseli">
                            <img src="ürünler/Gemini_Generated_Image_qyoaqvqyoaqvqyoa.jpg" alt="20K01" class="studio-img resizable-img" style="height: 130px; object-fit: contain; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" data-scale="1.0">
                            <div class="img-quick-tools">
                                <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))">🔄 Seç</button>
                                <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)">🔍 -</button>
                                <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)">🔍 +</button>
                            </div>
                        </div>
                        <div class="editable-img-box resizable-container" data-label="20K02 Vitrin Görseli">
                            <img src="ürünler/Gemini_Generated_Image_ab5yiiab5yiiab5y.jpg" alt="20K02" class="studio-img resizable-img" style="height: 130px; object-fit: contain; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" data-scale="1.0">
                            <div class="img-quick-tools">
                                <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))">🔄 Seç</button>
                                <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)">🔍 -</button>
                                <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)">🔍 +</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="page-footer">
                <span class="footer-brand">PROMKOL &bull; www.promkol.com.tr</span>
                <span class="footer-page-num">{cur_page:02d}</span>
            </div>
        </div>
"""
cur_page += 1

# ----------------- BÖLÜM 3: KRİSTAL CAM SERİSİ -----------------
# Bölüm Kapağı
html += f"""
        <!-- SAYFA {cur_page}: BÖLÜM 3 KAPAĞI -->
        <div class="a4-page divider-page" style="background-image: url('assets/promkol_cover_crystal.jpg');" id="page-{cur_page}">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa {cur_page:02d} (Bölüm 3 Kapağı)</span>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            <div class="divider-overlay"></div>
            
            <div class="divider-header divider-content">
                <div class="editable-img-box resizable-container" data-label="Bölüm Logosu">
                    <img class="divider-logo studio-img resizable-img" src="assets/promkol_logo_vector_clean.png" alt="PROMKOL" style="height: 68px;" data-scale="1.0">
                    <div class="img-quick-tools">
                        <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))">🔄 Logo</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)">🔍 -</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)">🔍 +</button>
                    </div>
                </div>
                <div class="divider-slogan" contenteditable="true" spellcheck="false">Miss gibi promosyon</div>
            </div>

            <div class="divider-body">
                <div class="divider-num" contenteditable="true" spellcheck="false">03</div>
                <div class="divider-title" contenteditable="true" spellcheck="false">KRİSTAL & LÜKS CAM SERİSİ</div>
                <div class="divider-line"></div>
                <div class="divider-desc" contenteditable="true" spellcheck="false">
                    Ağır tabanlı kristal cam gövdeler, metalik valfli sprey başlıklar ve geleneksel dökme tıpalı modeller. VIP yönetici setleri, prestijli iş ortakları ve özel kutlamalar için tasarlanmış amiral gemisi koleksiyon.
                </div>
            </div>

            <div class="divider-footer">
                <div contenteditable="true" spellcheck="false">LINEA &bull; DIAMOND &bull; RIGA &bull; SIGNATURE MODELLERİ</div>
                <div>Sayfa {cur_page:02d}</div>
            </div>
        </div>
"""
cur_page += 1

# Cam Product Pages
for pair in cam_pairs:
    html += f"""
        <!-- SAYFA {cur_page}: CAM ÜRÜNLERİ -->
        <div class="a4-page" id="page-{cur_page}">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa {cur_page:02d}</span>
                <button class="page-action-btn" onclick="addNewProductRowToPage(this.closest('.a4-page'))">➕ Ürün Ekle</button>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            {render_page_header("03 • KRİSTAL CAM SERİSİ")}

            <div class="page-body">
                {render_product_card(pair[0])}
                {render_product_card(pair[1]) if len(pair) > 1 else ''}
            </div>

            <div class="page-footer">
                <span class="footer-brand">PROMKOL &bull; www.promkol.com.tr</span>
                <span class="footer-page-num">{cur_page:02d}</span>
            </div>
        </div>
    """
    cur_page += 1

# ----------------- SAYFA 18: ESANS & TEKNİK REHBER -----------------
html += f"""
        <!-- SAYFA {cur_page}: ESANS & TEKNİK REHBER -->
        <div class="a4-page" id="page-{cur_page}">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa {cur_page:02d} (Teknik Rehber)</span>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            {render_page_header("TEKNİK REHBER & ESANS SEÇENEKLERİ")}

            <div class="page-body" style="justify-content: flex-start; gap: 20px;">
                <!-- Esans Koleksiyonu -->
                <div>
                    <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 800; color: var(--pk-lime-dark); letter-spacing: 1px;">80 DERECE ETİL ALKOL GÜVENCESİ</span>
                    <h2 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 900; color: var(--pk-navy); margin-top: 4px;" contenteditable="true" spellcheck="false">PREMİUM ESANS SEÇENEKLERİ</h2>
                    <div class="ilpen-accent-line" style="margin-bottom: 16px;"></div>

                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
                        <div style="background: var(--pk-gray-50); border: 1px solid var(--pk-gray-200); border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 800; font-size: 13px; color: var(--pk-navy);" contenteditable="true" spellcheck="false">🍋 Çeşme Limonu</div>
                            <div style="font-size: 11px; color: #64748B; margin-top: 4px;" contenteditable="true" spellcheck="false">Geleneksel taze narenciye ferahlığı. En çok tercih edilen klasik koku.</div>
                        </div>
                        <div style="background: var(--pk-gray-50); border: 1px solid var(--pk-gray-200); border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 800; font-size: 13px; color: var(--pk-navy);" contenteditable="true" spellcheck="false">🌿 Bodrum Mandalinası</div>
                            <div style="font-size: 11px; color: #64748B; margin-top: 4px;" contenteditable="true" spellcheck="false">Yoğun meyvemsi tatlı ferahlık, enerjik ve modern kurumsal esans.</div>
                        </div>
                        <div style="background: var(--pk-gray-50); border: 1px solid var(--pk-gray-200); border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 800; font-size: 13px; color: var(--pk-navy);" contenteditable="true" spellcheck="false">🌸 Japon Kiraz Çiçeği</div>
                            <div style="font-size: 11px; color: #64748B; margin-top: 4px;" contenteditable="true" spellcheck="false">Zarif çiçeksi notalar, kadınlara ve prestij etkinliklere özel koku.</div>
                        </div>
                        <div style="background: var(--pk-gray-50); border: 1px solid var(--pk-gray-200); border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 800; font-size: 13px; color: var(--pk-navy);" contenteditable="true" spellcheck="false">🌊 Okyanus / Amber</div>
                            <div style="font-size: 11px; color: #64748B; margin-top: 4px;" contenteditable="true" spellcheck="false">Kalıcı ve sofistike maskülen koku. Cam serisi için ideal VIP tercih.</div>
                        </div>
                    </div>
                </div>

                <!-- Baskı ve Özelleştirme -->
                <div style="margin-top: 10px;">
                    <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 800; color: var(--pk-lime-dark); letter-spacing: 1px;">KURUMSAL KİMLİK UYGULAMALARI</span>
                    <h2 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 900; color: var(--pk-navy); margin-top: 4px;" contenteditable="true" spellcheck="false">BASKI TEKNOLOJİLERİ</h2>
                    <div class="ilpen-accent-line" style="margin-bottom: 16px;"></div>

                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
                        <div style="border-left: 3px solid var(--pk-navy); padding-left: 12px;">
                            <div style="font-weight: 800; font-size: 13px; color: var(--pk-navy);" contenteditable="true" spellcheck="false">TAM RENKLİ KUŞE ETİKET</div>
                            <div style="font-size: 11px; color: #64748B; margin-top: 4px;" contenteditable="true" spellcheck="false">Fotoğraf kalitesinde dijital ve ofset baskı. Suya ve alkole dayanıklı koruyucu selefon kaplama.</div>
                        </div>
                        <div style="border-left: 3px solid var(--pk-lime); padding-left: 12px;">
                            <div style="font-weight: 800; font-size: 13px; color: var(--pk-navy);" contenteditable="true" spellcheck="false">ŞEFFAF / SİLVER ETİKET</div>
                            <div style="font-size: 11px; color: #64748B; margin-top: 4px;" contenteditable="true" spellcheck="false">Şişe içi sıvının rengini gösteren 'no-label' şeffaf veya gümüş/metalize yaldız zemin uygulamaları.</div>
                        </div>
                        <div style="border-left: 3px solid var(--pk-navy-dark); padding-left: 12px;">
                            <div style="font-weight: 800; font-size: 13px; color: var(--pk-navy);" contenteditable="true" spellcheck="false">UV VE SERİGRAFİ BASKI</div>
                            <div style="font-size: 11px; color: #64748B; margin-top: 4px;" contenteditable="true" spellcheck="false">Doğrudan şişe gövdesine kabartmalı ve çizilmez UV serigrafik baskı teknolojisi.</div>
                        </div>
                    </div>
                </div>

                <!-- Kalite Belgesi & İletişim Kutusu -->
                <div style="background: linear-gradient(135deg, #1E2B45 0%, #121B2D 100%); border-radius: 12px; padding: 24px; color: #FFFFFF; margin-top: auto; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 800; color: #FFFFFF;" contenteditable="true" spellcheck="false">SAĞLIK BAKANLIĞI BİLDİRİMLİ & ISO GÜVENCELİ</div>
                        <div style="font-size: 12px; color: #CBD5E1; margin-top: 6px; max-width: 500px;" contenteditable="true" spellcheck="false">
                            Tüm formülasyonlarımız yürürlükteki kozmetik yönetmeliğine uygun üretilmekte olup UTS (Ürün Takip Sistemi) kayıtlıdır.
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-family: 'Caveat', cursive; font-size: 26px; color: var(--pk-lime); font-weight: 700;">Miss gibi promosyon</span>
                        <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">PROMKOL 2027 KURUMSAL</div>
                    </div>
                </div>
            </div>

            <div class="page-footer">
                <span class="footer-brand">PROMKOL &bull; www.promkol.com.tr</span>
                <span class="footer-page-num">{cur_page:02d}</span>
            </div>
        </div>
"""
cur_page += 1

# ----------------- SAYFA 19: ARKA KAPAK (Back Cover) -----------------
html += f"""
        <!-- SAYFA {cur_page}: ARKA KAPAK -->
        <div class="a4-page divider-page" style="background-image: url('assets/promkol_cover_main.jpg');" id="page-{cur_page}">
            <div class="page-actions-bar">
                <span class="page-badge-lbl">Sayfa {cur_page:02d} (Arka Kapak)</span>
                <button class="page-action-btn" onclick="duplicatePage(this.closest('.a4-page'))">📑 Kopyala</button>
                <button class="page-action-btn del" onclick="deletePage(this.closest('.a4-page'))">🗑️ Sil</button>
            </div>

            <div class="divider-overlay" style="background: linear-gradient(135deg, rgba(11, 19, 32, 0.9) 0%, rgba(18, 27, 45, 0.75) 50%, rgba(11, 19, 32, 0.95) 100%);"></div>
            
            <div class="divider-header divider-content">
                <div class="editable-img-box resizable-container" data-label="Arka Kapak Logosu">
                    <img class="divider-logo studio-img resizable-img" src="assets/promkol_logo_vector_clean.png" alt="PROMKOL" style="height: 52px;" data-scale="1.0">
                    <div class="img-quick-tools">
                        <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))">🔄 Logo</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)">🔍 -</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)">🔍 +</button>
                    </div>
                </div>
                <div class="divider-slogan" contenteditable="true" spellcheck="false">Miss gibi promosyon</div>
            </div>

            <div class="divider-body">
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; font-weight: 800; color: var(--pk-lime); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;">
                    TÜRKİYE'NİN KURUMSAL KOLONYA ÇÖZÜM ORTAĞI
                </div>
                <div class="divider-title" style="font-size: 34px; max-width: 500px;" contenteditable="true" spellcheck="false">
                    MARKANIZIN PRESTİJİNİ BİRLİKTE YÜKSELTELİM
                </div>
                <div class="divider-line"></div>
                <div class="divider-desc" style="max-width: 520px; font-size: 14px; margin-bottom: 24px;" contenteditable="true" spellcheck="false">
                    Numune talebi, özel koku seçimi, kurumsal logo uygulama simülasyonları ve yüksek adetli sipariş teklifleriniz için uzman müşteri temsilcilerimizle iletişime geçebilirsiniz.
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 520px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 20px;">
                    <div>
                        <div style="font-size: 11px; font-weight: 700; color: var(--pk-lime); text-transform: uppercase;">MERKEZ OFİS & FABRİKA</div>
                        <div style="font-size: 13px; color: #FFFFFF; margin-top: 4px;" contenteditable="true" spellcheck="false">İkitelli OSB, Promosyon Sanayi Sitesi, İstanbul / TÜRKİYE</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; font-weight: 700; color: var(--pk-lime); text-transform: uppercase;">İLETİŞİM</div>
                        <div style="font-size: 13px; color: #FFFFFF; margin-top: 4px;" contenteditable="true" spellcheck="false">bilgi@promkol.com.tr<br>www.promkol.com.tr</div>
                    </div>
                </div>
            </div>

            <div class="divider-footer">
                <div>&copy; 2027 PROMKOL. TÜM HAKLARI SAKLIDIR.</div>
                <div>Sayfa {cur_page:02d}</div>
            </div>
        </div>
"""

# Embed Assets Manifest directly as JSON
embedded_manifest_json = json.dumps(manifest_data, ensure_ascii=False)

# Studio JavaScript Engine
html += f"""
    </main>

    <!-- STUDIO CLIENT JAVASCRIPT ENGINE -->
    <script>
        // EMBEDDED ASSETS DATA
        window.STUDIO_ASSETS = {embedded_manifest_json};

        // STUDIO STATE
        let activeTargetImg = null;
        let activeColorDot = null;
        let activeTab = 'urunler';
        let isSidebarOpen = true;
        let isPreviewMode = false;
        let undoStack = [];
        let redoStack = [];
        const MAX_HISTORY = 30;
        const STORAGE_KEY = 'promkol_studio_catalog_v2';

        // Auto Save to LocalStorage
        function autoSaveToStorage() {{
            try {{
                const canvas = document.getElementById('catalogContainer');
                if (!canvas) return;
                localStorage.setItem(STORAGE_KEY, canvas.innerHTML);
            }} catch (e) {{
                console.warn('Storage limit reached or unavailable:', e);
            }}
        }}

        // Take snapshot for Undo
        function takeSnapshot() {{
            const canvas = document.getElementById('catalogContainer');
            if (!canvas) return;
            undoStack.push(canvas.innerHTML);
            if (undoStack.length > MAX_HISTORY) undoStack.shift();
            redoStack = [];
            autoSaveToStorage();
        }}

        // Undo
        function studioUndo() {{
            if (undoStack.length === 0) {{
                showToast('ℹ️ Geri alınacak işlem yok.');
                return;
            }}
            const canvas = document.getElementById('catalogContainer');
            redoStack.push(canvas.innerHTML);
            const prev = undoStack.pop();
            canvas.innerHTML = prev;
            bindStudioEvents();
            autoSaveToStorage();
            showToast('↩️ Geri alındı!');
        }}

        // Redo
        function studioRedo() {{
            if (redoStack.length === 0) {{
                showToast('ℹ️ İleri alınacak işlem yok.');
                return;
            }}
            const canvas = document.getElementById('catalogContainer');
            undoStack.push(canvas.innerHTML);
            const next = redoStack.pop();
            canvas.innerHTML = next;
            bindStudioEvents();
            autoSaveToStorage();
            showToast('↪️ İleri alındı!');
        }}

        // Toast notifications
        function showToast(msg, duration = 3000) {{
            const container = document.getElementById('toastContainer');
            const el = document.createElement('div');
            el.className = 'toast-msg';
            el.innerHTML = msg;
            container.appendChild(el);
            setTimeout(() => {{
                el.style.opacity = '0';
                el.style.transform = 'translateY(10px)';
                setTimeout(() => el.remove(), 300);
            }}, duration);
        }}

        // Mode switch: Edit vs Preview
        function setStudioMode(mode) {{
            isPreviewMode = (mode === 'preview');
            const body = document.body;
            const btnEdit = document.getElementById('btnModeEdit');
            const btnPrev = document.getElementById('btnModePreview');

            if (isPreviewMode) {{
                body.classList.add('preview-mode');
                btnPrev.classList.add('active');
                btnEdit.classList.remove('active');
                if (activeTargetImg) deselectActiveImg();
                showToast('👁️ Baskı Önizlemesi aktif (Düzenleme araçları gizlendi)');
            }} else {{
                body.classList.remove('preview-mode');
                btnEdit.classList.add('active');
                btnPrev.classList.remove('active');
                showToast('✏️ Düzenleme Modu aktif');
            }}
        }}

        // Sidebar / Mobile Bottom Sheet Handlers
        function openSidebar() {{
            isSidebarOpen = true;
            const sidebar = document.getElementById('mediaSidebar');
            const backdrop = document.getElementById('sidebarBackdrop');
            if (sidebar) sidebar.classList.remove('collapsed');
            if (backdrop) backdrop.classList.add('active');
            if (window.innerWidth > 900) {{
                document.body.classList.add('sidebar-open');
            }}
        }}

        function closeSidebar() {{
            isSidebarOpen = false;
            const sidebar = document.getElementById('mediaSidebar');
            const backdrop = document.getElementById('sidebarBackdrop');
            if (sidebar) sidebar.classList.add('collapsed');
            if (backdrop) backdrop.classList.remove('active');
            document.body.classList.remove('sidebar-open');
        }}

        function toggleSidebar() {{
            if (isSidebarOpen) {{
                closeSidebar();
            }} else {{
                openSidebar();
            }}
        }}

        // Mobile Quick Add Product Button
        function quickAddProductToCatalog() {{
            takeSnapshot();
            const pages = document.querySelectorAll('.a4-page:not(.divider-page):not(.toc-page)');
            if (pages.length === 0) {{
                showToast('⚠️ Ürün eklenebilecek sayfa bulunamadı.');
                return;
            }}
            let targetPage = pages[0];
            const scrollPos = window.scrollY + 200;
            pages.forEach(p => {{
                if (p.offsetTop <= scrollPos) {{
                    targetPage = p;
                }}
            }});
            addNewProductRowToPage(targetPage);
            targetPage.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            showToast('➕ Yeni ürün kartı eklendi! Düzenlemek için üzerine dokunun.');
        }}

        // Active Target Image Selection
        function setActiveImg(imgEl) {{
            if (!imgEl) return;
            if (activeTargetImg) {{
                activeTargetImg.classList.remove('editor-active-img');
            }}
            activeTargetImg = imgEl;
            activeTargetImg.classList.add('editor-active-img');

            openSidebar();

            const parentBox = imgEl.closest('.editable-img-box');
            const label = (parentBox && parentBox.getAttribute('data-label')) || imgEl.alt || 'Katalog Görseli';
            document.getElementById('targetLabelText').textContent = label;
            document.getElementById('targetDescText').innerHTML = 'Aşağıdaki galeriden herhangi bir fotoğrafa dokunarak <b>' + label + '</b> görselini anında değiştirin!';

            showToast('🎯 <b>' + label + '</b> seçildi! Galeriden yeni görsel seçebilirsiniz.');
        }}

        function deselectActiveImg() {{
            if (activeTargetImg) {{
                activeTargetImg.classList.remove('editor-active-img');
                activeTargetImg = null;
            }}
            document.getElementById('targetLabelText').textContent = 'Henüz seçilmedi';
            document.getElementById('targetDescText').textContent = 'Katalogdaki herhangi bir şişe, logo veya fotoğrafa dokunun, ardından buradaki bir görsele dokunarak anında değiştirin!';
        }}

        function openSidebarForImg(imgEl) {{
            setActiveImg(imgEl);
        }}

        function clearImageSrc(imgEl) {{
            if (!imgEl) return;
            takeSnapshot();
            imgEl.src = 'assets/podium_pet.jpg';
            showToast('🗑️ Görsel temizlendi!');
        }}

        // IMAGE SCALE & RESIZING ENGINE (Büyültüp Küçültme)
        function adjustImgScale(imgEl, delta) {{
            if (!imgEl) return;
            takeSnapshot();
            let curScale = parseFloat(imgEl.getAttribute('data-scale') || '1.0');
            let newScale = Math.max(0.3, Math.min(3.0, curScale + delta));
            newScale = Math.round(newScale * 10) / 10;
            imgEl.setAttribute('data-scale', newScale);
            imgEl.style.transform = 'scale(' + newScale + ')';
            showToast('🔍 Görsel boyutu: %' + Math.round(newScale * 100));
        }}

        function resetImgScale(imgEl) {{
            if (!imgEl) return;
            takeSnapshot();
            imgEl.setAttribute('data-scale', '1.0');
            imgEl.style.transform = 'scale(1.0)';
            showToast('↺ Görsel boyutu sıfırlandı (%100)');
        }}

        // Interactive Corner Drag Resize
        let isDraggingResize = false;
        let dragTargetImg = null;
        let startX = 0, startScale = 1.0;

        function initDragResize(e, imgEl) {{
            e.preventDefault();
            e.stopPropagation();
            if (!imgEl) return;
            takeSnapshot();
            isDraggingResize = true;
            dragTargetImg = imgEl;
            startX = e.clientX;
            startScale = parseFloat(imgEl.getAttribute('data-scale') || '1.0');

            document.addEventListener('mousemove', onDragResize);
            document.addEventListener('mouseup', stopDragResize);
        }}

        function onDragResize(e) {{
            if (!isDraggingResize || !dragTargetImg) return;
            let diffX = e.clientX - startX;
            let scaleDelta = diffX / 150;
            let newScale = Math.max(0.3, Math.min(3.0, startScale + scaleDelta));
            newScale = Math.round(newScale * 20) / 20;
            dragTargetImg.setAttribute('data-scale', newScale);
            dragTargetImg.style.transform = 'scale(' + newScale + ')';
        }}

        function stopDragResize() {{
            if (isDraggingResize) {{
                isDraggingResize = false;
                document.removeEventListener('mousemove', onDragResize);
                document.removeEventListener('mouseup', stopDragResize);
                autoSaveToStorage();
                showToast('🔍 Boyut güncellendi');
            }}
        }}

        // SPECS GRID EDITING (Buraları da)
        const AVAILABLE_ICONS = [
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
        ];

        function cycleSpecIcon(iconEl) {{
            takeSnapshot();
            let curIndex = parseInt(iconEl.getAttribute('data-icon-idx') || '0');
            curIndex = (curIndex + 1) % AVAILABLE_ICONS.length;
            iconEl.setAttribute('data-icon-idx', curIndex);
            iconEl.innerHTML = AVAILABLE_ICONS[curIndex];
            showToast('🔄 İkon değiştirildi');
        }}

        function deleteSpecItem(itemEl) {{
            if (!itemEl) return;
            takeSnapshot();
            itemEl.remove();
            showToast('🗑️ Özellik silindi');
        }}

        function addNewSpecItem(gridEl) {{
            if (!gridEl) return;
            takeSnapshot();
            const newItem = document.createElement('div');
            newItem.className = 'spec-item editable-spec-item';
            newItem.title = 'Tıkla ve düzenle';
            newItem.innerHTML = `
                <div class="spec-icon" onclick="cycleSpecIcon(this)" title="İkon Değiştir">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
                </div>
                <div class="spec-texts">
                    <span class="spec-val" contenteditable="true" spellcheck="false">Özellik Başlığı</span>
                    <span class="spec-lbl" contenteditable="true" spellcheck="false">Açıklama / Detay</span>
                </div>
                <button class="spec-del-btn" onclick="deleteSpecItem(this.closest('.spec-item'))" title="Bu Özelliği Sil">×</button>
            `;
            const addBtn = gridEl.querySelector('.btn-add-spec');
            if (addBtn) {{
                gridEl.insertBefore(newItem, addBtn);
            }} else {{
                gridEl.appendChild(newItem);
            }}
            bindStudioEvents();
            showToast('➕ Yeni özellik eklendi!');
        }}

        // CAPS & COLOR SECTION EDITING (Altındaki yerler de)
        function editColorDot(dotEl) {{
            activeColorDot = dotEl;
            const picker = document.getElementById('universalColorPicker');
            picker.click();
        }}

        function onColorPicked(e) {{
            if (activeColorDot) {{
                takeSnapshot();
                activeColorDot.style.background = e.target.value;
                activeColorDot.title = 'Özel Renk (' + e.target.value + ')';
                showToast('🎨 Kapak rengi güncellendi: ' + e.target.value);
            }}
        }}

        function addColorDot(containerEl) {{
            if (!containerEl) return;
            takeSnapshot();
            const dot = document.createElement('span');
            dot.className = 'color-dot';
            dot.style.background = '#91CE17';
            dot.title = 'Özel Renk (Değiştirmek için tıkla)';
            dot.onclick = () => editColorDot(dot);
            dot.oncontextmenu = (e) => deleteColorDot(e, dot);
            containerEl.appendChild(dot);
            showToast('🎨 Yeni kapak rengi eklendi!');
        }}

        function deleteColorDot(e, dotEl) {{
            e.preventDefault();
            takeSnapshot();
            dotEl.remove();
            showToast('🗑️ Kapak rengi silindi');
        }}

        function deleteCapBadge(badgeEl) {{
            if (!badgeEl) return;
            takeSnapshot();
            badgeEl.remove();
            showToast('🗑️ Kapak modeli silindi');
        }}

        function duplicateCapBadge(badgeEl) {{
            if (!badgeEl) return;
            takeSnapshot();
            const clone = badgeEl.cloneNode(true);
            badgeEl.parentNode.insertBefore(clone, badgeEl.nextSibling);
            bindStudioEvents();
            showToast('📋 Kapak modeli çoğaltıldı');
        }}

        function addNewCapBadge(flexEl) {{
            if (!flexEl) return;
            takeSnapshot();
            const newBadge = document.createElement('div');
            newBadge.className = 'ilpen-cap-badge';
            newBadge.innerHTML = `
                <div class="cap-badge-actions">
                    <button class="cap-act-btn clone" onclick="duplicateCapBadge(this.closest('.ilpen-cap-badge'))" title="Kapağı Çoğalt">📋</button>
                    <button class="cap-act-btn del" onclick="deleteCapBadge(this.closest('.ilpen-cap-badge'))" title="Kapağı Sil">×</button>
                </div>
                <div class="cap-thumb-box editable-img-box" data-label="Yeni Kapak">
                    <img src="assets/cap_crops/cap_30P01F.png" alt="Yeni Kapak" class="studio-img resizable-img" data-scale="1.0">
                    <div class="img-quick-tools">
                        <button class="img-tool-btn" onclick="openSidebarForImg(this.closest('.editable-img-box').querySelector('img'))">🔄</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), -0.1)">🔍 -</button>
                        <button class="img-tool-btn scale-btn" onclick="adjustImgScale(this.closest('.editable-img-box').querySelector('img'), 0.1)">🔍 +</button>
                    </div>
                </div>
                <div class="cap-info">
                    <div class="cap-header-line">
                        <span class="cap-code" contenteditable="true" spellcheck="false">KOD01</span>
                        <span class="cap-title" contenteditable="true" spellcheck="false">KAPAK ADI</span>
                    </div>
                    <span class="cap-sub" contenteditable="true" spellcheck="false">Kullanım Türü</span>
                    <div class="cap-colors-row">
                        <span class="colors-label">Renkler:</span>
                        <div class="colors-dots-container">
                            <span class="color-dot" style="background:#1E293B;" onclick="editColorDot(this)" oncontextmenu="deleteColorDot(event, this)"></span>
                            <span class="color-dot" style="background:#FFFFFF;border:1px solid #CBD5E1;" onclick="editColorDot(this)" oncontextmenu="deleteColorDot(event, this)"></span>
                        </div>
                        <button class="btn-add-color-dot" onclick="addColorDot(this.previousElementSibling)">+</button>
                    </div>
                </div>
            `;
            flexEl.appendChild(newBadge);
            bindStudioEvents();
            showToast('➕ Yeni kapak modeli eklendi!');
        }}

        // Apply chosen asset to currently active image
        function applyAsset(path) {{
            if (!activeTargetImg) {{
                showToast('⚠️ Önce katalogdan değiştirmek istediğiniz bir fotoğrafa veya logoya dokunun!');
                return;
            }}
            takeSnapshot();
            activeTargetImg.src = path;
            activeTargetImg.style.transition = 'transform 0.2s ease';
            activeTargetImg.style.transform = 'scale(1.08)';
            setTimeout(() => {{
                if (activeTargetImg) activeTargetImg.style.transform = 'scale(' + (activeTargetImg.getAttribute('data-scale') || '1.0') + ')';
            }}, 200);
            showToast('✅ Görsel güncellendi: ' + path.split('/').pop());

            // On mobile devices, automatically collapse bottom sheet drawer so user can view the result
            if (window.innerWidth <= 900) {{
                setTimeout(() => {{
                    closeSidebar();
                }}, 350);
            }}
        }}

        // Render Sidebar Gallery
        function renderSidebarGallery(category, query = '') {{
            const container = document.getElementById('sidebarGallery');
            container.innerHTML = '';

            if (category === 'upload') {{
                const dropzone = document.createElement('div');
                dropzone.className = 'upload-dropzone';
                dropzone.innerHTML = `
                    <div style="font-size: 32px; margin-bottom: 8px;">📤</div>
                    <div style="font-weight: 800; font-size: 14px; color: var(--pk-lime);">Bilgisayardan Fotoğraf Yükle</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">PNG, JPG, WEBP dosyalarınızı buraya sürükleyin veya tıklayın</div>
                    <button style="margin-top: 12px; padding: 6px 14px; background: var(--pk-lime); color: var(--pk-navy-deep); border: none; border-radius: 6px; font-weight: 800; font-size: 12px; cursor: pointer;">Dosya Seç</button>
                `;
                dropzone.onclick = () => document.getElementById('customImgFileInput').click();

                dropzone.ondragover = (e) => {{ e.preventDefault(); dropzone.style.background = 'rgba(145,206,23,0.2)'; }};
                dropzone.ondragleave = () => {{ dropzone.style.background = 'rgba(145,206,23,0.05)'; }};
                dropzone.ondrop = (e) => {{
                    e.preventDefault();
                    dropzone.style.background = 'rgba(145,206,23,0.05)';
                    if (e.dataTransfer.files && e.dataTransfer.files[0]) {{
                        processCustomFile(e.dataTransfer.files[0]);
                    }}
                }};
                container.appendChild(dropzone);

                const userItems = window.STUDIO_ASSETS['kullanici'] || [];
                userItems.forEach(item => {{
                    renderGalleryCard(item, container);
                }});
                return;
            }}

            const items = window.STUDIO_ASSETS[category] || [];
            const filtered = items.filter(it => it.name.toLowerCase().includes(query.toLowerCase()) || it.path.toLowerCase().includes(query.toLowerCase()));

            if (filtered.length === 0) {{
                container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: #94A3B8; padding: 30px 10px; font-size: 12px;">Eşleşen fotoğraf bulunamadı.</div>';
                return;
            }}

            filtered.forEach(it => renderGalleryCard(it, container));
        }}

        function renderGalleryCard(item, container) {{
            const card = document.createElement('div');
            card.className = 'gallery-card';
            card.setAttribute('draggable', 'true');
            card.innerHTML = `
                <div class="gallery-thumb-wrap">
                    <img class="gallery-thumb-img" src="${{item.path}}" alt="${{item.name}}" loading="lazy">
                </div>
                <div class="gallery-name" title="${{item.name}}">${{item.name}}</div>
                <button class="gallery-btn-use">Görseli Kullan</button>
            `;
            card.onclick = () => applyAsset(item.path);

            card.ondragstart = (e) => {{
                e.dataTransfer.setData('text/plain', item.path);
            }};

            container.appendChild(card);
        }}

        function switchSidebarTab(tabKey, btnEl) {{
            activeTab = tabKey;
            document.querySelectorAll('.sidebar-tab-btn').forEach(b => b.classList.remove('active'));
            if (btnEl) btnEl.classList.add('active');
            const query = document.getElementById('sidebarSearchInput').value;
            renderSidebarGallery(activeTab, query);
        }}

        function filterSidebarGallery(query) {{
            renderSidebarGallery(activeTab, query);
        }}

        // Custom File Upload
        function handleCustomFileUpload(e) {{
            if (e.target.files && e.target.files[0]) {{
                processCustomFile(e.target.files[0]);
            }}
        }}

        function processCustomFile(file) {{
            const reader = new FileReader();
            reader.onload = function(evt) {{
                const dataUrl = evt.target.result;
                const fileName = file.name;
                
                if (!window.STUDIO_ASSETS['kullanici']) window.STUDIO_ASSETS['kullanici'] = [];
                window.STUDIO_ASSETS['kullanici'].unshift({{
                    name: fileName,
                    path: dataUrl,
                    category: 'kullanici'
                }});

                // Also try server upload if running locally
                fetch('/api/upload', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ filename: fileName, data: dataUrl }})
                }}).catch(() => {{}});

                if (activeTargetImg) {{
                    applyAsset(dataUrl);
                }}

                switchSidebarTab('upload');
                showToast('📤 Fotoğraf yüklendi: ' + fileName);
            }};
            reader.readAsDataURL(file);
        }}

        // PRODUCT ROW ACTIONS
        function deleteRow(rowEl) {{
            if (!rowEl) return;
            takeSnapshot();
            const badge = rowEl.querySelector('.ilpen-code-badge');
            const code = badge ? badge.textContent.trim() : 'Ürün';
            rowEl.style.transition = 'all 0.3s ease';
            rowEl.style.opacity = '0';
            rowEl.style.transform = 'scale(0.95)';
            setTimeout(() => {{
                rowEl.remove();
                showToast('🗑️ <b>' + code + '</b> ürünü silindi! [Geri Al: Ctrl+Z]');
            }}, 250);
        }}

        function duplicateRow(rowEl) {{
            if (!rowEl) return;
            takeSnapshot();
            const clone = rowEl.cloneNode(true);
            clone.id = 'prod-clone-' + Date.now();
            rowEl.parentNode.insertBefore(clone, rowEl.nextSibling);
            bindStudioEvents();
            showToast('📋 Ürün kopyalandı ve eklendi!');
        }}

        function moveRowUp(rowEl) {{
            if (!rowEl || !rowEl.previousElementSibling) return;
            takeSnapshot();
            rowEl.parentNode.insertBefore(rowEl, rowEl.previousElementSibling);
            showToast('▲ Ürün yukarı taşındı');
        }}

        function moveRowDown(rowEl) {{
            if (!rowEl || !rowEl.nextElementSibling) return;
            takeSnapshot();
            rowEl.parentNode.insertBefore(rowEl.nextElementSibling, rowEl);
            showToast('▼ Ürün aşağı taşındı');
        }}

        // PAGE ACTIONS
        function deletePage(pageEl) {{
            if (!pageEl) return;
            if (document.querySelectorAll('.a4-page').length <= 1) {{
                alert('Katalogdaki tek sayfayı silemezsiniz!');
                return;
            }}
            if (confirm('Bu sayfayı katalogdan tamamen silmek istediğinize emin misiniz?')) {{
                takeSnapshot();
                pageEl.style.transition = 'all 0.3s ease';
                pageEl.style.opacity = '0';
                pageEl.style.transform = 'scale(0.95)';
                setTimeout(() => {{
                    pageEl.remove();
                    showToast('🗑️ Sayfa silindi! [Geri Al: Ctrl+Z]');
                }}, 250);
            }}
        }}

        function duplicatePage(pageEl) {{
            if (!pageEl) return;
            takeSnapshot();
            const clone = pageEl.cloneNode(true);
            clone.id = 'page-clone-' + Date.now();
            pageEl.parentNode.insertBefore(clone, pageEl.nextSibling);
            bindStudioEvents();
            showToast('📑 Sayfa kopyalandı!');
        }}

        function addNewProductRowToPage(pageEl) {{
            if (!pageEl) return;
            const body = pageEl.querySelector('.page-body');
            if (!body) return;
            takeSnapshot();
            
            const firstRow = document.querySelector('.ilpen-product-row');
            if (firstRow) {{
                const newRow = firstRow.cloneNode(true);
                newRow.id = 'prod-new-' + Date.now();
                const codeBadge = newRow.querySelector('.ilpen-code-badge');
                if (codeBadge) codeBadge.textContent = 'YENI01';
                const title = newRow.querySelector('.ilpen-prod-title');
                if (title) title.textContent = 'YENİ ÜRÜN BAŞLIĞI';
                body.appendChild(newRow);
                bindStudioEvents();
                showToast('➕ Sayfaya yeni ürün kartı eklendi!');
            }}
        }}

        // BIND EVENT LISTENERS TO CANVAS
        function bindStudioEvents() {{
            document.querySelectorAll('.editable-img-box img, .ilpen-bottle-img, .header-logo, .divider-logo').forEach(img => {{
                img.onclick = (e) => {{
                    e.stopPropagation();
                    setActiveImg(img);
                }};

                // Wheel zooming with Alt or Ctrl
                img.onwheel = (e) => {{
                    if (e.altKey || e.ctrlKey) {{
                        e.preventDefault();
                        adjustImgScale(img, e.deltaY < 0 ? 0.05 : -0.05);
                    }}
                }};
            }});

            document.querySelectorAll('.editable-img-box, .ilpen-bottle-podium, .ilpen-bottle-podium-mini').forEach(box => {{
                box.ondragover = (e) => {{
                    e.preventDefault();
                    box.style.outline = '3px dashed #91CE17';
                }};
                box.ondragleave = () => {{
                    box.style.outline = '';
                }};
                box.ondrop = (e) => {{
                    e.preventDefault();
                    box.style.outline = '';
                    const assetPath = e.dataTransfer.getData('text/plain');
                    const targetImg = box.querySelector('img');
                    if (targetImg) {{
                        takeSnapshot();
                        if (assetPath) {{
                            targetImg.src = assetPath;
                            showToast('✅ Fotoğraf bırakıldı ve güncellendi!');
                        }} else if (e.dataTransfer.files && e.dataTransfer.files[0]) {{
                            processCustomFile(e.dataTransfer.files[0]);
                            setActiveImg(targetImg);
                        }}
                    }}
                }};
            }});

            // Listen to contenteditable changes to auto-save
            document.querySelectorAll('[contenteditable="true"]').forEach(el => {{
                el.oninput = () => autoSaveToStorage();
            }});
        }}

        // SAVE CATALOG TO DISK (Works on both Local Server and Vercel)
        async function saveCatalogToDisk() {{
            if (activeTargetImg) deselectActiveImg();
            autoSaveToStorage();

            const cloneDoc = document.documentElement.cloneNode(true);
            const cleanHtml = "<!DOCTYPE html>\\n" + cloneDoc.outerHTML;

            try {{
                const res = await fetch('/api/save', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ html: cleanHtml, export_pdf: true }})
                }});
                const data = await res.json();
                if (data.success) {{
                    showToast('🎉 BAŞARILI! Katalog kaydedildi ve PDF güncellendi!');
                    return;
                }}
            }} catch (err) {{}}

            // If on Vercel / static hosting, notify that local browser storage is saved
            showToast('💾 Tüm değişiklikler tarayıcınıza kaydedildi!');
        }}

        function downloadCurrentCatalogHtml() {{
            if (activeTargetImg) deselectActiveImg();
            const cloneDoc = document.documentElement.cloneNode(true);
            const cleanHtml = "<!DOCTYPE html>\\n" + cloneDoc.outerHTML;

            const blob = new Blob([cleanHtml], {{ type: 'text/html;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'katalog_duzenlenmis.html';
            a.click();
            URL.revokeObjectURL(url);
            showToast('📥 Düzenlenmiş katalog HTML olarak indirildi!');
        }}

        function resetCatalogToInitial() {{
            if (confirm('Katalogda yaptığınız tüm değişiklikleri sıfırlayıp orijinal haline döndürmek istiyor musunuz?')) {{
                localStorage.removeItem(STORAGE_KEY);
                location.reload();
            }}
        }}

        // PRINT / PDF EXPORT
        function triggerPrint() {{
            const prevMode = isPreviewMode;
            setStudioMode('preview');
            setTimeout(() => {{
                window.print();
                if (!prevMode) setStudioMode('edit');
            }}, 350);
        }}

        // KEYBOARD SHORTCUTS
        window.addEventListener('keydown', (e) => {{
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') {{
                e.preventDefault();
                studioUndo();
            }} else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y') {{
                e.preventDefault();
                studioRedo();
            }} else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') {{
                e.preventDefault();
                saveCatalogToDisk();
            }} else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'p') {{
                e.preventDefault();
                triggerPrint();
            }} else if (e.key === 'Escape') {{
                deselectActiveImg();
            }}
        }});

        // INIT ON LOAD (Check LocalStorage restoration)
        window.addEventListener('DOMContentLoaded', () => {{
            // Mobile initial state: start collapsed on phone, open on desktop
            if (window.innerWidth <= 900) {{
                closeSidebar();
            }} else {{
                openSidebar();
            }}

            const savedHtml = localStorage.getItem(STORAGE_KEY);
            if (savedHtml) {{
                const canvas = document.getElementById('catalogContainer');
                if (canvas && savedHtml.trim().length > 100) {{
                    canvas.innerHTML = savedHtml;
                    showToast('📂 Kaydedilmiş düzenlemeleriniz tarayıcıdan yüklendi!');
                }}
            }}

            renderSidebarGallery(activeTab);
            bindStudioEvents();
            takeSnapshot();
        }});
    </script>

    <!-- STICKY MOBILE BOTTOM NAVIGATION BAR -->
    <nav class="mobile-bottom-bar" id="mobileBottomBar">
        <button class="mob-nav-btn" onclick="openSidebar()" title="Fotoğraf Seçici">
            <span class="mob-nav-icon">📸</span>
            <span class="mob-nav-lbl">Fotoğraf</span>
        </button>
        <button class="mob-nav-btn" onclick="quickAddProductToCatalog()" title="Yeni Ürün Ekle">
            <span class="mob-nav-icon">➕</span>
            <span class="mob-nav-lbl">Ürün Ekle</span>
        </button>
        <button class="mob-nav-btn primary" onclick="saveCatalogToDisk()" title="Kaydet">
            <span class="mob-nav-icon">💾</span>
            <span class="mob-nav-lbl">Kaydet</span>
        </button>
        <button class="mob-nav-btn" onclick="triggerPrint()" title="PDF İndir">
            <span class="mob-nav-icon">🖨️</span>
            <span class="mob-nav-lbl">PDF (A4)</span>
        </button>
        <button class="mob-nav-btn" onclick="studioUndo()" title="Geri Al">
            <span class="mob-nav-icon">↩️</span>
            <span class="mob-nav-lbl">Geri Al</span>
        </button>
    </nav>
</body>
</html>
"""

# Save updated katalog.html
html_path = os.path.join(base_dir, "katalog.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

# Also write index.html for root Vercel deployment!
index_path = os.path.join(base_dir, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Catalog Studio successfully generated with {cur_page} pages!")
print(f"Saved to: {html_path} and {index_path}")
