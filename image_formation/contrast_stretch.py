import numpy as np

S_MIN = 0
S_MAX = 255

def contrast_stretch(img, r_min, r_max):

    # Apply contrast stretching formula
    stretched_img = (img - r_min) * ((S_MAX - S_MIN) / (r_max - r_min)) + S_MIN
    stretched_img = np.clip(stretched_img, S_MIN, S_MAX)  # Make sure values are within [0, 255]

    return stretched_img.astype(np.uint8)