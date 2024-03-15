import numpy as np
from statsmodels.tsa.seasonal import STL
from src.online_decomposition.base_STL import base_STL


class slidingSTL(base_STL):
    """
    Online with classical STL [1]
    REF:
        [1] Cleveland, R. B., Cleveland, W. S., McRae, J. E., & Terpenning, I. J. (1990).
            STL: A seasonal-trend decomposition procedure based on loess.
            Journal of Official Statistics, 6(1), 3–33.
        [2] Mishra, A., Sriharsha R., & Zhong S. (2022).
            OnlineSTL: scaling time series decomposition by 100x.
            Proc. VLDB Endow. 15, 7 (March 2022), 1417–1425.
    """

    def __init__(self, max_season_length: int, max_cycles: int = 4):
        """
        Initialize phase (offline phase)

        Parameters
        ----------
        max_season_length : int
            Maximum seasonality length (m)
        """
        self.max_season_length = max_season_length
        self.buffer = np.zeros(max_cycles * max_season_length, float)
        self.buffer_size = max_cycles * max_season_length

    def initialize_phase(self, input_data: np.ndarray):
        """
        Initialize phase (offline phase)

        Parameters
        ----------
        input_data : ndarray or list
            Original time series (Y, where the length of Y must be 5 * m).
            Note that we set this parameter as the same OnlineSTL [2].

        Returns
        -------
        trend : ndarray
            Trend component (T).
        seasonal : ndarray
            Seasonal component (S)
        residual : ndarray
            Residual component (R)
        """
        input_data = np.atleast_1d(input_data)

        assert input_data.ndim == 1, (
            f"Expected 1D array (samples,), got {input_data.shape}!"
        )

        # print(input_data.size)
        assert input_data.size >= self.buffer_size, (
            f"Input length is less than {self.buffer_size}, which is not allowed."
        )

        self.buffer = np.array(input_data[:self.buffer_size])
        stl = STL(self.buffer, period=self.max_season_length, robust=True).fit()
        trend, seasonal, residual = stl.trend, stl.seasonal, stl.resid

        # input remains (len(Y_i > 4 * m))
        if input_data.size > self.buffer_size:
            for y_i in input_data[self.buffer_size:]:
                trend_i, seasonal_i, residual_i = self.online_update(y_i)
                trend = np.append(trend, trend_i)
                seasonal = np.append(seasonal, seasonal_i)
                residual = np.append(residual, residual_i)

        return trend, seasonal, residual

    def online_update(self, y_i: float):
        """
        Online phase

        Parameters
        ----------
        y_i : float
            Latest original time series.

        Returns
        -------
        trend_i : float
            Trend component (T_i).
        seasonal_i : float
            Seasonal component (S_i).
        residual_i : float
            Residual component (R_i).
        """
        self.buffer = self._update_array(self.buffer, y_i)
        stl = STL(self.buffer, period=self.max_season_length, robust=True).fit()

        return stl.trend[-1], stl.seasonal[-1], stl.resid[-1]
