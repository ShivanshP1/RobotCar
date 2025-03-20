from PIL import Image
import numpy as np
import os

Image.MAX_IMAGE_PIXELS = None
img = Image.open('Map.png')
img_gray = img.convert('L')
img_array = np.array(img_gray)
print(f"Original image size: {img_array.shape}")


def max_pooling(image, pool_size=3):
    height, width = image.shape
    new_height = height // pool_size
    new_width = width // pool_size
    pooled_image = np.zeros((new_height, new_width))
    for i in range(new_height):
        for j in range(new_width):
            region = image[i*pool_size:(i+1)*pool_size, j*pool_size:(j+1)*pool_size]
            pooled_image[i, j] = np.max(region)  
    return pooled_image


pooled_img = img_array
for _ in range(3): 
    pooled_img = max_pooling(pooled_img)
print(f"Pooled image size: {pooled_img.shape}")
threshold = 128 
bitmap = (pooled_img > threshold).astype(int)
print("Bitmap:")
print(bitmap)

output_path = "pooled_bitmap.txt"
np.savetxt(output_path, bitmap, fmt='%d', delimiter=' ')
print(f"Bitmap saved to {output_path}")
