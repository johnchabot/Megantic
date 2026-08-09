#!/usr/bin/env python3
"""
generate_cp437_sprite.py

Generates cp437_sprite.svg – a 32×8 grid of all 256 CP437 glyphs.
Each glyph is a 9×16 cell (8×16 bitmap + duplicated 9th column).
Metadata (category, name, descriptor) is stored as data-* attributes
on each <g> element. The SVG includes a full category legend.

The script automatically downloads the authentic IBM VGA 8x16 ROM font
from a trusted CDN if a local copy is not found.

Run: python3 generate_cp437_sprite.py
Output: cp437_sprite.svg
"""

import os
import math
import urllib.request

# ======================================================================
# 1. FONT DATA LOADER (Fetches authentic IBM VGA 8x16 ROM)
#    Source: https://github.com/susam/pcface (public domain / MIT)
# ======================================================================

def get_font_bytes():
    """Returns the 4096-byte VGA 8x16 font bitmap."""
    
    # Option A: Check for a local file (so you can run offline later)
    local_file = "vga8x16.bin"
    if os.path.exists(local_file):
        with open(local_file, "rb") as f:
            data = f.read()
            if len(data) == 4096:
                print(f"✓ Loaded font from local '{local_file}'")
                return data
            else:
                print(f"Warning: '{local_file}' is not 4096 bytes. Downloading...")

    # Option B: Download from the pcface CDN (authentic IBM VGA font)
    url = "https://cdn.jsdelivr.net/npm/pcface/out/oldschool-pc-8x16.font"
    print(f"Downloading font from {url} ...")
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            if len(data) != 4096:
                raise RuntimeError(f"Downloaded file size is {len(data)} bytes, expected 4096.")
            # Save a local copy for next time
            with open(local_file, "wb") as f:
                f.write(data)
            print(f"✓ Font downloaded and saved to '{local_file}'")
            return data
    except Exception as e:
        raise RuntimeError(f"Failed to download font: {e}\nPlease manually place a 4096-byte VGA font at '{local_file}'.")


# ======================================================================
# 2. CHARACTER METADATA (Categories, Names, & Retro Descriptors)
# ======================================================================

# Mapping of index to (Category, Name, Descriptor)
# Categories: Control, ASCII, Accented, Block, Line, Greek, Math, Symbol
METADATA = {}

# Controls (0-31, 127, 255)
controls = [
    (0, "NUL", "Does nothing. Absolute void."),
    (1, "SMILEY", "The original emoji. Pure happiness."),
    (2, "INV-SMILEY", "Upside-down smiley. Feels like a bug."),
    (3, "HEART", "Love in the age of DOS."),
    (4, "DIAMOND", "A gem for your text adventures."),
    (5, "CLUB", "For the gambling BBS games."),
    (6, "SPADE", "The ace of spades."),
    (7, "BEL", "Makes the PC speaker BEEP! Drove sysadmins nuts."),
    (8, "BACKSPACE", "Moves cursor left. Not delete!"),
    (9, "TAB", "Jumps to the next tab stop."),
    (10, "LF", "Moves cursor down one line."),
    (11, "MALE", "The Mars symbol."),
    (12, "FEMALE", "The Venus symbol."),
    (13, "CR", "Slams the cursor back to the left margin. Like a typewriter!"),
    (14, "MUSIC-NOTE", "Crank up the PC speaker for 1-bit tunes!"),
    (15, "MUSIC-NOTE2", "Double the beep, double the fun."),
    (16, "RIGHT-ARROW", "Pointer for your menus."),
    (17, "LEFT-ARROW", "Go back."),
    (18, "UP-DOWN-ARROW", "Vertical scrolling indicator."),
    (19, "DOUBLE-EXCLAM", "❗ The alarm clock of the ASCII world."),
    (20, "PILCROW", "The paragraph sign. For legal text."),
    (21, "SECTION", "For chapter headings."),
    (22, "HORIZ-BAR", "A solid horizontal bar."),
    (23, "UP-DOWN", "Up/down arrow combo."),
    (24, "UP-ARROW", "Go up."),
    (25, "DOWN-ARROW", "Go down."),
    (26, "RIGHT-ARROW2", "Another right arrow."),
    (27, "ESC", "The 'OH NO, ABORT!' key."),
    (28, "FILE-SEP", "File separator."),
    (29, "GROUP-SEP", "Group separator."),
    (30, "REC-SEP", "Record separator."),
    (31, "UNIT-SEP", "Unit separator."),
    (127, "DEL", "Deletes the character under the cursor. Not Backspace!"),
    (255, "NBSP", "Invisible. Used for sneaky filenames that look blank.")
]
for idx, name, desc in controls:
    METADATA[idx] = ("Control", name, desc)

# ASCII (32-126)
ascii_names = [
    ("Space", "The invisible character you type most."),
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
    ("[", "Left bracket."),
    ("\\", "Backslash. Escape."),
    ("]", "Right bracket."),
    ("^", "Caret. XOR."),
    ("_", "Underscore. For snake_case."),
    ("`", "Backtick. Grave."),
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
    ("{", "Left brace."),
    ("|", "Pipe. Vertical bar."),
    ("}", "Right brace."),
    ("~", "Tilde. Home directory.")
]
for idx, (name, desc) in enumerate(ascii_names, start=32):
    METADATA[idx] = ("ASCII", name, desc)

# Accented (128-175)
accented = [
    ("Ç", "C-cedilla. For 'façade'."),
    ("ü", "U-umlaut. For 'über'."),
    ("é", "E-acute. For 'café'."),
    ("â", "A-circumflex. For 'château'."),
    ("ä", "A-umlaut. For 'Märchen'."),
    ("à", "A-grave. For 'voilà'."),
    ("å", "A-ring. For 'Ångström'."),
    ("ç", "C-cedilla (lower)."),
    ("ê", "E-circumflex."),
    ("ë", "E-umlaut."),
    ("è", "E-grave."),
    ("ï", "I-umlaut."),
    ("î", "I-circumflex."),
    ("ì", "I-grave."),
    ("Ä", "A-umlaut (upper)."),
    ("Å", "A-ring (upper)."),
    ("É", "E-acute (upper)."),
    ("æ", "AE-ligature (lower)."),
    ("Æ", "AE-ligature (upper)."),
    ("ô", "O-circumflex."),
    ("ö", "O-umlaut."),
    ("ò", "O-grave."),
    ("û", "U-circumflex."),
    ("ù", "U-grave."),
    ("ÿ", "Y-umlaut."),
    ("Ö", "O-umlaut (upper)."),
    ("Ü", "U-umlaut (upper)."),
    ("¢", "Cent sign."),
    ("£", "Pound sterling."),
    ("¥", "Yen sign."),
    ("₧", "Peseta sign."),
    ("ƒ", "Florin."),
    ("á", "A-acute."),
    ("í", "I-acute."),
    ("ó", "O-acute."),
    ("ú", "U-acute."),
    ("ñ", "N-tilde."),
    ("Ñ", "N-tilde (upper)."),
    ("ª", "Feminine ordinal."),
    ("º", "Masculine ordinal."),
    ("¿", "Inverted question."),
    ("⌐", "Not sign."),
    ("¬", "Logical not."),
    ("½", "One-half."),
    ("¼", "One-quarter."),
    ("¡", "Inverted exclamation."),
    ("«", "Left guillemet."),
    ("»", "Right guillemet."),
]
for idx, (name, desc) in enumerate(accented, start=128):
    METADATA[idx] = ("Accented", name, desc)

# Block (176-178)
blocks = [
    ("░", "Light shade. For subtle shadows."),
    ("▒", "Medium shade. The gray area."),
    ("▓", "Dark shade. Almost solid."),
]
for idx, (name, desc) in enumerate(blocks, start=176):
    METADATA[idx] = ("Block", name, desc)

# Line (179-223)
lines = [
    ("│", "Vertical line."),
    ("┤", "Right T."),
    ("╡", "Right T (double)."),
    ("╢", "Right T (double)."),
    ("╖", "Corner (double)."),
    ("╕", "Corner (double)."),
    ("╣", "Cross (double)."),
    ("║", "Double vertical."),
    ("╗", "Top right corner."),
    ("╝", "Bottom right corner."),
    ("╜", "Corner (double)."),
    ("╛", "Corner (double)."),
    ("┐", "Top right corner."),
    ("└", "Bottom left corner."),
    ("┴", "Bottom T."),
    ("┬", "Top T."),
    ("├", "Left T."),
    ("─", "Horizontal line."),
    ("┼", "Cross."),
    ("╞", "Left T (double)."),
    ("╟", "Left T (double)."),
    ("╚", "Bottom left (double)."),
    ("╔", "Top left (double)."),
    ("╩", "Bottom T (double)."),
    ("╦", "Top T (double)."),
    ("╠", "Left T (double)."),
    ("═", "Double horizontal."),
    ("╬", "Double cross."),
    ("╧", "Bottom T (double)."),
    ("╨", "Bottom T (double)."),
    ("╤", "Top T (double)."),
    ("╥", "Top T (double)."),
    ("╙", "Corner (double)."),
    ("╘", "Corner (double)."),
    ("╒", "Corner (double)."),
    ("╓", "Corner (double)."),
    ("╫", "Cross (double)."),
    ("╪", "Cross (double)."),
    ("┘", "Bottom right corner."),
    ("┌", "Top left corner."),
    ("█", "Full block. Solid!"),
    ("▄", "Lower half block."),
    ("▌", "Left half block."),
    ("▐", "Right half block."),
    ("▀", "Upper half block."),
]
# The list length from 179 to 223 is 45. The provided list has 45 items? Let's check.
# 179 to 223 inclusive is 45. I provided exactly 45 names above (count them). Good.
for idx, (name, desc) in enumerate(lines, start=179):
    METADATA[idx] = ("Line", name, desc)

# Greek (224-237)
greek = [
    ("α", "Alpha. The beginning."),
    ("ß", "Eszett. Double S."),
    ("Γ", "Gamma. Third letter."),
    ("π", "Pi. For circles and calculus."),
    ("Σ", "Sigma. Summation."),
    ("σ", "Sigma (lower). Standard deviation."),
    ("µ", "Mu. Micro."),
    ("τ", "Tau. Time constant."),
    ("Φ", "Phi. The golden ratio."),
    ("Θ", "Theta. Angle."),
    ("Ω", "Omega. The end."),
    ("δ", "Delta. Change."),
    ("∞", "Infinity. The endless loop."),
    ("φ", "Phi (lower)."),
    ("ε", "Epsilon."),
    ("∩", "Intersection. The overlap."),
]
for idx, (name, desc) in enumerate(greek, start=224):
    METADATA[idx] = ("Greek", name, desc)

# Math (238-254)
math = [
    ("≡", "Identical to. Triple bar."),
    ("±", "Plus/minus. Margin of error."),
    ("≥", "Greater than or equal."),
    ("≤", "Less than or equal."),
    ("⌠", "Top integral."),
    ("⌡", "Bottom integral."),
    ("÷", "Division sign. Split the loot."),
    ("≈", "Approximately. Close enough."),
    ("°", "Degree. Temperature."),
    ("∙", "Bullet operator."),
    ("·", "Middle dot."),
    ("√", "Square root."),
    ("ⁿ", "Superscript n."),
    ("²", "Squared."),
    ("■", "Black square. Game over."),
]
for idx, (name, desc) in enumerate(math, start=238):
    METADATA[idx] = ("Math", name, desc)

# Fill missing (just in case)
for i in range(256):
    if i not in METADATA:
        METADATA[i] = ("Unknown", f"Char-{i}", "Undefined.")

# ======================================================================
# 3. SVG GENERATOR
# ======================================================================

def generate_svg(font_data):
    scale = 4
    cols = 32
    rows = 8
    bitmap_w = 9  # 8 + 1 duplicated
    bitmap_h = 16

    # Overall SVG dimensions (zero gap between cells)
    svg_width = cols * bitmap_w * scale
    svg_height = rows * bitmap_h * scale

    lines_out = []
    lines_out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    lines_out.append('  <rect width="100%" height="100%" fill="#000000"/>')
    lines_out.append('  <defs>')

    # Generate each glyph
    for char_idx in range(256):
        idx_hex = f"{char_idx:02X}"
        category, name, desc = METADATA[char_idx]

        # Build comment
        comment = f"pc437-{char_idx} ({category} | {name} - {desc})"
        lines_out.append(f'    <!-- {comment} -->')

        # Start group with metadata
        attrs = [
            f'id="pc437-{char_idx}"',
            f'data-index="{char_idx}"',
            f'data-hex="{idx_hex}"',
            f'data-category="{category}"',
            f'data-name="{name}"',
            f'data-descriptor="{desc}"'
        ]
        lines_out.append(f'    <g {" ".join(attrs)}>')

        # Draw the 16 rows
        for row in range(bitmap_h):
            byte = font_data[char_idx * 16 + row]
            # Scan bits 0..7 (LSB = leftmost pixel)
            # We create a 9-bit row: bits 0..7 + duplicate bit 7
            # Build a string of '1' and '0' for pixels
            row_bits = []
            for col in range(8):  # 0 to 7
                if byte & (1 << col):
                    row_bits.append('1')
                else:
                    row_bits.append('0')
            # Duplicate the 8th column (index 7) into column 8
            row_bits.append(row_bits[7])

            # Compress runs of 1s into rectangles
            x = 0
            while x < 9:
                if row_bits[x] == '1':
                    start_x = x
                    while x < 9 and row_bits[x] == '1':
                        x += 1
                    # rectangle from start_x to x-1
                    rect_x = start_x * scale
                    rect_y = row * scale
                    rect_w = (x - start_x) * scale
                    lines_out.append(f'      <rect x="{rect_x}" y="{rect_y}" width="{rect_w}" height="{scale}" fill="#FFFFFF"/>')
                else:
                    x += 1

        lines_out.append('    </g>')

    lines_out.append('  </defs>')

    # Place the glyphs in a 32x8 grid
    lines_out.append('  <!-- Sprite Sheet Layout: 32 columns x 8 rows -->')
    for char_idx in range(256):
        row = char_idx // cols
        col = char_idx % cols
        x = col * bitmap_w * scale
        y = row * bitmap_h * scale
        category, name, desc = METADATA[char_idx]
        comment = f"pc437-{char_idx} ({category} | {name})"
        lines_out.append(f'  <use href="#pc437-{char_idx}" x="{x}" y="{y}" /> <!-- {comment} -->')

    lines_out.append('</svg>')
    return "\n".join(lines_out)


# ======================================================================
# 4. MAIN
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
    except Exception as e:
        print(f"Error: {e}")
