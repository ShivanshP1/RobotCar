from PIL import Image, ImageDraw, ImageFont, ImageColor
import numpy as np

def visualize_pooled_map(pooled_txt_path, output_image_path, coordinates,
                         highlight_color='blue', font_size=8,
                         x_scale_factor=1, y_scale_factor=1):
    """
    Creates a 1:1 visualization from a pooled text file with exact grid size.
    
    Args:
        pooled_txt_path: Path to pooled text file
        output_image_path: Path to save output image
        coordinates: List of (x,y) tuples to highlight
        highlight_color: Color for highlighted coordinates
        font_size: Font size for labels (smaller for 1:1 scale)
        x_scale_factor: Divides x coordinates by this factor
        y_scale_factor: Divides y coordinates by this factor
    """
    try:
        # Read the pooled text file
        with open(pooled_txt_path, 'r') as f:
            lines = f.readlines()[1:]  # Skip header line
        
        # Parse the bitmap data
        bitmap = []
        for line in lines:
            parts = line.strip().split()[1:]  # Skip row number
            row = [int(p) for p in parts]
            bitmap.append(row)
        
        bitmap = np.array(bitmap)
        height, width = bitmap.shape
        
        print(f"Input grid dimensions: {width}x{height} cells")
        print(f"Output image dimensions: {width}x{height} pixels (1:1 scale)")
        print(f"X scale factor: {x_scale_factor}, Y scale factor: {y_scale_factor}")

        # Create 1:1 scale image
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Load font (smaller size for 1:1 scale)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Draw each pixel at actual size
        for y in range(height):
            for x in range(width):
                if bitmap[y, x] == 1:
                    img.putpixel((x, y), (0, 0, 0))  # Black for 1s
        
        # Create annotation layer for labels
        annot_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        annot_draw = ImageDraw.Draw(annot_img)
        
        # Highlight coordinates with scaling
        for i, (x, y) in enumerate(coordinates, 1):
            # Apply coordinate scaling separately
            scaled_x = int(x / x_scale_factor)
            scaled_y = int(y / y_scale_factor)
            
            # Verify coordinates are within bounds
            if not (0 <= scaled_x < width and 0 <= scaled_y < height):
                print(f"Warning: Coordinate #{i} ({x},{y}) scaled to ({scaled_x},{scaled_y}) is out of bounds")
                continue
            
            # Draw small cross for highlighting (visible at 1:1 scale)
            cross_size = 1
            highlight_rgb = ImageColor.getrgb(highlight_color)
            for offset in range(-cross_size, cross_size+1):
                if 0 <= scaled_x + offset < width:
                    img.putpixel((scaled_x + offset, scaled_y), highlight_rgb)
                if 0 <= scaled_y + offset < height:
                    img.putpixel((scaled_x, scaled_y + offset), highlight_rgb)
            
            # Draw label for this coordinate
            label_text = f"{i}"
            text_x = scaled_x
            text_y = max(0, scaled_y - 6)  # 6 pixels above
            
            # Draw text with background
            text_bbox = annot_draw.textbbox((text_x, text_y), label_text, font=font)
            padding = 1
            annot_draw.rectangle([
                text_bbox[0] - padding,
                text_bbox[1] - padding,
                text_bbox[2] + padding,
                text_bbox[3] + padding
            ], fill='black')
            annot_draw.text((text_x, text_y), label_text, fill='white', font=font)
        
        # Composite annotations with original image
        img = Image.alpha_composite(img.convert('RGBA'), annot_img)
        img = img.convert('RGB')
        img.save(output_image_path)
        
        print(f"Visualization saved to {output_image_path}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Configuration
    pooled_txt_path = "ResizedMap_pooled_2x2.txt"
    output_image_path = "PooledMap_Visualization.png"
    
    # Original coordinates (before scaling)
    coordinates = [
        (29, 129),   # Coordinate 1 Top Left
        (135, 585),  # Coordinate 2 Bottom Left 
        (233 ,305 ),  # Coordinate 3 Center
        (459, 181 ),  # Coordinate 4 Bottom Left
        (465, 452)   # Coordinate 5 Bottom Right
    ]
    
    # Generate 1:1 visualization
    visualize_pooled_map(
        pooled_txt_path,
        output_image_path,
        coordinates,
        highlight_color='blue',
        font_size=18,
        x_scale_factor=1.00,
        y_scale_factor=1.00
    )

if __name__ == "__main__":
    main()