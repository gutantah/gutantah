import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path):
    print(f"Reading {input_path}...")
    try:
        input_image = Image.open(input_path)
    except FileNotFoundError:
        print(f"Error: Could not find '{input_path}'. Make sure it's in the same folder.")
        sys.exit(1)

    # 1. Remove the background with rembg
    print("Removing background...")
    subject_only = remove(input_image)

    # 3. Composite onto pure white
    print("Compositing onto white background...")
    white_bg = Image.new("RGBA", subject_only.size, (255, 255, 255, 255))
    white_bg.paste(subject_only, (0, 0), subject_only)
    
    # Convert to grayscale for contrast adjustment
    gray_image = white_bg.convert("L")
    gray_np = np.array(gray_image)

    # 2. Boost local contrast with OpenCV's CLAHE
    print("Boosting local contrast...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    final_np = clahe.apply(gray_np)

    # Output as grayscale source-prepped.png
    final_img = Image.fromarray(final_np)
    output_path = "source-prepped.png"
    final_img.save(output_path)
    print(f"Success! Output saved as {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py source-photo.jpg")
        sys.exit(1)
    
    prep_photo(sys.argv[1])