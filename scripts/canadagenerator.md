
Canada Sprite Generator 🍁

A Python tool that extracts glyphs from .otf or .ttf font files and generates a self-contained SVG sprite sheet. Each character is rendered as a clean black vector path on a white background, organized in color‑coded rows.

This is the second generation of sprite generators we built together (after the glowing Megantic vector segment system). The Canada generator focuses on high‑fidelity reproduction of a modern font's outlines using fonttools.

python3 canada-generator.py canada1500-rg.otf



Interpreting the Canvas Size
The 980px width is determined by the widest row—in this case, French/Spanish Lower with 32 characters:
    Each 1× cell is 18 + 12 (padding) = 30px wide
    32 characters × 30px = 960px
    Plus 20px left padding = 980px

Metric	Value	What It Tells You
Unicode mappings	1791	The font supports this many characters (Unicode code points)
Glyphs extracted	182	The number of characters from your list that were found in the font
Canvas width	980	The width of the SVG (determined by the longest row)
Canvas height	797	The height of the SVG (sum of all rows + padding)
Rows	12	The number of character groups (each row is a group)
Cell size	18×39	The base size of each glyph cell before padding (1× scale)


Metadata & File Structure
Each glyph is stored as a <g> element in the SVG's <defs> section:


Attribute	    Purpose
id             	Uniquely identifies each glyph (used by <use> tags)
data-index  	The Unicode code point (decimal)
data-group  	The character group (e.g., Uppercase, Digits)
data-name	    The character itself (for easy identification)

Changing Row Scale
Each row in ROWS has a scale factor:
# Space is 4× larger than other cells
("Space", [" "], 4.0),
# All other rows are 1×
("Keyboard (1)", [...], 1.0),


The Layout Section
The sprite sheet uses <use> tags to place each glyph in its row:
 <use href="#canada-65" x="20" y="20" /> <!-- canada-65 (Uppercase | A) -->
Each row starts at a calculated y position, and characters are placed left-to-right with fixed x spacing.


Customizing & Adding Characters
Adding New Characters
  #      Add the character to CHARACTER_SET with its Unicode code point
      python
  
  CHARACTER_SET = {
      # ... existing entries ...
      "€": 0x20AC,   # Euro symbol
      "©": 0x00A9,   # Copyright
  }

To find the Unicode code point for a character, use:
  python
  
  print(ord("€"))   # 8364 (decimal)
  print(hex(ord("€")))  # 0x20AC (hex)
  
  Add the character to the appropriate row in ROWS:
  python

ROWS = [
    # ... existing rows ...
    ("Symbols", ["–", "—", "‘", "’", "•", "…", "←", "↑", "→", "↓", "↔", "↕", "☺", "☼", "♀", "♂", "♥", "€", "©"], 1.0),
]

Re-run the script


Adjusting Cell Size & Padding

Edit these constants in the script:

BASE_CELL_W = 18     # Width of each cell (1× scale)
BASE_CELL_H = 39     # Height of each cell (1× scale)
PAD_RIGHT = 12       # Padding to the right of each cell
PAD_BOTTOM = 16      # Padding below each cell
ROW_PAD_LEFT = 20    # Left padding at the start of each row
ROW_PAD_TOP = 20     # Top padding above the first row
