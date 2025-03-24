import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None 

def load_and_convert_image_to_bitmap(image_path):

    file_extension = os.path.splitext(image_path)[1].lower()
    image_name = os.path.basename(image_path)
    supported_formats = ['.png', '.jpg', '.jpeg', '.gif']
    
    if file_extension in supported_formats:
        try:
            img = Image.open(image_path)
            width, height = img.size
            print(f"Loading image: {image_name} (Map)")
            print(f"Image dimensions: {width} x {height} (Width x Height)")
            bw_img = img.convert('L')
            bitmap = []
            for y in range(bw_img.height):
                row = []
                for x in range(bw_img.width):
                    pixel = bw_img.getpixel((x, y))
                    row.append(1 if pixel == 255 else 0)
                bitmap.append(row)            
            save_path = os.path.join(os.getcwd(), 'bitmap_output.txt')
            with open(save_path, 'w') as f:
                for row in bitmap:
                    f.write(' '.join(map(str, row)) + '\n')
            
            print(f"Bitmap saved to {save_path}")
        except Exception as e:
            print(f"Error opening or saving the image: {e}")
    else:
        print(f"Unsupported file format: {file_extension}")


if __name__ == "__main__":
    image_path = 'Map.png'     
    load_and_convert_image_to_bitmap(image_path)
