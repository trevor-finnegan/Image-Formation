import numpy as np
import apply_convolution as conv
import calculate_gradient as cg
import directional_edge_detector as ded
calculate_gradient = cg.calculate_gradient
directional_edge_detector = ded.directional_edge_detector

SOBEL_X = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]], dtype=np.float32)

SOBEL_Y = np.array([[-1,-2,-1],
                    [ 0, 0, 0],
                    [ 1, 2, 1]], dtype=np.float32) 


def sobel_edge_detector(img, threshold):
    gx = conv.apply_convolution(img, SOBEL_X)
    gy = conv.apply_convolution(img, SOBEL_Y)

    # Compute gradient magnitude
    mag = np.sqrt(gx*gx + gy*gy)

    if threshold is None:
        threshold = np.percentile(mag, 95)
        print(f"Using threshold: {threshold:.1f}")

    # Apply thresholding
    for i in range(mag.shape[0]):
        for j in range(mag.shape[1]):
            if mag[i, j] < threshold:
                mag[i, j] = 0
            else:
                mag[i, j] = 255

    return mag.astype(np.uint8)

if __name__ == "__main__":
    import cv2
    import matplotlib.pyplot as plt

    # --- Load grayscale test image ---
    img = cv2.imread("images/rose_grayscale.jpg", cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("Could not read image. Check the path.")

    # --- Sobel magnitude only ---
    sobel_edges = sobel_edge_detector(img, threshold=None)

    # --- Directional edges around 45 degrees ---
    dir_edges_45 = directional_edge_detector(img, (40, 50))

    # --- OpenCV Canny ---
    # Initialize thresholds based on the median intensity
    med = np.median(img)
    lower = int(max(0, 0.66 * med))
    upper = int(min(255, 1.33 * med))
    canny_edges = cv2.Canny(img, lower, upper)

    # --- Plot ---
    plt.figure(figsize=(12, 6))
    
    # Original, Sobel, Directional, Canny
    plt.subplot(2, 2, 1); plt.title("Original"); plt.imshow(img, cmap="gray"); plt.axis("off")
    plt.subplot(2, 2, 2); plt.title(f"Sobel (threshold≈{35.5:.1f})"); plt.imshow(sobel_edges, cmap="gray", vmin=0, vmax=255); plt.axis("off")
    plt.subplot(2, 2, 3); plt.title("Directional (≈45°)"); plt.imshow(dir_edges_45, cmap="gray", vmin=0, vmax=255); plt.axis("off")
    plt.subplot(2, 2, 4); plt.title(f"Canny ({lower},{upper})"); plt.imshow(canny_edges, cmap="gray", vmin=0, vmax=255); plt.axis("off")
    plt.tight_layout()
    plt.show()