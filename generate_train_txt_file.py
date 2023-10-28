import os

def generate_txt_file(file_path, directories):
    """Generate .txt file containing paths to images from given directories."""
    with open(file_path, 'w') as file:
        for directory in directories:
            print(f"Processing directory: {directory}")
            if not os.path.exists(directory):
                print(f"Directory not found: {directory}")
                continue
            file_count = 0
            for root, _, files in os.walk(directory):
                for img_file in files:
                    if img_file.endswith(('.jpg', '.jpeg', '.png')):
                        file.write(os.path.join('../',root, img_file) + '\n') # eg is  ../data/day/img/train/Barcelona/Barcelona_000000_000000_leftImg8bit.png
                        file_count += 1
            print(f"Found {file_count} image files in {directory}")

# Directories for training, validation, and testing images
train_directories = [
    "data/day/img/train/",
    "data/night/img/train/"
]

valid_directories = [
    "data/day/img/val/",
    "data/night/img/val/"
]

# Assuming there's a test directory like this, adjust if different
test_directories = [
    "data/day/img/test/",
    "data/night/img/test/"
]

# Generate .txt files
generate_txt_file("data/train.txt", train_directories)
generate_txt_file("data/valid.txt", valid_directories)
generate_txt_file("data/test.txt", test_directories)
