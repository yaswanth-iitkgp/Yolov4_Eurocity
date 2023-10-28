#!/bin/bash

# Loop over each line (image path) in test.txt
cd darknet
while IFS= read -r image_path; do
    # Run YOLOv4 detector on the image
    ../darknet/darknet detector test ../data/eurocity.data ../data/yolov4_eurocity.cfg ../saved_model/yolov4_eurocity_best.weights -thresh 0.5 "$image_path"

    # Move and rename the predictions.jpg file
    mv predictions.jpg ../data/saved_predictions_p5_map6336/$(basename "$image_path")
done < ../data/test.txt
