import numpy as np
import matplotlib.pyplot as plt
# Constants and parameters
C = 1        # Capacitance (1 μF)
g_Na = 120   # Sodium conductance (mS/cm^2)
g_K = 36     # Potassium conductance (mS/cm^2)
g_L = 0.3    # Leak conductance (mS/cm^2)
E_Na = 50    # Sodium reversal potential (mV)
E_K = -77    # Potassium reversal potential (mV)
E_L = -54.4  # Leak reversal potential (mV)

# Initial conditions
V0 = 20 # Resting membrane potential (mV)
n0 = 0.32
m0 = 0.05
h0 = 0.6


# Time parameters
dt = 0.01  # Time step (ms)
t_max = 20  # Total simulation time (ms)
num_steps = int(t_max / dt)

# Injected current parameters
starting_time_I = 0 #7 #ms
I_amplitude = -20  # 20 μA/cm^2
I_duration = 0.2#5 # ms

# Initialize arrays to store results
V = np.zeros(num_steps)
n_mat = np.zeros(num_steps)
m_mat = np.zeros(num_steps)
h_mat = np.zeros(num_steps)
gNa_values = np.zeros(num_steps)
gK_values = np.zeros(num_steps)
I=np.zeros(num_steps)
I[int(starting_time_I/dt):int(starting_time_I/dt) + int(I_duration/dt)] = I_amplitude
INa = np.zeros(num_steps)
IK = np.zeros(num_steps)
IL = np.zeros(num_steps)

# Set initial values
V[0] = V0
n_mat[0] = n0
m_mat[0] = m0
h_mat[0] = h0
n = n0
m = m0
h = h0

alpha_n = lambda V: 0.01 * (V[i] + 55) / (1 - np.exp(-(V[i] + 55) / 10))
beta_n = lambda V: 0.125 * np.exp(-(V[i] + 65) / 80)
alpha_m = lambda V: 0.1 * (V[i] + 40) / (1 - np.exp(-(V[i] + 40) / 10))
beta_m = lambda V: 4 * np.exp(-(V[i] + 65) / 18)
alpha_h = lambda V: 0.07 * np.exp(-(V[i] + 65) / 20)
beta_h = lambda V: 1 / (1 + np.exp(-(V[i] + 35) / 10))


# Simulate the model
for i in range(0, num_steps-1):
    n += dt * (alpha_n(V) * (1 - n) - beta_n(V) * n)
    m += dt * (alpha_m(V) * (1 - m) - beta_m(V) * m)
    h += dt * (alpha_h(V) * (1 - h) - beta_h(V) * h)

    n_mat[i+1] = n
    m_mat[i+1] = m
    h_mat[i+1] = h    
    
    INa[i] = g_Na * m**3 * h * (V[i] - E_Na)
    IK[i] = g_K * n**4 * (V[i] - E_K)
    IL [i]= g_L * (V[i] - E_L)

    gNa_values[i] = g_Na * (m ** 3) * h
    gK_values[i] = g_K * (n ** 4)
    
    dV = I[i] - INa[i] - IK[i] - IL[i]
    # Compute alpha and beta functions (as in the previous response)
    # Update variables using Euler method (as in the previous response)

    # Inject current during the specified duration
    V[i + 1] = V[i] + dt * dV

# Plot the membrane potential
plt.figure(figsize=(10, 6))

plt.subplot(4, 1, 1)
plt.plot(np.arange(0, t_max, dt), V, label="Membrane Potential (mV)")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.title("Hodgkin-Huxley Model: Action Potential")
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(np.arange(0, t_max, dt), gNa_values, label="gNa (mS/cm^2)")
plt.plot(np.arange(0, t_max, dt), gK_values, label="gK (mS/cm^2)")
plt.xlabel("Time (ms)")
plt.ylabel("Conductance (mS/cm^2)")
plt.title("Sodium and Potassium Conductances")
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(np.arange(0, t_max, dt), m_mat, label="m (mS/cm^2)")
plt.plot(np.arange(0, t_max, dt), n_mat, label="n (mS/cm^2)")
plt.plot(np.arange(0, t_max, dt), h_mat, label="h (mS/cm^2)")
plt.xlabel("Time (ms)")
plt.ylabel("Conductance (mS/cm^2)")
plt.title("Sodium and Potassium Conductances")
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(np.arange(0, t_max, dt), INa, label="INa (μA/cm^2)")
plt.plot(np.arange(0, t_max, dt), IK, label="IK (μA/cm^2)")
plt.plot(np.arange(0, t_max, dt), IL, label="IL (μA/cm^2)")
plt.xlabel("Time (ms)")
plt.ylabel("Injected current (μA/cm^2)")
plt.title("Injected current")
plt.grid(True)
plt.legend()



plt.tight_layout()
plt.show()
