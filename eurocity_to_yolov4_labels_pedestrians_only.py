import os
import json
import random
import shutil
from tqdm import tqdm

def parse_eurocity_annotation(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        
    annotations = []
    for item in data.get('children', []):
        # Check for ignore conditions
        if 'ignore' in item.get('tags', []) or (item.get('x1', 0) - item.get('x0', 0)) < 20 or (item.get('y1', 0) - item.get('y0', 0)) < 20:
            continue  # Skip the annotation
        xmin = item.get('x0', 0)
        ymin = item.get('y0', 0)
        xmax = item.get('x1', 0)
        ymax = item.get('y1', 0)
        
        # Get the class name from the JSON file
        class_name = item.get('identity', 'unknown')
        
        if (xmax - xmin) >= 20 or (ymax - ymin) >= 20:  # Check if width and height are at least 20 pixels
            annotations.append((class_name, xmin, ymin, xmax, ymax))
    
    img_width = data.get('imagewidth', 0)
    img_height = data.get('imageheight', 0)
    
    return annotations, img_width, img_height

# Define a dictionary to map class names to class IDs
# The 'pedestrian' class is mapped to the class ID 0, and all other classes are mapped to the class ID 1
class_dict = {
    'pedestrian': 0,
    'person-group-far-away': 0,
    'rider': 0
}

def convert_to_yolo_format(annotations, img_width, img_height, class_dict):
    yolo_data = []
    for (class_name, xmin, ymin, xmax, ymax) in annotations:
        # Convert class name to class ID
        class_id = class_dict.get(class_name, 1) # 0 is the class ID for all non-pedestrian classes
        
        x_center = (xmin + xmax) / 2.0 / img_width
        y_center = (ymin + ymax) / 2.0 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        #if class_id == 0:  # Only include annotations for the 'pedestrian', 'rider', and related classes
        yolo_data.append(f"{class_id} {x_center} {y_center} {width} {height}")
    
    return yolo_data



def copy_and_convert_flat_structure(train_dir, target_dir, img_train_dir, img_target_dir, percentage=1.0):
    for city in tqdm(os.listdir(train_dir), desc="Processing cities", unit="city"):
        city_train_dir = os.path.join(train_dir, city)
        city_img_train_dir = os.path.join(img_train_dir, city)

        train_files = [f for f in os.listdir(city_train_dir) if f.endswith('.json')]
        num_target_files = int(len(train_files) * percentage)
        target_files = random.sample(train_files, num_target_files)

        for file in target_files:
            json_path = os.path.join(city_train_dir, file)
            annotations, img_width, img_height = parse_eurocity_annotation(json_path)
            yolo_data = convert_to_yolo_format(annotations, img_width, img_height, class_dict)
            #annotations, img_width, img_height = parse_eurocity_annotation(json_path)
            #yolo_data = convert_to_yolo_format(annotations, img_width, img_height)

            # Only write non-empty annotations
            # Move images and label files without annotations to another folder
            if yolo_data:
                output_file_name = os.path.splitext(file)[0] + ".txt"
                
                # Ensure target directory exists
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                with open(os.path.join(target_dir, output_file_name), 'w') as outfile:
                    outfile.write("\n".join(yolo_data))
        

            for ext in ['.jpg', '.jpeg', '.png']:
                img_file = file.replace('.json', ext)
                img_path = os.path.join(city_img_train_dir, img_file)
                if os.path.exists(img_path):
                    shutil.copy(img_path, os.path.join(img_target_dir, img_file.replace('.json', ext)))
                    break

BASE_DIR = "../eurocity/ECP"
PERIODS = ["day", "night"]
YOLO_OUTPUT_DIR = "data"

for period in PERIODS:
    TRAIN_DIR = os.path.join(BASE_DIR, period, "labels/train")
    VAL_DIR = os.path.join(BASE_DIR, period, "labels/val")

    IMG_TRAIN_DIR = os.path.join(BASE_DIR, period, "img/train")
    IMG_VAL_DIR = os.path.join(BASE_DIR, period, "img/val")

    # for training we need labels also in the same directory as images
    YOLO_TRAIN_DIR = os.path.join(YOLO_OUTPUT_DIR, period, "img/train")
    YOLO_VAL_DIR = os.path.join(YOLO_OUTPUT_DIR, period, "img/val")
    YOLO_TEST_DIR = os.path.join(YOLO_OUTPUT_DIR, period, "img/test")

    YOLO_IMG_TRAIN_DIR = os.path.join(YOLO_OUTPUT_DIR, period, "img/train")
    YOLO_IMG_VAL_DIR = os.path.join(YOLO_OUTPUT_DIR, period, "img/val")
    YOLO_IMG_TEST_DIR = os.path.join(YOLO_OUTPUT_DIR, period, "img/test")

    if not os.path.exists(YOLO_IMG_TRAIN_DIR):
        os.makedirs(YOLO_IMG_TRAIN_DIR)
    if not os.path.exists(YOLO_IMG_VAL_DIR):
        os.makedirs(YOLO_IMG_VAL_DIR)
    if not os.path.exists(YOLO_IMG_TEST_DIR):
        os.makedirs(YOLO_IMG_TEST_DIR)


    # Copy and convert 10% of the training data to YOLO validation format
    copy_and_convert_flat_structure(TRAIN_DIR, YOLO_VAL_DIR, IMG_TRAIN_DIR, YOLO_IMG_VAL_DIR, percentage=0.1)

    # Copy and convert the remaining 90% of training data to YOLO training format
    copy_and_convert_flat_structure(TRAIN_DIR, YOLO_TRAIN_DIR, IMG_TRAIN_DIR, YOLO_IMG_TRAIN_DIR, percentage=0.9)

    # Copy and convert ECP validation data to YOLO test format
    copy_and_convert_flat_structure(VAL_DIR, YOLO_TEST_DIR, IMG_VAL_DIR, YOLO_IMG_TEST_DIR)
