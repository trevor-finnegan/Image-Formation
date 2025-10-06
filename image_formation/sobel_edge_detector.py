import numpy as np
import apply_convolution as conv
import calculate_gradient as cg
calculate_gradient = cg.calculate_gradient

SOBEL_X = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]], dtype=np.float32)  # verticle edges

SOBEL_Y = np.array([[-1,-2,-1],
                    [ 0, 0, 0],
                    [ 1, 2, 1]], dtype=np.float32)  # horizontal edges


def sobel_edge_detector(img, threshold):
    gx = conv.apply_convolution(img, SOBEL_X)
    gy = conv.apply_convolution(img, SOBEL_Y)

    # Compute gradient magnitude
    mag = np.sqrt(gx*gx + gy*gy)

    # Apply thresholding
    for i in range(mag.shape[0]):
        for j in range(mag.shape[1]):
            if mag[i, j] < threshold:
                mag[i, j] = 0
            else:
                mag[i, j] = 255

    return mag.astype(np.uint8)

def directional_edge_detector(img, direction_range):
    _, angle = calculate_gradient(img, return_angle=True)

    angle_deg = np.degrees(angle)
    angle_deg = (angle_deg + 180) % 180

    min_angle, max_angle = direction_range

    mask = (angle_deg >= min_angle) & (angle_deg <= max_angle)
    result = np.zeros_like(img)
    result[mask] = 255

    return result.astype(np.uint8)

if __name__ == "__main__":
    import cv2
    import matplotlib.pyplot as plt

    # --- load grayscale test image ---
    img = cv2.imread("images/rose_grayscale.jpg", cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("Could not read image. Check the path.")

    # --- (A) Sobel magnitude only ---
    # pick a threshold automatically from the raw magnitude to avoid hand-tuning
    # we recompute gx,gy here to estimate a percentile-based threshold
    sobel_edges = sobel_edge_detector(img, threshold=14.0)

    # --- (B) Directional edges around 45 degrees ---
    dir_edges_45 = directional_edge_detector(img, (40, 50))

    # --- (C) OpenCV Canny ---
    # Use simple auto thresholds based on the median intensity
    med = np.median(img)
    lower = int(max(0, 0.66 * med))
    upper = int(min(255, 1.33 * med))
    canny_edges = cv2.Canny(img, lower, upper)

    # --- Display ---
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 2, 1); plt.title("Original"); plt.imshow(img, cmap="gray"); plt.axis("off")
    plt.subplot(2, 2, 2); plt.title(f"Sobel (thr≈{14.0:.1f})"); plt.imshow(sobel_edges, cmap="gray", vmin=0, vmax=255); plt.axis("off")
    plt.subplot(2, 2, 3); plt.title("Directional (≈45°)"); plt.imshow(dir_edges_45, cmap="gray", vmin=0, vmax=255); plt.axis("off")
    plt.subplot(2, 2, 4); plt.title(f"Canny ({lower},{upper})"); plt.imshow(canny_edges, cmap="gray", vmin=0, vmax=255); plt.axis("off")
    plt.tight_layout()
    plt.show()