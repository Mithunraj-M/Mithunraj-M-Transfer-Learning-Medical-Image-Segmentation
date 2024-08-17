import os
import pydicom
from PIL import Image
import numpy as np

# Set the paths
input_dir = r"C:\Users\mithu\Desktop\research intership cad\Datasets\ProstateX_mask_DICOM\manifest-1605042674814\PROSTATEx"
output_dir = r"C:\Users\mithu\Desktop\research intership cad\Datasets\ProstateX_mask"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to convert multi-frame DICOM file to images
def dicom_to_images(dicom_file_path, output_dir):
    ds = pydicom.dcmread(dicom_file_path)
    
    # Calculate the number of frames to process (one-fourth of total frames)
    num_frames = ds.NumberOfFrames if 'NumberOfFrames' in ds else 1
    max_frames = num_frames // 4
    
    # Debug: Print DICOM metadata and pixel array stats
    print(f"Processing file: {dicom_file_path}")
    print(f"Photometric Interpretation: {ds.PhotometricInterpretation}")
    print(f"Total Number of Frames: {num_frames}")
    print(f"Processing the first one-fourth: {max_frames} frames")
    print(f"Pixel Array Shape: {ds.pixel_array.shape}")
    print(f"Min Pixel Value: {ds.pixel_array.min()}")
    print(f"Max Pixel Value: {ds.pixel_array.max()}")
    
    # Process the first one-fourth of the frames
    for i in range(max_frames):
        # Extract the correct image array
        image_array = ds.pixel_array[i] if num_frames > 1 else ds.pixel_array
        
        # Convert binary images directly without normalization
        image_array = (image_array * 255).astype(np.uint8)
        
        # Convert to image using Pillow
        image = Image.fromarray(image_array, 'L')  # 'L' mode is for grayscale images
        
        # Construct output image file name with a unique identifier
        relative_path = os.path.relpath(dicom_file_path, input_dir)
        relative_path = relative_path.replace(os.sep, '_')  # Replace folder separators with underscores
        output_file_name = f"{relative_path.replace('.dcm', f'_{i+1}.png')}"
        output_file_path = os.path.join(output_dir, output_file_name)
        
        # Save the image
        image.save(output_file_path)

# Process all DICOM files in the nested directory structure
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.dcm'):  # Ensure it's a DICOM file
            dicom_file_path = os.path.join(root, file)
            
            # Convert and save the images (only the first one-fourth of the frames)
            dicom_to_images(dicom_file_path, output_dir)

print("Conversion complete!")
