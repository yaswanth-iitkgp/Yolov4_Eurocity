#!/bin/bash

# Create a folder to store the results
mkdir -p results

# go to darknet folder
cd darknet

# modify the Makefile
sed -i 's/GPU=0/GPU=1/' Makefile
sed -i 's/CUDNN=0/CUDNN=1/' Makefile
sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile
sed -i 's/OPENCV=0/OPENCV=1/' Makefile
sed -i 's/AVX=0/AVX=1/' Makefile
sed -i 's/OPENMP=0/OPENMP=1/' Makefile
sed -i 's/LIBSO=0/LIBSO=1/' Makefile
sed -i 's/WANDB=0/WANDB=1/' Makefile

# compile the Darknet framework
make

# Get the number of training and testing images
NUM_TRAINING_IMAGES=$(wc -l < ../data/eurocity.train)
NUM_TESTING_IMAGES_DAY=$(wc -l < ../data/day/test.txt)
NUM_TESTING_IMAGES_NIGHT=$(wc -l < ../data/night/test.txt)

# Print the number of training and testing images
echo "Number of training images: $NUM_TRAINING_IMAGES" | tee -a ../results/setup_details.txt
echo "Number of testing images (day): $NUM_TESTING_IMAGES_DAY" | tee -a ../results/setup_details.txt
echo "Number of testing images (night): $NUM_TESTING_IMAGES_NIGHT" | tee -a ../results/setup_details.txt

# Print the GPU information and selected parameters from the cfg file to a file
nvidia-smi > ../results/setup_details.txt
grep 'batch\|subdivisions\|width\|height\|channels\|momentum\|decay\|learning_rate\|burn_in\|max_batches\|policy\|steps\|scales' ../data/yolov4_eurocity.cfg >> ../results/setup_details.txt

# Store the start time
START_TIME=$(date +%s)
CURRENT_DATE_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo "Training Start time: $CURRENT_DATA_TIME" | tee -a ../results/setup_details.txt

# Run the training
#../darknet/darknet detector train ../data/eurocity.data ../data/yolov4_eurocity.cfg yolov4.weights -dont_show -map -clear| tee ../results/training_log.txt
../darknet/darknet detector train ../data/eurocity.data ../data/yolov4_eurocity.cfg yolov4.conv.137 -dont_show -map | tee ../results/training_log.txt
#../darknet/darknet detector train ../data/eurocity.data ../data/yolov4_eurocity.cfg ../saved_model_old/yolov4_eurocity_best.weights -dont_show -map | tee ../results/training_log.txt

# Store the end time of training
TRAINING_END_TIME=$(date +%s)
#echo "Training Start time: $CURRENT_DATA_TIME" | tee -a ../results/setup_details.txt
# TEST_START_TIME=$(date +%s)
# # Loop over each line (image path) in test.txt
# cd darknet
# while IFS= read -r image_path; do
#     # Run YOLOv4 detector on the image
#     ../darknet/darknet detector test ../data/eurocity.data ../data/yolov4_eurocity.cfg ../saved_model/yolov4_eurocity_best.weights -thresh 0.5 "$image_path"

#     # Move and rename the predictions.jpg file
#     mv predictions.jpg ../data/saved_predictions_p5/$(basename "$image_path")
# done < ../data/test.txt
# TEST_END_TIME=$(date +%s)

# Calculate the time taken for training and testing
TRAINING_TIME=$((TRAINING_END_TIME - START_TIME))
# TESTING_TIME=$((TEST_END_TIME - TEST_START_TIME))

# Print the time taken for training and testing
echo "Training time: $((TRAINING_TIME / 86400)) days, $((TRAINING_TIME % 86400 / 3600)) hours, $((TRAINING_TIME % 3600 / 60)) minutes, $((TRAINING_TIME % 60)) seconds" | tee -a ../results/training_log.txt
# echo "Testing time: $((TESTING_TIME / 86400)) days, $((TESTING_TIME % 86400 / 3600)) hours, $((TESTING_TIME % 3600 / 60)) minutes, $((TESTING_TIME % 60)) seconds" | tee -a ../results/training_log.txt

