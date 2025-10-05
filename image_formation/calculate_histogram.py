def calculate_histogram(img, bins):
    # Initialize histogram
    hist = [0] * bins # Array of length 'bins' initialized to 0
    bin_width = 255 / bins # Width of each bin

    # Flatten the image and count occurrences
    for pixel in img.flatten():
        # Clamp pixel value to [0, 255]
        value = min(max(int(pixel), 0), 255)
        bin_idx = int(value // bin_width)
        if bin_idx == bins:  # Handle edge case where value == 255
            bin_idx = bins - 1
        hist[bin_idx] += 1

    total = sum(hist)
    dist = [h / total for h in hist] if total > 0 else [0] * bins
    return hist, dist

# Plot the distribution of the x-ray image:S 
if __name__ == "__main__":
    import cv2
    import matplotlib.pyplot as plt

    # Load a grayscale image
    image = cv2.imread('images\\x_ray_low_contrast.jpg', cv2.IMREAD_GRAYSCALE)

    # Calculate histogram with 256 bins
    hist, dist = calculate_histogram(image, 256)

    # Plot histogram
    plt.figure(figsize=(7, 7))
    plt.subplot(1, 1, 1)
    plt.title('Histogram')
    plt.bar(range(256), hist, width=1.0)
    plt.xlim([0, 255])
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()