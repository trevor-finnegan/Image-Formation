import numpy as np

def apply_convolution(image, filter):
    # Apply 2D convolution using explicit for loops (grayscale, odd-sized filter).
    # Boundary condition: zero padding.
    img = image.astype(np.float32, copy=False)

    # Flip filter for true convolution
    k = np.flipud(np.fliplr(filter.astype(np.float32)))

    kH, kW = k.shape
    if kH % 2 == 0 or kW % 2 == 0:
        raise ValueError("Kernel must be odd-sized (e.g., 3x3, 5x5).")

    iH, iW = img.shape
    pad_h, pad_w = kH // 2, kW // 2

    # Zero padding ("0 boundary")
    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)

    # Output (float32)
    out = np.zeros((iH, iW), dtype=np.float32)

    # Loop of summations
    for i in range(iH):
        for j in range(iW):
            acc = 0.0
            for u in range(kH):
                for v in range(kW):
                    acc += padded[i + u, j + v] * k[u, v]
            out[i, j] = acc

    # Clip to [0,255] for grayscale display
    return np.clip(out, 0, 255).astype(np.uint8)