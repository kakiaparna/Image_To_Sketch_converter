import cv2
import numpy as np

def convert_to_sketch(input_path, output_path, sketch_type='pencil'):
    """
    Convert an image to a sketch using OpenCV
    
    Parameters:
    input_path (str): Path to the input image
    output_path (str): Path to save the output sketch
    sketch_type (str): Type of sketch effect ('pencil', 'detail', 'contour')
    """
    # Read the image
    image = cv2.imread(input_path)
    
    if image is None:
        raise ValueError(f"Could not read image from {input_path}")
    
    if sketch_type == 'pencil':
        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Invert the grayscale image
        inverted_image = 255 - gray_image
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)
        
        # Invert the blurred image
        inverted_blurred = 255 - blurred
        
        # Create pencil sketch
        sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
        
        # Save the sketch
        cv2.imwrite(output_path, sketch)
    
    elif sketch_type == 'detail':
        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray_image, 30, 100)
        
        # Save the sketch
        cv2.imwrite(output_path, edges)
    
    elif sketch_type == 'contour':
        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter to reduce noise and keep edges sharp
        bilateral = cv2.bilateralFilter(gray_image, 9, 75, 75)
        
        # Use adaptive thresholding
        sketch = cv2.adaptiveThreshold(bilateral, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
        
        # Save the sketch
        cv2.imwrite(output_path, sketch)
    
    else:
        raise ValueError(f"Unsupported sketch type: {sketch_type}")
    
    return output_path