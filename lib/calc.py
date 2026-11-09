#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?                        __
#?            _________ _/ /____
#?           / ___/ __ `/ / ___/
#?          / /__/ /_/ / / /__
#?          \___/\__,_/_/\___/
#?
#?
#? Name:        calc.py
#? Purpose:     signal math (RMS, average, FFT, harmonics, envelopes).
#?              Derived: parameters computed from others, recomputed per sweep point.
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     09/15/2024
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
#? -------------------------------------------------------------------------------
import  numpy                       as      np

from    scipy.fft                   import  rfft
#?----------------------------------------------------------------------------------------------------------------------------------------
class PMath:
    """Signal math on simulation results."""

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Harmonics of one signal
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def compute_harmonics(t, y, f0, n_harmonics, window):
        """Amplitudes of harmonic orders 1..n_harmonics of f0 in the signal y(t), over its last `window` seconds
        resampled uniformly (fine enough for the highest order). Harmonic k is read at bin k*f0*window, exact when the
        window holds a whole number of f0 periods (e.g. 80 kHz over whole 50 Hz cycles). Returns (orders, H)."""
        N                   = max(int(np.sum(t >= t[-1] - window)), int(4 * n_harmonics * f0 * window))
        t_u                 = t[-1] - window + np.arange(N) * (window / N)             # endpoint excluded: one exact period set
        spectrum            = np.abs(rfft(np.interp(t_u, t, y))) * (2.0 / N)
        orders              = np.arange(1, n_harmonics + 1)
        return orders, spectrum[np.rint(orders * f0 * window).astype(int)]

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Batch metrics: every column of Y (one column per waveform) over the last `window` seconds of t (None = all of t)
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def analysis_window(t, f_base, n_cycles=None):
        """Length [s] of the last whole f_base cycles of t (all of them, or up to n_cycles); None if f_base is None or
        less than one cycle is saved (the metrics then use the whole of t)."""
        if not f_base:
            return None
        cycles              = int((t[-1] - t[0]) * f_base + 1e-9)
        cycles              = min(cycles, n_cycles) if n_cycles else cycles
        return cycles / f_base if cycles >= 1 else None

    @staticmethod
    def _windowed(t, Y, window=None):
        """t and Y restricted to the last `window` seconds, with a sample interpolated exactly at the window start."""
        t                   = np.asarray(t, dtype=float)
        Y                   = np.asarray(Y, dtype=float).reshape(len(t), -1)
        if not window or window >= t[-1] - t[0]:
            return t, Y
        t0                  = t[-1] - window
        i                   = int(np.searchsorted(t, t0, side='right'))
        y0                  = np.array([np.interp(t0, t, Y[:, k]) for k in range(Y.shape[1])])
        return np.concatenate(([t0], t[i:])), np.vstack((y0, Y[i:]))

    @staticmethod
    def rms(t, Y, window=None):
        """Time-weighted RMS of each column (variable-step samples, trapezoidal integration)."""
        t, Y                = PMath._windowed(t, Y, window)
        return np.sqrt(np.trapezoid(Y**2, x=t, axis=0) / (t[-1] - t[0]))

    @staticmethod
    def average(t, Y, window=None):
        """Time-weighted average of each column."""
        t, Y                = PMath._windowed(t, Y, window)
        return np.trapezoid(Y, x=t, axis=0) / (t[-1] - t[0])

    @staticmethod
    def maximum(t, Y, window=None):
        return PMath._windowed(t, Y, window)[1].max(axis=0)

    @staticmethod
    def minimum(t, Y, window=None):
        return PMath._windowed(t, Y, window)[1].min(axis=0)

    @staticmethod
    def peak_to_peak(t, Y, window=None):
        Yw                  = PMath._windowed(t, Y, window)[1]
        return Yw.max(axis=0) - Yw.min(axis=0)

    @staticmethod
    def peak(t, Y, window=None):
        """Largest absolute value of each column."""
        return np.abs(PMath._windowed(t, Y, window)[1]).max(axis=0)

    @staticmethod
    def harmonics(t, Y, f0s, n_harmonics, window):
        """Harmonic amplitudes of each column for its own fundamental f0s[k] (None = not computed).
        Returns (orders, H) with H[k] = amplitudes of orders 1..n_harmonics of column k, NaN where f0s[k] is None."""
        orders              = np.arange(1, n_harmonics + 1)
        H                   = np.full((Y.shape[1], n_harmonics), np.nan)
        for k, f0 in enumerate(f0s):
            if f0 and window:
                H[k]        = PMath.compute_harmonics(t, Y[:, k], f0, n_harmonics, window)[1]
        return orders, H

    @staticmethod
    def calc_metrics(t, Y, window=None):
        """Every scalar metric of PMath.METRICS for each column of Y: {type: array of one value per column}."""
        return {name: func(t, Y, window) for name, func in PMath.METRICS.items()}

    @staticmethod
    def envelope(x, Y, n_buckets, log=False):
        """Min/max envelope of the columns of Y over n_buckets equal-width (or log-width) bins of the sorted x.
        Keeps switching ripple / spectral peaks visible with ~2*n_buckets points. Returns (x_env, Y_env)."""
        if len(x) <= 2 * n_buckets:
            return x, Y
        edges               = (np.geomspace(x[0], x[-1], n_buckets + 1) if log else np.linspace(x[0], x[-1], n_buckets + 1))[:-1]
        idx                 = np.unique(np.searchsorted(x, edges))
        Y_env               = np.empty((2 * len(idx), Y.shape[1]))
        Y_env[0::2]         = np.minimum.reduceat(Y, idx, axis=0)
        Y_env[1::2]         = np.maximum.reduceat(Y, idx, axis=0)
        return np.repeat(x[idx], 2), Y_env
#?----------------------------------------------------------------------------------------------------------------------------------------
#? Scalar metrics computed for every waveform: result type (also the name of its result folder / HTML report) -> function.
#? The harmonics are the additional 'FFT' type (PMath.harmonics), computed per waveform with its own fundamental.
PMath.METRICS               = {
                                'RMS'        : PMath.rms,
                                'Average'    : PMath.average,
                                'PeakToPeak' : PMath.peak_to_peak,
                                'Max'        : PMath.maximum,
                                'Min'        : PMath.minimum,
                                'Peak'       : PMath.peak,
                              }
PMath.RESULT_TYPES          = list(PMath.METRICS) + ['FFT']
#?----------------------------------------------------------------------------------------------------------------------------------------
class Derived:
    """Parameters computed from other ones; update() is called on every sweep point after the swept values are set. [system specific]"""

    @staticmethod
    def update(mdlvar):
        """Recompute the parameters derived from other ones (same formulas as in vars.py), after a sweep changed the base values."""
        PFC, DC, Ctrl, Ld          = mdlvar['PFC'], mdlvar['DCLink'], mdlvar['CTRL'], mdlvar['Load']
        Choke, Sw                  = PFC['Choke'], PFC['SW']
        DC['Vinit']                = 0 if DC['Config'] == 1 else -2**0.5 * mdlvar['Grid']['Vin']   # line peak (CDC flipped); Ideal (1): 0, like Cout in parallel
        Ctrl['L_boost']            = Choke['L1'] + Choke['L2'] - 2 * Choke['Lm']
        Ctrl['C_out']              = PFC['Cout'] + DC['Cap_s'] * DC['Npara'] / DC['Nseri']
        Ctrl['fc_i']               = Ctrl['fsw'] / 10
        Ctrl['Kp_i']               = 2 * np.pi * Ctrl['fc_i'] * Ctrl['L_boost']
        Ctrl['Ki_i']               = (2 * np.pi * Ctrl['fc_i'])**2 / 10 * Ctrl['L_boost']
        Ctrl['Kp_v']               = 2 * np.pi * Ctrl['fc_v'] * Ctrl['C_out'] * Ctrl['Vref']
        Ctrl['Ki_v']               = (2 * np.pi * Ctrl['fc_v'])**2 / 2 * Ctrl['C_out'] * Ctrl['Vref']
        Ctrl['t_car']              = 1 / Ctrl['fsw'] - 1 / (2 * np.pi * mdlvar['Sensors']['Iin']['BW'])   # carrier delay: ADC samples one sensor delay after the valley
        Ctrl['Pout']               = Ld['Pout']                                              # rated power of the controller = load power
        Vload                      = Ctrl['Vset'] if mdlvar['LLC']['Stage'] != 3 else Ctrl['Vref']   # load at the LLC output (DC link when the LLC stage is Pass)
        Ld['Vout1'] = Ld['Vout2']  = Vload
        Ld['R']                    = Vload**2 / Ld['Pout']
        for s in (Sw, mdlvar['LLC']['HS1'], mdlvar['LLC']['SRHS1']):                       # switch ambient / initial junction temperature
            s['Tamb']              = s['T_init'] = mdlvar['Thermals']['T_amb']
        mdlvar['MCU']['ADC']['Ts'] = 1 / Ctrl['fsw']                                         # ADC samples once per PWM period
        Sim                        = mdlvar['Sim_param']
        if Sim['warm_start']:                                                                # start at the operating point, a few line cycles
            Sim['tSim']            = Sim['warm_tSim']
            Sim['load_tflip']      = Sim['tSim'] / 2
            mdlvar['ToFile']['tsave'] = Sim['tSim'] - 1 / mdlvar['Grid']['f']                # last line cycle saved
            if DC['Config'] != 1:
                DC['Vinit']        = -Ctrl['Vref']                                           # DC link at Vref (CDC flipped)
            Ctrl['P0']             = Ld['Pout']                                              # power loop integrator at the load power
            Ctrl['t_ss']           = 1e-6                                                    # no soft start
            Ctrl['t_en']           = Sim['warm_t_en']
            Ctrl['Vrms_min']       = 0.97 * mdlvar['Grid']['Vin']                            # line RMS valid from the start (RMS window still empty)
        Ld['t_switch']             = Sim['tSim'] - Sim['load_tflip']
        Ld['t_dead']               = Ld['t_switch'] / 2
        return mdlvar
#?----------------------------------------------------------------------------------------------------------------------------------------
