from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = 1000000000 

def resize_image(input_image_path, output_image_path, max_width=None, max_height=None, 
                threshold=128, pool_size=3, rotation_degrees=0):
    """
    Processes an image with optional rotation, resizing, thresholding, and pooling.
    
    Args:
        input_image_path: Path to input image
        output_image_path: Path to save output image
        max_width: Maximum width for resizing
        max_height: Maximum height for resizing
        threshold: Binarization threshold (0-255)
        pool_size: Size of pooling window (n x n)
        rotation_degrees: Degrees to rotate clockwise (0, 90, 180, or 270)
    """
    img = Image.open(input_image_path)
    
    # Apply rotation (only supports 90° increments for clean pixel alignment)
    if rotation_degrees not in [0, 90, 180, 270]:
        raise ValueError("Rotation must be 0, 90, 180, or 270 degrees")
    
    if rotation_degrees == 90:
        img = img.transpose(Image.ROTATE_90)
    elif rotation_degrees == 180:
        img = img.transpose(Image.ROTATE_180)
    elif rotation_degrees == 270:
        img = img.transpose(Image.ROTATE_270)
    
    # Calculate target size maintaining aspect ratio
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height
    
    if max_width is not None and max_height is not None:
        # If both max dimensions are specified, choose the one that gives smaller image
        target_width1 = max_width
        target_height1 = int(target_width1 / aspect_ratio)
        
        target_height2 = max_height
        target_width2 = int(target_height2 * aspect_ratio)
        
        if target_width1 * target_height1 < target_width2 * target_height2:
            target_width, target_height = target_width1, target_height1
        else:
            target_width, target_height = target_width2, target_height2
    elif max_width is not None:
        target_width = max_width
        target_height = int(target_width / aspect_ratio)
    elif max_height is not None:
        target_height = max_height
        target_width = int(target_height * aspect_ratio)
    else:
        # If no max dimensions specified, keep original size
        target_width, target_height = original_width, original_height
    
    img.thumbnail((target_width, target_height), Image.LANCZOS)
    img = img.convert('L')
    img = img.point(lambda p: 255 if p > threshold else 0)
    img.save(output_image_path)
    
    # Generate text files
    generate_text_files(output_image_path, img, pool_size)
    
    print(f"Processing complete. Image rotated {rotation_degrees}° clockwise.")

def generate_text_files(output_image_path, img, pool_size):
    """Generates the bitmap and pooled text files."""
    width, height = img.size    
    pixels = list(img.getdata()) 
    
    # Standard bitmap file
    bitmap_text_path = output_image_path.replace('.png', '.txt')  
    with open(bitmap_text_path, 'w') as f:
        f.write("    " + " ".join([f"{x%10}" for x in range(width)]) + "\n")
        for y in range(height):
            row = pixels[y*width:(y+1)*width]
            row_str = " ".join(['1' if pixel == 255 else '0' for pixel in row])
            f.write(f"{y%10:3} {row_str}\n")
    print(f"Bitmap text file saved as {bitmap_text_path}")
    
    # Pooled bitmap file
    pooled_bitmap_text_path = output_image_path.replace('.png', f'_pooled_{pool_size}x{pool_size}.txt')
    pooled_pixels = pool_bitmap(pixels, width, height, pool_size)
    with open(pooled_bitmap_text_path, 'w') as f:
        pooled_width = width // pool_size 
        f.write("    " + " ".join([f"{x%10}" for x in range(pooled_width)]) + "\n")
        for y in range(len(pooled_pixels)):
            row_str = " ".join(['1' if pixel == 1 else '0' for pixel in pooled_pixels[y]])
            f.write(f"{y%10:3} {row_str}\n")
    print(f"Pooled bitmap text file saved as {pooled_bitmap_text_path}")

def pool_bitmap(pixels, width, height, pool_size):
    pooled_pixels = []
    for y in range(0, height, pool_size):
        pooled_row = []
        for x in range(0, width, pool_size):
            block = [pixels[(y+i)*width + (x+j)] for i in range(pool_size) 
                    for j in range(pool_size) if y+i < height and x+j < width]            
            pooled_value = 1 if any(pixel == 255 for pixel in block) else 0
            pooled_row.append(pooled_value)        
        pooled_pixels.append(pooled_row)    
    return pooled_pixels

# Example usage:
resize_image('MapR.png', 'ResizedMap.png', 
             max_width=960, 
             pool_size=2, 
             rotation_degrees=270)  # Rotate 270° clockwise