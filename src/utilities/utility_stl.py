import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.animation import HTMLWriter, FuncAnimation
from scipy.fft import fftfreq


def tricube_kernel(u: float):
    if 0 <= u < 1:
        return (1 - (u ** 3)) ** 3
    else:
        return 0



# for symmetric_w ([x_{t-lambda/2},... x_{t-1}, x_t, x{t+1},...,x_{t+lambda/2})
# lambda must be buffer_size/2
# To fast computation, we collect weight in to [total_lenght x total_lenght]
# Total length of ini phase is 4m.
def symmetric_weights(total_length: int, buffer_size: int):
    weights = np.zeros((total_length, total_length))
    input_lambda = round(buffer_size / 2)
    # for each point, we compute weight with 2m

    for i in range(total_length):
        # only symmetric weight idx
        if i in range(input_lambda, total_length - input_lambda):
            for j in range(total_length):
                u = abs((i - j) / input_lambda)
                weights[i][j] = tricube_kernel(u)
        else:
            weights[i][:] = np.nan

    return weights


# window for each point <- [x_{t-lambda/2},... x_{t-1}, x_t, x{t+1},...,x_{t+lambda/2}
# Single seasonality m = m_p, then A is 4m and buffer for symmetric trend must be 2m
def symmetric_trend_filter(input_data: np.ndarray, buffer_size: int):
    total_length = len(input_data)
    weights = symmetric_weights(total_length, buffer_size)
    smoothed_trend = np.zeros(total_length)
    for i in range(total_length):
        local_weights = weights[i]
        smoothed_trend[i] = trend_filter(weights=local_weights, data=input_data)

    return smoothed_trend


def non_symmetric_weights(input_lambda: int):
    weights = [tricube_kernel((input_lambda - k) / input_lambda) for k in range(1, input_lambda + 1)]
    return np.array(weights)


def trend_filter(weights: np.ndarray, data: np.ndarray):
    t_i = np.sum(data * weights) / np.linalg.norm(np.nan_to_num(weights), ord=1)
    return t_i


def seasonality_filter(x_t: float, s_pre: float, gamma: float):
    s_t = gamma * x_t + (1 - gamma) * s_pre
    return s_t


def Znormalization(data: np.ndarray):
    mean = np.mean(data)
    std_dev = np.std(data)
    data_normalized = data - mean
    data_normalized /= std_dev
    return data_normalized


def update_array(x: np.ndarray, y):
    # Check if the array is empty
    if x.size == 0:
        return x  # If empty, nothing to update

    # Pop the oldest element (leftmost) from the deque
    x = x[1:]

    # Append the new value y to the deque
    x = np.append(x, y)

    return x


def simple_detread(data: np.ndarray):
    index = np.arange(data.shape[0])
    trend_fit = linregress(index, data)
    if trend_fit.slope > 1e-4:
        trend = trend_fit.intercept + index * trend_fit.slope
        data = data - trend
    else:
        data = data - data.mean()

    return data


def calculate_smoothness(ts):
    # Calculate the first-order difference
    first_order_difference = np.diff(ts)

    # Calculate the standard deviation of the first-order difference
    smoothness_measure = np.std(first_order_difference)

    return smoothness_measure


# wait to cleaning parameter
def animate_streaming_STL(full_data, full_trend_component, results: list[dict], file_name: str):
    """
        Export animation all components results into HTML.

        Parameters
        ----------
        results: list[dict]
            results from Online STL
            buffer : original data in buffer at t
            fft : fft result # do not used
            periodogram : periodogram in buffer at t
            frame : idx of frame
            peak : idx peak of periodogram
            period : seasonality length from periodogram (mp)
            trend : trend component at t
            seasonal : seasonal component at t
            residual : residual component at t

        Returns
        -------
        None
            Exports the plot results into HTML. Ordering of subplots are as follow
            0 : Full data with highlight
            1:  original
            2 : trend component
            3 : seasonal component
            4 : residual component
            5 : periodogram

        """
    fig, axs = plt.subplots(2, 3, figsize=(11, 6))
    axs = axs.flatten()
    buffer_size = len(results[0]['buffer'])
    xf = fftfreq(buffer_size)[:int(buffer_size / 2)]

    def animate(frame_idx):
        raw_plot = results[frame_idx]['buffer']
        periodogram = results[frame_idx]['periodogram']
        trend_component = results[frame_idx]['trend']
        seasonal_component = results[frame_idx]['seasonal']
        residual_component = results[frame_idx]['residual']
        mp = results[frame_idx]['period']

        min_raw = results[frame_idx]['min_raw']
        max_raw = results[frame_idx]['max_raw']
        min_pden = results[frame_idx]['min_pden']
        max_pden = results[frame_idx]['max_pden']
        min_trend = results[frame_idx]['min_trend']
        max_trend = results[frame_idx]['max_trend']
        min_seasonal = results[frame_idx]['min_seasonal']
        max_seasonal = results[frame_idx]['max_seasonal']
        min_residual = results[frame_idx]['min_residual']
        max_residual = results[frame_idx]['max_residual']

        # plot full
        axs[0].clear()
        axs[0].set_title('Original data')
        axs[0].set_xlim((0, len(full_data)))
        axs[0].set_ylim((min(full_data), max(full_data)))
        axs[0].set_xlabel('instances')
        axs[0].plot(np.arange(len(full_data)), full_data, label='raw data')
        highlight_start = frame_idx
        highlight_end = frame_idx + buffer_size
        axs[0].axvline(x=highlight_start, color='red', linestyle='--')
        axs[0].axvline(x=highlight_end, color='red', linestyle='--')
        axs[0].plot(np.arange(len(full_trend_component)), full_trend_component, 'red', label = 'Final Trend')
        axs[0].legend()

        # plot raw
        axs[1].clear()
        axs[1].set_title('Buffer')
        axs[1].set_xlim((0, buffer_size))
        axs[1].set_ylim((min(full_data), max(full_data)))
        axs[1].set_xlabel('instances')
        axs[1].plot(np.arange(len(raw_plot)), raw_plot)
        axs[1].set_xticks(np.arange(0, len(raw_plot), 20))

        # plot periodogram
        axs[2].clear()
        axs[2].set_title(f'Periodogram: Seasonal length estimate = {mp}')
        axs[2].set_xlim((min(xf), max(xf)))
        axs[2].set_ylim((min_pden, max_pden))
        axs[2].set_xlabel('frequency')
        axs[2].plot(xf, periodogram)
        if mp > 0:
            peak = results[frame_idx]['peak']
            axs[2].plot([xf[peak]], [periodogram[peak]], 'ro')

        # plot trend
        axs[3].clear()
        axs[3].set_title('Trend component')
        axs[3].set_xlim((0, buffer_size))
        axs[3].set_ylim((min(full_data), max(full_data)))
        axs[3].set_xlabel('instances')
        axs[3].plot(np.arange(len(trend_component)), trend_component)
        axs[3].set_xticks(np.arange(0, len(trend_component), 20))

        # plot seasonal
        axs[4].clear()
        axs[4].set_title('Seasonal component')
        axs[4].set_xlim((0, buffer_size))
        axs[4].set_ylim(min_seasonal, max_seasonal)
        axs[4].set_xlabel('instance')
        axs[4].plot(np.arange(len(seasonal_component)), seasonal_component)
        axs[4].set_xticks(np.arange(0, len(seasonal_component), 20))

        # residual
        axs[5].clear()
        axs[5].set_title('residual component')
        axs[5].set_xlim((0, buffer_size))
        axs[5].set_ylim((min(full_data), max(full_data)))
        axs[5].set_xlabel('instance')
        axs[5].plot(np.arange(len(residual_component)), residual_component)
        axs[5].set_xticks(np.arange(0, len(residual_component), 20))

        plt.tight_layout()

    anim = FuncAnimation(fig, animate,
                         frames=len(results), interval=len(results))

    html_writer = HTMLWriter(fps=25)
    anim.save(f'{file_name}.html', writer=html_writer)


def plot_all_components(Y_i: np.ndarray, T_i: np.ndarray, S_i: np.ndarray, R_i: np.ndarray):
    """
    Plot all components result with raw data.

    Parameters
    ----------
    Y_i : ndarray
        Original time series data.
    T_i : ndarray
        Trend component.
    S_i : ndarray
        Seasonal component.
    R_i : ndarray
        Residual component.

    Returns
    -------
    None
        Displays the plot result.
    """
    plot_labels = ['Raw data', 'Trend component', 'Seasonal component', 'Residual component']
    plot_data = [Y_i, T_i, S_i, R_i]

    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    for i, ax in enumerate(axes.ravel()):
        if i == 0:
            ax.plot(plot_data[0], label="raw")
            ax.plot(plot_data[1], 'r', alpha=0.7, label="trend")
            ax.legend()
            y_lim = ax.get_ylim()
        else:
            ax.plot(plot_data[i])
            ax.set_ylim(y_lim)
        ax.set_title(plot_labels[i])
    fig.suptitle('All components')
    plt.tight_layout()
    plt.show()
    plt.clf()

def result_aggregation(dataset_name, algo_name, window_size, input_results):
    """
    Aggregate results for plotting.

    Parameters
    ----------
    dataset_name: str
    algo_name: str
    window_size: input sliding window size
    input_results: results for each sliding window

    """
    error_bounds = [0, 2, 5, 10, 15, 20]
    output_results = []
    for error_bound in error_bounds:
        count_result = 0
        for row in input_results:
            if error_bound == 0:
                lb = row['answer']
                ub = row['answer']
            else:
                lb = row['answer'] * ((100-error_bound) / 100)
                ub = row['answer'] * ((100+error_bound) / 100)
            pred_result = row['result']
            if (lb <= pred_result) & (pred_result<= ub):
                count_result = count_result+1
        accuracy_ratio = count_result / len(input_results)
        output_results.append({
            'dataset_name': dataset_name,
            'algorithms': algo_name,
            'error_bound': error_bound,
            'window_size': window_size,
            'accuracy_ratio': accuracy_ratio
        })
    return output_results
