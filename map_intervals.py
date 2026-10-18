import glob
import os
import re

files = sorted([os.path.basename(f) for f in glob.glob('drive-download-20261018T133157Z-1-001/*.JPG')])

note_crops = sorted(os.listdir('assets/note_crops'))
note_files = [f.replace('crop_', '') for f in note_crops]

print("Notes found in assets/note_crops:", len(note_files))

# Let's inspect the intervals between note cards
intervals = []
start_idx = 0
for nf in note_files:
    if nf in files:
        end_idx = files.index(nf)
        prod_photos = files[start_idx:end_idx]
        intervals.append({
            'note_file': nf,
            'photos': prod_photos
        })
        start_idx = end_idx + 1

# Any remaining after last note
if start_idx < len(files):
    intervals.append({
        'note_file': 'NONE (END)',
        'photos': files[start_idx:]
    })

for i, inv in enumerate(intervals):
    print(f"[{i+1}] Note: {inv['note_file']} -> {len(inv['photos'])} photos: {inv['photos']}")
