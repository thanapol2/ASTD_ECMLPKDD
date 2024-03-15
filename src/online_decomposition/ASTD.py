import numpy as np
import src.utilities.utility_stl as utility_stl
from scipy.fft import fft, fftfreq
import src.utilities.utility_frequency_analysis as utility_frequency

class ASTD():

    def __init__(self, window_size, seasonality_smoothing: float = 0.7):

        if not 0 <= seasonality_smoothing < 1:
            raise ValueError("seasonality smoothing should be in the range [0, 1)")

        # set parameter
        self.gamma = seasonality_smoothing
        self.N = window_size                                    # N is W size
        self.kernel_c = utility_stl.non_symmetric_weights(self.N)   # non symmetric weights
        # self.kernel_half_c = utility_stl.non_symmetric_weights(round(self.N/2))
        # array to store data with N length
        self.W = np.zeros(self.N)               # original data at last N size
        self.t1_diff_W = np.zeros(self.N)       # detrend data at last W size for adjust zero lagging
        self.ds_diff_W = np.zeros(self.N)       # detrend (Final) at last W size for adjust zero lagging
        self.T1 = np.zeros(self.N)              # Initiation trend data at last W size
        self.X = np.zeros(self.N)               # Detrend data at last W size (X)
        self.DS = np.zeros(self.N)              # Deseasonal data at last W size
        self.start_fft = fft(self.W)            # start fft with zero signal
        self.xfreq, self.periodogram_den = utility_frequency.peridogram(self.N, self.start_fft, 'rec')
        self.T = np.zeros(self.N)               # final trend component at last W size
        self.S = np.zeros(self.N)               # final seasonal component at last W size
        self.R = np.zeros(self.N)               # final residual component at last W size

    def _update_peridogogram_den(self):
        self.xfreq, self.periodogram_den = utility_frequency.peridogram(self.N, self.start_fft, 'rec')

    def initialization_phase(self, xi: np.ndarray):
        # de initiation trend phase
        for idx, xi in enumerate(xi):
            self.W = utility_stl.update_array(self.W, xi)

            # de initiation trend
            t1 = utility_stl.trend_filter(weights=self.kernel_c, data=self.W)
            t_diff = xi - t1
            self.t1_diff_W = utility_stl.update_array(self.t1_diff_W, t_diff)
            t1_lagg = utility_stl.trend_filter(weights=self.kernel_c, data=self.t1_diff_W)

            # Initiation trend
            self.T1 = utility_stl.update_array(self.T1, t1 + t1_lagg)

            # Diff X-T1
            newest_dt = self.W[-1] - self.T1[-1]
            self.X = utility_stl.update_array(self.X, newest_dt)

        # SLE X phase and find M
        self.start_fft = fft(self.X)
        self._update_peridogogram_den()

        # HAQSE Phase
        k_peak, frequency_peak = utility_frequency.haqse(self.periodogram_den, self.X)
        # HAQSE Phase

        # seasonality found
        # if (k_hat > 1) & (k_peak > 1):
        if round(k_peak) > 1:
            self.seasonal_length = round(1 / frequency_peak)
            for idx, xi in enumerate(self.W):
                if idx < self.seasonal_length:
                    self.S[idx] = self.X[idx]
                else:
                    self.S[idx] = utility_stl.seasonality_filter(d=self.X[idx],
                                                                 Epsilon_r=self.S[idx - self.seasonal_length],
                                                                 gamma=self.gamma)
        # seasonality did not found
        else:
            self.seasonal_length = 0
            self.S = np.zeros(self.N)


        # Desasonalized from W
        self.DS = self.W - self.S

        # Final trend
        t5_buffer = np.zeros(self.N)
        for idx, dsi in enumerate(self.DS):
            t5_buffer = utility_stl.update_array(t5_buffer, dsi)
            t5 = utility_stl.trend_filter(weights=self.kernel_c, data=t5_buffer)
            ds_diff = dsi - t5

            self.ds_diff_W = utility_stl.update_array(self.ds_diff_W, ds_diff)
            t5_lagg = utility_stl.trend_filter(weights=self.kernel_c, data=self.ds_diff_W)

            self.T = utility_stl.update_array(self.T, t5 + t5_lagg)
        #
        #
        self.R = self.W - self.T - self.S

        return self.T, self.S, self.R

    def update_phase(self, xi: float):
        self.W = utility_stl.update_array(self.W, xi)

        # de initiation trend
        t1 = utility_stl.trend_filter(weights=self.kernel_c, data=self.W)
        t_diff = xi - t1
        self.t1_diff_W = utility_stl.update_array(self.t1_diff_W, t_diff)
        t1_lagg = utility_stl.trend_filter(weights=self.kernel_c, data=self.t1_diff_W)

        # Initiation trend
        self.T1 = utility_stl.update_array(self.T1, t1+t1_lagg)

        # Diff X-T1
        x_oldest = self.X[0]
        x_newest = self.W[-1] - self.T1[-1]
        self.X = utility_stl.update_array(self.X, x_newest)

        # SLE X
        self.start_fft = utility_frequency.update_sDFT(self.start_fft, x_oldest, x_newest)
        self._update_peridogogram_den()

        # find M
        k_peak, frequency_peak = utility_frequency.haqse(self.periodogram_den, self.X)
        # avoid main_length 0 and W length
        # if (k_hat > 1) & (k_peak > 1):
        if round(k_peak) > 1:
            self.seasonal_length = round(1 / frequency_peak)
            if (2 + self.seasonal_length  >= len(self.S)):
                print('a')
            Si = utility_stl.seasonality_filter(d= self.X[-1], Epsilon_r=self.S[ - self.seasonal_length],
                                                gamma=self.gamma)
        else:
            # no seasonal component
            Si = 0
            self.seasonal_length = 0

        # update final Si into Seasonal component
        self.S = utility_stl.update_array(self.S, Si)

        # Desasonalized from W
        ds = xi - Si
        self.DS = utility_stl.update_array(self.DS, ds)


        # TF for final trend
        t5 = utility_stl.trend_filter(weights=self.kernel_c, data=self.DS)
        ds_diff = ds - t5
        # remove lagging
        self.ds_diff_W = utility_stl.update_array(self.ds_diff_W, ds_diff)
        t5_lagg = utility_stl.trend_filter(weights=self.kernel_c, data=self.ds_diff_W)
        Ti = t5 + t5_lagg   # final trend
        self.T = utility_stl.update_array(self.T, Ti)

        # final residual
        Ri = xi - Ti - Si

        self.R = utility_stl.update_array(self.R, Ri)

        return Ti, Si, Ri

