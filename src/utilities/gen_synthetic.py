import json
import numpy as np
import math
import matplotlib.pyplot as plt


def sinewave(length: int, period: int, amplitude: int):
    one_period = np.arange(0, period, 1)
    frequency = 1 / period
    theta = 0
    one_period = amplitude * np.sin(2 * np.pi * frequency * one_period + theta)
    number_cycle = math.ceil(length / period)
    seasonal = []
    for i in range(number_cycle):
        seasonal = np.concatenate([seasonal, one_period])

    return seasonal[:length]


def generate_syn1(filename: str = "syn1.json", is_export=False):
    """
    All datasets are export into JSON files
    Data dic :
    1. main_length denotes season length of seasonal component
    2. transition_points denotes answer of starting point of seasonality transitions
    3  main_length_ts denotes answer of season length of each timestamp
    4. ts denotes time series data (y)
    5. trend denotes trend component (T)
    6. seasonal denotes seasonal component (S)
    7. residual denotes residual component (R)
    """

    np.random.seed(0)
    trend_increase = np.linspace(0, 2, num=2200)
    trend_stability = np.ones(600) + 1
    trend_decrease = np.linspace(2, 0, num=2200)
    trend_component = np.concatenate((trend_increase, trend_stability, trend_decrease))
    M_1 = 50
    M_2 = 80
    first_pattern = sinewave(1800, M_1, 1)
    second_pattern = sinewave(1800, M_2, 1)
    third_pattern = sinewave(1400, M_1, 1)
    seasonal_component = np.concatenate((first_pattern,
                                  second_pattern,
                                  third_pattern))

    main_length_ts = np.concatenate((np.repeat(M_1, 1800),
                                    np.repeat(M_2, 1800),
                                    np.repeat(M_1, 1400)))

    residual_component = 0.03 * np.random.randn(len(trend_component))
    ts = trend_component + seasonal_component + residual_component

    data = {'main_length': [M_1, M_2],
            'transition_points': [1800, 3200],
            'main_length_ts': main_length_ts.tolist(),
            'ts': ts.tolist(),
            'trend': trend_component.tolist(),
            'seasonal': seasonal_component.tolist(),
            'residual': residual_component.tolist()}

    if is_export:
        with open(filename, "w") as outfile:
            json.dump(data, outfile)

    return data


def generate_syn2(filename: str = "syn2.json", is_export=False):
    """
    All datasets are export into JSON files
    Data dic :
    1. main_length denotes season length of seasonal component
    2. transition_points denotes answer of starting point of seasonality transitions
    3  main_length_ts denotes answer of season length of each timestamp
    4. ts denotes time series data (y)
    5. trend denotes trend component (T)
    6. seasonal denotes seasonal component (S)
    7. residual denotes residual component (R)
    """

    np.random.seed(0)

    total_cycle = 60
    temporal_cycle = 10
    M_normal = 80
    M_fluctuations = np.random.choice(np.arange(40, 170), size=temporal_cycle, replace=False)
    normal_cycle = sinewave(M_normal, M_normal, 1)
    fluctuation_index = np.random.choice(np.arange(10, total_cycle - 10),
                                      size=temporal_cycle, replace=False)
    seasonal_component = []
    timestamp_changing = []
    answer_mp = []
    count = 0
    for idx in range(total_cycle):
        if idx in fluctuation_index:
            timestamp_changing.append(len(seasonal_component))
            answer_mp = answer_mp + ([int(M_fluctuations[count])] * M_fluctuations[count])
            anomaly_cycle = sinewave(M_fluctuations[count], M_fluctuations[count], 1)
            count = count + 1
            seasonal_component = np.concatenate([seasonal_component, anomaly_cycle])
        else:
            answer_mp = answer_mp + ([int(M_normal)] * M_normal)
            seasonal_component = np.concatenate([seasonal_component, normal_cycle])

    trend_component = np.zeros(M_normal * 7)  # avoid 5m for oneshot
    remaining_len = round((len(seasonal_component) - (M_normal * 7)) / 4)
    final_len = len(seasonal_component) - (M_normal * 7) - (3 * remaining_len)
    trend_component = np.concatenate([trend_component, np.ones(remaining_len)])
    trend_component = np.concatenate([trend_component, 1.5 * np.ones(remaining_len)])
    trend_component = np.concatenate([trend_component, 1 * np.ones(remaining_len)])
    trend_component = np.concatenate([trend_component, np.zeros(final_len)])

    residual_component = 0.03 * np.random.randn(len(trend_component))
    ts = trend_component + seasonal_component + residual_component

    data = {'main_length': [M_normal],
            'transition_points': [],
            'main_length_ts': answer_mp,
            'ts': ts.tolist(),
            'trend': trend_component.tolist(),
            'seasonal': seasonal_component.tolist(),
            'residual': residual_component.tolist()}

    if is_export:
        with open(filename, "w") as outfile:
            json.dump(data, outfile)

    return data

def generate_syn3(noise_level = 0.7, filename: str = "syn3.json", is_export=False):
    """
    All datasets are export into JSON files
    Data dic :
    1. main_length denotes season length of seasonal component
    2. transition_points denotes answer of starting point of seasonality transitions
    3  main_length_ts denotes answer of season length of each timestamp
    4. ts denotes time series data (y)
    5. trend denotes trend component (T)
    6. seasonal denotes seasonal component (S)
    7. residual denotes residual component (R)
    """

    np.random.seed(0)

    timestamps = np.arange(0, 5000)
    phase_1_end = 1800
    phase_2_end = 3000
    linear_trend_1 = np.linspace(0, 3, num=phase_1_end)
    time_phase_2 = timestamps[phase_1_end:phase_2_end] - phase_1_end
    polynomial_trend = - 0.001 * (time_phase_2 ** 2) + 0.1 * time_phase_2
    trend_min, trend_max = polynomial_trend.min(), polynomial_trend.max()
    polynomial_trend = 5 * (polynomial_trend - trend_min) / (trend_max - trend_min)

    time_phase_3 = timestamps[phase_2_end:] - phase_2_end
    exponential_trend = np.exp(0.005 * time_phase_3) - 1
    trend_min, trend_max = exponential_trend.min(), exponential_trend.max()
    exponential_trend = 5 * (exponential_trend - trend_min) / (trend_max - trend_min)

    trend_component = np.concatenate((linear_trend_1, exponential_trend, polynomial_trend))


    M_1 = 53
    M_2 = 120
    first_pattern = sinewave(1800, M_1, 1)
    second_pattern = sinewave(len(timestamps) - 1800, M_2, 1.5)
    seasonal_component = np.concatenate((first_pattern, second_pattern))

    residual_component = noise_level * np.random.randn(len(trend_component))

    num_outliers = 100
    outliers_indices = np.random.choice(len(timestamps), num_outliers, replace=False)
    outliers_values = np.random.choice([1, -1], num_outliers) * (np.random.uniform(4, 7, num_outliers))

    residual_component[outliers_indices] = outliers_values

    ts = trend_component + seasonal_component + residual_component

    main_length_ts = np.concatenate((np.repeat(M_1, 1800),
                                     np.repeat(M_2, len(timestamps) - 1800)))

    data = {'main_length': [M_1, M_2],
            'transition_points': [1800],
            'main_length_ts': main_length_ts.tolist(),
            'ts': ts.tolist(),
            'trend': trend_component.tolist(),
            'seasonal': seasonal_component.tolist(),
            'residual': residual_component.tolist()}

    if is_export:
        with open(filename, "w") as outfile:
            json.dump(data, outfile)

    return data