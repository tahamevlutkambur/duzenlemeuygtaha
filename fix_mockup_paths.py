import re

with open('make_ilpen_catalog.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace mockups/mock_{code}.png with assets/cropped_mockups/crop_{code}_mock.png
new_text = re.sub(r'"mockup":\s*"mockups/mock_([^"]+)\.png"', r'"mockup": "assets/cropped_mockups/crop_\1_mock.png"', text)

with open('make_ilpen_catalog.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Updated make_ilpen_catalog.py with cropped mockups!')
