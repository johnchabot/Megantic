#!/usr/bin/env python3
"""
canada-generator.py

Generates a Canada sprite sheet from a .ttf or .otf font file.
Uses fonttools to extract glyph outlines and convert them to SVG paths.

The output is a self-contained SVG sprite sheet with rows grouped by character type.

Usage:
    python3 canada-generator.py Canada-Regular.ttf
    python3 canada-generator.py Canada-Regular.otf
    python3 canada-generator.py Canada-Regular.ttx   # For testing with TTX
Output: canada_sprite.svg
"""

import sys
import os
import math
import xml.etree.ElementTree as ET

# Try to import fonttools (optional if using TTX directly)
try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    FONTTOOLS_AVAILABLE = True
except ImportError:
    FONTTOOLS_AVAILABLE = False
    print("⚠️ fonttools not installed. Install with: pip install fonttools")
    print("   Falling back to TTX XML parsing (if you pass a .ttx file)")

# ------------------------------------------------------------------
# 1. CHARACTER MAPPING
# ------------------------------------------------------------------

# Map glyph names (from the font) to CP437 codes and display characters
# This is based on standard PostScript glyph names
GLYPH_MAP = {
    # Special
    "space": 32,
    
    # Punctuation (33–47)
    "exclam": 33,
    "quotedbl": 34,
    "numbersign": 35,
    "dollar": 36,
    "percent": 37,
    "ampersand": 38,
    "quotesingle": 39,
    "parenleft": 40,
    "parenright": 41,
    "asterisk": 42,
    "plus": 43,
    "comma": 44,
    "hyphen": 45,
    "period": 46,
    "slash": 47,
    
    # Digits (48–57)
    "zero": 48,
    "one": 49,
    "two": 50,
    "three": 51,
    "four": 52,
    "five": 53,
    "six": 54,
    "seven": 55,
    "eight": 56,
    "nine": 57,
    
    # Punctuation (58–64)
    "colon": 58,
    "semicolon": 59,
    "less": 60,
    "equal": 61,
    "greater": 62,
    "question": 63,
    "at": 64,
    
    # Uppercase Letters (65–90)
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69,
    "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79,
    "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89,
    "Z": 90,
    
    # Brackets and symbols (91–96)
    "bracketleft": 91,
    "backslash": 92,
    "bracketright": 93,
    "asciicircum": 94,
    "underscore": 95,
    "grave": 96,
    
    # Lowercase Letters (97–122)
    "a": 97, "b": 98, "c": 99, "d": 100, "e": 101,
    "f": 102, "g": 103, "h": 104, "i": 105, "j": 106,
    "k": 107, "l": 108, "m": 109, "n": 110, "o": 111,
    "p": 112, "q": 113, "r": 114, "s": 115, "t": 116,
    "u": 117, "v": 118, "w": 119, "x": 120, "y": 121,
    "z": 122,
    
    # Braces and tilde (123–126)
    "braceleft": 123,
    "bar": 124,
    "braceright": 125,
    "asciitilde": 126,
}

# Reverse map: code → character (for metadata)
CODE_TO_GLYPH = {v: k for k, v in GLYPH_MAP.items() if k in GLYPH_MAP}
CODE_TO_CHAR = {v: k[0].upper() if len(k) == 1 else k for k, v in GLYPH_MAP.items()}

def get_group_for_code(code):
    """Return the group name for a CP437 code."""
    if code == 32:
        return "Space"
    elif 48 <= code <= 57:
        return "Digits"
    elif 65 <= code <= 90:
        return "Uppercase"
    elif 97 <= code <= 122:
        return "Lowercase"
    elif 33 <= code <= 64 or 91 <= code <= 96 or 123 <= code <= 126:
        return "Punctuation"
    else:
        return "Extended"

# ------------------------------------------------------------------
# 2. GLYPH EXTRACTION (from TTF/OTF or TTX)
# ------------------------------------------------------------------

def extract_glyph_path_ttf(font_path, glyph_name):
    """Extract SVG path data for a glyph from a TTF/OTF file."""
    if not FONTTOOLS_AVAILABLE:
        return None
    
    font = TTFont(font_path)
    glyph_set = font.getGlyphSet()
    
    if glyph_name not in glyph_set:
        return None
    
    glyph = glyph_set[glyph_name]
    pen = SVGPathPen(glyph_set)
    glyph.draw(pen)
    return pen.getCommands()

def extract_glyph_path_ttx(ttx_path, glyph_name):
    """Extract SVG path data for a glyph from a TTX XML file."""
    tree = ET.parse(ttx_path)
    root = tree.getroot()
    
    # Find the glyf table
    glyf = root.find("glyf")
    if glyf is None:
        return None
    
    # Find the glyph entry
    for elem in glyf.findall("TTGlyph"):
        if elem.get("name") == glyph_name:
            # Convert the TTX outline to a path string
            # This is a simplified version - TTX uses a custom format
            path_data = convert_ttx_outline_to_path(elem)
            return path_data
    
    return None

def convert_ttx_outline_to_path(ttglyph_elem):
    """Convert a TTX TTGlyph element to an SVG path string."""
    # This is a placeholder - TTX outlines are in the 'contour' format
    # For a full implementation, we'd need to parse the contour and instructions
    # Since we're using fonttools for the actual extraction, this is just a fallback
    return None

# ------------------------------------------------------------------
# 3. PATH PROCESSING
# ------------------------------------------------------------------

def normalize_path_to_cell(path_data, cell_width=18, cell_height=39):
    """Scale and center a path to fit inside a cell."""
    if not path_data:
        return path_data
    
    # Parse the path to find the bounding box
    # This is a simplification - for a real implementation we'd parse the path
    # or use fonttools' built-in bounding box methods
    
    # For now, we'll just return the path and let the SVG handle scaling via viewBox
    return path_data

# ------------------------------------------------------------------
# 4. SVG GENERATOR
# ------------------------------------------------------------------

def generate_sprite_sheet(font_source):
    """Generate the Canada sprite sheet from a font file or TTX file."""
    
    # Determine the source type
    is_ttx = font_source.endswith('.ttx')
    is_font = font_source.endswith('.ttf') or font_source.endswith('.otf')
    
    if not is_ttx and not is_font:
        print("❌ Error: Input must be a .ttf, .otf, or .ttx file")
        return
    
    # Extract all glyphs we need
    glyphs_data = {}
    
    for glyph_name, code in GLYPH_MAP.items():
        if is_font and FONTTOOLS_AVAILABLE:
            path = extract_glyph_path_ttf(font_source, glyph_name)
        elif is_ttx:
            path = extract_glyph_path_ttx(font_source, glyph_name)
        else:
            print(f"⚠️ Skipping '{glyph_name}' - no extraction method available")
            continue
        
        if path:
            glyphs_data[code] = {
                "glyph_name": glyph_name,
                "path": path,
                "char": CODE_TO_CHAR.get(code, glyph_name)
            }
        else:
            print(f"⚠️ Skipping '{glyph_name}' - no path data found")
    
    if not glyphs_data:
        print("❌ No glyphs extracted!")
        return
    
    print(f"✓ Extracted {len(glyphs_data)} glyphs")
    
    # ------------------------------------------------------------------
    # Row Layout
    # ------------------------------------------------------------------
    
    # Define rows: each row is (group_name, list_of_codes, scale_factor)
    ROWS = [
        # Row 1: Special 4× cells (Space only for now)
        ("Space", [32], 4.0),
        
        # Row 2: Digits (standard 1×)
        ("Digits", list(range(48, 58)), 1.0),
        
        # Row 3: Uppercase (standard 1×)
        ("Uppercase", list(range(65, 91)), 1.0),
        
        # Row 4: Lowercase (standard 1×)
        ("Lowercase", list(range(97, 123)), 1.0),
        
        # Row 5: Punctuation (standard 1×)
        ("Punctuation", [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 58, 59, 60, 61, 62, 63, 64, 91, 92, 93, 94, 95, 96, 123, 124, 125, 126], 1.0),
    ]
    
    # Filter out codes that aren't available
    ROWS = [(name, [c for c in codes if c in glyphs_data], scale) for name, codes, scale in ROWS]
    
    # ------------------------------------------------------------------
    # Cell Dimensions
    # ------------------------------------------------------------------
    
    BASE_CELL_W = 18
    BASE_CELL_H = 39
    PAD_RIGHT = 12
    PAD_BOTTOM = 16
    ROW_PAD_LEFT = 20
    ROW_PAD_TOP = 20
    
    def cell_dimensions(scale):
        return (int(BASE_CELL_W * scale), int(BASE_CELL_H * scale))
    
    def row_width(num_chars, scale):
        cell_w, _ = cell_dimensions(scale)
        return ROW_PAD_LEFT + (num_chars * (cell_w + PAD_RIGHT))
    
    def row_height(scale):
        _, cell_h = cell_dimensions(scale)
        return cell_h + PAD_BOTTOM
    
    # Calculate total canvas size
    max_width = 0
    for _, chars, scale in ROWS:
        if chars:
            w = row_width(len(chars), scale)
            if w > max_width:
                max_width = w
    
    total_height = ROW_PAD_TOP
    for _, chars, scale in ROWS:
        if chars:
            total_height += row_height(scale)
    
    if max_width == 0:
        max_width = 100
        total_height = 100
        print("⚠️ Warning: No rows with characters found!")
    
    # ------------------------------------------------------------------
    # Build the SVG
    # ------------------------------------------------------------------
    
    output = []
    
    output.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max_width} {total_height}" width="{max_width}" height="{total_height}">')
    
    output.append('  <style>')
    output.append('    :root {')
    output.append('      --bg-color:   #0a0a0a;')
    output.append('      --glyph-color: #ffa500;')
    output.append('    }')
    output.append('    svg { background: var(--bg-color); }')
    output.append('    .glyph-on { fill: var(--glyph-color); stroke: #000000; stroke-width: 1.5; filter: brightness(1.3) drop-shadow(0px 0px 6px rgba(255,165,0,0.9)); }')
    output.append('  </style>')
    
    # --- DEFS ---
    output.append('  <defs>')
    
    for code, data in glyphs_data.items():
        glyph_name = data["glyph_name"]
        char = data["char"]
        path = data["path"]
        group = get_group_for_code(code)
        
        output.append(f'    <!-- Glyph: "{char}" (code {code}) glyph: {glyph_name} -->')
        output.append(f'    <g id="canada-{code}" data-index="{code}" data-group="{group}" data-name="{char}">')
        output.append(f'      <path d="{path}" class="glyph-on"/>')
        output.append('    </g>')
    
    output.append('  </defs>')
    
    # --- LAYOUT ---
    output.append('  <!-- Sprite Sheet Layout: Row-based grouping -->')
    
    current_y = ROW_PAD_TOP
    
    for group_name, chars, scale in ROWS:
        if not chars:
            continue
        
        output.append(f'  <!-- ========== ROW: {group_name} ({len(chars)} characters) scale:{scale} ========== -->')
        
        current_x = ROW_PAD_LEFT
        cell_w, cell_h = cell_dimensions(scale)
        
        for code in chars:
            if code in glyphs_data:
                output.append(f'  <use href="#canada-{code}" x="{current_x}" y="{current_y}" /> <!-- canada-{code} ({group_name} | {glyphs_data[code]["char"]}) -->')
            else:
                output.append(f'  <rect x="{current_x}" y="{current_y}" width="{cell_w}" height="{cell_h}" fill="none" stroke="#1a1a1a" stroke-width="0.5" /> <!-- MISSING: {code} -->')
            
            current_x += cell_w + PAD_RIGHT
        
        current_y += cell_h + PAD_BOTTOM
    
    output.append('</svg>')
    
    # Write the file
    output_file = "canada_sprite.svg"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    
    print(f"\n[SUCCESS] Generated Canada sprite sheet: {output_file}")
    print(f"  Rows: {len([r for r in ROWS if r[1]])}")
    print(f"  Total glyphs: {len(glyphs_data)}")
    print(f"  Canvas: {max_width}×{total_height}")

# ------------------------------------------------------------------
# 5. MAIN
# ------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 canada-generator.py <font.ttf|.otf|.ttx>")
        print("  Example: python3 canada-generator.py Canada-Regular.otf")
        print("           python3 canada-generator.py Canada-Regular.ttx")
        sys.exit(1)
    
    font_source = sys.argv[1]
    
    if not os.path.exists(font_source):
        print(f"❌ Error: File not found: {font_source}")
        sys.exit(1)
    
    generate_sprite_sheet(font_source)
