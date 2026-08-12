"""
patterns.py - Decoupled Material Registry
"""
import math, random

class CamouflageMaterial:
    def get_css_rules(self): return "rect { shape-rendering: crispEdges; } .camo-base { fill: #1D231A; } .camo-macro { fill: #34442D; } .camo-micro { fill: #566E4C; } .camo-accent { fill: #8A9B74; }"
    def get_xml_defs(self): return ""
    def evaluate_pixel_class(self, c, r, cols, rows):
        random.seed(c * 37 + r * 101)
        roll = random.random()
        if roll > 0.85: return "camo-accent"
        if roll > 0.60: return "camo-micro"
        if roll > 0.35: return "camo-macro"
        return "camo-base"

class HoneycombPatternMaterial:
    def get_css_rules(self): return ".honeycomb-fill { fill: url(#honeycomb); }"
    def get_xml_defs(self): return """
    <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#462523;" /><stop offset="50%" style="stop-color:#f6f2c0;" /><stop offset="100%" style="stop-color:#462523;" />
    </linearGradient>
    <pattern id="honeycomb" width="40" height="69.28" patternUnits="userSpaceOnUse">
      <rect width="40" height="69.28" fill="#000000"/>
      <polygon points="20,0 40,11.55 40,34.64 20,46.19 0,34.64 0,11.55" fill="none" stroke="url(#goldGradient)" stroke-width="3"/>
      <polygon points="40,34.64 60,46.19 60,69.28 40,80.83 20,69.28 20,46.19" fill="none" stroke="url(#goldGradient)" stroke-width="3"/>
    </pattern>"""
    def evaluate_pixel_class(self, c, r, cols, rows): return "honeycomb-fill"

class CottonWeaveMaterial:
    def get_css_rules(self): return ".cotton-fabric { background-color: #fcfaf2; fill: url(#cotton-weave); filter: url(#inset-vignette); }"
    def get_xml_defs(self): return """
    <filter id="inset-vignette"><feGaussianBlur stdDeviation="15" result="b"/><feComposite operator="in" in="b" in2="SourceGraphic" result="c"/><feBlend mode="multiply" in="SourceGraphic" in2="c"/></filter>
    <pattern id="cotton-weave" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#fcfaf2" />
      <rect width="3" height="6" fill="#000000" fill-opacity="0.03" />
      <rect width="6" height="3" fill="#000000" fill-opacity="0.03" />
    </pattern>"""
    def evaluate_pixel_class(self, c, r, cols, rows): return "cotton-fabric"

class BrushedSteelMaterial:
    def get_css_rules(self): return ".steel-plate { fill: url(#steel-base); } .grain-overlay { fill: url(#steel-grain); mix-blend-mode: overlay; }"
    def get_xml_defs(self): return """
    <linearGradient id="steel-base" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#99a1a6"/><stop offset="50%" stop-color="#70777a"/><stop offset="100%" stop-color="#cfd4d9"/></linearGradient>
    <pattern id="steel-grain" width="10" height="2" patternUnits="userSpaceOnUse"><rect width="10" height="1" fill="#ffffff" fill-opacity="0.12"/></pattern>"""
    def evaluate_pixel_class(self, c, r, cols, rows): return "brushed-steel-plate"

class CodePage437ShadeMaterial:
    def get_css_rules(self): return "rect { shape-rendering: crispEdges; } .cp-25 { fill: url(#stipple-25); } .cp-50 { fill: url(#stipple-50); } .cp-75 { fill: url(#stipple-75); }"
    def get_xml_defs(self): return """
    <pattern id="stipple-25" width="4" height="4" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="1" height="1" fill="#ffffff"/><rect x="2" y="2" width="1" height="1" fill="#ffffff"/></pattern>
    <pattern id="stipple-50" width="4" height="4" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="2" height="2" fill="#ffffff"/><rect x="2" y="2" width="2" height="2" fill="#ffffff"/></pattern>
    <pattern id="stipple-75" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#ffffff"/><rect x="0" y="0" width="1" height="1" fill="#000000"/><rect x="2" y="2" width="1" height="1" fill="#000000"/></pattern>"""
    def evaluate_pixel_class(self, c, r, cols, rows):
        if (c / cols) > 0.66: return "cp-75"
        if (c / cols) > 0.33: return "cp-50"
        return "cp-25"

class PlinthTartanMaterial:
    def get_css_rules(self): return ".tartan-canvas { fill: url(#tartan-mesh); }"
    def get_xml_defs(self): return """
    <pattern id="tartan-mesh" width="100" height="100" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <g stroke="none">
        <rect x="0" width="28.5" height="100" fill="rgb(252,252,252)"/><rect x="28.5" width="28.5" height="100" fill="rgb(241,241,241)"/><rect x="57" width="43" height="100" fill="rgb(218,218,218)"/>
      </g>
      <g stroke="none" fill-opacity="0.46">
        <rect y="0" width="100" height="28.5" fill="rgb(159,159,159)"/><rect y="28.5" width="100" height="28.5" fill="rgb(171,171,171)"/><rect y="57" width="100" height="43" fill="rgb(196,196,196)"/>
      </g>
    </pattern>"""
    def evaluate_pixel_class(self, c, r, cols, rows): return "tartan-canvas"

# Active Abstract Placeholders (Awaiting Logic Verification)
class ConcreteMaterial:
    def get_css_rules(self): return ""
    def get_xml_defs(self): return ""
    def evaluate_pixel_class(self, c, r, cols, rows): return "concrete-fallback"

class ObsidianMaterial:
    def get_css_rules(self): return ""
    def get_xml_defs(self): return ""
    def evaluate_pixel_class(self, c, r, cols, rows): return "obsidian-fallback"

class SubwayTileMaterial:
    def get_css_rules(self): return ""
    def get_xml_defs(self): return ""
    def evaluate_pixel_class(self, c, r, cols, rows): return "subway-fallback"
