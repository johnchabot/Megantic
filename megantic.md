# Megantic Sprite Generator

A Python tool that generates a **vector sprite sheet** from a segment‑based font blueprint. 
Instead of relying on traditional bitmap fonts (like CP437), this system uses a set of 45 geometric "shards" that combine to form each glyph. 
The output is a clean, self‑contained SVG optimized for display on modern screens with a distinctive glowing aesthetic.

---

## 🧱 Overview

The Megantic font system is built around a modular design:

- **45 Core Segments** – defined as SVG primitives (polygons, paths, rectangles) stored in `SEGMENT_GEOMETRY`.
- **Glyph Recipes** – each character is defined as a list of segment IDs (its “recipe”) in `GLYPH_RECIPE_BOOK`.
- **Harvester (optional)** – `HarvesterGenerator.py` compiles the recipes into a 45‑bit JSON lookup table (bitmask / hex) for hardware‑friendly addressing.
- **Sprite Generator** – `megantic-generator.py` reads the geometry and recipes to produce a complete SVG sprite sheet with minimal, clean metadata.

This approach gives you complete control over the shape and style of every character while keeping the font data extremely compact.

---

## 📁 Project Structure

```
├── SpriteGenerator.py          # Core definitions (SEGMENT_GEOMETRY, GLYPH_RECIPE_BOOK)
├── HarvesterGenerator.py       # (Optional) Creates JSON bitmask LUT
├── megantic-generator.py       # Main script that outputs the sprite sheet
├── megantic_sprite.svg         # Generated sprite sheet (output)
└── README.md                   # This file
```

---

## 🚀 Getting Started

### 1. Prerequisites: Python 3.6+ (no external libraries required – only the standard library is used).
### 2. Place Files Together: `SpriteGenerator.py` and `megantic-generator.py` are in the same directory.
### 3. Run the Generator: python3 megantic-generator.py
```

The script will:
- Import `SEGMENT_GEOMETRY` and `GLYPH_RECIPE_BOOK` from `SpriteGenerator.py`.
- Report which characters have recipes and skip any that are missing.
- Generate `megantic_sprite.svg` in the current directory.

---

## 🎨 Current Character Set

| Row | Group | Characters | CP437 Codes | Scale |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Special 4× | Space, Full Block | 32, 219 | 4× |
| 2 | Digits | 0–9 | 48–57 | 1× |
| 3 | Uppercase | A–Z | 65–90 | 1× |
| 4 | Lowercase | a–z | 97–122 | 1× |

**Total supported glyphs:** 64 (plus more can be added).
The **Space** character renders as a completely empty (off) matrix.  
The **Full Block** renders every segment in the matrix fully lit.

---

## ⚙️ How It Works

### The 45‑Segment Matrix
Each character cell is a **10×12 matrix grid** (approximated, geometry is custom) where the 45 segments occupy precise positions. The script checks each character's recipe and:

1. **Renders all active (ON) segments** with a glowing orange fill (`#ffa500`), a thin black stroke, and a CSS drop‑shadow filter.
2. **Omits inactive (OFF) segments** (the background is a solid dark `#0a0a0a`), keeping the output clean and lightweight.
3. **Applies scaling** – the first row (Space and Full Block) is rendered at **4×** the standard cell size for emphasis.

### Cell Dimensions
- **Base cell:** `18 × 39` units (1× scale)
- **Padded cell step:** `width + 12px` (right padding), `height + 16px` (bottom padding)
- **Special 4× cell:** `72 × 156` units

The script automatically calculates the total canvas width (based on the longest row) and height (sum of all rows).

### SVG Metadata
Each glyph is stored as a `<g>` element with:

```svg
<g id="megantic-65" 
   data-index="65" 
   data-group="Uppercase" 
   data-name="A">
  <!-- geometry -->
</g>
```

The `<use>` tags in the layout reference these IDs, making the sprite sheet easy to parse and use in web or application contexts.

---

## 🛠️ Customizing & Extending

### Adding a New Character

1. **Define the recipe** in `SpriteGenerator.py`:
   ```python
   GLYPH_RECIPE_BOOK["!"] = ["core-top-l-bar", "core-up-c-spine", ...]
   ```

2. **Add the character to `GLYPH_MAP`** in `megantic-generator.py`:
   ```python
   "!": 33,
   ```

3. **Add it to a row** in the `ROWS` list (choose the appropriate group):
   ```python
   ("Punctuation", ["!", ...], 1.0),
   ```

4. **Re‑run** `python3 megantic-generator.py`.

The script will automatically include it in the next sprite sheet generation.

### Adjusting Cell Size / Padding

Edit these constants at the top of `megantic-generator.py`:

```python
BASE_CELL_W = 18
BASE_CELL_H = 39
PAD_RIGHT = 12
PAD_BOTTOM = 16
ROW_PAD_LEFT = 20
ROW_PAD_TOP = 20
```

### Changing the Visual Style

The SVG uses CSS custom properties. Modify the `<style>` block inside the script:

```css
:root {
  --bg-color:   #0a0a0a;   /* Background */
  --seg-on:     #ffa500;   /* Active segment colour */
  --grid-color: #1a1a1a;   /* Unused in this version, kept for reference */
}
.seg-on {
  fill: var(--seg-on);
  stroke: #000000;
  stroke-width: 1.5;
  filter: brightness(1.3) drop-shadow(0px 0px 6px rgba(255,165,0,0.9));
}
```

---

## 📤 Output Example

The generator writes a single SVG file: `megantic_sprite.svg`.

**Structure:**
```
svg
├── <style> ... </style>
├── <defs>
│   ├── <g id="megantic-32"> ... </g>   (Space)
│   ├── <g id="megantic-219"> ... </g>  (Full Block)
│   ├── <g id="megantic-48"> ... </g>   (0)
│   ├── ...
│   ├── <g id="megantic-65"> ... </g>   (A)
│   └── ...
├── <!-- ROW: Special 4× -->
│   ├── <use href="#megantic-32" ... />
│   └── <use href="#megantic-219" ... />
├── <!-- ROW: Digits -->
│   └── <use href="#megantic-48" ... /> ... 
├── <!-- ROW: Uppercase -->
│   └── <use href="#megantic-65" ... /> ...
└── <!-- ROW: Lowercase -->
    └── <use href="#megantic-97" ... /> ...
```

The SVG is fully self‑contained – no external images, fonts, or scripts are required.

---

## 📝 Notes on the Harvester (Optional)

`HarvesterGenerator.py` is an auxiliary tool that compiles the recipes into a **45‑bit lookup table**. It outputs `matrix_lut_database.json` with binary and hexadecimal masks for each character. This is useful for embedded systems or hardware that need a compact numeric representation of the font, but it is **not required** for generating the sprite sheet.

---

## 🤝 Troubleshooting

| Issue | Likely Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'SpriteGenerator'` | `SpriteGenerator.py` is not in the same directory | Move it to the same folder as `megantic-generator.py` |
| `Skipping 'X' - no recipe found` | The character is mapped but missing from `GLYPH_RECIPE_BOOK` | Define the recipe in `SpriteGenerator.py` |
| `No characters with recipes found!` | `GLYPH_RECIPE_BOOK` is empty or not imported properly | Check `SpriteGenerator.py` for valid entries |
| Output SVG is empty | `ROWS` are empty or all characters were skipped | Verify your recipes and mapping |

---

## 🔮 Future Iterations

- **Punctuation** – Once recipes for `!`, `?`, `@`, etc. are defined, they can be added to a new `Punctuation` row.
- **Extended Latin** – Characters like `é`, `ü`, `ñ` can be added to an `Extended` row.
- **Multi‑scale support** – Rows can be assigned custom scale factors (e.g., 1.5×, 2×) for visual hierarchy.
- **Alternative palettes** – The CSS is easy to override for different colour schemes (e.g., blue glow, neon green).

---

## 📄 License

*This tool is provided as‑is. Feel free to use, modify, and distribute as needed for your own projects.*

---

*Built for the Megantic vector font system.*
