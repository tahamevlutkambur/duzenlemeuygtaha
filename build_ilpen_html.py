# build_ilpen_html.py - Redirects to full catalog studio builder
import os
import subprocess
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
studio_script = os.path.join(base_dir, "build_catalog_studio.py")

if __name__ == "__main__":
    result = subprocess.run([sys.executable, studio_script], cwd=base_dir)
    sys.exit(result.returncode)
