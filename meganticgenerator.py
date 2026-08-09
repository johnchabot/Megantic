#!/usr/bin/env python3
"""
megantic-generator.py

Generates a Megantic vector sprite sheet from your segment-based font system.
Uses the SEGMENT_GEOMETRY and GLYPH_RECIPE_BOOK definitions from SpriteGenerator.py.

SPECIAL: Row 1 (Space + Full Block) is rendered 4× larger than all other rows.
All other rows use the standard 18×39 cell size.

Only includes characters that are confirmed to have recipes in GLYPH_RECIPE_BOOK.
Punctuation is omitted for now and can be added later.

Run: python3 megantic-generator.py
Output: megantic_sprite.svg
"""

import sys
from pathlib import Path

# ------------------------------------------------------------------
# 1. IMPORT YOUR EXISTING DEFINITIONS
# ------------------------------------------------------------------

try:
    from SpriteGenerator import SEGMENT_GEOMETRY, GLYPH_RECIPE_BOOK
    print("✓ Imported definitions from SpriteGenerator.py")
    print(f"  Total recipes: {len(GLYPH_RECIPE_BOOK)}")
except ImportError:
    print("⚠️ Could not import from SpriteGenerator.py.")
    print("Please ensure SpriteGenerator.py is in the same directory.")
    print("Falling back to inline definitions...")
    SEGMENT_GEOMETRY = {}
    GLYPH_RECIPE_BOOK = {}

# ------------------------------------------------------------------
# 2. CHARACTER MAPPING (Only characters with confirmed recipes)
# ------------------------------------------------------------------

GLYPH_MAP = {
    # Space (32) - Row 1
    " ": 32,
    
    # Full Block (219) - Row 1
    "█": 219,  # Using Unicode FULL BLOCK U+2588
    
    # Digits (48–57) - Row 2
    "0": 48, "1": 49, "2": 50, "3": 51, "4": 52,
    "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
    
    # Uppercase Letters (65–90) - Row 3
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69,
    "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79,
    "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89,
    "Z": 90,
    
    # Lowercase Letters (97–122) - Row 4
    "a": 97, "b": 98, "c": 99, "d": 100, "e": 101,
    "f": 102, "g": 103, "h": 104, "i": 105, "j": 106,
    "k": 107, "l": 108, "m": 109, "n": 110, "o": 111,
    "p": 112, "q": 113, "r": 114, "s": 115, "t": 116,
    "u": 117, "v": 118, "w": 119, "x": 120, "y": 121,
    "z": 122,
}

# Reverse map: code → character
CODE_TO_CHAR = {v: k for k, v in GLYPH_MAP.items() if k in GLYPH_RECIPE_BOOK}

# Filter out characters that don't have recipes
CHAR_RECIPES_AVAILABLE = {}
for char, code in GLYPH_MAP.items():
    if char in GLYPH_RECIPE_BOOK:
        CHAR_RECIPES_AVAILABLE[char] = code
    else:
        print(f"⚠️ Skipping '{char}' - no recipe found in GLYPH_RECIPE_BOOK")

if not CHAR_RECIPES_AVAILABLE:
    print("❌ ERROR: No characters with recipes found!")
    sys.exit(1)

print(f"✓ Using {len(CHAR_RECIPES_AVAILABLE)} characters with confirmed recipes")

# ------------------------------------------------------------------
# 3. GROUP MAPPING
# ------------------------------------------------------------------

def get_group_for_char(char):
    """Return the group name for a character."""
    if char == " ":
        return "Space"
    elif char == "█":
        return "Full Block"
    elif char.isupper():
        return "Uppercase"
    elif char.islower():
        return "Lowercase"
    elif char.isdigit():
        return "Digits"
    else:
        return "Other"

# ------------------------------------------------------------------
# 4. ROW LAYOUT CONFIGURATION
# ------------------------------------------------------------------

# Define rows: each row is (group_name, list_of_characters, scale_factor)
# Only include characters that have recipes
ROWS = [
    # Row 1: Special 4× cells
    ("Special 4×", [char for char in [" ", "█"] if char in CHAR_RECIPES_AVAILABLE], 4.0),
    
    # Row 2: Numbers (standard 1×)
    ("Digits", [char for char in [chr(c) for c in range(48, 58)] if char in CHAR_RECIPES_AVAILABLE], 1.0),
    
    # Row 3: Uppercase (standard 1×)
    ("Uppercase", [char for char in [chr(c) for c in range(65, 91)] if char in CHAR_RECIPES_AVAILABLE], 1.0),
    
    # Row 4: Lowercase (standard 1×)
    ("Lowercase", [char for char in [chr(c) for c in range(97, 123)] if char in CHAR_RECIPES_AVAILABLE], 1.0),
]

# Flatten all characters for quick lookup
ALL_CHARS = []
for _, chars, _ in ROWS:
    ALL_CHARS.extend(chars)

# ------------------------------------------------------------------
# 5. CELL AND CANVAS DIMENSIONS
# ------------------------------------------------------------------

# Base cell size (1× scale)
BASE_CELL_W = 18
BASE_CELL_H = 39

# Padding to the right and bottom of each cell
PAD_RIGHT = 12
PAD_BOTTOM = 16

# Additional padding at the start of each row
ROW_PAD_LEFT = 20
ROW_PAD_TOP = 20

def cell_dimensions(scale):
    """Return (width, height) for a given scale factor."""
    return (int(BASE_CELL_W * scale), int(BASE_CELL_H * scale))

def row_width(num_chars, scale):
    """Calculate the total width of a row."""
    cell_w, _ = cell_dimensions(scale)
    return ROW_PAD_LEFT + (num_chars * (cell_w + PAD_RIGHT))

def row_height(scale):
    """Calculate the height of a row."""
    _, cell_h = cell_dimensions(scale)
    return cell_h + PAD_BOTTOM

# Calculate total canvas size
max_width = 0
for _, chars, scale in ROWS:
    if chars:  # Only if row has characters
        w = row_width(len(chars), scale)
        if w > max_width:
            max_width = w

total_height = ROW_PAD_TOP
for _, chars, scale in ROWS:
    if chars:  # Only if row has characters
        total_height += row_height(scale)

# If no rows, set minimum size
if max_width == 0:
    max_width = 100
    total_height = 100
    print("⚠️ Warning: No rows with characters found!")

# ------------------------------------------------------------------
# 6. SVG GENERATOR
# ------------------------------------------------------------------

def generate_glyph_element(char, code, group, scale=1.0):
    """Generate the SVG group for a single glyph, with optional scaling."""
    recipe = GLYPH_RECIPE_BOOK.get(char, [])
    
    lines = []
    lines.append(f'    <!-- Glyph: "{char}" (code {code}) scale:{scale} -->')
    lines.append(f'    <g id="megantic-{code}" data-index="{code}" data-group="{group}" data-name="{char}">')
    
    # Apply transform scaling if needed
    if scale != 1.0:
        lines.append(f'      <g transform="scale({scale})">')
    
    for seg_id in recipe:
        if seg_id in SEGMENT_GEOMETRY:
            tag = SEGMENT_GEOMETRY[seg_id].replace('/>', 'class="seg-on" />')
            lines.append(f'        {tag}')
    
    if scale != 1.0:
        lines.append('      </g>')
    
    lines.append('    </g>')
    return "\n".join(lines)

def generate_sprite_sheet():
    """Generate the Megantic sprite sheet from your glyph recipes."""
    
    output = []
    
    # SVG header
    output.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max_width} {total_height}" width="{max_width}" height="{total_height}">')
    
    # CSS Styles
    output.append('  <style>')
    output.append('    :root {')
    output.append('      --bg-color:   #0a0a0a;')
    output.append('      --seg-on:     #ffa500;')
    output.append('      --grid-color: #1a1a1a;')
    output.append('    }')
    output.append('    svg { background: var(--bg-color); }')
    output.append('    .seg-on { fill: var(--seg-on); stroke: #000000; stroke-width: 1.5; filter: brightness(1.3) drop-shadow(0px 0px 6px rgba(255,165,0,0.9)); }')
    output.append('  </style>')
    
    # --- DEFS: Build all glyph definitions ---
    output.append('  <defs>')
    
    for char in ALL_CHARS:
        if char in CHAR_RECIPES_AVAILABLE:
            code = CHAR_RECIPES_AVAILABLE[char]
            group = get_group_for_char(char)
            # Find the scale for this character
            scale = 1.0
            for _, chars, s in ROWS:
                if char in chars:
                    scale = s
                    break
            output.append(generate_glyph_element(char, code, group, scale))
    
    output.append('  </defs>')
    
    # --- LAYOUT: Place glyphs in rows ---
    output.append('  <!-- Sprite Sheet Layout: Row-based grouping -->')
    
    current_y = ROW_PAD_TOP
    
    for group_name, chars, scale in ROWS:
        if not chars:
            continue  # Skip empty rows
            
        output.append(f'  <!-- ========== ROW: {group_name} ({len(chars)} characters) scale:{scale} ========== -->')
        
        current_x = ROW_PAD_LEFT
        cell_w, cell_h = cell_dimensions(scale)
        
        for char in chars:
            if char in CHAR_RECIPES_AVAILABLE:
                code = CHAR_RECIPES_AVAILABLE[char]
                output.append(f'  <use href="#megantic-{code}" x="{current_x}" y="{current_y}" /> <!-- megantic-{code} ({group_name} | {char}) -->')
            else:
                # Should not happen since we filtered above
                output.append(f'  <rect x="{current_x}" y="{current_y}" width="{cell_w}" height="{cell_h}" fill="none" stroke="#1a1a1a" stroke-width="0.5" /> <!-- MISSING: {char} -->')
            
            # Move to next cell (with right padding)
            current_x += cell_w + PAD_RIGHT
        
        # Move to next row (with bottom padding)
        current_y += cell_h + PAD_BOTTOM
    
    output.append('</svg>')
    
    # Write the file
    output_file = "megantic_sprite.svg"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    
    print(f"\n[SUCCESS] Generated Megantic sprite sheet: {output_file}")
    print(f"  Rows: {len([r for r in ROWS if r[1]])}")
    print(f"  Total glyphs: {len(ALL_CHARS)}")
    print(f"  Canvas: {max_width}×{total_height}")
    print(f"  Base cell: {BASE_CELL_W}×{BASE_CELL_H}")
    print(f"  Special 4× cell: {BASE_CELL_W*4}×{BASE_CELL_H*4}")

if __name__ == "__main__":
    generate_sprite_sheet()
