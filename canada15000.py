#Chunk 1: Script Header & Canvas Dimension Logic
#!/usr/bin/env python3
"""
canada-pipeline.py (CHUNK 1 OF 3)
Maintains all original structural mechanics, explicit character mapping,
verbose text line generation, and architectural loops intact.
"""

import sys
import os

try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
except ImportError:
    print("❌ Error: fonttools library not found on this system.")
    print("Please resolve the dependency by executing: pip install fonttools")
    sys.exit(1)

# Explicit character set dictionary mapping
CHARACTER_SET = {
    " ": 0x0020, "!": 0x0021, '"': 0x0022, "#": 0x0023, "$": 0x0024,
    "%": 0x0025, "&": 0x0026, "'": 0x0027, "(": 0x0028, ")": 0x0029,
    "*": 0x002A, "+": 0x002B, ",": 0x002C, "-": 0x002D, ".": 0x002E,
    "/": 0x002F, ":": 0x003A, ";": 0x003B, "<": 0x003C, "=": 0x003D,
    ">": 0x003E, "?": 0x003F, "@": 0x0040, "[": 0x005B, "\\\\": 0x005C,
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
    ("Space", [" "]),
    ("Keyboard (1)", ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/"]),
    ("Digits", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]),
    ("Keyboard (2)", [":", ";", "<", "=", ">", "?", "@"]),
    ("Uppercase", ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]),
    ("Keyboard (3)", ["[", "\\\\", "]", "^", "_", "`"]),
    ("Lowercase", ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]),
    ("Keyboard (4)", ["{", "|", "}", "~"]),
    ("ASCII+Weird", ["§", "¨", "«", "»", "¼", "½", "¿"]),
    ("French/Spanish Upper", ["À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï", "Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "Þ"]),
    ("French/Spanish Lower", ["à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï", "ð", "ñ", "ò", "ó", "ô", "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ"]),
    ("Symbols", ["–", "—", "‘", "’", "•", "…", "←", "↑", "→", "↓", "↔", "↕", "☺", "☼", "♀", "♂", "♥"]),
]

def get_group_for_char(char):
    if char == " ": return "Space"
    elif char.isdigit(): return "Digits"
    elif char.isupper(): return "Uppercase"
    elif char.islower(): return "Lowercase"
    elif char in ["§", "¨", "«", "»", "¼", "½", "¿"]: return "ASCII+Weird"
    elif ord(char) in range(0x00C0, 0x00FF + 1): return "French/Spanish"
    elif ord(char) in [0x2013, 0x2014, 0x2018, 0x2019, 0x2022, 0x2026, 0x2190, 0x2191, 0x2192, 0x2193, 0x2194, 0x2195, 0x263A, 0x263C, 0x2640, 0x2642, 0x2665]: return "Symbols"
    else: return "Keyboard"

def escape_xml_attr(value):
    if value is None: return ""
    return str(value).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;")

def extract_glyph_with_bounds(font, unicode_map, char, cell_w, cell_h):
    code = ord(char)
    glyph_name = unicode_map.get(code)
    if glyph_name is None: return None, None, 0, 0, None
    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set: return None, None, 0, 0, None
    glyph = glyph_set[glyph_name]
    pen = SVGPathPen(glyph_set)
    glyph.draw(pen)
    raw_path = pen.getCommands()
    if not raw_path: return "", None, 0, 0, glyph_name
    try: bounds = glyph.getBounds()
    except AttributeError: bounds = None

    active_box_w, active_box_h = 48, 48
    if bounds is not None:
        xMin, yMin, xMax, yMax = bounds
        glyph_w, glyph_h = xMax - xMin, yMax - yMin
        if glyph_w <= 0 or glyph_h <= 0: return raw_path, None, cell_w, cell_h, glyph_name
        margin = 0.05
        scale = min((active_box_w * (1 - 2 * margin)) / glyph_w, (active_box_h * (1 - 2 * margin)) / glyph_h)
        if scale > 1.0: scale = 1.0
        tx = ((cell_w - glyph_w * scale) / 2) - xMin * scale
        ty = ((cell_h - 12 - glyph_h * scale) / 2) + yMax * scale + 6
        return raw_path, f"translate({tx:.2f}, {ty:.2f}) scale({scale:.4f}, {-scale:.4f})", cell_w, cell_h, glyph_name

    upem = font['head'].unitsPerEm
    scale = min(active_box_w / (upem * 0.7), active_box_h / (upem * 0.7))
    if scale > 1.0: scale = 1.0
    return raw_path, f"translate(12, 48) scale({scale:.4f}, {-scale:.4f})", cell_w, cell_h, glyph_name

def generate_sprite_sheet(font_path):
    if not os.path.exists(font_path):
        print(f"❌ Error: File target location does not exist: {font_path}")
        return

    font = TTFont(font_path)
    cmap = font.getBestCmap()
    unicode_map = {code: name for code, name in cmap.items()}

    BASE_CELL_W, BASE_CELL_H, label_box_h = 72, 72, 12
    PAD_BOTTOM, ROW_PAD_LEFT, ROW_PAD_TOP = 12, 72, 72

    glyphs_data = {}
    for char, code in CHARACTER_SET.items():
        path, transform, _, _, glyph_name = extract_glyph_with_bounds(font, unicode_map, char, BASE_CELL_W, BASE_CELL_H)
        if path is not None:
            glyphs_data[char] = {"char": char, "code": code, "path": path, "transform": transform, "group": get_group_for_char(char), "glyph_name": glyph_name}

    built_rows = []
    for group_name, chars in ROWS:
        filtered = [c for c in chars if c in glyphs_data]
        if filtered: built_rows.append((group_name, filtered))

    if not built_rows:
        print("❌ Script termination: No valid typeface vector arrays resolved.")
        return

    max_width = 0
    for _, chars in built_rows:
        w = ROW_PAD_LEFT + len(chars) * BASE_CELL_W + ROW_PAD_LEFT
        # FIXED: This block is now perfectly indented inside the tracking iteration loop!
        if w > max_width:
            max_width = w
            
    max_width = ((max_width + 11) // 12) * 12

    total_height = ROW_PAD_TOP
    for _, _ in built_rows:
        total_height += BASE_CELL_H + PAD_BOTTOM
    total_height += (ROW_PAD_TOP - PAD_BOTTOM)


#CHUNK2 This section handles the generation of your verbose XML stream builder array, the modern light/dark embedded styles, the recursive atomic-unit and macro-enclosure defs, and the automated loop calculations for your cross-cutting 2:1 perimeter ticks.
    # --- VERBOSE XML COMPILATION STREAM WRITER ARRAY ---
    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append(f'<svg xmlns="http://w3.org" xmlns:xlink="http://w3.org" viewBox="0 0 {max_width} {total_height}" width="{max_width}" height="{total_height}">')
    
    # Inline Stylesheet Overrides Layer (Modern Web Browser Theme Engines)
    out.append('  <style type="text/css">')
    out.append('    @media (prefers-color-scheme: dark) {')
    out.append('      svg { background: #161a1d !important; }')
    out.append('      .atomic-axis { stroke: #2c3539 !important; opacity: 0.35 !important; }')
    out.append('      .macro-axis { stroke: #48565e !important; opacity: 0.55 !important; }')
    out.append('      .perimeter-frame { stroke: #8ba1ad !important; opacity: 0.80 !important; }')
    out.append('      .tick-mark { stroke: #8ba1ad !important; opacity: 0.65 !important; }')
    out.append('      .glyph-on { fill: #f5f7fa !important; }')
    out.append('      .technical-notation { fill: #94a3b8 !important; }')
    out.append('    }')
    out.append('    .technical-notation { font-family: "SF Mono", "Courier New", Courier, monospace; font-size: 6px; font-weight: 500; text-anchor: middle; }')
    out.append('  </style>')

    # CORE RECURSIVE LAYOUT DEFINITIONS (IrfanView Safe Fallbacks)
    out.append('  <defs>')
    out.append('    <!-- 1. THE ATOMIC UNIT (Base 6x6 Subdivision Grid) -->')
    out.append('    <pattern id="atomic-unit" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="translate(72, 72)">')
    out.append('      <line x1="0" y1="6" x2="6" y2="6" stroke="#a3b8c2" stroke-width="0.3" opacity="0.22" class="atomic-axis"/>')
    out.append('      <line x1="6" y1="0" x2="6" y2="6" stroke="#a3b8c2" stroke-width="0.3" opacity="0.22" class="atomic-axis"/>')
    out.append('    </pattern>')
    out.append('')
    out.append('    <!-- 2. THE MACRO ENCLOSURE (Recursive 72x72 Cartesian Module) -->')
    out.append('    <pattern id="macro-enclosure" width="72" height="72" patternUnits="userSpaceOnUse" patternTransform="translate(72, 72)">')
    out.append('      <rect width="72" height="72" fill="url(#atomic-unit)"/>')
    out.append('      <line x1="0" y1="36" x2="72" y2="36" stroke="#5c727d" stroke-width="0.5" stroke-dasharray="1,2" opacity="0.45" class="macro-axis"/>')
    out.append('      <line x1="36" y1="0" x2="36" y2="72" stroke="#5c727d" stroke-width="0.5" stroke-dasharray="1,2" opacity="0.45" class="macro-axis"/>')
    out.append('      <line x1="0" y1="72" x2="72" y2="72" stroke="#5c727d" stroke-width="1.0" opacity="0.40" class="macro-axis"/>')
    out.append('      <line x1="72" y1="0" x2="72" y2="72" stroke="#5c727d" stroke-width="1.0" opacity="0.40" class="macro-axis"/>')
    out.append('      <circle cx="0" cy="0" r="0.8" fill="#5c727d" opacity="0.6"/>')
    out.append('      <circle cx="36" cy="36" r="0.6" fill="#5c727d" opacity="0.4"/>')
    out.append('    </pattern>')
    out.append('  </defs>')

    # LAYER 1: THE BACKGROUND STRUCTURAL CONSTRUCTION PLANE
    out.append('  <g id="construction-plane">')
    out.append('    <rect width="100%" height="100%" fill="url(#macro-enclosure)"/>')
    
    # Trace absolute bounding boundary perimeter frame
    active_w = max_width - 144
    active_h = total_height - 144
    out.append(f'    <rect x="72" y="72" width="{active_w}" height="{active_h}" fill="none" stroke="#1e2930" stroke-width="1.2" opacity="0.65" class="perimeter-frame"/>')

    # AUTOMATED SYSTEM BORDER TICK COMPILING LOOPS (2:1 Proportional Axis Marks)
    for tx in range(72, max_width - 71, 72):
        out.append(f'    <line x1="{tx}" y1="68" x2="{tx}" y2="76" stroke="#1e2930" stroke-width="1.0" opacity="0.60" class="tick-mark"/>')
        out.append(f'    <line x1="{tx}" y1="{total_height - 76}" x2="{tx}" y2="{total_height - 68}" stroke="#1e2930" stroke-width="1.0" opacity="0.60" class="tick-mark"/>')
    for ty in range(72, total_height - 71, 72):
        out.append(f'    <line x1="68" y1="{ty}" x2="76" y2="{ty}" stroke="#1e2930" stroke-width="1.0" opacity="0.60" class="tick-mark"/>')
        out.append(f'    <line x1="{max_width - 76}" y1="{ty}" x2="{max_width - 68}" y2="{ty}" stroke="#1e2930" stroke-width="1.0" opacity="0.60" class="tick-mark"/>')
    out.append('  </g>')

# chunk3
# This section stores the inline path dictionary database entries inside <defs>, maps out the active character specimen row groups with their proportional metadata labels, commits the stream data array to canada_sprite.svg, and wraps up the main execution block.

    # DEFS ARCHIVE DICTIONARY: INDEPENDENT DATA GLYPH BLOCKS STORAGE
    out.append('  <defs>')
    for char, data in glyphs_data.items():
        code = data["code"]
        path = data["path"]
        group = data["group"]
        transform = data["transform"]
        
        escaped_char = escape_xml_attr(char)
        escaped_group = escape_xml_attr(group)
        escaped_path = escape_xml_attr(path)

        out.append(f'    <!-- Vector Database Entry: "{escaped_char}" (U+{code:04X}) -->')
        out.append(f'    <g id="canada-{code}" data-index="{code}" data-group="{escaped_group}" data-name="{escaped_char}">')
        if path and transform:
            out.append(f'      <g transform="{transform}">')
            out.append(f'        <path d="{escaped_path}" fill="#000000" class="glyph-on"/>')
            out.append('      </g>')
        elif path:
            out.append(f'      <path d="{escaped_path}" fill="#000000" class="glyph-on"/>')
        out.append('    </g>')
    out.append('  </defs>')

    # LAYER 2: SYSTEMATIC MONOSPACED GLYPH DISPLAY LAYER
    out.append('  <g id="typographic-specimen-matrix" transform="translate(72, 72)">')
    current_y = 0
    
    for group_name, chars in built_rows:
        out.append(f'    <!-- Category Sector Stream: {escape_xml_attr(group_name)} -->')
        row_id_string = f"row-{group_name.replace(' ', '-').replace('(', '').replace(')', '')}"
        out.append(f'    <g id="{row_id_string}" data-row="{escape_xml_attr(group_name)}" transform="translate(0, {current_y})">')
        
        current_x = 0
        for char in chars:
            code = glyphs_data[char]["code"]
            out.append(f'      <use href="#canada-{code}" x="{current_x}" y="0"/>')
            
            # Place explicit metadata notation text on target character row baseline
            label_x = current_x + (BASE_CELL_W / 2)
            label_y = BASE_CELL_H - 4
            out.append(f'      <text x="{label_x}" y="{label_y}" fill="#475569" class="technical-notation">U+{code:04X}</text>')
            
            current_x += BASE_CELL_W

        out.append('    </g>')
        current_y += BASE_CELL_H + PAD_BOTTOM
        
    out.append('  </g>')
    out.append('</svg>')

    # Stream out final document file array block
    with open("canada_sprite.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"\n[SUCCESS] Matrix Compiled Flawlessly: canada_sprite.svg ({max_width}x{total_height})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 canada-pipeline.py <font.otf|ttf>")
        sys.exit(1)
    # Execution entry targets the first command line file path string variable argument index
    generate_sprite_sheet(sys.argv[1])
