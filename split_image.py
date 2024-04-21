from PIL import Image
import os

def slice_image(input_image_path, output_folder, tile_width=600, tile_height=600):
    # Open the image file
    img = Image.open(input_image_path)
    image_width, image_height = img.size

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop over the image in 600x300 steps
    tile_num = 0
    for top in range(0, image_height, tile_height):
        for left in range(0, image_width, tile_width):
            # Compute the new bottom and right coordinates for the image slice
            bottom = min(top + tile_height, image_height)
            right = min(left + tile_width, image_width)

            # Crop the image to the 600x300 tile
            tile = img.crop((left, top, right, bottom))

            # Save the tile to an output file
            tile_path = os.path.join(output_folder, f"tile_{tile_num}.png")
            tile.save(tile_path)
            tile_num += 1

    print(f"Generated {tile_num} tiles for {input_image_path}.")

def process_images_in_folder(input_folder, output_base_folder):
    # List all files in the input directory
    for image_file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, image_file)
        # Check if the file is an image
        if os.path.isfile(file_path) and image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Create a unique output folder for each image
            output_folder = os.path.join(output_base_folder, os.path.splitext(image_file)[0] + '_tiles')
            slice_image(file_path, output_folder)

# Usage
input_folder = "./images"
output_base_folder = "./split_images"
process_images_in_folder(input_folder, output_base_folder)
