import numpy as np
import math
from scipy.fft import fftfreq
from typing import Tuple


def peridogram(sliding_window_size: int, fft_ts: np.ndarray[np.complex128], window_type='rec') \
        -> Tuple[np.ndarray, np.ndarray]:
    """
    Peridoogram

    Parameters
    ----------
    fft_ts : np.ndarray[np.complex128]
        Input FFT signal.
    window_type : str, optional
        Type of window to apply.
        1. reg : rectangular window
        2. hann : Hanning window
    Returns
    -------
    Tuple :[np.ndarray, np.ndarray]
        Tuple containing the result of Periodogram:
        - xfreq : Array of sample frequencies (np.ndarray).
        - Peridogram :  Peridogram of fft_ts (np.ndarray).

    Note than results are at most half of the maximum signal frequency, due to the Nyquist fundamental theorem.
    """

    if window_type == 'rec':
        periodogram_den = (fft_ts *
                           np.conjugate(fft_ts)) / sliding_window_size
    elif window_type == 'hann':
        periodogram_den = (windowing(fft_ts) *
                           np.conjugate(windowing(fft_ts))) / sliding_window_size

    xfreq = fftfreq(sliding_window_size)[:int(sliding_window_size / 2)]

    return xfreq, periodogram_den[:int(sliding_window_size / 2)].real


# def Hanning_window()
def windowing(fft_x: np.ndarray[np.complex128], window_type='hann'):
    """
   Apply windowing to the input FFT signal.

   Parameters
   ----------
   fft_x : np.ndarray[np.complex128]
       Input FFT signal.
   window_type : str, optional
       Type of window to apply. Currently only supports 'hann'.
       1. Hanning window from Eq. (9) in E. Jacobsen and R. Lyons, "The sliding DFT," in IEEE Signal Processing Magazine
       , vol. 20, no. 2, pp. 74-80, March 2003, doi: 10.1109/MSP.2003.1184347.

   Returns
   -------
   np.ndarray[np.complex128]
       Windowed FFT signal.
   """
    if window_type == 'hann':
        y = np.hstack((
            np.conj(fft_x[+1][None]),
            fft_x,
            np.conj(fft_x[-2][None])))
        fft_mid = y[1:-1]
        fft_left = y[:-2]
        fft_right = y[2:]
        return 0.5 * fft_mid - 0.25 * (fft_left + fft_right)
    else:
        raise ValueError("Unsupported window type.")


def get_period_hints(periodogram_density: np.ndarray[np.complex128], percentile_threshold: float = 99.):
    """
    Identify significant periods from a periodogram density.

    Parameters
    ----------
    periodogram_density : np.ndarray[np.complex128]
        Periodogram density, typically obtained from Fourier analysis.
    percentile_threshold : float, optional
        Percentile threshold for identifying significant peaks (default is 99%).

    Returns
    -------
    tuple
        Indices of periods above the threshold and the index of the peak.
    """
    # Extract the real part of the periodogram density
    power = periodogram_density.real

    # Calculate the threshold value based on the specified percentile
    threshold_value = np.percentile(power, percentile_threshold)

    # Find indices where the power is above the threshold, excluding the DC component
    indices_above_threshold = np.where(power > threshold_value)[0]
    mask = indices_above_threshold != 0
    indices_above_threshold = indices_above_threshold[mask]

    # Find the index of the peak (maximum power)
    index_peak = np.argmax(power)

    return indices_above_threshold, index_peak


def update_sDFT(fft_X: np.ndarray[np.complex128], old_x: float, new_x: float) -> np.ndarray[np.complex128]:
    """
    Update a signal's Discrete Fourier Transform (sDFT) using sliding DFT.

    Parameters
    ----------
    fft_X : np.ndarray[np.complex128]
        Previous sDFT.
    old_x : float
        Value to be replaced in the original sDFT.
    new_x : float
        New value to replace the old value.

    Returns
    -------
    np.ndarray[np.complex128]
        New sDFT.

    References
    ----------
    [1] E. Jacobsen and R. Lyons, "The sliding DFT," in IEEE Signal Processing Magazine,
       vol. 20, no. 2, pp. 74-80, March 2003, doi: 10.1109/MSP.2003.1184347.
    [2] E. Jacobsen and R. Lyons, "An update to the sliding DFT," in IEEE Signal Processing Magazine,
       vol. 21, no. 1, pp. 110-111, Jan. 2004, doi: 10.1109/MSP.2004.1516381.
    """
    N = len(fft_X)
    k = np.arange(N)
    twiddle = np.exp(2j * np.pi * k / N)
    new_fft_X = (fft_X - old_x + new_x) * twiddle

    return new_fft_X


def quin2_estimator(fft_X: np.ndarray[np.complex128], k: int, frequency_range: float):
    """
    Identify peak frequencies using Quinn's second estimator [1].

    Notably, E. Jacobsen and P. Kootsookos mentioned the Quinn's second estimator that works well for analysis
    when applying a rectangular window with DFT [2].


    Parameters
    ----------
    fft_X : np.ndarray[np.complex128]
        Discrete Fourier Transform (DFT) values.
    k : int
        index of peaks of DFT.
    frequency_range : float
        Frequency range.

    Returns
    -------
    Tuple[float, float]
        Tuple containing the estimated index (k_peak) and frequency_tone:
        - k_peak: Estimated index of the identified peak (float).
        - frequency_tone: Frequency value corresponding to the identified peak.

    References
    ----------
    [1]  B. G. Quinn, "Estimation of frequency, amplitude, and phase from the DFT of a time series,"
        in IEEE Transactions on Signal Processing, vol. 45, no. 3, pp. 814-817, March 1997, doi: 10.1109/78.558515.
    [2]  E. Jacobsen and P. Kootsookos, "Fast, Accurate Frequency Estimators [DSP Tips & Tricks],"
        in IEEE Signal Processing Magazine, vol. 24, no. 3, pp. 123-125, May 2007, doi: 10.1109/MSP.2007.361611.
    [3]  E. Jacobsen, Eric Jacobsen's Second Frequency Estimation Page. Retrieved December 21, 2023
        from http://www.ericjacobsen.org/fe2/fe2.htm (Original Source code in Matlab)

    """

    if k > 1:  # Avoid division by zero in the calculation
        betam = fft_X[k - 1].real / fft_X[k].real
        betap = fft_X[k + 1].real / fft_X[k].real
        dm = -betam / (betam - 1)
        dp = betap / (betap - 1)

        kappap = (1 / 4) * math.log(3 * (dp ** 4) + 6 * (dp ** 2) + 1) - (math.sqrt(6) / 24) * math.log(
            ((dp ** 2) + 1 - math.sqrt(2 / 3)) / ((dp ** 2) + 1 + math.sqrt(2 / 3)))

        kappam = (1 / 4) * math.log(3 * (dm ** 4) + 6 * (dm ** 2) + 1) - (math.sqrt(6) / 24) * math.log(
            ((dm ** 2) + 1 - math.sqrt(2 / 3)) / ((dm ** 2) + 1 + math.sqrt(2 / 3)))

        delta = (dm + dp) / 2 + kappap - kappam
        k_peak = k + delta
        frequency_tone = k_peak * frequency_range
    else:
        k_peak = k
        frequency_tone = 0.

    return k_peak, frequency_tone


def grandke_estimator(fft_X: np.ndarray[np.complex128], k: int, frequency_range: float):
    """
    Identify peak frequencies using Grandke estimator [1].

    Notably, E. Jacobsen and P. Kootsookos mentioned the Grandke estimator that works well for analysis
    when applying a Hanning window with DFT [2].

    Parameters
    ----------
    fft_X : np.ndarray[np.complex128]
        Discrete Fourier Transform (DFT) values.
    k : int
        Index of the DFT peak associated with the maximum magnitude.
    frequency_range : float
        Frequency range.

    Returns
    -------
    Tuple[float, float]
        Tuple containing the estimated index (k_peak) and frequency_tone:
        - k_peak: Estimated index of the identified peak (float).
        - frequency_tone: Frequency value corresponding to the identified peak.

    References
    ----------
    [1]  T. Grandke, "Interpolation Algorithms for Discrete Fourier Transforms of Weighted Signals,"
        in IEEE Transactions on Instrumentation and Measurement, vol. 32, no. 2, pp. 350-355, June 1983,
        doi: 10.1109/TIM.1983.4315077.
    [2]  E. Jacobsen and P. Kootsookos, "Fast, Accurate Frequency Estimators [DSP Tips & Tricks],"
        in IEEE Signal Processing Magazine, vol. 24, no. 3, pp. 123-125, May 2007, doi: 10.1109/MSP.2007.361611.
    """

    if k > 1:  # Avoid division by zero in the calculation
        if abs(fft_X[k - 1]) > fft_X[k + 1]:
            alpha = abs(fft_X[k]) / abs(fft_X[k - 1])
            delta = (alpha - 2) / (alpha + 1)
        else:
            alpha = abs(fft_X[k + 1]) / abs(fft_X[k])
            delta = (2 * alpha - 1) / (alpha + 1)

        k_peak = k + delta
        frequency_tone = k_peak * frequency_range
    else:
        k_peak = k
        frequency_tone = 0.

    return k_peak, frequency_tone


def qse(w: np.ndarray[float], k: int, frequency_range: float):
    """
    Identify peak frequencies using Q-Shift frequency Estimator (QSE) [1].
    This method is an iterative method to Identify peak frequencies.

    Note that the original source code was implemented in Matlab.

    Parameters
    ----------
    w : np.ndarray
        1D array representing the data in the sliding window.
    k : int
        Index of the DFT peak associated with the maximum magnitude.
    frequency_range : float
        Frequency range.

    Returns
    -------
    Tuple[float, float]
        Tuple containing the estimated index (k_peak) and frequency_tone:
        - k_peak: Estimated index of the identified peak (float).
        - frequency_tone: Frequency value corresponding to the identified peak.

    References
    ----------
    [1] A. Serbes, "Fast and Efficient Sinusoidal Frequency Estimation by Using the DFT Coefficients,"
        in IEEE Transactions on Communications, vol. 67, no. 3, pp. 2333-2342, March 2019,
        doi: 10.1109/TCOMM.2018.2886355.
    """

    # Find the required number of iterations
    N = len(w)
    Qtemp = np.ceil(np.log(np.log2(N / (np.log(N)))) / np.log(3))
    Q = max(3, Qtemp)

    # Calculate the optimum shift q_opt
    q = (1 / N) ** (1 / 3)

    # Calculate c(q)
    cq = (1 - np.pi * q * 1 / np.tan(np.pi * q)) / (q * np.cos(np.pi * q) ** 2)

    # Set the initial residual frequency to zero.
    delta = 0

    # Set the time index
    n = np.arange(N)

    # Start the QSE algorithm
    for it in range(int(Q)):
        # This computes S_{q}
        Sp = np.sum(w * np.exp(-1j * 2 * np.pi / N * (k + delta + q) * n))
        # And this is S_{-q}
        Sn = np.sum(w * np.exp(-1j * 2 * np.pi / N * (k + delta - q) * n))

        # Update the new residual frequency estimate
        delta = delta + np.real((Sp - Sn) / (Sp + Sn)) / cq

    # Finally, produce the frequency estimate
    k_peak = k + delta
    frequency_tone = k_peak * frequency_range
    return k_peak, frequency_tone


def haqse(periodogram_den: np.ndarray[np.complex128], w: np.ndarray[float]):
    """
    Identify peak frequencies using Hybrid A&M and Q-shift estimator (HAQSE) [1].
    This method is an iterative method to Identify peak frequencies.

    Note that the original source code was implemented in Matlab.

    Parameters
    ----------
    periodogram_den : np.ndarray[np.complex128]
        periodogram result of the sliding window
    w : np.ndarray
        1D array representing the data in the sliding window. (detrend series= x)

    Returns
    -------
    Tuple[float, float]
        Tuple containing the estimated index (k_peak) and frequency_tone:
        - k_peak: Estimated index of the identified peak (float).
        - frequency_peak: Frequency value corresponding to the identified peak.

    References
    ----------
    [1] A. Serbes, "Fast and Efficient Sinusoidal Frequency Estimation by Using the DFT Coefficients,"
        in IEEE Transactions on Communications, vol. 67, no. 3, pp. 2333-2342, March 2019,
        doi: 10.1109/TCOMM.2018.2886355.
    """
    # Step 1: peak identification
    location, k_hat = get_period_hints(periodogram_den)

    # Find the required number of iterations
    N = len(w)
    # Set the time index
    n = np.arange(N)

    # Step 2: initial delta_alpha calculation
    # # Start the HAQSE algorithm by applying A&M interpolator first
    # # This computes S_{0.5}
    Sp5 = np.sum(w * np.exp(-1j * 2 * np.pi / N * (k_hat + 0.5) * n))
    # # And this is S_{-0.5}
    Sn5 = np.sum(w * np.exp(-1j * 2 * np.pi / N * (k_hat - 0.5) * n))

    # # Find the fine residual frequency estimate
    delta_a = (1/2) * np.real((Sp5 + Sn5) / (Sp5 - Sn5))

    # Step 3: final delta estimation
    # # Calculate the optimum shift q_opt
    q = (1 / N) ** (1 / 3)
    # # Calculate c(q)
    cq = (1 - np.pi * q * np.tan(np.pi * q)) / (q * np.cos(np.pi * q) ** 2)

    # # Second iteration of HAQSE
    # # The HAQSE algorithm is finalized by applying the QSE interpolator
    # # This computes S_{k_hat + delta_a + q}
    Spq = np.sum(w * np.exp(-1j * 2 * np.pi / N * (k_hat + q + delta_a) * n))
    # And this is S_{k_hat + delta_a - q}
    Snq = np.sum(w * np.exp(-1j * 2 * np.pi / N * (k_hat - q + delta_a) * n))

    # Find the finer residual frequency estimate
    delta_h = np.real((Spq - Snq) / (Spq + Snq)) / cq + delta_a

    # Finally, produce the frequency estimate
    k_peak = k_hat + delta_h
    frequency_peak = k_peak / N
    return k_peak, frequency_peak
