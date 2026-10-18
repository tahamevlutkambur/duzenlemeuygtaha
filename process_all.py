import os
import sys
import time
from PIL import Image
from rembg import remove, new_session

def main():
    src_dir = r"C:\Users\Taha\Pictures\kolonya\drive-download-20261018T133157Z-1-001"
    base_out = r"C:\Users\Taha\Pictures\kolonya"
    
    png_dir = os.path.join(base_out, "seffaf_png")
    white_dir = os.path.join(base_out, "beyaz_arka_plan")
    
    os.makedirs(png_dir, exist_ok=True)
    os.makedirs(white_dir, exist_ok=True)
    
    # Get all images
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    files = [f for f in os.listdir(src_dir) if os.path.splitext(f)[1].lower() in valid_exts]
    files.sort()
    
    total = len(files)
    print(f"Toplam {total} adet fotoğraf bulundu.")
    print(f"Hedef klasörler:")
    print(f"  1. Şeffaf PNG: {png_dir}")
    print(f"  2. Beyaz Arka Plan: {white_dir}")
    
    # Initialize session
    print("AI Modeli (isnet-general-use) yükleniyor...")
    t_start_model = time.time()
    session = new_session("isnet-general-use")
    print(f"Model hazır ({time.time() - t_start_model:.2f}s). İşlem başlıyor!\n")
    
    total_start = time.time()
    success_count = 0
    skipped_count = 0
    error_count = 0
    
    for idx, fname in enumerate(files, 1):
        name_without_ext = os.path.splitext(fname)[0]
        png_path = os.path.join(png_dir, f"{name_without_ext}.png")
        white_path = os.path.join(white_dir, f"{name_without_ext}.jpg")
        
        # Check if already processed
        if os.path.exists(png_path) and os.path.exists(white_path) and os.path.getsize(png_path) > 1000:
            skipped_count += 1
            print(f"[{idx}/{total}] {fname} -> Zaten işlenmiş, atlandı.")
            continue
            
        src_path = os.path.join(src_dir, fname)
        t0 = time.time()
        
        try:
            with Image.open(src_path) as img:
                # Remove background -> returns RGBA
                rgba_img = remove(img, session=session)
                
                # Save transparent PNG
                rgba_img.save(png_path, format="PNG")
                
                # Create pure white background JPG
                white_bg = Image.new("RGB", rgba_img.size, (255, 255, 255))
                # Use alpha channel as mask
                alpha = rgba_img.split()[3]
                white_bg.paste(rgba_img, mask=alpha)
                white_bg.save(white_path, format="JPEG", quality=95)
                
            elapsed = time.time() - t0
            success_count += 1
            avg_time = (time.time() - total_start) / (success_count)
            remaining_sec = avg_time * (total - idx)
            rem_min = int(remaining_sec // 60)
            rem_sec = int(remaining_sec % 60)
            
            print(f"[{idx}/{total}] {fname} tamamlandı ({elapsed:.2f}s) | Kalan tahmini süre: {rem_min}dk {rem_sec}sn")
            sys.stdout.flush()
            
        except Exception as e:
            error_count += 1
            print(f"[{idx}/{total}] HATA: {fname} -> {e}")
            sys.stdout.flush()
            
    total_elapsed = time.time() - total_start
    print("\n" + "="*50)
    print(f"İŞLEM TAMAMLANDI!")
    print(f"Toplam Süre: {total_elapsed/60:.2f} dakika")
    print(f"Başarılı: {success_count}")
    print(f"Atlanan (önceden hazır): {skipped_count}")
    print(f"Hata: {error_count}")
    print(f"Şeffaf PNG klasörü: {png_dir}")
    print(f"Beyaz Arka Plan klasörü: {white_dir}")
    print("="*50)

if __name__ == "__main__":
    main()
