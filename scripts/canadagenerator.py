#!/usr/bin/env python3
"""
canada-generator.py (with auto-scaling & robust font handling)

Generates a Canada sprite sheet from a .ttf or .otf font file.
Glyphs are automatically scaled to fit the 18×39 cells.

Handles both TTF (glyf table) and OTF (CFF table) fonts.
Fixes: getHead() → font['head'], getBounds() fallback.

Usage:
    python3 canada-generator.py <font.otf|ttf>
Output: canada_sprite.svg
"""

import sys
import os

try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    FONTTOOLS_AVAILABLE = True
except ImportError:
    FONTTOOLS_AVAILABLE = False
    print("⚠️ fonttools not installed. Install with: pip install fonttools")
    sys.exit(1)

# ------------------------------------------------------------------
# 1. CHARACTER SET (Unicode code points)
# ------------------------------------------------------------------

CHARACTER_SET = {
    " ": 0x0020,
    "!": 0x0021,
    '"': 0x0022,
    "#": 0x0023,
    "$": 0x0024,
    "%": 0x0025,
    "&": 0x0026,
    "'": 0x0027,
    "(": 0x0028,
    ")": 0x0029,
    "*": 0x002A,
    "+": 0x002B,
    ",": 0x002C,
    "-": 0x002D,
    ".": 0x002E,
    "/": 0x002F,
    ":": 0x003A,
    ";": 0x003B,
    "<": 0x003C,
    "=": 0x003D,
    ">": 0x003E,
    "?": 0x003F,
    "@": 0x0040,
    "[": 0x005B,
    "\\": 0x005C,
    "]": 0x005D,
    "^": 0x005E,
    "_": 0x005F,
    "`": 0x0060,
    "{": 0x007B,
    "|": 0x007C,
    "}": 0x007D,
    "~": 0x007E,
    "0": 0x0030,
    "1": 0x0031,
    "2": 0x0032,
    "3": 0x0033,
    "4": 0x0034,
    "5": 0x0035,
    "6": 0x0036,
    "7": 0x0037,
    "8": 0x0038,
    "9": 0x0039,
    "A": 0x0041,
    "B": 0x0042,
    "C": 0x0043,
    "D": 0x0044,
    "E": 0x0045,
    "F": 0x0046,
    "G": 0x0047,
    "H": 0x0048,
    "I": 0x0049,
    "J": 0x004A,
    "K": 0x004B,
    "L": 0x004C,
    "M": 0x004D,
    "N": 0x004E,
    "O": 0x004F,
    "P": 0x0050,
    "Q": 0x0051,
    "R": 0x0052,
    "S": 0x0053,
    "T": 0x0054,
    "U": 0x0055,
    "V": 0x0056,
    "W": 0x0057,
    "X": 0x0058,
    "Y": 0x0059,
    "Z": 0x005A,
    "a": 0x0061,
    "b": 0x0062,
    "c": 0x0063,
    "d": 0x0064,
    "e": 0x0065,
    "f": 0x0066,
    "g": 0x0067,
    "h": 0x0068,
    "i": 0x0069,
    "j": 0x006A,
    "k": 0x006B,
    "l": 0x006C,
    "m": 0x006D,
    "n": 0x006E,
    "o": 0x006F,
    "p": 0x0070,
    "q": 0x0071,
    "r": 0x0072,
    "s": 0x0073,
    "t": 0x0074,
    "u": 0x0075,
    "v": 0x0076,
    "w": 0x0077,
    "x": 0x0078,
    "y": 0x0079,
    "z": 0x007A,
    "§": 0x00A7,
    "¨": 0x00A8,
    "«": 0x00AB,
    "»": 0x00BB,
    "¼": 0x00BC,
    "½": 0x00BD,
    "¿": 0x00BF,
    "À": 0x00C0,
    "Á": 0x00C1,
    "Â": 0x00C2,
    "Ã": 0x00C3,
    "Ä": 0x00C4,
    "Å": 0x00C5,
    "Æ": 0x00C6,
    "Ç": 0x00C7,
    "È": 0x00C8,
    "É": 0x00C9,
    "Ê": 0x00CA,
    "Ë": 0x00CB,
    "Ì": 0x00CC,
    "Í": 0x00CD,
    "Î": 0x00CE,
    "Ï": 0x00CF,
    "Ð": 0x00D0,
    "Ñ": 0x00D1,
    "Ò": 0x00D2,
    "Ó": 0x00D3,
    "Ô": 0x00D4,
    "Õ": 0x00D5,
    "Ö": 0x00D6,
    "×": 0x00D7,
    "Ø": 0x00D8,
    "Ù": 0x00D9,
    "Ú": 0x00DA,
    "Û": 0x00DB,
    "Ü": 0x00DC,
    "Ý": 0x00DD,
    "Þ": 0x00DE,
    "à": 0x00E0,
    "á": 0x00E1,
    "â": 0x00E2,
    "ã": 0x00E3,
    "ä": 0x00E4,
    "å": 0x00E5,
    "æ": 0x00E6,
    "ç": 0x00E7,
    "è": 0x00E8,
    "é": 0x00E9,
    "ê": 0x00EA,
    "ë": 0x00EB,
    "ì": 0x00EC,
    "í": 0x00ED,
    "î": 0x00EE,
    "ï": 0x00EF,
    "ð": 0x00F0,
    "ñ": 0x00F1,
    "ò": 0x00F2,
    "ó": 0x00F3,
    "ô": 0x00F4,
    "õ": 0x00F5,
    "ö": 0x00F6,
    "÷": 0x00F7,
    "ø": 0x00F8,
    "ù": 0x00F9,
    "ú": 0x00FA,
    "û": 0x00FB,
    "ü": 0x00FC,
    "ý": 0x00FD,
    "þ": 0x00FE,
    "ÿ": 0x00FF,
    "–": 0x2013,
    "—": 0x2014,
    "‘": 0x2018,
    "’": 0x2019,
    "•": 0x2022,
    "…": 0x2026,
    "←": 0x2190,
    "↑": 0x2191,
    "→": 0x2192,
    "↓": 0x2193,
    "↔": 0x2194,
    "↕": 0x2195,
    "☺": 0x263A,
    "☼": 0x263C,
    "♀": 0x2640,
    "♂": 0x2642,
    "♥": 0x2665,
}

# ------------------------------------------------------------------
# 2. ROWS CONFIGURATION
# ------------------------------------------------------------------

ROWS = [
    ("Space", [" "], 4.0),
    ("Keyboard (1)", ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/"], 1.0),
    ("Digits", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 1.0),
    ("Keyboard (2)", [":", ";", "<", "=", ">", "?", "@"], 1.0),
    ("Uppercase", ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], 1.0),
    ("Keyboard (3)", ["[", "\\", "]", "^", "_", "`"], 1.0),
    ("Lowercase", ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"], 1.0),
    ("Keyboard (4)", ["{", "|", "}", "~"], 1.0),
    ("ASCII+Weird", ["§", "¨", "«", "»", "¼", "½", "¿"], 1.0),
    ("French/Spanish Upper", ["À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï", "Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "Þ"], 1.0),
    ("French/Spanish Lower", ["à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï", "ð", "ñ", "ò", "ó", "ô", "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ"], 1.0),
    ("Symbols", ["–", "—", "‘", "’", "•", "…", "←", "↑", "→", "↓", "↔", "↕", "☺", "☼", "♀", "♂", "♥"], 1.0),
]

# ------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# ------------------------------------------------------------------

def get_group_for_char(char):
    if char == " ":
        return "Space"
    elif char.isdigit():
        return "Digits"
    elif char.isupper():
        return "Uppercase"
    elif char.islower():
        return "Lowercase"
    elif char in ["§", "¨", "«", "»", "¼", "½", "¿"]:
        return "ASCII+Weird"
    elif ord(char) in range(0x00C0, 0x00FF + 1):
        return "French/Spanish"
    elif ord(char) in [0x2013, 0x2014, 0x2018, 0x2019, 0x2022, 0x2026, 0x2190, 0x2191, 0x2192, 0x2193, 0x2194, 0x2195, 0x263A, 0x263C, 0x2640, 0x2642, 0x2665]:
        return "Symbols"
    else:
        return "Keyboard"

def escape_xml_attr(value):
    if value is None:
        return ""
    return (str(value)
            .replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("'", "&apos;"))

# ------------------------------------------------------------------
# 4. GLYPH EXTRACTION WITH AUTO-SCALING (fixed for OTF/CFF)
# ------------------------------------------------------------------

def extract_glyph_with_bounds(font, unicode_map, char, cell_w, cell_h):
    code = ord(char)
    glyph_name = unicode_map.get(code)
    if glyph_name is None:
        return None, None, 0, 0

    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set:
        return None, None, 0, 0

    glyph = glyph_set[glyph_name]
    pen = SVGPathPen(glyph_set)
    glyph.draw(pen)
    raw_path = pen.getCommands()
    if not raw_path:
        # Empty glyph (like space) – return empty path with no transform
        return "", None, 0, 0

    # Try to get bounding box from the glyph (works for TTF; may fail for OTF/CFF)
    try:
        bounds = glyph.getBounds()
    except AttributeError:
        bounds = None

    # If we have bounds, use them for precise scaling and centering
    if bounds is not None:
        xMin, yMin, xMax, yMax = bounds
        glyph_w = xMax - xMin
        glyph_h = yMax - yMin
        if glyph_w <= 0 or glyph_h <= 0:
            # Degenerate glyph – skip or fallback
            return raw_path, None, cell_w, cell_h
        margin = 0.1
        avail_w = cell_w * (1 - 2 * margin)
        avail_h = cell_h * (1 - 2 * margin)
        scale = min(avail_w / glyph_w, avail_h / glyph_h)
        # Clamp to avoid scaling up too much (max 1.0)
        if scale > 1.0:
            scale = 1.0
        # Center the glyph within the cell
        cx_cell = cell_w / 2
        cy_cell = cell_h / 2
        cx_glyph = (xMin + xMax) / 2
        cy_glyph = (yMin + yMax) / 2
        tx = cx_cell - cx_glyph * scale
        ty = cy_cell - cy_glyph * scale
        transform = f"translate({tx:.2f}, {ty:.2f}) scale({scale:.4f})"
        return raw_path, transform, cell_w, cell_h

    # Fallback for fonts without bounding box (CFF)
    upem = font['head'].unitsPerEm
    # Estimate glyph size based on em square (assume ~70% of em)
    est_w = upem * 0.7
    est_h = upem * 0.7
    scale = min(cell_w / est_w, cell_h / est_h)
    if scale > 1.0:
        scale = 1.0
    # No centering; just scale from origin (0,0)
    transform = f"scale({scale:.4f})"
    return raw_path, transform, cell_w, cell_h

# ------------------------------------------------------------------
# 5. SVG GENERATOR
# ------------------------------------------------------------------

def generate_sprite_sheet(font_path):
    if not os.path.exists(font_path):
        print(f"❌ Error: File not found: {font_path}")
        return

    print(f"Loading font: {font_path}...")
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    unicode_map = {code: name for code, name in cmap.items()}
    print(f"✓ Found {len(unicode_map)} Unicode mappings")

    # Get UPEM (safe method)
    try:
        upem = font['head'].unitsPerEm
    except KeyError:
        upem = 1000  # fallback
    print(f"✓ Font UPEM: {upem}")

    # Base cell dimensions
    BASE_CELL_W = 18
    BASE_CELL_H = 39
    PAD_RIGHT = 12
    PAD_BOTTOM = 16
    ROW_PAD_LEFT = 20
    ROW_PAD_TOP = 20

    def cell_dimensions(scale):
        return (int(BASE_CELL_W * scale), int(BASE_CELL_H * scale))

    # Extract all glyphs
    glyphs_data = {}
    for char, code in CHARACTER_SET.items():
        # Determine scale for this character (from ROWS)
        cell_scale = 1.0
        for _, chars, s in ROWS:
            if char in chars:
                cell_scale = s
                break
        cell_w, cell_h = cell_dimensions(cell_scale)

        path, transform, _, _ = extract_glyph_with_bounds(font, unicode_map, char, cell_w, cell_h)
        if path is not None:
            glyphs_data[char] = {
                "char": char,
                "code": code,
                "path": path,
                "transform": transform,
                "group": get_group_for_char(char),
                "cell_w": cell_w,
                "cell_h": cell_h,
            }
        else:
            print(f"⚠️ Skipping '{char}' (U+{code:04X}) - not found in font")

    if not glyphs_data:
        print("❌ No glyphs extracted!")
        return

    print(f"✓ Extracted {len(glyphs_data)} glyphs")

    # Build rows
    built_rows = []
    for group_name, chars, scale in ROWS:
        filtered = [c for c in chars if c in glyphs_data]
        if filtered:
            built_rows.append((group_name, filtered, scale))
        else:
            print(f"⚠️ Warning: Row '{group_name}' has no characters")

    if not built_rows:
        print("❌ No rows with characters found!")
        return

    # Calculate canvas size
    max_width = 0
    for _, chars, scale in built_rows:
        cell_w, _ = cell_dimensions(scale)
        w = ROW_PAD_LEFT + len(chars) * (cell_w + PAD_RIGHT)
        if w > max_width:
            max_width = w

    total_height = ROW_PAD_TOP
    for _, _, scale in built_rows:
        _, cell_h = cell_dimensions(scale)
        total_height += cell_h + PAD_BOTTOM

    print(f"Canvas: {max_width}×{total_height}")
    print(f"Rows: {len(built_rows)}")

    # Build SVG
    output = []
    output.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max_width} {total_height}" width="{max_width}" height="{total_height}">')
    output.append('  <style>')
    output.append('    :root { --bg-color: #ffffff; --glyph-color: #000000; }')
    output.append('    svg { background: var(--bg-color); }')
    output.append('    .glyph-on { fill: var(--glyph-color); }')
    output.append('  </style>')

    output.append('  <defs>')
    for char, data in glyphs_data.items():
        code = data["code"]
        path = data["path"]
        group = data["group"]
        transform = data["transform"]
        escaped_char = escape_xml_attr(char)
        escaped_group = escape_xml_attr(group)
        escaped_path = escape_xml_attr(path)

        output.append(f'    <!-- Glyph: "{escaped_char}" (U+{code:04X}) -->')
        output.append(f'    <g id="canada-{code}" data-index="{code}" data-group="{escaped_group}" data-name="{escaped_char}">')
        if path and transform:
            output.append(f'      <g transform="{transform}">')
            output.append(f'        <path d="{escaped_path}" class="glyph-on"/>')
            output.append('      </g>')
        elif path:
            # Should not happen for valid glyphs
            output.append(f'      <path d="{escaped_path}" class="glyph-on"/>')
        output.append('    </g>')
    output.append('  </defs>')

    # Layout (row grouping)
    output.append('  <!-- Sprite Sheet Layout: Row-based grouping -->')
    current_y = ROW_PAD_TOP
    for group_name, chars, scale in built_rows:
        output.append(f'  <!-- ========== ROW: {escape_xml_attr(group_name)} ({len(chars)} chars) scale:{scale} ========== -->')
        row_id = f"row-{group_name.replace(' ', '-').replace('(', '').replace(')', '')}"
        output.append(f'  <g id="{row_id}" data-row="{escape_xml_attr(group_name)}" transform="translate(0, {current_y})">')
        current_x = ROW_PAD_LEFT
        cell_w, cell_h = cell_dimensions(scale)
        for char in chars:
            if char in glyphs_data:
                code = glyphs_data[char]["code"]
                escaped_char = escape_xml_attr(char)
                output.append(f'    <use href="#canada-{code}" x="{current_x}" /> <!-- canada-{code} ({escape_xml_attr(group_name)} | {escaped_char}) -->')
            else:
                output.append(f'    <rect x="{current_x}" y="0" width="{cell_w}" height="{cell_h}" fill="none" stroke="#cccccc" stroke-width="0.5" /> <!-- MISSING: {char} -->')
            current_x += cell_w + PAD_RIGHT
        output.append('  </g>')
        current_y += cell_h + PAD_BOTTOM

    output.append('</svg>')

    with open("canada_sprite.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"\n[SUCCESS] Generated Canada sprite sheet: canada_sprite.svg")
    print(f"  Rows: {len(built_rows)}")
    print(f"  Total glyphs: {len(glyphs_data)}")
    print(f"  Canvas: {max_width}×{total_height}")
    print(f"  Cell size: {BASE_CELL_W}×{BASE_CELL_H} (1×)")

# ------------------------------------------------------------------
# 6. MAIN
# ------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 canada-generator.py <font.otf|ttf>")
        sys.exit(1)
    font_path = sys.argv[1]
    generate_sprite_sheet(font_path)
