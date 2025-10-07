import numpy as np
import contrast_stretch as cs
import matplotlib.pyplot as plt

def equalize_histogram(img):
        # Flatten the image to a 1D array
        flat = img.flatten()
        # Compute histogram
        hist = [0] * 256
        for pixel in flat:
            hist[pixel] += 1
        # Compute cumulative distribution function (CDF)
        cdf = [0] * 256
        cdf[0] = hist[0]
        for i in range(1, 256):
            cdf[i] = cdf[i-1] + hist[i]
        # Normalize the CDF
        cdf_min = min(x for x in cdf if x > 0)
        total_pixels = len(flat)
        equalized = [0] * 256
        for i in range(256):
            equalized[i] = round((cdf[i] - cdf_min) / (total_pixels - cdf_min) * 255)
        # Map the pixels using the equalized CDF
        result = np.zeros_like(img)
        rows, cols = img.shape
        for i in range(rows):
            for j in range(cols):
                result[i, j] = equalized[img[i, j]]
        return result

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import cv2

    image = cv2.imread('images\\tree_low_contrast.jpg', cv2.IMREAD_GRAYSCALE)

    # Set r_min and r_max to 2nd and 98th percentile respectively for contrast stretching
    # Using percentiles helps to avoid the influence of outliers (i.e. better than [0, 255])
    r_min, r_max = np.percentile(image, 2), np.percentile(image, 98)

    # Calculate contrast stretched and histogram equalized images
    stretched_image = cs.contrast_stretch(image, r_min, r_max)
    equalized_image = equalize_histogram(image)

    # Plot the original image
    plt.figure(figsize=(15, 4))
    plt.subplot(1, 3, 1)
    plt.title('Original Image')
    plt.imshow(image, cmap='gray')
    plt.axis('off')

    # Plot the contrast stretched image
    plt.subplot(1, 3, 2)
    plt.title('Contrast Stretched')
    plt.imshow(stretched_image, cmap='gray')
    plt.axis('off')

    # Plot the histogram equalized image
    plt.subplot(1, 3, 3)
    plt.title('Histogram Equalized')
    plt.imshow(equalized_image, cmap='gray')
    plt.axis('off')

    # Plot histograms
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(15, 4))

    # Original histogram
    plt.subplot(1, 3, 1)
    plt.title("Original Histogram")
    plt.hist(image.flatten(), bins=256, range=[0, 255], color='black')
    plt.xlabel("Intensity")
    plt.ylabel("Count")

    # Stretched histogram
    plt.subplot(1, 3, 2)
    plt.title("Stretched Histogram")
    plt.hist(stretched_image.flatten(), bins=256, range=[0, 255], color='black')
    plt.xlabel("Intensity")
    plt.ylabel("Count")

    # Equalized histogram
    plt.subplot(1, 3, 3)
    plt.title("Equalized Histogram")
    plt.hist(equalized_image.flatten(), bins=256, range=[0, 255], color='black')
    plt.xlabel("Intensity")
    plt.ylabel("Count")

    plt.tight_layout()
    plt.show()
	
