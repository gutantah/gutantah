import json

def render_heatmap():
    try:
        with open("data/contributions.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: Run fetch_contributions.py first!")
        return

    # The specific 6-level palette from the guide
    PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
    
    box_size = 10
    gap = 4
    width = 53 * (box_size + gap) + 20
    height = 7 * (box_size + gap) + 40
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<style>',
        f'  .bg {{ fill: #0d1117; }}', 
        f'  .text {{ font-family: monospace; font-size: 10px; fill: #8b949e; }}',
        f'  .box {{ rx: 2px; ry: 2px; }}',
        # CSS keyframes that play on load, then freeze (no looping glow)
        f'  .anim {{ opacity: 0; animation: slideDown 0.8s forwards; }}',
        f'  @keyframes slideDown {{',
        f'    from {{ opacity: 0; transform: translateY(-10px); }}',
        f'    to {{ opacity: 1; transform: translateY(0); }}',
        f'  }}',
        f'</style>',
        f'<rect width="100%" height="100%" class="bg"/>',
        f'<g transform="translate(10, 10)">'
    ]

    days = data.get("days", [])
    for i, day in enumerate(days):
        col = i // 7
        row = i % 7
        x = col * (box_size + gap)
        y = row * (box_size + gap)
        
        level = day.get("level", 0)
        color = PALETTE[level] if level < len(PALETTE) else PALETTE[-1]
        
        # Diagonal stagger: delay is based on column + row position
        delay = (col + row) * 0.03
        
        svg.append(f'<rect class="box anim" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" style="animation-delay: {delay}s;" />')
    
    # Add the Less -> More legend
    svg.append(f'<text x="0" y="{7 * (box_size + gap) + 15}" class="text">Less</text>')
    for i, color in enumerate(PALETTE):
        svg.append(f'<rect class="box" x="{30 + i*14}" y="{7 * (box_size + gap) + 7}" width="{box_size}" height="{box_size}" fill="{color}" />')
    svg.append(f'<text x="{30 + len(PALETTE)*14 + 5}" y="{7 * (box_size + gap) + 15}" class="text">More</text>')
    
    # Add the stats footer
    svg.append(f'<text x="{width - 160}" y="{7 * (box_size + gap) + 15}" class="text">Contributions in the last year</text>')
    
    svg.append('</g></svg>')

    with open("contrib-heatmap.svg", "w") as f:
        f.write("\n".join(svg))
        
    print("Success! Output written to contrib-heatmap.svg")

if __name__ == "__main__":
    render_heatmap()