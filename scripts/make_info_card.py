import os

def generate_info_card(output_path="info-card.svg"):
    # Check if STATIC=1 env var is set for frozen Quick Look previews
    is_static = os.environ.get("STATIC") == "1"

    # Profile data mapped to the required keys
    title = "radu@github ~"
    rows = [
        ("Now", "CS Student @ Technical University of Cluj-Napoca"),
        ("Prev", "AI Training &amp; LLM Evaluation"),
        ("Stack", "C, C++, Java, Python, VHDL, SQL"),
        ("Highlights", "32-bit MIPS CPU, Budget Management app")
    ]

    width = 600
    height = 250
    font_size = 14
    row_height = 28

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<style>',
        f'  .bg {{ fill: #1e1e1e; rx: 8px; }}',
        f'  .text {{ font-family: monospace; font-size: {font_size}px; fill: #d4d4d4; }}',
        f'  .key {{ fill: #569cd6; font-weight: bold; }}',
        f'  .title {{ fill: #4ec9b0; font-weight: bold; }}',
    ]

    # Add staggered fade/slide animation unless STATIC=1 is passed
    if not is_static:
        svg.append(f'  .anim {{ opacity: 0; animation: fadeInSlide 0.5s forwards; }}')
        svg.append(f'  @keyframes fadeInSlide {{')
        svg.append(f'    from {{ opacity: 0; transform: translateX(-15px); }}')
        svg.append(f'    to {{ opacity: 1; transform: translateX(0); }}')
        svg.append(f'  }}')

    svg.append(f'</style>')
    svg.append(f'<rect class="bg" width="100%" height="100%" />')

    # Header
    svg.append(f'<text x="20" y="35" class="text title">{title}</text>')
    svg.append(f'<text x="20" y="50" class="text">---------------------------------------</text>')

    # Key/Value rows
    y_offset = 85
    for i, (key, value) in enumerate(rows):
        anim_class = "anim" if not is_static else ""
        delay = f'style="animation-delay: {i * 0.15 + 0.2}s;"' if not is_static else ""

        svg.append(f'<g class="{anim_class}" {delay}>')
        svg.append(f'  <text x="20" y="{y_offset}" class="text key">{key}</text>')
        svg.append(f'  <text x="120" y="{y_offset}" class="text">{value}</text>')
        svg.append(f'</g>')
        y_offset += row_height

    svg.append(f'</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    
    print(f"Success! Info card written to {output_path}")

if __name__ == "__main__":
    generate_info_card()