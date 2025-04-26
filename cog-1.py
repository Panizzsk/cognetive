import numpy as np
import matplotlib.pyplot as plt

# Hodgkin-Huxley model parameters
C = 1.0  # Capacitance (μF/cm²)
gNa = 120.0  # Sodium conductance (mS/cm²)
gK = 36.0  # Potassium conductance (mS/cm²)
gL = 0.3  # Leak conductance (mS/cm²)
ENa = 50.0  # Sodium reversal potential (mV)
EK = -77.0  # Potassium reversal potential (mV)
EL = -54.4  # Leak reversal potential (mV)

# Initial conditions
V0 = -65.0  # Initial membrane voltage (mV)
n0 = 0.32
m0 = 0.05
h0 = 0.6

# Create a stimulus waveform (e.g., a square pulse)
stim_duration = 500  # Duration of the applied current (ms)
stim_amplitude = 20.0  # Amplitude of the applied current (μA/cm²)
stim = np.zeros(1999)
stim[700:700 + stim_duration] = stim_amplitude

# Simulate the Hodgkin-Huxley model
dt = 0.01  # Time step (ms)
timesteps = np.arange(0, len(stim)) * dt

v = np.zeros(len(stim))
n, m, h = n0, m0, h0

for i, I in enumerate(stim):
    alpha_m = lambda v: 0.1 * (v[i] + 40) / (1 - np.exp(-(v[i] + 40) / 10))
    beta_m = lambda v: 4 * np.exp(-(v[i] + 65) / 18)
    alpha_h = lambda v: 0.07 * np.exp(-(v[i] + 65) / 20)
    beta_h = lambda v: 1 / (1 + np.exp(-(v[i] + 35) / 10))
    alpha_n = lambda v: 0.01 * (v[i] + 55) / (1 - np.exp(-(v[i] + 55) / 10))
    beta_n = lambda v: 0.125 * np.exp(-(v[i] + 65) / 80)

    n += dt * (alpha_n() * (1 - n) - beta_n() * n)
    m += dt * (alpha_m() * (1 - m) - beta_m() * m)
    h += dt * (alpha_h() * (1 - h) - beta_h() * h)

    INa = gNa * m**3 * h * (v[i] - ENa)
    IK = gK * n**4 * (v[i] - EK)
    IL = gL * (v[i] - EL)

    dv = (I - INa - IK - IL) / C
    v[i + 1] = v[i] + dt * dv

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(timesteps, v, label="Membrane Voltage (mV)", color="blue")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.title("Hodgkin-Huxley Spiking Neuron Model")
plt.grid()
plt.legend()
plt.show()
