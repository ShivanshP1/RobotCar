from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = 1000000000 

def resize_image(input_image_path, output_image_path, target_width=1920, target_height=1080, threshold=128, pool_size=3):
    img = Image.open(input_image_path)
    img.thumbnail((target_width, target_height), Image.LANCZOS)
    img = img.convert('L')
    img = img.point(lambda p: 255 if p > threshold else 0)
    img.save(output_image_path)
    
   
    bitmap_text_path = output_image_path.replace('.png', '.txt')  
    width, height = img.size 
    pixels = list(img.getdata()) 
    
    with open(bitmap_text_path, 'w') as f:
        f.write("   " + " ".join([f"{x:3}" for x in range(width)]) + "\n") 

        for y in range(height):
            row = pixels[y*width:(y+1)*width]
            row_str = " ".join([f"{1 if pixel == 255 else 0:3}" for pixel in row])
            f.write(f"{y:3} {row_str}\n")
    
    print(f"Resized image saved as {output_image_path}")
    print(f"Bitmap text file saved as {bitmap_text_path}")
    pooled_bitmap_text_path = output_image_path.replace('.png', f'_pooled_{pool_size}x{pool_size}.txt')
    pooled_pixels = pool_bitmap(pixels, width, height, pool_size)

    with open(pooled_bitmap_text_path, 'w') as f:
        pooled_width = width // pool_size 
        f.write("   " + " ".join([f"{x:3}" for x in range(pooled_width)]) + "\n") 
        
        for y in range(len(pooled_pixels)):
            row_str = " ".join([f"{pixel:3}" for pixel in pooled_pixels[y]])
            f.write(f"{y:3} {row_str}\n")
    
    print(f"Pooled bitmap text file saved as {pooled_bitmap_text_path}")

def pool_bitmap(pixels, width, height, pool_size):
    pooled_pixels = []
    for y in range(0, height, pool_size):
        pooled_row = []
        for x in range(0, width, pool_size):
            block = [pixels[(y+i)*width + (x+j)] for i in range(pool_size) for j in range(pool_size) if y+i < height and x+j < width]            
            pooled_value = 1 if any(pixel == 255 for pixel in block) else 0
            pooled_row.append(pooled_value)        
        pooled_pixels.append(pooled_row)    
    return pooled_pixels

resize_image('Map.png', 'ResizedMap.png', pool_size=5) 
