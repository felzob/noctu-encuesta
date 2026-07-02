from PIL import Image
import os

# Open the catalog image
img = Image.open(r"Tipos de pijama/Catalogo.jpg")
w, h = img.size
print(f"Image size: {w}x{h}")

# Grid: 6 columns x 3 rows
cols = 6
rows = 3

# Margins
top_margin = int(h * 0.06)  # main title area
left_margin = int(w * 0.01)
right_margin = int(w * 0.01)

usable_w = w - left_margin - right_margin
usable_h = h - top_margin

cell_w = usable_w // cols
cell_h = usable_h // rows

# Within each cell, the title takes ~12% top and description ~15% bottom
# We want only the image (person) in the middle
cell_top_trim = 0.14   # skip title bar at top of cell
cell_bottom_trim = 0.18  # skip description at bottom of cell

# Positions (row, col) - 0-indexed
selections = {
    "01-clasico": (0, 0),
    "02-moderno": (0, 1),
    "03-resort": (0, 2),
    "05-camiseta-pantalon": (0, 4),
    "06-henley": (0, 5),
    "07-cuello-mao": (1, 0),
    "12-oversized": (1, 5),
    "13-short-set": (2, 0),
}

output_dir = "Tipos de pijama"
os.makedirs(output_dir, exist_ok=True)

# Fixed output size for all thumbnails (square-ish, uniform)
THUMB_W = 200
THUMB_H = 240

for name, (row, col) in selections.items():
    x1 = left_margin + col * cell_w
    y1 = top_margin + row * cell_h
    x2 = x1 + cell_w
    y2 = y1 + cell_h
    
    # Trim title and description from cell
    trim_top = int(cell_h * cell_top_trim)
    trim_bottom = int(cell_h * cell_bottom_trim)
    
    # Also trim a bit of left/right padding within cell
    trim_side = int(cell_w * 0.05)
    
    crop_x1 = x1 + trim_side
    crop_y1 = y1 + trim_top
    crop_x2 = x2 - trim_side
    crop_y2 = y2 - trim_bottom
    
    cell = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    
    # Resize to uniform size
    cell = cell.resize((THUMB_W, THUMB_H), Image.LANCZOS)
    
    output_path = os.path.join(output_dir, f"{name}.jpg")
    cell.save(output_path, "JPEG", quality=88)
    print(f"Saved: {output_path} ({THUMB_W}x{THUMB_H})")

print("\nDone! All thumbnails cropped uniformly.")
