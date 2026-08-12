"""
engine.py - Core Context Layout Compiler
"""
import math

class UnifiedCanvasEngine:
    def __init__(self, width=800, height=800):
        self.width = width
        self.height = height
        self.cx, self.cy = width / 2, height / 2

    def _project_3d(self, x, y, z, scale=180):
        rad_yaw, rad_pitch = math.radians(40.0), math.radians(35.0)
        x_rot = x * math.cos(rad_yaw) - z * math.sin(rad_yaw)
        y_screen = y * math.cos(rad_pitch) - (x * math.sin(rad_yaw) + z * math.cos(rad_yaw)) * math.sin(rad_pitch)
        return self.cx + (x_rot * scale), self.cy + (y_screen * scale)

    def compile_asset(self, material_instance, layout_mode="GRID", canvas_schema=None, filename="output.svg"):
        with open(filename, "w") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(f'<svg xmlns="http://w3.org" viewBox="0 0 {self.width} {self.height}" width="100%" height="100%">\n\n')
            
            if material_instance.get_xml_defs():
                f.write(f'  <defs>\n{material_instance.get_xml_defs()}\n  </defs>\n\n')
                
            f.write(f'  <style type="text/css">\n{material_instance.get_css_rules()}\n  </style>\n\n')
            f.write(f'  <g id="render-viewport">\n')

            if layout_mode == "3D" and canvas_schema:
                vertices = canvas_schema["vertices"]
                subdivisions = canvas_schema.get("subdivisions", 10)
                for face in canvas_schema["faces"]:
                    n0, n1, n2, n3 = [vertices[node] for node in face["nodes"]]
                    for u in range(subdivisions):
                        u0, u1 = u / subdivisions, (u + 1) / subdivisions
                        for v in range(subdivisions):
                            v0, v1 = v / subdivisions, (v + 1) / subdivisions
                            bilerp = lambda u_v, v_v, i: (1-u_v)*(1-v_v)*n0[i] + u_v*(1-v_v)*n1[i] + u_v*v_v*n2[i] + (1-u_v)*v_v*n3[i]
                            mx, my, mz = [bilerp((u0+u1)/2, (v0+v1)/2, i) for i in range(3)]
                            cls = material_instance.evaluate_pixel_class(u, v, subdivisions, subdivisions)
                            quad = [[bilerp(us, vs, i) for i in range(3)] for us, vs in [(u0,v0), (u1,v0), (u1,v1), (u0,v1)]]
                            screen_pts = [f"{sx:.1f},{sy:.1f}" for sx, sy in [self._project_3d(*pt) for pt in quad]]
                            f.write(f'    <polygon class="{cls}" points="{" ".join(screen_pts)}" />\n')

            elif layout_mode == "TILED_FILL":
                cls = material_instance.evaluate_pixel_class(0, 0, 1, 1)
                if cls == "brushed-steel-plate":
                    f.write(f'    <rect width="{self.width}" height="{self.height}" class="brushed-steel-plate" />\n')
                    f.write(f'    <rect width="{self.width}" height="{self.height}" class="brushed-grain-overlay" />\n')
                else:
                    f.write(f'    <rect width="{self.width}" height="{self.height}" class="{cls}" />\n')

            else: # Standard 2D GRID
                spacing = 16
                cols, rows = self.width // spacing, self.height // spacing
                for r in range(rows):
                    for c in range(cols):
                        cls = material_instance.evaluate_pixel_class(c, r, cols, rows)
                        f.write(f'    <rect x="{c*spacing}" y="{r*spacing}" width="{spacing}" height="{spacing}" class="{cls}" />\n')

            f.write('  </g>\n</svg>\n')
        print(f"[Core Engine] Baked: '{filename}'")
