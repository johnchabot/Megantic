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
    # Safety Interceptor: Automatically resolve multi-character escaping artifacts
    if len(char) > 1: 
        char = "\\" if "\\" in char else char

    code = ord(char)
    glyph_name = unicode_map.get(code)
    
    # 5-Part Tuple Safeguards: Prevents main engine unpacking loops from panicking on unsupported characters
    if glyph_name is None: 
        return None, None, 0, 0, None
        
    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set: 
        return None, None, 0, 0, None

    glyph = glyph_set[glyph_name]
    pen = SVGPathPen(glyph_set)
    glyph.draw(pen)
    raw_path = pen.getCommands()
    
    # Track empty or whitespace characters safely
    if not raw_path: 
        return "", None, 0, 0, glyph_name

    # === PIPELINE-SAFE LEFT-JUSTIFIED EXTRACTION GRAPH MATH ===
    # Preserves authentic font spacing metrics for machine ingestion tracking
    try:
        upem = font['head'].unitsPerEm
    except (KeyError, AttributeError):
        upem = 1000  # Standalone fallback limit default if font metadata header is unreadable

    active_canvas_h = 48   # Strict drawing bounds height for character ascender limits
    
    # Map the typeface internal Em coordinate framework directly onto our 48px baseline sandbox boundary
    scale = active_canvas_h / upem

    # Anchor typographic origin (0,0) exactly at X=18 (margin cushion) and Y=18
    # This pulls the alternative glyph vectors cleanly up to the top-left ceiling of the modules
    tx = 18.0
    ty = 18.0

    # Clean inversion matrix rotates the bottom-to-top font layout into top-to-bottom SVG coordinates
    transform = f"translate({tx:.2f}, {ty:.2f}) scale({scale:.4f}, {-scale:.4f})"
    
    return raw_path, transform, cell_w, cell_h, glyph_name


def generate_sprite_sheet(font_path):
    if not os.path.exists(font_path):
        print(f"❌ Error: File target location does not exist: {font_path}")
        return

    font = TTFont(font_path)
    cmap = font.getBestCmap()
    unicode_map = {code: name for code, name in cmap.items()}

    # === MICRO-PATCH: 12-GRID BLUEPRINT LAYOUT CONSTANTS ===
    GRID_UNIT = 6          # The absolute atomic structural division
    BASE_CELL_W = 72       # Macro enclosure width pitch (12 * GRID_UNIT)
    BASE_CELL_H = 72       # Macro enclosure height pitch (12 * GRID_UNIT)
    label_box_h = 12       # Proportional 1:12 metadata label tracking height
    
    PAD_RIGHT = 0          # Monospaced columns step strictly at 72 intervals
    PAD_BOTTOM = 24        # Vertical cushion padding between row sets
    ROW_PAD_LEFT = 72      # Canvas outer frame left margin offset width
    ROW_PAD_TOP = 108      # Canvas outer frame top margin offset height


        # === SURGICAL SAFETNET PATCH ===

    glyphs_data = {}

    for char, code in CHARACTER_SET.items():
        res = extract_glyph_with_bounds(font, unicode_map, char, BASE_CELL_W, BASE_CELL_H)
        
        # Verify we received a safe, unpackable 5-part data sequence
        if res is None or not isinstance(res, tuple) or len(res) < 5:
            continue
            
        # Bypass direct variable unpacking to eliminate NoneType crashing
        if res[0] is not None and res[0] != "":
            glyphs_data[char] = {
                "char": char,
                "code": code,
                "path": res[0],
                "transform": res[1],
                "group": get_group_for_char(char),
                "glyph_name": res[4],
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
        # FIXED: This block is now perfectly indented inside the tracking iteration loop!
        if w > max_width:
            max_width = w
            
    max_width = ((max_width + 11) // 12) * 12

    total_height = ROW_PAD_TOP
    for _, _ in built_rows:
        total_height += BASE_CELL_H + PAD_BOTTOM
    total_height += (ROW_PAD_TOP - PAD_BOTTOM)

    
#CHUNK2 This section handles the generation of your verbose XML stream builder array, the modern light/dark embedded styles, the recursive atomic-unit and macro-enclosure defs, and the automated loop calculations for your cross-cutting 2:1 perimeter ticks.

    # === DETONATION-PROOF RUNTIME STRING STITCHING ===
    xml_header = "<?xml version=" + '"1.0" ' + 'encoding="UTF-8"?>'
    
    # We break up the strings manually so the script cannot truncate the domain names
    svg_tag = "<svg xmlns=" + '"http://www.w3.org/2000/svg" '
    svg_tag += "xmlns:xlink=" + '"http://www.w3.org/1999/xlink" '
    svg_tag += f'viewBox="0 0 {max_width} {total_height}" width="{max_width}" height="{total_height}">'
    
    out = []
    out.append(xml_header)
    out.append(svg_tag)
  
    # CSS Custom Theme Injector (Browser responsive overrides)
    out.append('  <style type="text/css">')
    out.append('    /* Default Global Layout Styles (Light Mode Base) */')
    out.append('    .technical-notation { font-family: "SF Mono", "Courier New", Courier, monospace; font-size: 5px; font-weight: bold; fill: #475569; text-anchor: middle; }')
    out.append('    .blueprint-title-main { font-family: "SF Mono", "Courier New", Courier, monospace; font-size: 12px; font-weight: bold; fill: #1e2930; text-anchor: start; }')
    out.append('    .blueprint-title-sub { font-family: "SF Mono", "Courier New", Courier, monospace; font-size: 6px; font-weight: 500; fill: #475569; opacity: 0.7; text-anchor: start; }')
    out.append('')
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


    # === OPERATION 1: UN-STRETCHED 6x6 CONTROL PLANE PATTERNS ===
    out.append('  <defs>')
    out.append('    <!-- 1. THE ATOMIC UNIT (Base 6x6 Subdivision Grid Mesh) -->')
    out.append('    <pattern id="atomic-unit" width="6" height="6" patternUnits="userSpaceOnUse" class="control-plane">')
    out.append('      <line x1="0" y1="6" x2="6" y2="6" stroke="#a3b8c2" stroke-width="0.3" opacity="0.22" class="atomic-axis"/>')
    out.append('      <line x1="6" y1="0" x2="6" y2="6" stroke="#a3b8c2" stroke-width="0.3" opacity="0.22" class="atomic-axis"/>')
    out.append('    </pattern>')
    out.append('')
    out.append('    <!-- 2. THE MACRO ENCLOSURE (Recursive 72x72 Cartesian Module Viewport) -->')
    out.append('    <pattern id="macro-enclosure" width="72" height="72" patternUnits="userSpaceOnUse" class="control-plane">')
    out.append('      <rect width="72" height="72" fill="url(#atomic-unit)"/>')
    out.append('      <line x1="0" y1="72" x2="72" y2="72" stroke="#5c727d" stroke-width="0.8" opacity="0.40" class="macro-axis"/>')
    out.append('      <line x1="72" y1="0" x2="72" y2="72" stroke="#5c727d" stroke-width="0.8" opacity="0.40" class="macro-axis"/>')
    out.append('    </pattern>')
    out.append('  </defs>')

    # LAYER 1: BACKDROP PLANE & HARDCODED PERIMETER FRAME LOOPS (IrfanView Safe)
    # Added the class tracker to link your blueprint background to your CSS on/off toggle
    out.append('  <g id="construction-plane" class="control-plane">')
    out.append('    <rect width="100%" height="100%" fill="url(#macro-enclosure)"/>')
    active_w = max_width - 144
    active_h = total_height - 180
    out.append(f'    <rect x="72" y="108" width="{active_w}" height="{active_h}" fill="none" stroke="#1e2930" stroke-width="1.2" opacity="0.65" class="perimeter-frame"/>')

    # Programmatic Loops: Safely outputs discrete cross-cutting border ticks along boundaries
    for tx in range(72, max_width - 71, 72):
        out.append(f'    <line x1="{tx}" y1="104" x2="{tx}" y2="112" stroke="#1e2930" stroke-width="1.0" opacity="0.65" class="tick-mark"/>')
        out.append(f'    <line x1="{tx}" y1="{total_height - 76}" x2="{tx}" y2="{total_height - 68}" stroke="#1e2930" stroke-width="1.0" opacity="0.65" class="tick-mark"/>')
    for ty in range(108, total_height - 71, 72):
        out.append(f'    <line x1="68" y1="{ty}" x2="76" y2="{ty}" stroke="#1e2930" stroke-width="1.0" opacity="0.65" class="tick-mark"/>')
        out.append(f'    <line x1="{max_width - 76}" y1="{ty}" x2="{max_width - 68}" y2="{ty}" stroke="#1e2930" stroke-width="1.0" opacity="0.65" class="tick-mark"/>')
    out.append('  </g>')


    # === REPAIRED METADATA HEADER ASSEMBLY ===

    internal_font_name = "Alternative Custom Typeface"
    try:
        name_table = font['name']
        full_name_record = name_table.getName(4, 3, 1, 0x409) or name_table.getName(4, 1, 0, 0)
        if full_name_record:
            internal_font_name = full_name_record.toUnicode()
    except Exception:
        pass

    # === SURGICAL FIX: HEADER HEIGHT SHIFT ===
    out.append('  <!-- Proportional Engineering Title Block (12px/6px system rules) -->')
    # Change the Y value from 54 to 36 to slide the text safely up into the top padding zone
    out.append('  <g id="blueprint-metadata-header" transform="translate(72, 36)">')
    escaped_filename = escape_xml_attr(os.path.basename(font_path))
    escaped_fontname = escape_xml_attr(internal_font_name)
    out.append(f'    <text x="0" y="0" class="blueprint-title-main">TYPOGRAPHIC SPECIMEN MATRIX // SYSTEM NAME: {escaped_fontname}</text>')
    out.append(f'    <text x="0" y="12" class="blueprint-title-sub">SOURCE FILE: {escaped_filename} / WORKSPACE: 72px MONOSPACED MODULES / MATRIX SCALE RATIO: 1:12 / RESOLVED ASSETS: {len(glyphs_data)}</text>')
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

    # === FIXED SPECIMEN WORKSPACE MATRIX STACK ENTRY ===
    out.append('  <g id="typographic-specimen-matrix" transform="translate(72, 108)">')
    current_y = 0

    
    for group_name, chars in built_rows:
        out.append(f'    <!-- SPECIMEN TRACK GROUP: {escape_xml_attr(group_name)} -->')
        row_base_id = f"row-{group_name.replace(' ', '-').replace('(', '').replace(')', '')}"
        
        # A. Render the left-justified glyph outlines line
        out.append(f'    <g id="{row_base_id}-glyphs" data-row="{escape_xml_attr(group_name)}" transform="translate(0, {current_y})">')
        current_x = 0
        for char in chars:
            code = glyphs_data[char]["code"]
            out.append(f'      <use xlink:href="#canada-{code}" x="{current_x}" y="0"/>')
            current_x += BASE_CELL_W
        out.append('    </g>')
        
        # B. Render separate dual-notation metadata labels line (Inherits the grid control plane visibility setting)
        out.append(f'    <g id="{row_base_id}-labels" data-row="{escape_xml_attr(group_name)}" transform="translate(0, {current_y + 60})" class="control-plane">')
        current_x = 0
        for char in chars:
            code = glyphs_data[char]["code"]
            friendly_name = glyphs_data[char]["glyph_name"]
            label_x = current_x + (BASE_CELL_W / 2)
            
            # Stack Line 1: Standard Hexadecimal Unicode notation (U+XXXX)
            out.append(f'      <text x="{label_x}" y="-2" class="technical-notation">U+{code:04X}</text>')
            # Stack Line 2: The True PostScript "Friendly Design Name" string literal
            out.append(f'      <text x="{label_x}" y="6" class="technical-notation">{escape_xml_attr(friendly_name)}</text>')
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








