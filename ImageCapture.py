import cv2
import numpy as np
import os
import time

# Initialize camera
cap = cv2.VideoCapture(0)

# Create folder for saving processed images
output_folder = "processed_images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to process image and identify colors
def identify_colors(image):
    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Flatten the image into a 2D array of pixels
    reshaped_image = hsv_image.reshape((-1, 3))

    # Convert to floating point and define criteria
    reshaped_image = np.float32(reshaped_image)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Apply k-means clustering
    _, labels, centers = cv2.kmeans(reshaped_image, 8, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert centers to integer values
    centers = np.uint8(centers)

    # Flatten the labels array
    labels = labels.flatten()

    # Find unique labels and count occurrences
    unique_labels, counts = np.unique(labels, return_counts=True)

    # Initialize a dictionary to store colors and their counts
    color_counts = {}

    # Loop through unique labels and counts
    for label, count in zip(unique_labels, counts):
        # Extract color from centers
        color = centers[label].tolist()

        # Convert color from HSV to BGR for display
        bgr_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_HSV2BGR)[0][0]

        # Convert color to tuple
        color_tuple = tuple(bgr_color)

        # Add color and count to dictionary
        color_counts[color_tuple] = count

    return color_counts

# Main loop for capturing and processing images
while True:
    # Capture frame from camera
    ret, frame = cap.read()
    if not ret:
        break

    # Start time for measuring processing time
    start_time = time.time()

    # Process the captured frame
    color_counts = identify_colors(frame)

    # End time for measuring processing time
    end_time = time.time()
    processing_time = (end_time - start_time) * 1000  # Convert to milliseconds

    # Save the processed image
    timestamp = int(time.time())
    output_path = os.path.join(output_folder, f"processed_{timestamp}.jpg")
    cv2.imwrite(output_path, frame)

    # Display the processed image
    cv2.imshow('Processed Image', frame)

    # Print detected colors and processing time
    print("Detected Colors:")
    for color, count in color_counts.items():
        print("Color:", color, "Count:", count)
    print("Processing Time:", processing_time, "ms")

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
