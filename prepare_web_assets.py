import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

base_dir = r"C:\Users\Taha\Pictures\kolonya"

def process_img(args):
    src, dst, is_png = args
    if os.path.exists(dst):
        return
    try:
        im = Image.open(src)
        im.thumbnail((800, 800), Image.Resampling.LANCZOS)
        if is_png:
            im.save(dst, "PNG", optimize=True)
        else:
            im.convert("RGB").save(dst, "JPEG", quality=85, optimize=True)
    except Exception as e:
        print(f"Error {src}: {e}")

def prepare():
    os.makedirs(os.path.join(base_dir, "assets", "seffaf_web"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "assets", "beyaz_web"), exist_ok=True)

    tasks = []
    
    # Seffaf PNG
    seffaf_dir = os.path.join(base_dir, "seffaf_png")
    if os.path.exists(seffaf_dir):
        for f in os.listdir(seffaf_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                src = os.path.join(seffaf_dir, f)
                dst = os.path.join(base_dir, "assets", "seffaf_web", f"{os.path.splitext(f)[0]}.png")
                tasks.append((src, dst, True))

    # Beyaz Arka Plan
    beyaz_dir = os.path.join(base_dir, "beyaz_arka_plan")
    if os.path.exists(beyaz_dir):
        for f in os.listdir(beyaz_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                src = os.path.join(beyaz_dir, f)
                dst = os.path.join(base_dir, "assets", "beyaz_web", f"{os.path.splitext(f)[0]}.jpg")
                tasks.append((src, dst, False))

    print(f"Processing {len(tasks)} images with ThreadPoolExecutor...")
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(process_img, tasks))
    print("All web assets prepared successfully!")

if __name__ == "__main__":
    prepare()
