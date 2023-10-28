import cv2
import os
import sys

def draw_ground_truth_boxes(image_path, label_path, output_directory):
    # Ensure the directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Read the image
    img = cv2.imread(image_path)
    print(f"Read image from: {image_path}")
    h, w, _ = img.shape

    # Read the bounding box coordinates from the label file
    with open(label_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            split_line = line.strip().split()
            class_id, x_center, y_center, width, height = map(float, split_line)
            # Convert normalized YOLO bbox coordinates to actual image coordinates
            x_min = int((x_center - width / 2) * w)
            y_min = int((y_center - height / 2) * h)
            x_max = int((x_center + width / 2) * w)
            y_max = int((y_center + height / 2) * h)
            # Draw the bounding box on the image
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Save the image directly to the provided output directory
    output_path = os.path.join(output_directory, os.path.basename(image_path))
    print(f"Saved visualized image to: {output_path}")
    cv2.imwrite(output_path, img)

# Call the function with provided paths
# draw_ground_truth_boxes(
#     '/home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/data/day/img/test/wuerzburg_00705.png',
#     '/home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/data/day/img/test/wuerzburg_00705.txt',
#     '/home/narsupalli-pg/iuc/nnlut/YOLOv4_Eurocity/data/saved_ground_truth'
# )
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python groundtruth.py <image_path> <label_path> <output_directory>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    label_path = sys.argv[2]
    output_directory = sys.argv[3]
    
    draw_ground_truth_boxes(image_path, label_path, output_directory)