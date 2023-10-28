import os
import shutil
from tqdm import tqdm

# Specify the directories containing the images and labels
src_dirs = [
    'data/day/img/train',
    'data/day/img/test',
    'data/day/img/val',
    'data/night/img/train',
    'data/night/img/test',
    'data/night/img/val',
]

# Specify the directory to move images without corresponding labels
dst_dir = 'data/without_labels'

# Create the destination directory if it does not exist
os.makedirs(dst_dir, exist_ok=True)

# Initialize a counter for the number of images moved
total_count = 0

# For each source directory
for src_dir in src_dirs:
    # Get a list of all files in the source directory
    files = os.listdir(src_dir)

    # Initialize a counter for the number of images moved
    count = 0

    # For each file in the source directory
    for file in tqdm(files, desc=f'Processing {src_dir}', unit='file'):
        # Get the file name without the extension
        name, ext = os.path.splitext(file)
        # If the file is an image
        if ext in ['.jpg', '.png']:
            # If there is no corresponding .txt file
            if name + '.txt' not in files:
                # Define the destination path
                dst_path = os.path.join(dst_dir, file)
                # If the file already exists in the destination directory
                if os.path.exists(dst_path):
                    # Append a number to the file name to make it unique
                    i = 1
                    while os.path.exists(os.path.join(dst_dir, f'{name}_{i}{ext}')):
                        i += 1
                    dst_path = os.path.join(dst_dir, f'{name}_{i}{ext}')
                # Move the image to the destination directory
                shutil.move(os.path.join(src_dir, file), dst_path)
                # Increment the counter
                count += 1

    print(f'Moved {count} images from {src_dir} without corresponding .txt files')
    total_count += count

print(f'Total moved images: {total_count}')
