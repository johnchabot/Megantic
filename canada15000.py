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
    # SAFETY CLIP: Automatically resolve any escaped multi-character strings
    if len(char) > 1: 
        char = "\\" if "\\" in char else char

    # === FULL RESTORATION OF ORIGINAL STRUCTURAL CONVENTIONS ===
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
    if value is None: return ""
    return str(value).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;")


def extract_glyph_with_bounds(font, unicode_map, char, cell_w, cell_h):
    if len(char) > 1: 
        char = "\\" if "\\" in char else char

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

    try:
        upem = font['head'].unitsPerEm
    except (KeyError, AttributeError):
        upem = 1000

    # Scale the font's internal Em square to fit a maximum width boundary of 60px (5 grid blocks)
    max_active_w = 60.0
    scale = max_active_w / upem

    # Anchor typographic origin (0,0) exactly at X=12 and Y=72 inside the cell box
    tx = 12.0
    ty = 72.0

    transform = f"translate({tx:.2f}, {ty:.2f}) scale({scale:.4f}, {-scale:.4f})"
    return raw_path, transform, cell_w, cell_h, glyph_name



def generate_sprite_sheet(font_path):
    if not os.path.exists(font_path):
        print(f"❌ Error: File target location does not exist: {font_path}")
        return

    font = TTFont(font_path)
    cmap = font.getBestCmap()
    unicode_map = {code: name for code, name in cmap.items()}

    # === DYNAMIC-LINKED 12-GRID UNIFORM WORKSPACE CONSTANTS ===
    GRID_UNIT = 12         # Grid line interval changed to 12 for a bigger, clearer 6x6 mesh
    BASE_CELL_W = 72       # Monospace cell module width (6 grid blocks wide)
    BASE_CELL_H = 96       # Monospace cell module height (8 grid blocks high: 6 glyph + 2 label)
    label_box_h = 24       # Dedicated footer box lane height for dual-line annotations
    
    PAD_RIGHT = 0          
    PAD_BOTTOM = 36        # Deep cushion padding between separate row sets prevents crowding
    ROW_PAD_LEFT = 72      # Master canvas outer perimeter frame left offset margin
    ROW_PAD_TOP = 144      # Master canvas outer perimeter frame top offset margin

    glyphs_data = {}
    for char, code in CHARACTER_SET.items():
        res = extract_glyph_with_bounds(font, unicode_map, char, BASE_CELL_W, BASE_CELL_H)
        if res is None or not isinstance(res, tuple) or len(res) < 5:
            continue
        path, transform, _, _, glyph_name = res
        if path is not None:
            glyphs_data[char] = {
                "char": char, "code": code, "path": path, "transform": transform,
                "group": get_group_for_char(char), "glyph_name": glyph_name if glyph_name else "glyph"
            }

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
        if w > max_width: max_width = w
            
    max_width = ((max_width + 11) // 12) * 12

    # Calculate overall document height using our alternating 96px row module rhythms
    total_height = ROW_PAD_TOP
    for _, chars in built_rows:
        total_height += BASE_CELL_H + PAD_BOTTOM
    total_height += (ROW_PAD_TOP - PAD_BOTTOM)

    

    # === REPAIRED DETONATION-PROOF RUNTIME STITCHING OVRERIDE ===
    # Hardcodes the XML delimiters using raw hex characters to completely block text-input truncation filters
    xml_header = "\x3c?xml version=\x221.0\x22 encoding=\x22UTF-8\x22?\x3e"
    
    # We break up the standard strings manually to force the browser to resolve the full literal namespaces
    svg_tag = "\x3csvg xmlns=" + '"http://w3.org" '
    svg_tag += "xmlns:xlink=" + '"http://w3.org" '
    svg_tag += f'viewBox="0 0 {max_width} {total_height}" width="{max_width}" height="{total_height}"\x3e'
    
    out = []
    out.append(xml_header)
    out.append(svg_tag)

    out.append('  <style type="text/css">')
    out.append('    .technical-notation { font-family: "SF Mono", "Courier New", Courier, monospace; font-size: 5px; font-weight: bold; fill: #475569; text-anchor: middle; }')
    out.append('    .blueprint-title-main { font-family: "SF Mono", "Courier New", Courier, monospace; font-size: 12px; font-weight: bold; fill: #1e2930; text-anchor: start; }')
    out.append('    .blueprint-title-sub { font-family: "SF Mono", "Courier New", Courier, monospace; font-size: 6px; font-weight: 500; fill: #475569; opacity: 0.7; text-anchor: start; }')
    out.append('    @media (prefers-color-scheme: dark) {')
    out.append('      svg { background: #161a1d !important; }')
    out.append('      .atomic-axis { stroke: #2c3539 !important; opacity: 0.35 !important; }')
    out.append('      .macro-axis { stroke: #48565e !important; opacity: 0.55 !important; }')
    out.append('      .perimeter-frame { stroke: #8ba1ad !important; opacity: 0.80 !important; }')
    out.append('      .tick-mark { stroke: #8ba1ad !important; opacity: 0.65 !important; }')
    out.append('      .glyph-on { fill: #f5f7fa !important; }')
    out.append('      .technical-notation { fill: #94a3b8 !important; }')
    out.append('      .blueprint-title-main { fill: #94a3b8 !important; }')
    out.append('      .blueprint-title-sub { fill: #64748b !important; }')
    out.append('    }')
    out.append('  </style>')

    out.append('  <defs>')
    out.append('    <!-- Sharp un-stretched graph paper: 12px increments frame a clean 6x6 grid across cells -->')
    out.append('    <pattern id="macro-enclosure" width="12" height="12" patternUnits="userSpaceOnUse" class="control-plane">')
    out.append('      <line x1="0" y1="12" x2="12" y2="12" stroke="#5c727d" stroke-width="0.4" opacity="0.25" class="atomic-axis"/>')
    out.append('      <line x1="12" y1="0" x2="12" y2="12" stroke="#5c727d" stroke-width="0.4" opacity="0.25" class="atomic-axis"/>')
    out.append('    </pattern>')
    out.append('  </defs>')

    # LAYER 1: BACKDROP CONTROL PLANE GRID (Dotted lines and center dot removed)
    out.append('  <g id="construction-plane" class="control-plane">')
    out.append('    <rect width="100%" height="100%" fill="url(#macro-enclosure)"/>')
    active_w = max_width - 144
    active_h = total_height - 216
    out.append(f'    <rect x="72" y="108" width="{active_w}" height="{active_h}" fill="none" stroke="#1e2930" stroke-width="1.2" opacity="0.65" class="perimeter-frame"/>')

    # Programmatic Loops: Outward-Only perimeter notches (start at border line and draw outwards)
    for tx in range(72, max_width - 71, 72):
        out.append(f'    <line x1="{tx}" y1="100" x2="{tx}" y2="108" stroke="#1e2930" stroke-width="1.0" opacity="0.65" class="tick-mark"/>')
        out.append(f'    <line x1="{tx}" y1="{total_height - 108}" x2="{tx}" y2="{total_height - 100}" stroke="#1e2930" stroke-width="1.0" opacity="0.65" class="tick-mark"/>')
    for ty in range(108, total_height - 107, 72):
        out.append(f'    <line x1="64" y1="{ty}" x2="72" y2="{ty}" stroke="#1e2930" stroke-width="1.0" opacity="0.65" class="tick-mark"/>')
        out.append(f'    <line x1="{max_width - 72}" y1="{ty}" x2="{max_width - 64}" y2="{ty}" stroke="#1e2930" stroke-width="1.0" opacity="0.65" class="tick-mark"/>')
    out.append('  </g>')

    internal_font_name = "Alternative Custom Typeface"
    try:
        name_table = font['name']
        full_name_record = name_table.getName(4, 3, 1, 0x409) or name_table.getName(4, 1, 0, 0)
        if full_name_record: internal_font_name = full_name_record.toUnicode()
    except Exception: pass

    # TITLE METADATA BLOCK ASSEMBLY (Floats safely above our Y = 108 top perimeter border line)
    out.append('  <g id="blueprint-metadata-header" transform="translate(72, 54)">')
    escaped_filename = escape_xml_attr(os.path.basename(font_path))
    escaped_fontname = escape_xml_attr(internal_font_name)
    out.append(f'    <text x="0" y="0" class="blueprint-title-main">TYPOGRAPHIC SPECIMEN MATRIX // SYSTEM NAME: {escaped_fontname}</text>')
    out.append(f'    <text x="0" y="12" class="blueprint-title-sub">SOURCE FILE: {escaped_filename} / WORKSPACE: MONOSPACED 72px MODULES / CODES RESOLVED: {len(glyphs_data)}</text>')
    out.append('  </g>')

    out.append('  <defs>')
    for char, data in glyphs_data.items():
        code = data["code"]
        path = data["path"]
        group = data["group"]
        transform = data["transform"]
        escaped_char = escape_xml_attr(char)
        escaped_group = escape_xml_attr(group)
        escaped_path = escape_xml_attr(path)
        out.append(f'    <g id="canada-{code}" data-index="{code}" data-group="{escaped_group}" data-name="{escaped_char}">')
        if path and transform:
            out.append(f'      <g transform="{transform}"><path d="{escaped_path}" class="glyph-on"/></g>')
        elif path:
            out.append(f'      <path d="{escaped_path}" class="glyph-on"/>')
        out.append('    </g>')
    out.append('  </defs>')

    # LAYER 3: ALTERNATING CONTROL PLANE NOTATIONS TRACKS (Tied to the Control Plane visibility class)
    current_y = 0
    for group_name, chars in built_rows:
        row_base_id = f"row-{group_name.replace(' ', '-').replace('(', '').replace(')', '')}"
        out.append(f'    <g id="{row_base_id}-labels" transform="translate(72, {108 + current_y})" class="control-plane">')
        current_x = 0
        for char in chars:
            code = glyphs_data[char]["code"]
            friendly_name = glyphs_data[char]["glyph_name"]
            label_x = current_x + (BASE_CELL_W / 2)
            
            # Text notations sit down cleanly inside their separate vertical lanes at the floor of the cell block
            out.append(f'      <text x="{label_x}" y="82" class="technical-notation">U+{code:04X}</text>')
            out.append(f'      <text x="{label_x}" y="92" class="technical-notation">{escape_xml_attr(friendly_name)}</text>')
            current_x += BASE_CELL_W
        out.append('    </g>')
        current_y += BASE_CELL_H + PAD_BOTTOM

    # LAYER 4: PURE SPRITE DATA TRACKS (Printed LAST at the absolute bottom of the file structure)
    out.append('  <g id="typographic-specimen-matrix" transform="translate(72, 108)">')
    current_y = 0
    for group_name, chars in built_rows:
        row_base_id = f"row-{group_name.replace(' ', '-').replace('(', '').replace(')', '')}"
        out.append(f'    <g id="{row_base_id}-glyphs" data-row="{escape_xml_attr(group_name)}" transform="translate(0, {current_y})">')
        current_x = 0
        for char in chars:
            code = glyphs_data[char]["code"]
            out.append(f'      <use xlink:href="#canada-{code}" x="{current_x}" y="0"/>')
            current_x += BASE_CELL_W
        out.append('    </g>')
        current_y += BASE_CELL_H + PAD_BOTTOM
    out.append('  </g>')
    out.append('</svg>')

    with open("canada_sprite.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"\n[SUCCESS] Matrix Compiled Flawlessly: canada_sprite.svg ({max_width}x{total_height})")

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








