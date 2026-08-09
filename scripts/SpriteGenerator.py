#!/usr/bin/env python3
"""
===================================================================
10-COLUMN GRAPHIC ATLAS GENERATOR
===================================================================
Generates a highly efficient vector sprite sheet. 
Combines the shared blueprint framework into a singular asset row,
safely color-baked for cross-platform compliance.
"""

import json

# Define the global address schema (The 45 components mapped to their vector path tracers)
SEGMENT_GEOMETRY = {
    # Foundational Linear Core Elements
    "core-top-l-bar":      '<polygon points="0,0 90,0 90,30 0,30" />',
    "core-top-r-bar":      '<polygon points="90,0 180,0 180,30 90,30" />',
    "core-mid-l-cross":    '<polygon points="18,165 90,165 90,195 18,195" />',
    "core-mid-r-cross":    '<polygon points="90,165 162,165 162,195 90,195" />',
    "core-bot-l-bar":      '<polygon points="0,330 90,330 90,360 0,360" />',
    "core-bot-r-bar":      '<polygon points="90,330 180,330 180,360 90,360" />',
    "core-up-l-spine":     '<polygon points="0,30 18,30 18,180 0,180" />',
    "core-lo-l-spine":     '<polygon points="0,180 18,180 18,330 0,330" />',
    "core-up-r-spine":     '<polygon points="162,30 180,30 180,180 162,180" />',
    "core-lo-r-spine":     '<polygon points="162,180 180,180 180,330 162,330" />',
    "core-up-c-spine":     '<polygon points="81,30 99,30 99,135 81,135" />',
    "core-lo-c-spine":     '<polygon points="81,165 99,165 99,330 81,330" />',
    "core-diag-tl":        '<polygon points="18,30 36,30 81,112.5 81,135 63,135 18,60" />',
    "core-diag-tr":        '<polygon points="162,30 162,60 117,135 99,135 99,112.5 144,30" />',
    "core-diag-bl":        '<polygon points="18,330 18,300 63,165 81,165 81,187.5 36,330" />',
    "core-diag-br":        '<polygon points="162,330 144,330 99,187.5 99,165 117,165 162,300" />',
    "sat-attic-l":         '<polygon points="18,-15 54,-15 36,0 0,0" />',
    "sat-attic-r":         '<polygon points="126,-15 162,-15 180,0 144,0" />',
    "sat-basement-hook":   '<path d="M 144,330 L 180,330 L 180,345 Q 180,375 157.5,390 L 152.5,370 Q 165,360 165,345 Z" />',
    "node-colon-u":        '<rect x="81" y="75" width="18" height="30" />',
    "node-colon-l":        '<rect x="81" y="225" width="18" height="30" />',
    
    # Orange Engine Loop Facet Shards
    "cv-up-tl-shard":       '<path d="M 0,180 L 0,90 C 0,30 36,-15 90,-15 L 90,15 C 54,15 30,50 30,90 L 30,180 Z" />',
    "cv-up-tr-shard":       '<path d="M 180,180 L 180,90 C 180,30 144,-15 90,-15 L 90,15 C 126,15 150,50 150,90 L 150,180 Z" />',
    "cv-lo-bl-shard":       '<path d="M 0,180 L 0,270 C 0,330 36,375 90,375 L 90,345 C 54,345 30,310 30,270 L 30,180 Z" />',
    "cv-lo-br-shard":       '<path d="M 180,180 L 180,270 C 180,330 144,375 90,375 L 90,345 C 126,345 150,310 150,270 L 150,180 Z" />',
    
    # Blue Engine Mies Helix Wave Shards
    "bx-attic-l-flare":     '<path d="M 0,-15 C 10,0 20,15 30,30 L 48,15 C 38,5 22,-5 22,-15 Z" />',
    "bx-core-up-l-wave":    '<path d="M 30,30 C 50,40 65,75 90,180 L 112,180 C 87,75 72,40 52,30 Z" />',
    "bx-core-lo-r-wave":    '<path d="M 90,180 C 115,225 130,260 150,270 L 128,270 C 108,260 93,225 68,180 Z" />',
    "bx-basement-r-flare":  '<path d="M 150,270 C 160,285 170,300 180,315 L 180,330 L 158,330 L 158,315 C 158,300 148,285 128,270 Z" />',
    "bx-attic-r-flare":     '<path d="M 180,-15 C 170,0 160,15 150,30 L 132,15 C 142,5 158,-5 158,-15 Z" />',
    "bx-core-up-r-wave":    '<path d="M 150,30 C 130,40 115,75 90,180 L 68,180 C 93,75 108,40 128,30 Z" />',
    "bx-core-lo-l-wave":    '<path d="M 90,180 C 65,225 50,260 30,270 L 52,270 C 72,260 87,225 112,180 Z" />',
    "bx-basement-l-flare":  '<path d="M 30,270 C 20,285 10,300 0,315 L 0,330 L 22,330 L 22,315 C 22,300 32,285 52,270 Z" />',
    
    # Emergent Node Joints
    "bx-joint-center-u":    '<polygon points="90,180 78,165 90,150 102,165" />',
    "bx-joint-center-d":    '<polygon points="90,180 78,195 90,210 102,195" />',
    "bx-joint-center-l":    '<polygon points="90,180 72,180 78,165 78,195" />',
    "bx-joint-center-r":    '<polygon points="90,180 108,180 102,165 102,195" />'
}

# The Active Shard Selection maps to build "Mégantic " as separate, clean characters
GLYPH_RECIPE_BOOK = {
    "M": ["core-up-l-spine", "core-lo-l-spine", "core-up-r-spine", "core-lo-r-spine", "bx-core-up-l-wave", "bx-core-up-r-wave"],
    "é": ["cv-up-tl-shard", "cv-up-tr-shard", "cv-up-br-shard", "cv-lo-tl-shard", "cv-lo-tr-shard", "cv-lo-br-shard", "cv-lo-bl-shard", "core-mid-l-cross", "core-mid-r-cross", "sat-attic-r"],
    "g": ["cv-up-tl-shard", "cv-up-tr-shard", "cv-up-br-shard", "cv-lo-tl-shard", "cv-lo-tr-shard", "cv-lo-br-shard", "cv-lo-bl-shard", "core-mid-l-cross", "core-mid-r-cross", "core-lo-r-spine", "sat-basement-hook"],
    "a": ["cv-up-tl-shard", "cv-up-tr-shard", "cv-up-br-shard", "cv-lo-tl-shard", "cv-lo-tr-shard", "cv-lo-br-shard", "cv-lo-bl-shard", "core-mid-l-cross", "core-mid-r-cross", "core-bot-l-bar", "core-bot-r-bar", "core-lo-r-spine"],
    "n": ["cv-up-tl-shard", "cv-up-tr-shard", "core-up-l-spine", "core-lo-l-spine", "core-up-r-spine", "core-lo-r-spine"],
    "t": ["core-up-c-spine", "core-lo-c-spine", "core-mid-l-cross", "core-mid-r-cross"],
    "i": ["core-lo-c-spine", "node-colon-u"],
    "c": ["cv-up-tl-shard", "cv-up-tr-shard", "cv-lo-tl-shard", "cv-lo-bl-shard", "core-mid-l-cross", "core-bot-l-bar"],
    " ": []
}

def generate_svg_atlas():
    total_chars = len(GLYPH_RECIPE_BOOK)
    canvas_width = (total_chars * 220) + 40
    
    output = []
    output.append(f'<svg xmlns="http://w3.org" viewBox="0 0 {canvas_width} 500" width="100%" height="100%">')
    
    # Centralized CSS Layout Style Block
    output.append('  <style>')
    output.append('    :root {')
    output.append('      --bg-color:   #2a2e2f; --grid-color: #2a2e2f; --seg-off: #141617;')
    output.append('      --seg-on:     #ffa500; --chassis-rim: #0d0e0f;')
    output.append('    }')
    output.append('    svg { background: var(--bg-color); }')
    output.append('    .bg-shield { fill: var(--seg-off); stroke: var(--chassis-rim); stroke-width: 3; }')
    output.append('    .trace-line { fill: none; stroke: #4b5354; stroke-width: 1.2; stroke-dasharray: 2,3; }')
    output.append('    .mask-blade { fill: none; stroke: var(--grid-color); stroke-width: 3; }')
    output.append('    .seg-off { fill: var(--seg-off); stroke: var(--grid-color); stroke-width: 1.5; }')
    output.append('    .seg-on { fill: var(--seg-on); stroke: #000000; stroke-width: 1.5; filter: brightness(1.3) drop-shadow(0px 0px 6px rgba(255,165,0,0.9)); }')
    output.append('    .lbl-text { fill: #4b5354; font-family: monospace; font-size: 13px; font-weight: bold; letter-spacing: 1px; }')
    output.append('  </style>')
    
    for idx, (char, active_shards) in enumerate(GLYPH_RECIPE_BOOK.items()):
        x_offset = 40 + (idx * 220)
        output.append(f'  <!-- ==================== CHARACTER SLOT: "{char}" ==================== -->')
        output.append(f'  <g transform="translate({x_offset}, 70)">')
        output.append('    <rect x="0" y="-15" width="180" height="390" class="bg-shield" />')
        
        # Guide Lines
        cols = [18, 36, 54, 72, 90, 108, 126, 144, 162]
        rows = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
        for col_x in cols:
            output.append(f'    <line x1="{col_x}" y1="-15" x2="{col_x}" y2="375" class="trace-line" />')
        for row_y in rows:
            output.append(f'    <line x1="0" y1="{row_y}" x2="180" y2="{row_y}" class="trace-line" />')
            
        # Draw Base Inactive Face Shards
        for seg_id, path_data in SEGMENT_GEOMETRY.items():
            if seg_id not in active_shards:
                cleaned_tag = path_data.replace('/>', 'class="seg-off" />')
                output.append(f'    {cleaned_tag}')
                
        # Draw Active High-Intensity Illuminations on Top
        for seg_id in active_shards:
            if seg_id in SEGMENT_GEOMETRY:
                cleaned_tag = SEGMENT_GEOMETRY[seg_id].replace('/>', 'class="seg-on" />')
                output.append(f'    {cleaned_tag}')
                
        # Overlay the Strong Mask Cutter Lines
        for row_y in rows:
            output.append(f'    <line x1="0" y1="{row_y}" x2="180" y2="{row_y}" class="mask-blade" />')
        for col_x in cols:
            output.append(f'    <line x1="{col_x}" y1="0" x2="{col_x}" y2="360" class="mask-blade" />')
            
        output.append(f'    <text x="90" y="405" text-anchor="middle" class="lbl-text">GLYPH "{char}"</text>')
        output.append('  </g>')
        
    output.append('</svg>')
    
    with open("font_atlas.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print("[SUCCESS] Subdivided multi-glyph vector sprite sheet compiled as 'font_atlas.svg'")

if __name__ == "__main__":
    generate_svg_atlas()
