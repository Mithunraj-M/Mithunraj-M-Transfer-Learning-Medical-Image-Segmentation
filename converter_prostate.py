import os
import pydicom
from PIL import Image
import numpy as np

# Set the paths
input_dir = r"C:\Users\mithu\Desktop\research intership cad\Datasets\ProstateX\manifest-1605042674814\PROSTATEx"  # Main folder containing all 'ProstateX-XXX' folders
output_dir = r"C:\Users\mithu\Desktop\research intership cad\Datasets\ProstateX_dataset"  # Folder where you want to save the converted images

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to convert DICOM file to image
def dicom_to_image(dicom_file_path, output_file_path):
    ds = pydicom.dcmread(dicom_file_path)
    pixel_array = ds.pixel_array

    # Normalize the pixel array to 0-255 and convert to uint8
    image_array = ((pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)
    
    # Convert to image using Pillow and save it
    image = Image.fromarray(image_array)
    image.save(output_file_path)

# Process all DICOM files in the nested directory structure
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.dcm'):  # Ensure it's a DICOM file
            dicom_file_path = os.path.join(root, file)
            
            # Construct output image file name with a unique identifier
            relative_path = os.path.relpath(dicom_file_path, input_dir)
            relative_path = relative_path.replace(os.sep, '_')  # Replace folder separators with underscores
            output_file_name = relative_path.replace('.dcm', '.png')
            output_file_path = os.path.join(output_dir, output_file_name)
            
            # Convert and save the image
            dicom_to_image(dicom_file_path, output_file_path)

print("Conversion complete!")
