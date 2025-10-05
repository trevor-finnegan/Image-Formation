import numpy as np

def median_filter(image, size):
    if size % 2 == 0:
        raise ValueError("Size must be an odd integer.")

    # Add zero padding to the image
    pad_size = size // 2
    padded_image = np.pad(image, pad_size, mode='edge')
    filtered_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Extract the region of interest
            region = padded_image[i:i + size, j:j + size]
            # Compute the median and assign it to the filtered image
            filtered_image[i, j] = np.median(region)

    return filtered_image
