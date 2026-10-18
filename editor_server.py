import os
import sys
import json
import base64
import subprocess
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8080
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE_PATH):
    alt_edge = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(alt_edge):
        EDGE_PATH = alt_edge

def get_manifest():
    manifest_path = os.path.join(BASE_DIR, "assets_manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Generate on the fly
    manifest = {
        'urunler': [],
        'mockups': [],
        'assets': [],
        'seffaf_png': [],
        'beyaz_arka_plan': [],
        'kullanici': []
    }
    folders = [
        ('ürünler', 'urunler'),
        ('mockups', 'mockups'),
        ('assets', 'assets'),
        ('seffaf_png', 'seffaf_png'),
        ('beyaz_arka_plan', 'beyaz_arka_plan'),
        ('assets/kullanici', 'kullanici')
    ]
    for folder, key in folders:
        p = os.path.join(BASE_DIR, folder)
        if os.path.exists(p):
            for fname in sorted(os.listdir(p)):
                if fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.svg')):
                    manifest[key].append({
                        'name': fname,
                        'path': f"{folder}/{fname}",
                        'category': key
                    })
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest

class CatalogEditorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path

        if path == "/" or path == "/editor":
            self.send_response(302)
            self.send_header("Location", "/katalog.html")
            self.end_headers()
            return

        if path == "/api/assets":
            manifest = get_manifest()
            data = json.dumps(manifest, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
            return

        return super().do_GET()

    def do_POST(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        if path == "/api/save":
            try:
                payload = json.loads(post_data.decode("utf-8"))
                html_content = payload.get("html", "")
                save_pdf = payload.get("export_pdf", False)

                if html_content:
                    out_html = os.path.join(BASE_DIR, "katalog.html")
                    with open(out_html, "w", encoding="utf-8") as f:
                        f.write(html_content)

                    pdf_status = "not_requested"
                    if save_pdf and os.path.exists(EDGE_PATH):
                        pdf_path = os.path.join(BASE_DIR, "katalog.pdf")
                        html_url = f"file:///{out_html.replace(os.sep, '/')}"
                        cmd = [
                            EDGE_PATH,
                            "--headless",
                            "--disable-gpu",
                            "--no-pdf-header-footer",
                            "--run-all-compositor-stages-before-draw",
                            f"--print-to-pdf={pdf_path}",
                            html_url
                        ]
                        subprocess.run(cmd, check=True)
                        pdf_status = "success"

                    res = {
                        "success": True,
                        "message": "Katalog HTML ve PDF başarıyla güncellendi!",
                        "pdf_status": pdf_status
                    }
                else:
                    res = {"success": False, "error": "HTML içeriği boş!"}

            except Exception as e:
                res = {"success": False, "error": str(e)}

            data = json.dumps(res, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
            return

        if path == "/api/export_pdf":
            try:
                out_html = os.path.join(BASE_DIR, "katalog.html")
                pdf_path = os.path.join(BASE_DIR, "katalog.pdf")
                html_url = f"file:///{out_html.replace(os.sep, '/')}"

                if os.path.exists(EDGE_PATH):
                    cmd = [
                        EDGE_PATH,
                        "--headless",
                        "--disable-gpu",
                        "--no-pdf-header-footer",
                        "--run-all-compositor-stages-before-draw",
                        f"--print-to-pdf={pdf_path}",
                        html_url
                    ]
                    subprocess.run(cmd, check=True)
                    res = {"success": True, "message": "katalog.pdf başarıyla derlendi ve kaydedildi!"}
                else:
                    res = {"success": False, "error": "Microsoft Edge bulunamadı!"}
            except Exception as e:
                res = {"success": False, "error": str(e)}

            data = json.dumps(res, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
            return

        if path == "/api/upload":
            try:
                payload = json.loads(post_data.decode("utf-8"))
                filename = payload.get("filename", "upload.png")
                b64data = payload.get("data", "")
                if "," in b64data:
                    b64data = b64data.split(",", 1)[1]

                img_bytes = base64.b64decode(b64data)
                clean_name = os.path.basename(filename)
                target_path = os.path.join(BASE_DIR, "assets", "kullanici", clean_name)
                with open(target_path, "wb") as f:
                    f.write(img_bytes)

                # Re-generate manifest
                manifest_path = os.path.join(BASE_DIR, "assets_manifest.json")
                if os.path.exists(manifest_path):
                    os.remove(manifest_path)
                get_manifest()

                rel_path = f"assets/kullanici/{clean_name}"
                res = {"success": True, "path": rel_path, "name": clean_name}
            except Exception as e:
                res = {"success": False, "error": str(e)}

            data = json.dumps(res, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
            return

        self.send_response(404)
        self.end_headers()

def run_server():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, CatalogEditorHandler)
    print(f"=====================================================")
    print(f" PROMKOL KATALOG EDİTÖRÜ SUNUCUSU BAŞLATILDI!")
    print(f" URL: http://localhost:{PORT}/katalog.html")
    print(f"=====================================================")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Sunucu durduruluyor...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
