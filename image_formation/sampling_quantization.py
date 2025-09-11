import numpy as np
import matplotlib.pyplot as plt

signal_freq = 5.0 # in Hz
duration = 2 # in seconds
sampling_freq = 8 # in Hz
num_bits = 3 # 3-bit quantization (8 levels: 0 - 7)
min_signal = -1 # min signal value
max_signal = 1 # max signal value


def original_signal(t):
    return np.sin(2 * np.pi * signal_freq * t)

# Continuous signal for reference
t_points = np.linspace(0, duration, 1000, endpoint=False)
cont_signal = original_signal(t_points)
plt.plot(t_points, cont_signal, label="Continuous Signal")

# Sampled signal
n = int(sampling_freq * duration)
t_sampled = np.linspace(0, duration, n, endpoint=False)
sampled_signal = original_signal(t_sampled)

# Number of distinct amplitude levels we can represent (2^3 = 8)
n_levels = 2**num_bits

# Map each sampled value to the nearest allowed level:
qs = np.round(
    (sampled_signal - min_signal) / (max_signal - min_signal) * (n_levels - 1))

# Convert the integer code back to the representative amplitude value for plotting
qv = min_signal + qs * (max_signal - min_signal)/(n_levels - 1)

# Staircase display of the quantized signal
plt.step(
    t_sampled,
    qv,
    where="post",
    label=f"Quantized Signal ({num_bits} bits)",
    linestyle="--",
    color="r")

# Show the actual points where the quantized amplitude aligned with the continuous signal
plt.scatter(t_sampled, qv, s=60, zorder=3, color="r", edgecolor="black")

# Plot
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Sampling and Quantization of a 5 Hz Sine")
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend(loc="best", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()
