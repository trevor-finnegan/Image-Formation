import numpy as np
import matplotlib.pyplot as plt
import cv2
import apply_convolution as conv
import median_filter as mf
median_filter = mf.median_filter
apply_convolution = conv.apply_convolution

# Filter for SOBEL_X
SOBEL_X = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]], dtype=np.float32)

# Filter for SOBEL_Y
SOBEL_Y = np.array([[-1,-2,-1],
                    [ 0, 0, 0],
                    [ 1, 2, 1]], dtype=np.float32)

def calculate_gradient(img, return_angle=False):
    gx = apply_convolution(img, SOBEL_X)
    gy = apply_convolution(img, SOBEL_Y)

    mag = np.sqrt(gx*gx + gy*gy)
    # normalize to [0,255]
    mmax = mag.max()
    vis = (mag / mmax * 255.0) if mmax > 0 else np.zeros_like(mag)
    vis = vis.astype(np.uint8)

    if return_angle:
        angle = np.arctan2(gy, gx)  # float32, radians
        return vis, angle
    return vis

# Add random salt & pepper noise to the image
# ==> adds black & white pixels at a probability of p
def add_salt_pepper(img, p=0.05):
    rnd = np.random.rand(*img.shape)
    noisy = img.copy()
    noisy[rnd < (p/2)] = 0
    noisy[rnd > 1 - (p/2)] = 255
    return noisy

# Returns statistics of the gradient magnitude image
def summarize_grad(mag):
    nz = np.count_nonzero(mag)
    p95 = np.percentile(mag, 95)
    p99 = np.percentile(mag, 99)
    return nz, p95, p99

if __name__ == "__main__":
    img = cv2.imread("images/rose_grayscale.jpg", cv2.IMREAD_GRAYSCALE)
    assert img is not None

    # Corrupt with salt & pepper
    noisy = add_salt_pepper(img)

    # Median filters
    med3 = median_filter(noisy, size=3)
    med5 = median_filter(noisy, size=5)

    # Gradient magnitudes
    g_noisy = calculate_gradient(noisy)
    g_med3 = calculate_gradient(med3)
    g_med5 = calculate_gradient(med5)

    # Numeric summary
    for name, g in [("Noisy", g_noisy), ("Median 3x3", g_med3), ("Median 5x5", g_med5)]:
        nz, p95, p99 = summarize_grad(g)
        print(f"{name:12s} | nonzero: {nz:7d} | 95th percentile: {p95:6.1f} | 99th percentile: {p99:6.1f}")

    # Display Original, Noisy, Median 3x3
    plt.figure(figsize=(12, 8))
    plt.subplot(2,3,1); plt.title("Noisy (S&P)");plt.imshow(noisy,cmap="gray"); plt.axis("off")
    plt.subplot(2,3,2); plt.title("Median 3x3"); plt.imshow(med3, cmap="gray"); plt.axis("off")
    plt.subplot(2,3,3); plt.title("Median 5x5"); plt.imshow(med5,  cmap="gray"); plt.axis("off")

    # Display Gradients: Noisy, Median 3x3, Median 5x5
    plt.subplot(2,3,4); plt.title("Grad (Noisy)");  plt.imshow(g_noisy, cmap="gray", vmin=0, vmax=255); plt.axis("off")
    plt.subplot(2,3,5); plt.title("Grad (Med 3x3)");plt.imshow(g_med3,  cmap="gray", vmin=0, vmax=255); plt.axis("off")
    plt.subplot(2,3,6); plt.title("Grad (Med 5x5)");plt.imshow(g_med5,  cmap="gray", vmin=0, vmax=255); plt.axis("off")
    plt.tight_layout(); plt.show()