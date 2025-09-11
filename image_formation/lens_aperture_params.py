import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors

# Thin Lens Formula:
# -------------------------------------------------------------
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
    # Also get get the first element loglog returns (which is the line object)
    # since we will use its color for the vertical line
    line, = plt.loglog(z0, zi, label=f"f = {f}mm")
    plt.axvline(f, color=line.get_color(), linestyle='--') # Add dashed vertical line at f

plt.xlabel("Object distance z0 (mm)")
plt.ylabel("Image distance zi (mm)")
plt.ylim(0, 3000)
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()
# -------------------------------------------------------------

# F-number formula:
# -------------------------------------------------------------

# f numbers and their associated real world focal lengths
f_numbers = [
    (1.4, [24]),
    (1.8, [50]),
    (2.8, [70, 200, 400]),
    (4.0, [600])]

all_f_vals = np.linspace(24, 600, 400)

plt.figure(figsize=(8,6))

for N, f_vals in f_numbers:
    D_vals = all_f_vals / N
    line, = plt.plot(all_f_vals, D_vals, label=f"f/{N}", lw=2)

    # Add markers for real world focal lengths along the continuous line associated with an f-number
    for f in f_vals:
        # Vertical line along a representing a real world focal length 
        plt.axvline(f, ls="--", color=line.get_color(), lw=1.5, alpha=0.35, zorder=1)

        # Point along the continuous f-number line where real world the real world focal length intersects
        plt.scatter([f], [f/N], s=55, zorder=3, facecolor=line.get_color(), edgecolor="black")

plt.xlabel("Focal length f (mm)")
plt.ylabel("Aperture diameter D (mm)")
plt.title("Aperture Diameter vs Focal Length")
plt.grid(True, which="both", ls="--", alpha=0.25)

# Legends:

# Legend for lines (associated with a fixed f number and the
# aperture diameters the produce based on a increasing focal length)
line_legend = plt.legend(title="F-numbers", loc="upper left")
plt.gca().add_artist(line_legend)

# Legend for markers (associated with computed D values at 
# the given real world focal lengths along the lines for f numbers)
proxy_vline = Line2D([0], [0], ls="--", color="k", alpha=0.35)
proxy_point = Line2D([0], [0], marker="o", color="k", markerfacecolor="white",
                     markeredgecolor="black", lw=0)
plt.legend([proxy_vline, proxy_point],
           ["real-world focal length", "computed D at real-world focal length"],
           loc="upper center")

plt.tight_layout()
plt.show()