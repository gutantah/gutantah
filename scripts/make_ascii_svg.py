import sys
from PIL import Image

def make_ascii_svg(input_path="source-prepped.png", output_path="avi-ascii.svg"):
    # The prepped image is downsampled to a character grid (~100x53)
    WIDTH = 100
    HEIGHT = 53

    # Density ramp: bright (sparse) -> dark (dense)
    # Leading space clears the background to nothing
    RAMP = " .`:-=+*cs#%@"
    
    try:
        img = Image.open(input_path).convert("L")
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}. Did you run prep_photo.py first?")
        sys.exit(1)

    # Resize image to the character grid
    img = img.resize((WIDTH, HEIGHT))
    pixels = img.load()

    # Generate ASCII grid
    ascii_grid = []
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            # 255 is white (bright), 0 is black (dark)
            # Map bright -> 0 (space), dark -> max (dense)
            pixel_val = pixels[x, y]
            ramp_idx = int(((255 - pixel_val) / 255.0) * (len(RAMP) - 1))
            row += RAMP[ramp_idx]
        ascii_grid.append(row)

    # SVG layout configuration
    font_size = 14
    char_width = 8.4 # approximate width of a monospace character
    svg_width = int(WIDTH * char_width)
    svg_height = HEIGHT * font_size
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        f'<style>',
        # Monochrome light-gray fill color
        f'  .ascii {{ font-family: monospace; font-size: {font_size}px; fill: #d3d3d3; white-space: pre; }}', 
        f'</style>',
        f'<defs>'
    ]

    # Create the SMIL animation clipping paths
    for i in range(HEIGHT):
        delay = i * 0.05 # Staggered top to bottom
        svg_lines.append(f'  <clipPath id="wipe_{i}">')
        # Horizontal clip that wipes left-to-right, prints once and freezes (no looping)
        svg_lines.append(f'    <rect x="0" y="{i * font_size}" width="0" height="{font_size}">')
        svg_lines.append(f'      <animate attributeName="width" from="0" to="{svg_width}" begin="{delay}s" dur="0.8s" fill="freeze" />')
        svg_lines.append(f'    </rect>')
        svg_lines.append(f'  </clipPath>')
    svg_lines.append('</defs>')

    # Add the text rows wrapped in their respective clips
    for i, row_str in enumerate(ascii_grid):
        # Escape HTML characters
        clean_str = row_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        y_pos = (i + 1) * font_size
        svg_lines.append(f'<text x="0" y="{y_pos}" class="ascii" clip-path="url(#wipe_{i})">{clean_str}</text>')
        
    svg_lines.append('</svg>')

    # Write the avi-ascii.svg file
    with open(output_path, "w") as f:
        f.write("\n".join(svg_lines))
    
    print(f"Success! Output written to {output_path}")

if __name__ == "__main__":
    make_ascii_svg()