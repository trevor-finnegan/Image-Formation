import numpy as np

V_MIN = 0
V_MAX = 255

def contrast_stretch(img, r_min, r_max):

    # Apply contrast stretching formula
    stretched_img = (img - r_min) * ((V_MAX - V_MIN) / (r_max - r_min)) + V_MIN
    stretched_img = np.clip(stretched_img, V_MIN, V_MAX)  # Make sure values are within [0, 255]

    return stretched_img.astype(np.uint8)