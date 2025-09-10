import numpy as np
import matplotlib.pyplot as plt

# Solve for ideal zi based on f and z0
def thin_lens_zi(f, z0):
    return 1 / (1/f - 1/z0)

focal_lengths = [3, 9, 50, 200] # in millimeters

plt.figure(figsize=(8,6))

z0_max = 10**4 # Max value of z0 (consistent for all f values)

for f in focal_lengths:
    z0_min = 1.1*f # Min value of z0

    # Compute the number of samples: (range of z0) * (4 points per mm)
    # Also round up to the nearest integer
    num = int(np.ceil((z0_max - z0_min) * 4))

    # Generate sequence of values from z0_min to z0_max
    # num specifies how many evenly spaced points to create within the range
    z0 = np.linspace(z0_min, z0_max, num=num)
    zi = thin_lens_zi(f, z0) # Get corresponding zi value

    # Plot zi with respect to z0 with logarithmically scaling axes
    # Also get get the first element loglog returns which is the line object
    # since we will use its color for the vertical line
    line, = plt.loglog(z0, zi, label=f"f = {f}mm")
    plt.axvline(f, color=line.get_color(), linestyle='--') # Add dashed vertical line at f

plt.xlabel("Object distance z0 (mm)")
plt.ylabel("Image distance zi (mm)")
plt.ylim(0, 3000)
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()