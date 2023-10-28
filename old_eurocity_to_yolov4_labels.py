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
        xmin = item.get('x0', 0)
        ymin = item.get('y0', 0)
        xmax = item.get('x1', 0)
        ymax = item.get('y1', 0)
        
        annotations.append((xmin, ymin, xmax, ymax))
    
    img_width = data.get('imagewidth', 0)
    img_height = data.get('imageheight', 0)
    
    return annotations, img_width, img_height

def convert_to_yolo_format(annotations, img_width, img_height):
    yolo_data = []
    for (xmin, ymin, xmax, ymax) in annotations:
        x_center = (xmin + xmax) / 2.0 / img_width
        y_center = (ymin + ymax) / 2.0 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height
        yolo_data.append(f"0 {x_center} {y_center} {width} {height}")
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
            yolo_data = convert_to_yolo_format(annotations, img_width, img_height)

            # Only write non-empty annotations
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



BASE_DIR = "eurocity/ECP"
PERIODS = ["day", "night"]
YOLO_OUTPUT_DIR = "yolov4_data_eurocity"

for period in PERIODS:
    TRAIN_DIR = os.path.join(BASE_DIR, period, "labels/train")
    VAL_DIR = os.path.join(BASE_DIR, period, "labels/val")

    IMG_TRAIN_DIR = os.path.join(BASE_DIR, period, "img/train")
    IMG_VAL_DIR = os.path.join(BASE_DIR, period, "img/val")

    YOLO_TRAIN_DIR = os.path.join(YOLO_OUTPUT_DIR, period, "labels/train")
    YOLO_VAL_DIR = os.path.join(YOLO_OUTPUT_DIR, period, "labels/val")
    YOLO_TEST_DIR = os.path.join(YOLO_OUTPUT_DIR, period, "labels/test")

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
