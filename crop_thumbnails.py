from PIL import Image
import os

# Open the catalog image
img = Image.open(r"Tipos de pijama/Catalogo.jpg")
w, h = img.size
print(f"Image size: {w}x{h}")

# The grid is 6 columns x 3 rows
# There's a title bar at top and some padding
# Let's figure out the grid boundaries

# Based on typical layout: title takes ~8% top, then 3 equal rows
# Each cell has the image + text below

cols = 6
rows = 3

# Approximate margins (from visual inspection of the catalog)
top_margin = int(h * 0.06)  # title area
left_margin = int(w * 0.01)
right_margin = int(w * 0.01)
# Bottom has the "tejidos disponibles" section in row 3, cols 5-6

usable_w = w - left_margin - right_margin
usable_h = h - top_margin

cell_w = usable_w // cols
cell_h = usable_h // rows

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

for name, (row, col) in selections.items():
    x1 = left_margin + col * cell_w
    y1 = top_margin + row * cell_h
    x2 = x1 + cell_w
    y2 = y1 + cell_h
    
    # Crop the cell
    cell = img.crop((x1, y1, x2, y2))
    
    # Save as thumbnail (resize to ~300px wide for web)
    thumb_w = 300
    ratio = thumb_w / cell.width
    thumb_h = int(cell.height * ratio)
    cell = cell.resize((thumb_w, thumb_h), Image.LANCZOS)
    
    output_path = os.path.join(output_dir, f"{name}.jpg")
    cell.save(output_path, "JPEG", quality=85)
    print(f"Saved: {output_path} ({thumb_w}x{thumb_h})")

print("\nDone! All thumbnails cropped.")
