import numpy as np
import calculate_gradient as cg
calculate_gradient = cg.calculate_gradient

def directional_edge_detector(img, direction_range):
    # Calculate gradient angle
    _, angle = calculate_gradient(img, return_angle=True)

    angle_deg = np.degrees(angle) # Convert to degrees
    
    min_angle, max_angle = direction_range

    # Initialize mask that selects angles within the specified range
    mask = (angle_deg >= min_angle) & (angle_deg <= max_angle)

    # Create result image based on the mask
    result = np.zeros_like(img)
    result[mask] = 255

    return result.astype(np.uint8)