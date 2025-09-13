import numpy as np
import matplotlib.pyplot as plt

# ---------------- Parameters (same base as Ex. 3) ----------------
signal_freq   = 5.0   # Hz
duration      = 2.0   # seconds
sampling_freq = 8   # Hz (try raising this later)
num_bits      = 3     # 3-bit uniform quantizer -> 8 levels
min_signal    = -1.0
max_signal    =  1.0

noise_mean = 0.0
noise_std  = 0.1 

# 
def original_signal(t):
    return np.sin(2 * np.pi * signal_freq * t)

# Adds noise to a signal
def add_gaussian_noise(signal, mean, std):
    mag = np.max(signal) - np.min(signal)
    noise = np.random.normal(mean, std * mag, size=signal.shape)
    return signal + noise

# Creates the original signal
def create_original_signal():
    t_points = np.linspace(0, duration, 1000, endpoint=False)
    return original_signal(t_points)

# Creates a signal samped based on the constant sampling frequency
def create_sampled_signal():
    n = int(sampling_freq * duration)
    t_sampled = np.linspace(0, duration, n, endpoint=False)
    return original_signal(t_sampled), t_sampled

# Quantizes a sampled signal (based on constant variables)
# Returns quantized values at the sample times
def quantize(sampled_signal):
    n_levels = 2**num_bits
    qs = np.round(
        (sampled_signal - min_signal) / (max_signal - min_signal) * (n_levels - 1))
    quantized_noisy_signal = min_signal + qs * (max_signal - min_signal)/(n_levels - 1)
    return quantized_noisy_signal

# Computes mean square error
def mse(a, b):
    a = np.asarray(a)
    b = np.asarray(b)
    return np.mean((a - b)**2)

# Computes root mean square error
def rmse(a, b):
    return np.sqrt(mse(a, b))

# Computes peak signal-to-noise ratio
def psnr(a, b):
    mse_noise = mse(a, b)
    if mse_noise == 0:
        return np.inf
    return 10.0 * np.log10((max_signal**2) / mse_noise)


const_signal = create_original_signal() # Get the original signal
t_points = np.linspace(0, duration, 1000, endpoint=False) # create x-axis values for full signal

noisy_original_signal = add_gaussian_noise(const_signal, mean=noise_mean, std=noise_std) # add noise to original signal

sampled_signal, t_sampled = create_sampled_signal() # Get the sampled
noisy_sampled_signal = add_gaussian_noise(sampled_signal, noise_mean, noise_std) # Add noise to the sampled signal

plt.plot(t_points, noisy_original_signal, label="Noisy Sampled Signal") # Plot the noisy sampled signal with respect to the times sampled

quantized_noisy_signal = quantize(noisy_sampled_signal) # Quantize the noisy sampled signal

# Compute the error between the sampled signal and the sampled signal with noise
mse_noise = mse(sampled_signal, noisy_sampled_signal)
rmse_noise = rmse(sampled_signal, noisy_sampled_signal)
psnr_noise = psnr(sampled_signal, noisy_sampled_signal)

# Compute the error between the clean sampled signal and the noisy sampled signal after quantization
mse_total  = mse(sampled_signal, quantized_noisy_signal)
rmse_total = rmse(sampled_signal, quantized_noisy_signal)
psnr_total = psnr(sampled_signal, quantized_noisy_signal)

# Print the error metrics
print("===================== Error metrics: ======================")
print(f"Noise only:      MSE={mse_noise:.6f}  RMSE={rmse_noise:.6f}  PSNR={psnr_noise:.2f} dB")
print(f"Noise + quant.:  MSE={mse_total:.6f}  RMSE={rmse_total:.6f}  PSNR={psnr_total:.2f} dB")

# Plot
plt.step(
    t_sampled,
    quantized_noisy_signal,
    where="post",
    label=f"Quantized Signal ({num_bits} bits)",
    linestyle="--",
    color="r")

plt.scatter(t_sampled, quantized_noisy_signal, s=60, zorder=3, color="r", edgecolor="black")

plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Sampling and Quantization of a 5 Hz Sine")
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend(loc="best", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()



