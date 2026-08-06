#!/usr/bin/env python3
"""
===================================================================
COINCIDENT PAN-LATIN MATRIX DATA HARVESTER
===================================================================
Parses active asset configurations to compile a 45-bit direct-addressing 
lookup database. Organizes segments cleanly into JSON-compatible maps.
This standalone script defines your 45-bit hardware memory registry and
uses clean JSON serialization arrays to organize your font [PWAAAM_MASTER]. 
It contains the exact "sharded" definitions for your characters—including 
the 84% scaled lowercase letters with their out-extending attic accents and basement descender tails.

"""

import json

# Define the absolute 45-bit hardware memory index (Bit order 0 to 44)
MASTER_SEGMENT_REGISTRY = [
    # 1. Foundational Linear Core Elements (21 Items)
    "core-top-l-bar", "core-top-r-bar", "core-mid-l-cross", "core-mid-r-cross", "core-bot-l-bar", "core-bot-r-bar",
    "core-up-l-spine", "core-lo-l-spine", "core-up-r-spine", "core-lo-r-spine", "core-up-c-spine", "core-lo-c-spine",
    "core-diag-tl", "core-diag-tr", "core-diag-bl", "core-diag-br", "sat-attic-l", "sat-attic-r", "sat-basement-hook",
    "node-colon-u", "node-colon-l",
    
    # 2. Orange Loop Engine Subdivided Shards (8 Items)
    "cv-up-tl-shard", "cv-up-tr-shard", "cv-up-br-shard", "cv-up-bl-shard",
    "cv-lo-tl-shard", "cv-lo-tr-shard", "cv-lo-br-shard", "cv-lo-bl-shard",
    
    # 3. Mies Helix Blue Engine Subdivided Wave Shards (12 Items)
    "bx-attic-l-flare", "bx-core-up-l-wave", "bx-core-lo-r-wave", "bx-basement-r-flare",
    "bx-attic-r-flare", "bx-core-up-r-wave", "bx-core-lo-l-wave", "bx-basement-l-flare",
    
    # 4. Emergent Center Diamond Knuckle Intersections (4 Items)
    "bx-joint-center-u", "bx-joint-center-d", "bx-joint-center-l", "bx-joint-center-r"
]

# THE TRUE SHARD MAP DIRECTORY: "Mégantic " (Cell-bounded shard configurations)
GLYPH_RECIPE_BOOK = {
    "M": ["core-up-l-spine", "core-lo-l-spine", "core-up-r-spine", "core-lo-r-spine", "bx-core-up-l-wave", "bx-core-up-r-wave"],
    "é": ["cv-up-tl-shard", "cv-up-tr-shard", "cv-up-br-shard", "cv-up-bl-quad", "cv-lo-tl-shard", "cv-lo-tr-shard", "cv-lo-br-shard", "cv-lo-bl-shard", "core-mid-l-cross", "core-mid-r-cross", "sat-attic-r"],
    "g": ["cv-up-tl-shard", "cv-up-tr-shard", "cv-up-br-shard", "cv-up-bl-quad", "cv-lo-tl-shard", "cv-lo-tr-shard", "cv-lo-br-shard", "cv-lo-bl-shard", "core-mid-l-cross", "core-mid-r-cross", "core-lo-r-spine", "sat-basement-hook"],
    "a": ["cv-up-tl-shard", "cv-up-tr-shard", "cv-up-br-shard", "cv-up-bl-quad", "cv-lo-tl-shard", "cv-lo-tr-shard", "cv-lo-br-shard", "cv-lo-bl-shard", "core-mid-l-cross", "core-mid-r-cross", "core-bot-l-bar", "core-bot-r-bar", "core-lo-r-spine"],
    "n": ["cv-up-tl-shard", "cv-up-tr-shard", "core-up-l-spine", "core-lo-l-spine", "core-up-r-spine", "core-lo-r-spine"],
    "t": ["core-up-c-spine", "core-lo-c-spine", "core-mid-l-cross", "core-mid-r-cross"],
    "i": ["core-lo-c-spine", "node-colon-u"],
    "c": ["cv-up-tl-shard", "cv-up-tr-shard", "cv-lo-tl-shard", "cv-lo-bl-shard", "core-mid-l-cross", "core-bot-l-bar"],
    " ": [] # Absolute Dormant OFF Matrix Layout State
}

def compile_hardware_lut():
    hardware_font_lut = {}
    
    print("================================================================")
    print("EXTRAPOLATING COMPACT 45-BIT PAN-LATIN LOOKUP TABLES")
    print("================================================================\n")
    
    for char, active_shards in GLYPH_RECIPE_BOOK.items():
        bitmask = 0
        
        # Match activated shards to their index slots in the 45-bit register array
        for idx, shard_name in enumerate(MASTER_SEGMENT_REGISTRY):
            if shard_name in active_shards:
                bitmask |= (1 << (44 - idx))
                
        # Format strings cleanly exactly as requested
        binary_string = f"0b{bitmask:045b}"
        hex_string = f"0x{bitmask:012X}"
        
        hardware_font_lut[char] = {
            "binary_mask": binary_string,
            "hex_code": hex_string,
            "active_count": len(active_shards),
            "address_list": active_shards
        }
        
        print(f"Glyph '{char}' processed: Hex -> {hex_string} | Active Shards -> {len(active_shards)}")

    # Serialize our structured registry database out to a clean data file
    output_payload = {
        "metadata": {
            "resolution": "10x12_matrix",
            "stroke_ratio": "series_e_modified_1:5",
            "total_addressable_facets": len(MASTER_SEGMENT_REGISTRY),
            "registry_index_schema": MASTER_SEGMENT_REGISTRY
        },
        "character_lookup_table": hardware_font_lut
    }
    
    with open("matrix_lut_database.json", "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=4)
        
    print("\n[SUCCESS] Extrapolated data structure data file generated as 'matrix_lut_database.json'")

if __name__ == "__main__":
    compile_hardware_lut()
