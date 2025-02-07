
#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?                              __  __         ____
#?             ____ ___  ____ _/ /_/ /_       / __/_  ______  __________
#?            / __ `__ \/ __ `/ __/ __ \     / /_/ / / / __ \/ ___/ ___/
#?           / / / / / / /_/ / /_/ / / /    / __/ /_/ / / / / /__(__  ) 
#?          /_/ /_/ /_/\__,_/\__/_/ /_/____/_/  \__,_/_/ /_/\___/____/  
#?                                   /_____/
#?          
#?      
#?
#? Name:        math_funcs.py
#? Purpose:     Compute rms , average ....
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     09/15/2024
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------  
#? -------------------------------------------------------------------------------

import numpy as np
from scipy.fft import fft, fftfreq
#?----------------------------------------------------------------------------------------------------------------------------------------
def compute_fft(signal, fs):
    """
    Compute the Fast Fourier Transform (FFT) of a signal and return amplitude, phase, and frequency information.

    Parameters:
    signal (numpy.ndarray): Input signal.
    fs (float): Sampling frequency of the signal.

    Returns:
    tuple: Tuple containing amplitude, phase, and frequency arrays.
    """
    N = len(signal)  # Number of samples

    # Compute the FFT
    fft_result = fft(signal)

    # Compute the frequency values
    f = fftfreq(N, 1/fs)[:N//2]  # Only positive frequencies

    # Compute amplitude spectrum (normalize by N and double non-DC components)
    amplitude = (2.0 / N) * np.abs(fft_result[:N//2])

    # Compute the phase spectrum in degrees
    phase = np.angle(fft_result[:N//2], deg=True)

    return amplitude, phase, f



def resample_signal(time, signal):
    """
    Resample a signal to have uniform time points.

    Parameters:
    time (numpy.ndarray): Time values of the original signal.
    signal (numpy.ndarray): Signal values.

    Returns:
    tuple: Resampled time values and the corresponding resampled signal values.
    """
    # Generate uniform time points based on the original signal length
    new_time = np.linspace(time.min(), time.max(), len(signal))
    
    # Interpolate the signal at the new time points
    new_signal = np.interp(new_time, time, signal)
    
    return new_time, new_signal


def compute_average(signal, time_values):
    """
    Calculate the Average (AVG) of a single signal over given time values.

    Parameters:
    signal (numpy.ndarray): Signal values.
    time_values (numpy.ndarray): Time values corresponding to the signal.

    Returns:
    float: Average value of the signal.
    """
    delta_T = time_values[-1] - time_values[0]  # Total time interval

    if delta_T == 0:
        raise ValueError("Error: Time interval cannot be zero.")

    # Compute the average using trapezoidal integration
    avg_value = np.trapezoid(signal, x=time_values) / delta_T

    return avg_value


def compute_rms(signal, time_values):
    """
    Calculate the Root Mean Square (RMS) of a single signal over given time values.

    Parameters:
    signal (numpy.ndarray): Signal values.
    time_values (numpy.ndarray): Time values corresponding to the signal.

    Returns:
    float: RMS value of the signal.
    """
    delta_T = time_values[-1] - time_values[0]  # Total time interval

    if delta_T == 0:
        raise ValueError("Error: Time interval cannot be zero.")

    # Square the signal values and compute RMS using trapezoidal integration
    squared_values = signal ** 2
    rms_value = np.sqrt(np.trapz(squared_values, x=time_values) / delta_T)

    return rms_value

#?----------------------------------------------------------------------------------------------------------------------------------------