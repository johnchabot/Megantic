#!/usr/bin/env python3
"""
canada-generator.py (Dark Mode)

Generates a Canada sprite sheet from a .ttf or .otf font file.
Features:
- Auto-scaling to fit 48×48 cells
- Labels (Unicode character) in a 24px box under each glyph
- Row grouping with metadata
- Canvas width rounded to nearest multiple of 12
- Dark background (#2a2e2f) with off-white glyphs and labels (#f0f0f0)

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
# 1. CHARACTER SET & ROWS (unchanged)
# ------------------------------------------------------------------

CHARACTER_SET = {
    " ": 0x0020, "!": 0x0021, '"': 0x0022, "#": 0x0023, "$": 0x0024,
    "%": 0x0025, "&": 0x0026, "'": 0x0027, "(": 0x0028, ")": 0x0029,
    "*": 0x002A, "+": 0x002B, ",": 0x002C, "-": 0x002D, ".": 0x002E,
    "/": 0x002F, ":": 0x003A, ";": 0x003B, "<": 0x003C, "=": 0x003D,
    ">": 0x003E, "?": 0x003F, "@": 0x0040, "[": 0x005B, "\\": 0x005C,
    "]": 0x005D, "^": 0x005E, "_": 0x005F, "`": 0x0060, "{": 0x007B,
    "|": 0x007C, "}": 0x007D, "~": 0x007E,
    "0": 0x0030, "1": 0x0031, "2": 0x0032, "3": 0x0033, "4": 0x0034,
    "5": 0x0035, "6": 0x0036, "7": 0x0037, "8": 0x0038, "9": 0x0039,
    "A": 0x0041, "B": 0x0042, "C": 0x0043, "D": 0x0044, "E": 0x0045,
    "F": 0x0046, "G": 0x0047, "H": 0x0048, "I": 0x0049, "J": 0x004A,
    "K": 0x004B, "L": 0x004C, "M": 0x004D, "N": 0x004E, "O": 0x004F,
    "P": 0x0050, "Q": 0x0051, "R": 0x0052, "S": 0x0053, "T": 0x0054,
    "U": 0x0055, "V": 0x0056, "W": 0x0057, "X": 0x0058, "Y": 0x0059,
    "Z": 0x005A,
    "a": 0x0061, "b": 0x0062, "c": 0x0063, "d": 0x0064, "e": 0x0065,
    "f": 0x0066, "g": 0x0067, "h": 0x0068, "i": 0x0069, "j": 0x006A,
    "k": 0x006B, "l": 0x006C, "m": 0x006D, "n": 0x006E, "o": 0x006F,
    "p": 0x0070, "q": 0x0071, "r": 0x0072, "s": 0x0073, "t": 0x0074,
    "u": 0x0075, "v": 0x0076, "w": 0x0077, "x": 0x0078, "y": 0x0079,
    "z": 0x007A,
    "§": 0x00A7, "¨": 0x00A8, "«": 0x00AB, "»": 0x00BB,
    "¼": 0x00BC, "½": 0x00BD, "¿": 0x00BF,
    "À": 0x00C0, "Á": 0x00C1, "Â": 0x00C2, "Ã": 0x00C3,
    "Ä": 0x00C4, "Å": 0x00C5, "Æ": 0x00C6, "Ç": 0x00C7,
    "È": 0x00C8, "É": 0x00C9, "Ê": 0x00CA, "Ë": 0x00CB,
    "Ì": 0x00CC, "Í": 0x00CD, "Î": 0x00CE, "Ï": 0x00CF,
    "Ð": 0x00D0, "Ñ": 0x00D1, "Ò": 0x00D2, "Ó": 0x00D3,
    "Ô": 0x00D4, "Õ": 0x00D5, "Ö": 0x00D6, "×": 0x00D7,
    "Ø": 0x00D8, "Ù": 0x00D9, "Ú": 0x00DA, "Û": 0x00DB,
    "Ü": 0x00DC, "Ý": 0x00DD, "Þ": 0x00DE,
    "à": 0x00E0, "á": 0x00E1, "â": 0x00E2, "ã": 0x00E3,
    "ä": 0x00E4, "å": 0x00E5, "æ": 0x00E6, "ç": 0x00E7,
    "è": 0x00E8, "é": 0x00E9, "ê": 0x00EA, "ë": 0x00EB,
    "ì": 0x00EC, "í": 0x00ED, "î": 0x00EE, "ï": 0x00EF,
    "ð": 0x00F0, "ñ": 0x00F1, "ò": 0x00F2, "ó": 0x00F3,
    "ô": 0x00F4, "õ": 0x00F5, "ö": 0x00F6, "÷": 0x00F7,
    "ø": 0x00F8, "ù": 0x00F9, "ú": 0x00FA, "û": 0x00FB,
    "ü": 0x00FC, "ý": 0x00FD, "þ": 0x00FE, "ÿ": 0x00FF,
    "–": 0x2013, "—": 0x2014, "‘": 0x2018, "’": 0x2019,
    "•": 0x2022, "…": 0x2026,
    "←": 0x2190, "↑": 0x2191, "→": 0x2192, "↓": 0x2193,
    "↔": 0x2194, "↕": 0x2195,
    "☺": 0x263A, "☼": 0x263C, "♀": 0x2640, "♂": 0x2642, "♥": 0x2665,
}

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
# 2. HELPER FUNCTIONS (unchanged)
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
# 3. GLYPH EXTRACTION WITH AUTO-SCALING (unchanged)
# ------------------------------------------------------------------

def extract_glyph_with_bounds(font, unicode_map, char, cell_w, cell_h):
    code = ord(char)
    glyph_name = unicode_map.get(code)
    if glyph_name is None:
        return None, None, 0, 0, None

    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set:
        return None, None, 0, 0, None

    glyph = glyph_set[glyph_name]
    pen = SVGPathPen(glyph_set)
    glyph.draw(pen)
    raw_path = pen.getCommands()
    if not raw_path:
        return "", None, 0, 0, glyph_name

    try:
        bounds = glyph.getBounds()
    except AttributeError:
        bounds = None

    if bounds is not None:
        xMin, yMin, xMax, yMax = bounds
        glyph_w = xMax - xMin
        glyph_h = yMax - yMin
        if glyph_w <= 0 or glyph_h <= 0:
            return raw_path, None, cell_w, cell_h, glyph_name
        margin = 0.1
        avail_w = cell_w * (1 - 2 * margin)
        avail_h = cell_h * (1 - 2 * margin)
        scale = min(avail_w / glyph_w, avail_h / glyph_h)
        if scale > 1.0:
            scale = 1.0
        cx_cell = cell_w / 2
        cy_cell = cell_h / 2
        cx_glyph = (xMin + xMax) / 2
        cy_glyph = (yMin + yMax) / 2
        tx = cx_cell - cx_glyph * scale
        ty = cy_cell - cy_glyph * scale
        transform = f"translate({tx:.2f}, {ty:.2f}) scale({scale:.4f}, {-scale:.4f})"
        return raw_path, transform, cell_w, cell_h, glyph_name

    upem = font['head'].unitsPerEm
    est_w = upem * 0.7
    est_h = upem * 0.7
    scale = min(cell_w / est_w, cell_h / est_h)
    if scale > 1.0:
        scale = 1.0
    transform = f"scale({scale:.4f}, {-scale:.4f})"
    return raw_path, transform, cell_w, cell_h, glyph_name

# ------------------------------------------------------------------
# 4. SVG GENERATOR
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

    try:
        upem = font['head'].unitsPerEm
    except KeyError:
        upem = 1000
    print(f"✓ Font UPEM: {upem}")

    # ------------------------------------------------------------------
    # CELL DIMENSIONS
    # ------------------------------------------------------------------

# ------------------------------------------------------------------
# CELL DIMENSIONS (Updated)
# ------------------------------------------------------------------

BASE_CELL_W = 18
BASE_CELL_H = 48
LABEL_BOX_H = 24
PAD_RIGHT = 12
PAD_BOTTOM = 6          # ← updated: 6
ROW_PAD_LEFT = 24       # ← updated: 24 (2 × 12)
ROW_PAD_TOP = 24        # ← updated: 24 (2 × 12)

def cell_dimensions(scale):
    glyph_w = int(BASE_CELL_W * scale)
    glyph_h = int(BASE_CELL_H * scale)
    label_h = int(LABEL_BOX_H * scale)
    total_h = glyph_h + label_h
    return glyph_w, glyph_h, label_h, total_h

    # ------------------------------------------------------------------
    # EXTRACT GLYPHS
    # ------------------------------------------------------------------

    glyphs_data = {}
    for char, code in CHARACTER_SET.items():
        cell_scale = 1.0
        for _, chars, s in ROWS:
            if char in chars:
                cell_scale = s
                break
        cell_w, cell_h, _, _ = cell_dimensions(cell_scale)
        path, transform, _, _, glyph_name = extract_glyph_with_bounds(
            font, unicode_map, char, cell_w, cell_h
        )
        if path is not None:
            glyphs_data[char] = {
                "char": char,
                "code": code,
                "path": path,
                "transform": transform,
                "group": get_group_for_char(char),
                "glyph_name": glyph_name,
                "cell_w": cell_w,
                "cell_h": cell_h,
            }
        else:
            print(f"⚠️ Skipping '{char}' (U+{code:04X}) - not found in font")

    if not glyphs_data:
        print("❌ No glyphs extracted!")
        return

    print(f"✓ Extracted {len(glyphs_data)} glyphs")

    # ------------------------------------------------------------------
    # BUILD ROWS
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # CALCULATE CANVAS SIZE
    # ------------------------------------------------------------------

    max_width = 0
    for _, chars, scale in built_rows:
        cell_w, _, _, _ = cell_dimensions(scale)
        w = ROW_PAD_LEFT + len(chars) * (cell_w + PAD_RIGHT)
        if w > max_width:
            max_width = w

    # Round up to next multiple of 12
    max_width = ((max_width + 11) // 12) * 12

    total_height = ROW_PAD_TOP
    for _, _, scale in built_rows:
        _, _, _, total_h = cell_dimensions(scale)
        total_height += total_h + PAD_BOTTOM

    print(f"Canvas: {max_width}×{total_height}")
    print(f"Rows: {len(built_rows)}")

    # ------------------------------------------------------------------
    # BUILD SVG – UPDATED COLORS
    # ------------------------------------------------------------------

    output = []
    output.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max_width} {total_height}" width="{max_width}" height="{total_height}">')

    # --- CSS with dark mode colors ---
# --- CSS with light-dark() and grid toggling ---
output.append('  <style>')
output.append('    :root {')
output.append('      /* Enable light/dark mode detection */')
output.append('      color-scheme: light dark;')
output.append('')
output.append('      /* Background */')
output.append('      --bg-color: light-dark(#ffffff, #1a1a1a);')
output.append('')
output.append('      /* Grid colors (relational opacity) */')
output.append('      --fine-grid-color: light-dark(#a0a0a0, #4a4a4a);')
output.append('      --coarse-grid-color: light-dark(#666666, #999999);')
output.append('      --border-color: light-dark(#333333, #cccccc);')
output.append('')
output.append('      /* Grid opacities */')
output.append('      --fine-opacity: 0.25;')
output.append('      --coarse-opacity: 0.35;')
output.append('      --border-opacity: 0.5;')
output.append('')
output.append('      /* Glyph and label colors */')
output.append('      --glyph-color: light-dark(#000000, #f0f0f0);')
output.append('      --label-color: var(--glyph-color);')
output.append('')
output.append('      /* Grid toggling */')
output.append('      --grid-display: block;')
output.append('    }')
output.append('')
output.append('    /* Toggle grid off */')
output.append('    .hide-grid { --grid-display: none; }')
output.append('')
output.append('    svg { background: var(--bg-color); }')
output.append('    .glyph-on { fill: var(--glyph-color); }')
output.append('    .glyph-label { fill: var(--label-color); font-family: "Arial Narrow", "Helvetica Condensed", sans-serif; font-weight: bold; text-anchor: middle; }')
output.append('')
output.append('    /* Grid lines container */')
output.append('    .grid-lines { display: var(--grid-display, block); }')
output.append('    .grid-line { fill: none; }')
output.append('  </style>')

# --- GRID PATTERNS ---
output.append('  <defs>')
output.append('    <!-- 6×6 fine sub‑grid -->')
output.append('    <pattern id="fine-grid" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="translate(24, 24)">')
output.append('      <line x1="0" y1="6" x2="6" y2="6" stroke="var(--fine-grid-color)" stroke-width="0.3" opacity="var(--fine-opacity)"/>')
output.append('      <line x1="6" y1="0" x2="6" y2="6" stroke="var(--fine-grid-color)" stroke-width="0.3" opacity="var(--fine-opacity)"/>')
output.append('    </pattern>')
output.append('')
output.append('    <!-- 24×24 coarse grid (4 × 6) -->')
output.append('    <pattern id="coarse-grid" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="translate(24, 24)">')
output.append('      <!-- Fine grid fills each coarse cell -->')
output.append('      <rect width="24" height="24" fill="url(#fine-grid)"/>')
output.append('      <!-- Coarse grid lines -->')
output.append('      <line x1="0" y1="24" x2="24" y2="24" stroke="var(--coarse-grid-color)" stroke-width="0.8" opacity="var(--coarse-opacity)"/>')
output.append('      <line x1="24" y1="0" x2="24" y2="24" stroke="var(--coarse-grid-color)" stroke-width="0.8" opacity="var(--coarse-opacity)"/>')
output.append('    </pattern>')
output.append('  </defs>')

# --- BACKGROUND ---
output.append('  <!-- Graph paper background (togglable via .hide-grid) -->')
output.append('  <g class="grid-lines">')
output.append(f'    <rect width="100%" height="100%" fill="url(#coarse-grid)"/>')
# Canvas border overlay
output.append(f'    <rect x="0" y="0" width="100%" height="100%" class="grid-line" stroke="var(--border-color)" stroke-width="1" opacity="var(--border-opacity)"/>')
output.append('  </g>')

    # --- DEFS (glyphs) ---
    output.append('  <defs>')
    for char, data in glyphs_data.items():
        code = data["code"]
        path = data["path"]
        group = data["group"]
        transform = data["transform"]
        glyph_name = data["glyph_name"]
        escaped_char = escape_xml_attr(char)
        escaped_group = escape_xml_attr(group)
        escaped_path = escape_xml_attr(path)
        escaped_glyph_name = escape_xml_attr(glyph_name)

        output.append(f'    <!-- Glyph: "{escaped_char}" (U+{code:04X}) glyph: {escaped_glyph_name} -->')
        output.append(f'    <g id="canada-{code}" data-index="{code}" data-group="{escaped_group}" data-name="{escaped_char}">')
        if path and transform:
            output.append(f'      <g transform="{transform}">')
            output.append(f'        <path d="{escaped_path}" class="glyph-on"/>')
            output.append('      </g>')
        elif path:
            output.append(f'      <path d="{escaped_path}" class="glyph-on"/>')
        output.append('    </g>')
    output.append('  </defs>')

    # --- LAYOUT: rows with labels ---
    output.append('  <!-- Sprite Sheet Layout: Row-based grouping with labels -->')
    current_y = ROW_PAD_TOP
    for group_name, chars, scale in built_rows:
        output.append(f'  <!-- ========== ROW: {escape_xml_attr(group_name)} ({len(chars)} chars) scale:{scale} ========== -->')
        row_id = f"row-{group_name.replace(' ', '-').replace('(', '').replace(')', '')}"
        output.append(f'  <g id="{row_id}" data-row="{escape_xml_attr(group_name)}" transform="translate(0, {current_y})">')
        current_x = ROW_PAD_LEFT
        cell_w, cell_h, label_h, total_h = cell_dimensions(scale)

        for char in chars:
            if char in glyphs_data:
                code = glyphs_data[char]["code"]
                escaped_char = escape_xml_attr(char)
                output.append(f'    <use href="#canada-{code}" x="{current_x}" />')
                label_y = cell_h + label_h * 0.6
                font_size = int(label_h * 0.7)
                output.append(f'    <text class="glyph-label" x="{current_x + cell_w/2}" y="{label_y}" font-size="{font_size}">{escaped_char}</text>')
            else:
                output.append(f'    <rect x="{current_x}" y="0" width="{cell_w}" height="{cell_h}" fill="none" stroke="#444444" stroke-width="0.5" />')
                output.append(f'    <text class="glyph-label" x="{current_x + cell_w/2}" y="{cell_h + label_h*0.6}" font-size="{int(label_h*0.7)}">?</text>')
            current_x += cell_w + PAD_RIGHT

        output.append('  </g>')
        current_y += total_h + PAD_BOTTOM

    output.append('</svg>')

    with open("canada_sprite.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"\n[SUCCESS] Generated Canada sprite sheet: canada_sprite.svg")
    print(f"  Rows: {len(built_rows)}")
    print(f"  Total glyphs: {len(glyphs_data)}")
    print(f"  Canvas: {max_width}×{total_height}")
    print(f"  Cell size: {BASE_CELL_W}×{BASE_CELL_H} (1×)")
    print(f"  Label box: {LABEL_BOX_H}px (1×)")
    print(f"  Theme: Dark grey background with off-white text")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 canada-generator.py <font.otf|ttf>")
        sys.exit(1)
    font_path = sys.argv[1]
    generate_sprite_sheet(font_path)
