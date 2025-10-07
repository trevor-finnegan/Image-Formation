def calculate_histogram(img, bins):
    # Initialize histogram
    hist = [0] * bins # Array of length 'bins' initialized to 0
    bin_width = 255 / bins # Width of each bin

    # Flatten the image and count occurrences
    for pixel in img.flatten():
        value = min(max(int(pixel), 0), 255) # Clamp pixel value to [0, 255]
        bin_idx = int(value // bin_width)
        if bin_idx == bins:  # Handle edge case where value == 255
            bin_idx = bins - 1
        hist[bin_idx] += 1

    total = sum(hist)
    dist = [h / total for h in hist] if total > 0 else [0] * bins
    return hist, dist