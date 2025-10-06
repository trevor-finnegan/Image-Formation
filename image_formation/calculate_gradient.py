import numpy as np
import matplotlib.pyplot as plt
import cv2
import apply_convolution as conv

SOBEL_X = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]], dtype=np.float32)  # verticle edges

SOBEL_Y = np.array([[-1,-2,-1],
                    [ 0, 0, 0],
                    [ 1, 2, 1]], dtype=np.float32)  # horizontal edges

def calculate_gradient(img, return_angle=False):
    gx = conv.apply_convolution(img, SOBEL_X)  # float32, can be negative
    gy = conv.apply_convolution(img, SOBEL_Y)

    mag = np.sqrt(gx*gx + gy*gy)               # float32
    # normalize to [0,255]
    mmax = mag.max()
    vis = (mag / mmax * 255.0) if mmax > 0 else np.zeros_like(mag)
    vis = vis.astype(np.uint8)

    if return_angle:
        angle = np.arctan2(gy, gx)  # float32, radians
        return vis, angle
    return vis

if __name__ == "__main__":
# Example: gradient of a 2x2 checkerboard
    img = cv2.imread('images\\checkerboard.jpg', cv2.IMREAD_GRAYSCALE)

    # Compute gradient magnitude
    grad = calculate_gradient(img)

    # Display original and gradient images
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.title('Original')
    plt.imshow(img, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Gradient Magnitude')
    plt.imshow(grad, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    plt.tight_layout()
    plt.show()