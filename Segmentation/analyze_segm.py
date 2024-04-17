from PIL import Image
import numpy as np

def analyze_image_colors(image_path):
    img = Image.open(image_path)
    
    data = np.array(img)
    
    pixels = data.reshape((-1, 3))
    
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    total_pixels = pixels.shape[0]
    color_percentages = counts / total_pixels * 100
    
    for color, percentage in zip(unique_colors, color_percentages):
        print(f"Color {tuple(color)} occurs {percentage:.2f}% of the image.")
    
# image_path = 'images/1_3_Spartan1strep2-10.png'
image_path = './toptest3.png'
analyze_image_colors(image_path)
