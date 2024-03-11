from abc import ABCMeta, abstractmethod
import numpy as np


class base_STL(metaclass=ABCMeta):
    """
    Abstract STL

    All our STL implementation classes should follow this structure.
    """

    @staticmethod
    def _update_array(x: np.ndarray, y: float):
        """
        Update the array by popping the oldest element and appending the new value.

        Parameters
        ----------
        x : np.ndarray
            Input array.
        y : Any
            New value to be appended.

        Returns
        -------
        np.ndarray
            Updated array.
        """
        # Check if the array is empty
        if x.size == 0:
            return x  # If empty, nothing to update

        # Pop the oldest element (leftmost) from the array
        x = x[1:]

        # Append the new value y to the array
        x = np.append(x, y)

        return x

    @abstractmethod
    def initialize_phase(self, input_data):
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
        raise NotImplementedError

