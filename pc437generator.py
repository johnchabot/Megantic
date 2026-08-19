#!/usr/bin/env python3
"""
generate_cp437_sprite.py

Generates cp437_sprite.svg – a 32×8 grid of all 256 CP437 glyphs.
Each glyph is drawn using a single <path> with run-length encoding
(M x,y h width) for maximum efficiency while remaining human-editable.

The SVG is fully self-contained with all metadata as data-* attributes.

Run: python3 generate_cp437_sprite.py
Output: cp437_sprite.svg
"""

import os
import urllib.request

# ======================================================================
# 1. FONT DATA LOADER (Authentic IBM VGA 8x16 ROM)
# ======================================================================

def get_font_bytes():
    """Returns the 4096-byte VGA 8x16 font bitmap."""
    local_file = "vga8x16.bin"
    if os.path.exists(local_file):
        with open(local_file, "rb") as f:
            data = f.read()
            if len(data) == 4096:
                print(f"✓ Loaded font from local '{local_file}'")
                return data
            else:
                print(f"Warning: '{local_file}' is not 4096 bytes. Downloading...")

    url = "https://cdn.jsdelivr.net/npm/pcface/out/oldschool-pc-8x16.font"
    print(f"Downloading font from {url} ...")
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            if len(data) != 4096:
                raise RuntimeError(f"Downloaded file size is {len(data)} bytes, expected 4096.")
            with open(local_file, "wb") as f:
                f.write(data)
            print(f"✓ Font downloaded and saved to '{local_file}'")
            return data
    except Exception as e:
        raise RuntimeError(f"Failed to download font: {e}\nPlease manually place a 4096-byte VGA font at '{local_file}'.")


# ======================================================================
# 2. METADATA DICTIONARY (Parent Groups, Subranges, Names, Descriptors)
# ======================================================================

# We define subrange descriptors as a mapping from (parent_group, subrange) -> description
# Then each character maps to (parent_group, subrange, name, descriptor)

SUB_RANGES = {
    ("Control and Standard ASCII", "0"): "Null",
    ("Control and Standard ASCII", "01–06"): "Face icons and card suits",
    ("Control and Standard ASCII", "07–10"): "Bell, backspace, tab, line feed",
    ("Control and Standard ASCII", "11–12"): "Male, female symbols",
    ("Control and Standard ASCII", "13–31"): "Musical notes, arrows, and separators",
    ("Printable ASCII", "32–64"): "Space, punctuation, 0-9, special symbols",
    ("Printable ASCII", "65–90"): "Uppercase English letters from A to Z",
    ("Printable ASCII", "91–126"): "Brackets, symbols, and lowercase letters a-z",
    ("Extended and International Characters", "127–165"): "House icon, accented European vowels/consonants, and currency/math",
    ("Extended and International Characters", "166–223"): "Box-drawing lines, corners, intersections, and shaded fill blocks",
    ("Extended and International Characters", "224–254"): "Greek characters and math symbols",
    ("Extended and International Characters", "255"): "Non-breaking space",
}

# Character mapping: index -> (parent_group, subrange, name, descriptor)
CHAR_META = {}

# 0
CHAR_META[0] = ("Control and Standard ASCII", "0", "NUL", "Null Character")

# 1–6 (Face icons and card suits)
CHAR_META[1] = ("Control and Standard ASCII", "01–06", "WHITE SMILEY FACE", "Used as a player character in early rogue-like games.")
CHAR_META[2] = ("Control and Standard ASCII", "01–06", "BLACK SMILEY FACE", "Often used for enemy sprites or NPCs.")
CHAR_META[3] = ("Control and Standard ASCII", "01–06", "HEART", "Represented player health, lives, or romance text games.")
CHAR_META[4] = ("Control and Standard ASCII", "01–06", "DIAMOND", "Standard card suit for text-based casino games.")
CHAR_META[5] = ("Control and Standard ASCII", "01–06", "CLUB", "Card suit icon.")
CHAR_META[6] = ("Control and Standard ASCII", "01–06", "SPADE", "Card suit icon.")

# 7–10 (Bell, backspace, tab, line feed)
CHAR_META[7] = ("Control and Standard ASCII", "07–10", "BULLET", "Used for UI option lists or projectile weapon sprites.")
CHAR_META[8] = ("Control and Standard ASCII", "07–10", "INVERSE BULLET", "Used for toggled UI selections.")
CHAR_META[9] = ("Control and Standard ASCII", "07–10", "EMPTY CIRCLE", "Used for unchecked radio buttons.")
CHAR_META[10] = ("Control and Standard ASCII", "07–10", "INVERSE CIRCLE", "Used for checked radio buttons or target cursors.")

# 11–12 (Male, female symbols)
CHAR_META[11] = ("Control and Standard ASCII", "11–12", "MALE SYMBOL", "Used in early RPG character creation screens.")
CHAR_META[12] = ("Control and Standard ASCII", "11–12", "FEMALE SYMBOL", "Used in early RPG character creation screens.")

# 13–31 (Musical notes, arrows, and separators)
CHAR_META[13] = ("Control and Standard ASCII", "13–31", "EIGHTH NOTE", "Indicated background music files or text prompts.")
CHAR_META[14] = ("Control and Standard ASCII", "13–31", "BEAMED EIGHTH NOTES", "Audio setting indicators.")
CHAR_META[15] = ("Control and Standard ASCII", "13–31", "SUN/GEAR", "Represented brightness settings or daytime states.")
CHAR_META[16] = ("Control and Standard ASCII", "13–31", "FORWARD POINTER", "Used as menu selectors or media play buttons.")
CHAR_META[17] = ("Control and Standard ASCII", "13–31", "BACKWARD POINTER", "Menu navigators or media rewind buttons.")
CHAR_META[18] = ("Control and Standard ASCII", "13–31", "UP/DOWN ARROW", "Indicated that a text window could be scrolled vertically.")
CHAR_META[19] = ("Control and Standard ASCII", "13–31", "DOUBLE EXCLAMATION", "Critical alerts or text-adventure action prompts.")
CHAR_META[20] = ("Control and Standard ASCII", "13–31", "PARAGRAPH/PILCROW", "Word-processing layout markers.")
CHAR_META[21] = ("Control and Standard ASCII", "13–31", "SECTION SIGN", "Form mapping for legal or structured text blocks.")
CHAR_META[22] = ("Control and Standard ASCII", "13–31", "LOWER HALF BLOCK", "Block-art rendering to build faux-graphic landscapes.")
CHAR_META[23] = ("Control and Standard ASCII", "13–31", "UP ARROW WITH BASE", "Window scrolling indicator.")
CHAR_META[24] = ("Control and Standard ASCII", "13–31", "UP ARROW", "In-game directions and UI navigation.")
CHAR_META[25] = ("Control and Standard ASCII", "13–31", "DOWN ARROW", "In-game directions and UI navigation.")
CHAR_META[26] = ("Control and Standard ASCII", "13–31", "RIGHT ARROW", "Directional navigation pointer.")
CHAR_META[27] = ("Control and Standard ASCII", "13–31", "LEFT ARROW", "Directional navigation pointer.")
CHAR_META[28] = ("Control and Standard ASCII", "13–31", "RIGHT ANGLE/FILE SEP", "Form formatting and geometric data math.")
CHAR_META[29] = ("Control and Standard ASCII", "13–31", "LEFT/RIGHT ARROW", "Horizontal scrolling layout indicator.")
CHAR_META[30] = ("Control and Standard ASCII", "13–31", "UP TRIANGLE", "Menu scroll up indicators.")
CHAR_META[31] = ("Control and Standard ASCII", "13–31", "DOWN TRIANGLE", "Menu scroll down indicators.")

# 32–64 (Space, punctuation, 0-9, special symbols)
# We'll fill this programmatically
ascii_names_32_64 = [
    ("SPACE", "The invisible character you type most."),
    ("!", "Exclamation mark. Shout it!"),
    ("\"", "Double quote. For dialog."),
    ("#", "Hash. Number sign."),
    ("$", "Dollar. Money money money."),
    ("%", "Percent. Modulo operator."),
    ("&", "Ampersand. The 'and' sign."),
    ("'", "Single quote. Apostrophe."),
    ("(", "Left parenthesis. Open."),
    (")", "Right parenthesis. Close."),
    ("*", "Asterisk. Star. Wildcard."),
    ("+", "Plus. Add it up."),
    (",", "Comma. Pause."),
    ("-", "Minus. Hyphen."),
    (".", "Period. Dot. Full stop."),
    ("/", "Slash. Forward slash."),
    ("0", "Zero. The void digit."),
    ("1", "One. The loneliest number."),
    ("2", "Two."),
    ("3", "Three."),
    ("4", "Four."),
    ("5", "Five."),
    ("6", "Six."),
    ("7", "Seven."),
    ("8", "Eight."),
    ("9", "Nine."),
    (":", "Colon. Time and ratios."),
    (";", "Semicolon. Winking."),
    ("<", "Less than."),
    ("=", "Equals. Assignment."),
    (">", "Greater than."),
    ("?", "Question mark. Huh?"),
    ("@", "At sign. Addresses."),
]
for idx, (name, desc) in enumerate(ascii_names_32_64, start=32):
    CHAR_META[idx] = ("Printable ASCII", "32–64", name, desc)

# 65–90 (Uppercase English letters from A to Z)
ascii_names_65_90 = [
    ("A", "The first letter. The one that starts 'AARDVARK'."),
    ("B", "B. For 'BEE'."),
    ("C", "C. For 'CAT'."),
    ("D", "D. For 'DOG'."),
    ("E", "E. For 'ELEPHANT'."),
    ("F", "F. For 'FOX'."),
    ("G", "G. For 'GOLF'."),
    ("H", "H. For 'HOTEL'."),
    ("I", "I. For 'INDIA'."),
    ("J", "J. For 'JULIET'."),
    ("K", "K. For 'KILO'."),
    ("L", "L. For 'LIMA'."),
    ("M", "M. For 'MIKE'."),
    ("N", "N. For 'NOVEMBER'."),
    ("O", "O. For 'OSCAR'."),
    ("P", "P. For 'PAPA'."),
    ("Q", "Q. For 'QUEBEC'."),
    ("R", "R. For 'ROMEO'."),
    ("S", "S. For 'SIERRA'."),
    ("T", "T. For 'TANGO'."),
    ("U", "U. For 'UNIFORM'."),
    ("V", "V. For 'VICTOR'."),
    ("W", "W. For 'WHISKEY'."),
    ("X", "X. For 'XRAY'."),
    ("Y", "Y. For 'YANKEE'."),
    ("Z", "Z. For 'ZULU'."),
]
for idx, (name, desc) in enumerate(ascii_names_65_90, start=65):
    CHAR_META[idx] = ("Printable ASCII", "65–90", name, desc)

# 91–126 (Brackets, symbols, and lowercase letters a-z)
ascii_names_91_126 = [
    ("LEFT BRACKET", "The opening square bracket."),
    ("BACKSLASH", "Backslash. Escape."),
    ("RIGHT BRACKET", "The closing square bracket."),
    ("CARET", "Caret. XOR."),
    ("UNDERSCORE", "Underscore. For snake_case."),
    ("BACKTICK", "Backtick. Grave."),
    ("a", "Lowercase A. For 'apple'."),
    ("b", "Lowercase B."),
    ("c", "Lowercase C."),
    ("d", "Lowercase D."),
    ("e", "Lowercase E."),
    ("f", "Lowercase F."),
    ("g", "Lowercase G."),
    ("h", "Lowercase H."),
    ("i", "Lowercase I."),
    ("j", "Lowercase J."),
    ("k", "Lowercase K."),
    ("l", "Lowercase L."),
    ("m", "Lowercase M."),
    ("n", "Lowercase N."),
    ("o", "Lowercase O."),
    ("p", "Lowercase P."),
    ("q", "Lowercase Q."),
    ("r", "Lowercase R."),
    ("s", "Lowercase S."),
    ("t", "Lowercase T."),
    ("u", "Lowercase U."),
    ("v", "Lowercase V."),
    ("w", "Lowercase W."),
    ("x", "Lowercase X."),
    ("y", "Lowercase Y."),
    ("z", "Lowercase Z."),
    ("LEFT BRACE", "Left brace."),
    ("PIPE", "Pipe. Vertical bar."),
    ("RIGHT BRACE", "Right brace."),
    ("TILDE", "Tilde. Home directory."),
]
for idx, (name, desc) in enumerate(ascii_names_91_126, start=91):
    CHAR_META[idx] = ("Printable ASCII", "91–126", name, desc)

# 127 (House)
CHAR_META[127] = ("Extended and International Characters", "127–165", "HOUSE", "The classic IBM PC 'home' icon.")

# 128–165 (Accented vowels/consonants, currency/math)
accented_names = [
    ("C-CEDILLA", "C-cedilla. For 'façade'."),
    ("U-UMLAUT", "U-umlaut. For 'über'."),
    ("E-ACUTE", "E-acute. For 'café'."),
    ("A-CIRCUMFLEX", "A-circumflex. For 'château'."),
    ("A-UMLAUT", "A-umlaut. For 'Märchen'."),
    ("A-GRAVE", "A-grave. For 'voilà'."),
    ("A-RING", "A-ring. For 'Ångström'."),
    ("C-CEDILLA-LOWER", "C-cedilla (lower)."),
    ("E-CIRCUMFLEX", "E-circumflex."),
    ("E-UMLAUT", "E-umlaut."),
    ("E-GRAVE", "E-grave."),
    ("I-UMLAUT", "I-umlaut."),
    ("I-CIRCUMFLEX", "I-circumflex."),
    ("I-GRAVE", "I-grave."),
    ("A-UMLAUT-UPPER", "A-umlaut (upper)."),
    ("A-RING-UPPER", "A-ring (upper)."),
    ("E-ACUTE-UPPER", "E-acute (upper)."),
    ("AE-LIGATURE-LOWER", "AE-ligature (lower)."),
    ("AE-LIGATURE-UPPER", "AE-ligature (upper)."),
    ("O-CIRCUMFLEX", "O-circumflex."),
    ("O-UMLAUT", "O-umlaut."),
    ("O-GRAVE", "O-grave."),
    ("U-CIRCUMFLEX", "U-circumflex."),
    ("U-GRAVE", "U-grave."),
    ("Y-UMLAUT", "Y-umlaut."),
    ("O-UMLAUT-UPPER", "O-umlaut (upper)."),
    ("U-UMLAUT-UPPER", "U-umlaut (upper)."),
    ("CENT", "Cent sign."),
    ("POUND", "Pound sterling."),
    ("YEN", "Yen sign."),
    ("PESETA", "Peseta sign."),
    ("FLORIN", "Florin."),
    ("A-ACUTE", "A-acute."),
    ("I-ACUTE", "I-acute."),
    ("O-ACUTE", "O-acute."),
    ("U-ACUTE", "U-acute."),
    ("N-TILDE", "N-tilde."),
    ("N-TILDE-UPPER", "N-tilde (upper)."),
    ("FEMININE-ORDINAL", "Feminine ordinal."),
    ("MASCULINE-ORDINAL", "Masculine ordinal."),
    ("INVERTED-QUESTION", "Inverted question."),
    ("NOT-SIGN", "Not sign."),
    ("LOGICAL-NOT", "Logical not."),
    ("ONE-HALF", "One-half."),
    ("ONE-QUARTER", "One-quarter."),
    ("INVERTED-EXCLAMATION", "Inverted exclamation."),
    ("LEFT-GUILLEMET", "Left guillemet."),
    ("RIGHT-GUILLEMET", "Right guillemet."),
]
for idx, (name, desc) in enumerate(accented_names, start=128):
    CHAR_META[idx] = ("Extended and International Characters", "127–165", name, desc)

# 166–223 (Box-drawing lines, corners, intersections, shaded fill blocks)
line_names = [
    ("VERTICAL-LINE", "Vertical line."),
    ("RIGHT-T", "Right T."),
    ("RIGHT-T-DOUBLE", "Right T (double)."),
    ("RIGHT-T-DOUBLE-2", "Right T (double)."),
    ("CORNER-DOUBLE", "Corner (double)."),
    ("CORNER-DOUBLE-2", "Corner (double)."),
    ("CROSS-DOUBLE", "Cross (double)."),
    ("DOUBLE-VERTICAL", "Double vertical."),
    ("TOP-RIGHT-CORNER", "Top right corner."),
    ("BOTTOM-RIGHT-CORNER", "Bottom right corner."),
    ("CORNER-DOUBLE-3", "Corner (double)."),
    ("CORNER-DOUBLE-4", "Corner (double)."),
    ("TOP-RIGHT-CORNER-2", "Top right corner."),
    ("BOTTOM-LEFT-CORNER", "Bottom left corner."),
    ("BOTTOM-T", "Bottom T."),
    ("TOP-T", "Top T."),
    ("LEFT-T", "Left T."),
    ("HORIZONTAL-LINE", "Horizontal line."),
    ("CROSS", "Cross."),
    ("LEFT-T-DOUBLE", "Left T (double)."),
    ("LEFT-T-DOUBLE-2", "Left T (double)."),
    ("BOTTOM-LEFT-DOUBLE", "Bottom left (double)."),
    ("TOP-LEFT-DOUBLE", "Top left (double)."),
    ("BOTTOM-T-DOUBLE", "Bottom T (double)."),
    ("TOP-T-DOUBLE", "Top T (double)."),
    ("LEFT-T-DOUBLE-3", "Left T (double)."),
    ("DOUBLE-HORIZONTAL", "Double horizontal."),
    ("DOUBLE-CROSS", "Double cross."),
    ("BOTTOM-T-DOUBLE-2", "Bottom T (double)."),
    ("BOTTOM-T-DOUBLE-3", "Bottom T (double)."),
    ("TOP-T-DOUBLE-2", "Top T (double)."),
    ("TOP-T-DOUBLE-3", "Top T (double)."),
    ("CORNER-DOUBLE-5", "Corner (double)."),
    ("CORNER-DOUBLE-6", "Corner (double)."),
    ("CORNER-DOUBLE-7", "Corner (double)."),
    ("CORNER-DOUBLE-8", "Corner (double)."),
    ("CROSS-DOUBLE-2", "Cross (double)."),
    ("CROSS-DOUBLE-3", "Cross (double)."),
    ("BOTTOM-RIGHT-CORNER-2", "Bottom right corner."),
    ("TOP-LEFT-CORNER", "Top left corner."),
    ("FULL-BLOCK", "Full block. Solid!"),
    ("LOWER-HALF-BLOCK", "Lower half block."),
    ("LEFT-HALF-BLOCK", "Left half block."),
    ("RIGHT-HALF-BLOCK", "Right half block."),
    ("UPPER-HALF-BLOCK", "Upper half block."),
    # --- Missing 211–223 ---
    ("BOX-DRAWING-211", "Box drawing character 211."),
    ("BOX-DRAWING-212", "Box drawing character 212."),
    ("BOX-DRAWING-213", "Box drawing character 213."),
    ("BOX-DRAWING-214", "Box drawing character 214."),
    ("BOX-DRAWING-215", "Box drawing character 215."),
    ("BOX-DRAWING-216", "Box drawing character 216."),
    ("BOX-DRAWING-217", "Box drawing character 217."),
    ("BOX-DRAWING-218", "Box drawing character 218."),
    ("BOX-DRAWING-219", "Box drawing character 219."),
    ("BOX-DRAWING-220", "Box drawing character 220."),
    ("BOX-DRAWING-221", "Box drawing character 221."),
    ("BOX-DRAWING-222", "Box drawing character 222."),
    ("BOX-DRAWING-223", "Box drawing character 223."),
]
for idx, (name, desc) in enumerate(line_names, start=166):
    CHAR_META[idx] = ("Extended and International Characters", "166–223", name, desc)

# 224–254 (Greek characters and math symbols)
greek_math_names = [
    ("ALPHA", "Alpha. The beginning."),
    ("ESZETT", "Eszett. Double S."),
    ("GAMMA", "Gamma. Third letter."),
    ("PI", "Pi. For circles and calculus."),
    ("SIGMA-UPPER", "Sigma. Summation."),
    ("SIGMA-LOWER", "Sigma (lower). Standard deviation."),
    ("MU", "Mu. Micro."),
    ("TAU", "Tau. Time constant."),
    ("PHI-UPPER", "Phi. The golden ratio."),
    ("THETA", "Theta. Angle."),
    ("OMEGA", "Omega. The end."),
    ("DELTA-LOWER", "Delta. Change."),
    ("INFINITY", "Infinity. The endless loop."),
    ("PHI-LOWER", "Phi (lower)."),
    ("EPSILON", "Epsilon."),
    ("INTERSECTION", "Intersection. The overlap."),
    ("IDENTICAL-TO", "Identical to. Triple bar."),
    ("PLUS-MINUS", "Plus/minus. Margin of error."),
    ("GREATER-EQUAL", "Greater than or equal."),
    ("LESS-EQUAL", "Less than or equal."),
    ("TOP-INTEGRAL", "Top integral."),
    ("BOTTOM-INTEGRAL", "Bottom integral."),
    ("DIVISION", "Division sign. Split the loot."),
    ("APPROXIMATELY", "Approximately. Close enough."),
    ("DEGREE", "Degree. Temperature."),
    ("BULLET-OPERATOR", "Bullet operator."),
    ("MIDDLE-DOT", "Middle dot."),
    ("SQUARE-ROOT", "Square root."),
    ("SUPERSCRIPT-N", "Superscript n."),
    ("SQUARED", "Squared."),
    ("BLACK-SQUARE", "Black square. Game over."),
]
for idx, (name, desc) in enumerate(greek_math_names, start=224):
    CHAR_META[idx] = ("Extended and International Characters", "224–254", name, desc)

# 255 (NBSP)
CHAR_META[255] = ("Extended and International Characters", "255", "NBSP", "Invisible. Used for sneaky filenames that look blank.")


# ======================================================================
# 3. PATH GENERATOR (Run-Length Encoding)
# ======================================================================

def generate_path_for_glyph(font_data, char_idx, scale=4):
    """
    Returns a string containing the SVG path 'd' attribute for the glyph.
    Uses run-length encoding: M x,y h width for each run of lit pixels.
    The 9th column is duplicated from the 8th (VGA behavior).
    """
    commands = []
    for row in range(16):
        byte = font_data[char_idx * 16 + row]
        # Build 9-bit row: bits 0..7 (LSB = leftmost) + duplicate bit 7
        bits = []
        for col in range(8):
            bits.append(1 if (byte & (1 << col)) else 0)
        bits.append(bits[7])  # duplicate the 8th column

        # Scan for runs of 1s
        x = 0
        while x < 9:
            if bits[x] == 1:
                start_x = x
                while x < 9 and bits[x] == 1:
                    x += 1
                # Emit: M{start_x*scale},{row*scale} h{(x-start_x)*scale}
                commands.append(f"M{start_x * scale},{row * scale}h{(x - start_x) * scale}")
            else:
                x += 1
    if not commands:
        # Empty glyph (shouldn't happen, but just in case)
        return ""
    return " ".join(commands)


# ======================================================================
# 4. SVG GENERATOR
# ======================================================================

def generate_svg(font_data):
    scale = 4
    cols = 32
    rows = 8
    bitmap_w = 9  # 8 + duplicated 9th
    bitmap_h = 16

    svg_width = cols * bitmap_w * scale
    svg_height = rows * bitmap_h * scale

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')

    # ---- Header comments ----
    lines.append('  <!--')
    lines.append('    IBM Code Page 437 character set (256-glyph)')
    lines.append('    Presented in VGA 8×16 goodness')
    lines.append('    BIOS interrupt details (INT 9h/16h)')
    lines.append('    Renders standard 80×25 text modes and higher-resolution graphics layouts')
    lines.append('')
    lines.append('    Categories:')
    lines.append('    ===========')
    lines.append('    Control   | 0-31, 127, 255   | NUL, SOH, BEL, CR, ESC, DEL, etc.')
    lines.append('    ASCII     | 32-126           | Space, punctuation, A-Z, a-z, 0-9, brackets, symbols')
    lines.append('    Accented  | 128-175          | European accented vowels & consonants')
    lines.append('    Block     | 176-178          | Shading blocks (light, medium, dark)')
    lines.append('    Line      | 179-223          | Box-drawing lines, corners, intersections')
    lines.append('    Greek     | 224-237          | Greek letters (alpha, beta, pi, etc.)')
    lines.append('    Math      | 238-254          | Math symbols (degree, +/- , division, etc.)')
    lines.append('    Symbol    | 1-6, 9-12, 14-26 | Musical notes, arrows, card suits, smileys, house')
    lines.append('')
    lines.append('    Control and Standard ASCII (0–31):')
    lines.append('    0: Null')
    lines.append('    01–06: Face icons and card suits')
    lines.append('    07–10: Bell, backspace, tab, line feed')
    lines.append('    11–12: Male, female symbols')
    lines.append('    13–31: Musical notes, arrows, and separators')
    lines.append('')
    lines.append('    Printable ASCII (32–126):')
    lines.append('    32–64: Space, punctuation, numbers 0–9, and [uppercase A-Z (cleanup: these are 65–90)]')
    lines.append('    91–126: Brackets, symbols, and lowercase letters a–z')
    lines.append('')
    lines.append('    Extended and International Characters (127–255):')
    lines.append('    127–165: House icon, accented European vowels/consonants, and currency/math')
    lines.append('    166–223: Box-drawing lines, corners, intersections, and shaded fill blocks')
    lines.append('    224–254: Greek characters and math symbols')
    lines.append('    255: Non-breaking space')
    lines.append('  -->')
    lines.append('')

    lines.append('  <rect width="100%" height="100%" fill="#000000"/>')
    lines.append('  <defs>')

    # ---- Generate glyph definitions ----
    for char_idx in range(256):
        parent_group, subrange, name, desc = CHAR_META[char_idx]
        subrange_desc = SUB_RANGES.get((parent_group, subrange), "")

        # Inline comment
        lines.append(f'    <!-- pc437-{char_idx} ({parent_group} | {subrange} | {name}) -->')

        # Build path
        path_data = generate_path_for_glyph(font_data, char_idx, scale)

        # Attributes
        attrs = [
            f'id="pc437-{char_idx}"',
            f'data-index="{char_idx}"',
            f'data-parent-group="{parent_group}"',
            f'data-subrange="{subrange}"',
            f'data-subrange-descriptor="{subrange_desc}"',
            f'data-name="{name}"',
            f'data-descriptor="{desc}"',
        ]
        lines.append(f'    <g {" ".join(attrs)}>')
        if path_data:
            lines.append(f'      <path d="{path_data}" fill="#FFFFFF"/>')
        # If empty path (shouldn't happen), we just leave the group empty
        lines.append('    </g>')

    lines.append('  </defs>')
    lines.append('')

    # ---- Sprite Sheet Layout: 32 columns x 8 rows ----
    lines.append('  <!-- Sprite Sheet Layout: 32 columns x 8 rows -->')
    for char_idx in range(256):
        row = char_idx // cols
        col = char_idx % cols
        x = col * bitmap_w * scale
        y = row * bitmap_h * scale
        parent_group, subrange, name, desc = CHAR_META[char_idx]
        lines.append(f'  <use href="#pc437-{char_idx}" x="{x}" y="{y}" /> <!-- pc437-{char_idx} ({parent_group} | {subrange} | {name}) -->')

    lines.append('</svg>')
    return "\n".join(lines)


# ======================================================================
# 5. MAIN
# ======================================================================

if __name__ == "__main__":
    try:
        font = get_font_bytes()
        print("Generating SVG...")
        svg_content = generate_svg(font)
        output_file = "cp437_sprite.svg"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"✓ Successfully generated '{output_file}'")
        print(f"  Dimensions: 32x8 grid, {32 * 9 * 4} x {8 * 16 * 4} pixels")
        print(f"  File size: {os.path.getsize(output_file):,} bytes")
    except Exception as e:
        print(f"Error: {e}")
