import os
import pypdfium2 as pdfium

base_dir = r"C:\Users\Taha\Pictures\kolonya"
pdf_path = os.path.join(base_dir, "katalog_teknik_ozellikler.pdf")
out_dir = os.path.join(base_dir, "assets", "tech_previews")
os.makedirs(out_dir, exist_ok=True)

pdf = pdfium.PdfDocument(pdf_path)
pages_to_render = [1, 2, 3, 8, 12, 15, 19]

for pno in pages_to_render:
    page = pdf[pno - 1]
    image = page.render(scale=1.5).to_pil()
    out_img = os.path.join(out_dir, f"page_{pno:02d}.jpg")
    image.save(out_img, "JPEG", quality=90)
    print(f"Rendered page {pno:02d} -> {out_img}")
