#!/bin/bash

# Set paths
PYTHON_SCRIPT_PATH="/home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/groundtruth.py"  # Path to the Python script that draws bounding boxes
LABELS_DIR="/home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/data/day/img/test"  # Directory containing the YOLO label files
OUTPUT_DIR="/home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/data/saved_ground_truth"  # Directory to save visualized images with ground truth annotations

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR
BASE_PATH="/home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity"

# Loop through each image path in test.txt
while IFS= read -r relative_image_path; do
    # Convert relative path to absolute path
    image_path="$BASE_PATH/${relative_image_path:3}" 
    
    # Print the currently processed image for tracking
    echo "Processing image: $image_path"
    
    # Get the corresponding label file path
    label_file=$(basename "$image_path" .png).txt  # Assuming .png, modify if using another format
    label_path="$LABELS_DIR/$label_file"
    
    echo "Label file: $label_path"

    # Check if label file exists, if not, skip the image
    if [ ! -f "$label_path" ]; then
        echo "Label file for $image_path not found. Skipping."
        continue
    fi

    # Run the Python script to draw the ground truth boxes on the image
    python $PYTHON_SCRIPT_PATH "$image_path" "$label_path" "$OUTPUT_DIR"
done < /home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/data/test.txt
#python groundtruth.py /home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/data/day/img/test/wuerzburg_00726.png /home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/data/day/img/test/wuerzburg_00726.txt /home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/data/saved_ground_truth