import os
import glob
import cv2
import numpy as np
import shutil
import re


def isbright(image, dim=10, thresh_mean=0.5, thresh_white=0.4):
    """
    Checks if an image is bright based on average lightness and white pixel percentage.

    Args:
        image: The image to be analyzed (OpenCV image object).
        dim: Resize dimension for efficiency (default: 10).
        thresh_mean: Threshold for average lightness (default: 0.5).
        thresh_white: Threshold for white pixel percentage (default: 0.4).

    Returns:
        True if the image is bright, False otherwise.
    """
    try:
        # Resize image for efficiency
        image = cv2.resize(image, (dim, dim))

        # Convert to LAB and extract L channel
        L, A, B = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2LAB))
        # Normalize L channel
        L = L / np.max(L)

        # Check average lightness
        is_bright_mean = np.mean(L) > thresh_mean

        # Calculate white pixel percentage
        white_pixels = np.sum(L >= 0.95) / (
            dim * dim
        )  # Threshold for near-white pixels
        is_bright_white = white_pixels > thresh_white

        # Combine checks using logical OR for more flexibility
        return is_bright_mean or is_bright_white
    except (cv2.error, OSError) as e:
        print(f"Error processing image: {e}")
        return None  # Or handle differently (e.g., skip the image)


# Get current script's directory
current_path = os.path.dirname(os.path.abspath(__file__))

# Create output directories (improve error handling with exist_ok=True)
bright_dir = os.path.join(current_path, "bright")
dark_dir = os.path.join(current_path, "dark")
os.makedirs(bright_dir, exist_ok=True)
os.makedirs(dark_dir, exist_ok=True)

bright_count = 0
dark_count = 0

# Iterate through PNG images
for i, path in enumerate(glob.glob(os.path.join(current_path, "*.png"))):
    # Load image
    image = cv2.imread(path)

    # Classify image
    destination = bright_dir if isbright(image) else dark_dir
    filename = os.path.basename(path)
    destination_path = os.path.join(destination, filename)

    # Move image
    shutil.move(path, destination_path)

    if re.search(r"dark/", destination_path) is not None:
        dark_count += 1
        print(f"{filename} moved to dark")
    else:
        bright_count += 1
        print(f"{filename} moved to bright")


print("Finished!")
print("")
print(f"{bright_count} images classified as bright.")
print(f"{dark_count} images classified as dark.")
