import numpy as np
import pandas as pd
from scipy import signal
from scipy.io import savemat
import matplotlib.pyplot as plt

# System parameters
fs = 100e3  # Switching frequency (100 kHz)
f_line = 50  # Line frequency (Hz)
V_in_nom = 230  # Nominal input voltage (V)
V_out = 400  # DC output voltage (V)
P_max = 7000  # Maximum power (W)
I_max = P_max / V_in_nom  # Maximum input current (A)
dead_time = 100e-9  # Dead time (100 ns)

# Simulation parameters
t_sim = 0.02  # Simulation time (20 ms - one line cycle)
dt = 1/(fs*100)  # Time step
t = np.arange(0, t_sim, dt)

# Generate reference signals
def generate_pwm_signals():
    # Input voltage simulation (sine wave)
    v_in = V_in_nom * np.sqrt(2) * np.sin(2 * np.pi * f_line * t)
    
    # Input current reference (in phase with voltage for PFC)
    i_ref = I_max * np.sqrt(2) * np.sin(2 * np.pi * f_line * t)
    
    # Duty cycle generation for PFC operation
    duty = 0.5 + 0.4 * np.sin(2 * np.pi * f_line * t)  # Basic approximation
    
    # Create carrier wave for PWM
    carrier = signal.sawtooth(2 * np.pi * fs * t, 0.5)  # Triangle wave
    
    # Generate PWM signals for each leg with dead-time
    pwm_upper = []
    pwm_lower = []
    
    for i in range(len(t)):
        # Main PWM comparison
        upper_on = duty[i] > carrier[i]
        lower_on = (1 - duty[i]) > carrier[i]
        
        # Apply dead-time
        if upper_on and not lower_on:
            pwm_upper.append(1)
            pwm_lower.append(0)
        elif not upper_on and lower_on:
            pwm_upper.append(0)
            pwm_lower.append(1)
        else:  # Dead-time condition
            pwm_upper.append(0)
            pwm_lower.append(0)
    
    return np.array(pwm_upper), np.array(pwm_lower), v_in, i_ref

# Generate signals for all 3 legs
# Leg A (input side)
pwm_A_upper, pwm_A_lower, v_in, i_ref = generate_pwm_signals()

# Leg B (input side - complementary to Leg A with phase shift)
pwm_B_upper, pwm_B_lower, _, _ = generate_pwm_signals()

# Leg C (output side - DC-DC conversion)
# This would typically be a fixed duty cycle for DC-DC stage
duty_dcdc = V_in_nom / V_out  # Simplified
pwm_C_upper = (signal.sawtooth(2 * np.pi * fs * t, 0.5) < duty_dcdc).astype(int)
pwm_C_lower = (signal.sawtooth(2 * np.pi * fs * t, 0.5) > (1 - duty_dcdc)).astype(int)

# Apply protection features
def apply_protections(pwm_u, pwm_l, v_in, i_ref):
    # Simulate current measurement
    i_actual = i_ref * 0.98  # Simulate slight difference
    
    # Overcurrent protection
    oc_threshold = I_max * 1.2
    oc_condition = np.abs(i_actual) > oc_threshold
    
    # Overvoltage protection
    ov_threshold = V_in_nom * 1.3
    ov_condition = np.abs(v_in) > ov_threshold
    
    # Apply protections
    for i in range(len(t)):
        if oc_condition[i] or ov_condition[i]:
            pwm_u[i] = 0
            pwm_l[i] = 0
    
    return pwm_u, pwm_l

# Apply protections to all legs
pwm_A_upper, pwm_A_lower = apply_protections(pwm_A_upper, pwm_A_lower, v_in, i_ref)
pwm_B_upper, pwm_B_lower = apply_protections(pwm_B_upper, pwm_B_lower, v_in, i_ref)
pwm_C_upper, pwm_C_lower = apply_protections(pwm_C_upper, pwm_C_lower, v_in, i_ref)

import numpy as np
from scipy.io import savemat

# Generate your time vector and PWM signals
# t = np.arange(0, t_sim, dt)  # 200,000 elements
# pwm_A_upper, pwm_A_lower, etc. (each 200,000 elements)

# Create the data matrix with proper orientation (200,000×7)
data_matrix = np.vstack([
    t,              # Time (row 0)
    pwm_A_upper,    # Row 1
    pwm_A_lower,    # Row 2
    pwm_B_upper,    # Row 3
    pwm_B_lower,    # Row 4
    pwm_C_upper,    # Row 5
    pwm_C_lower     # Row 6
]).T  # Transpose to get 200,000 rows × 7 columns

# Save to .mat file
savemat('totem_pole_plecs.mat', 
        {'PWM_data': data_matrix},
        long_field_names=True)

# Optional: Add metadata
plecs_metadata = {
    'SwitchingFrequency': fs,
    'LineFrequency': f_line,
    'InputVoltage': V_in_nom,
    'OutputVoltage': V_out,
    'DeadTime': dead_time
}

savemat('totem_pole_plecs.mat', 
        {'PWM_data': data_matrix.T, 'parameters': plecs_metadata},
        long_field_names=True)


# Plot all upper and lower PWM signals
plt.plot(t, pwm_A_upper, 'b-', label='Leg 1 Upper', linewidth=1)
plt.plot(t, pwm_A_lower, 'b--', label='Leg 1 Lower', linewidth=1)
plt.plot(t, pwm_B_upper, 'g-', label='Leg 2 Upper', linewidth=1)
plt.plot(t, pwm_B_lower, 'g--', label='Leg 2 Lower', linewidth=1)
plt.plot(t, pwm_C_upper, 'r-', label='Leg 3 Upper', linewidth=1)
plt.plot(t, pwm_C_lower, 'r--', label='Leg 3 Lower', linewidth=1)

plt.title('All PWM Signals (Full Dataset)')
plt.xlabel('Time (s)')
plt.ylabel('PWM State')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
plt.ylim(-0.1, 1.1)

# Add zoomed inset for better visibility of switching details
ax = plt.gca()
ax_inset = ax.inset_axes([0.5, 0.5, 0.45, 0.45])
ax_inset.plot(t[1000:1200], pwm_A_upper[1000:1200], 'b-', label='Leg 1 Upper')
ax_inset.plot(t[1000:1200], pwm_A_lower[1000:1200], 'b--', label='Leg 1 Lower')
ax_inset.plot(t[1000:1200], pwm_B_upper[1000:1200], 'g-', label='Leg 2 Upper')
ax_inset.plot(t[1000:1200], pwm_B_lower[1000:1200], 'g--', label='Leg 2 Lower')
ax_inset.plot(t[1000:1200], pwm_C_upper[1000:1200], 'r-', label='Leg 3 Upper')
ax_inset.plot(t[1000:1200], pwm_C_lower[1000:1200], 'r--', label='Leg 3 Lower')
ax_inset.set_title('Zoomed View (200 points)')
ax_inset.grid(True)
ax_inset.set_ylim(-0.1, 1.1)

plt.tight_layout()
plt.show()
