# From ChatGPT

from PIL import Image
import os

# Specify the input folder containing .tiff images
# input_folder = "C:/Purdue/LeGrand/WIP/datasets/xviewLatest/train/imagesTiff"
input_folder = "C:/Purdue/LeGrand/WIP/datasets/xviewLatest/valid/imagesTiff"


# Specify the output folder where you want to save .png images
# output_folder = "C:/Purdue/LeGrand/WIP/datasets/xviewLatest/train/imagesPNG"
output_folder = "C:/Purdue/LeGrand/WIP/datasets/xviewLatest/valid/imagesPNG"


# Create the output folder if it doesn't exist
# os.makedirs(output_folder, exist_ok=True)

# List all files in the input folder
file_list = os.listdir(input_folder)

# Loop through each file in the input folder
for file_name in file_list:
    if file_name.endswith(".tiff") or file_name.endswith(".tif"):
        # Open the .tiff image
        image = Image.open(os.path.join(input_folder, file_name))

        # Construct the output file path with the .png extension
        output_file = os.path.splitext(file_name)[0] + ".png"
        output_path = os.path.join(output_folder, output_file)

        # Convert and save the image as .png
        image.save(output_path, "PNG")

        # print(f"Converted {file_name} to {output_file}")

print("Conversion complete.")
