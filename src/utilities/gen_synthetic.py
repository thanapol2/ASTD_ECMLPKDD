import json
import numpy as np
import math
import matplotlib.pyplot as plt


def four_sine(no_large=False):
    np.random.seed(0)
    M_1 = 80
    M_2 = 25
    M_3 = 123
    first_cycles = sinewave(455, M_1, 1)
    secord_cycles = sinewave(315, M_2, 1)
    data = np.append(first_cycles, secord_cycles)
    if no_large:
        fourth_cycles = sinewave(400, M_1, 1)
        data = np.append(data, fourth_cycles)
    else:
        third_cycles = sinewave(690, M_3, 1)
        fourth_cycles = sinewave(300, M_1, 1)
        data = np.append(data, third_cycles)
        data = np.append(data, fourth_cycles)

    R_t = 0.05 * np.random.randn(len(data))
    data = data + R_t
    return data, 'four_sine_largewindow'


def square_wave(length, period, amplitude):
    one_period = np.arange(0, period, 1)
    one_period = amplitude * np.sign(np.sin(2 * np.pi * (1 / period) * one_period))
    number_cycle = math.ceil(length / period)
    seasonal = []
    for i in range(number_cycle):
        seasonal = np.concatenate([seasonal, one_period])

    return seasonal[:length]


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


def cubic_curve(time, a, b, c, d):
    return a * time ** 3 + b * time ** 2 + c * time + d


# All datasets are export into JSON files
# Data dic :
# 1. main_length denotes length of main seasonal component
# 2. sub_length denotes length of sub seasonal component (in case multiple seasons)
# 3. changing_point denotes answer of seasonal changing point
# 4. main_length_ts denotes the answer seasonality length (main seasonal component) for each timestamp
# 5. sub_length_ts denotes the answer seasonality length (main seasonal component) for each timestamp
# 4. ts denotes time series data (Y_t)
# 5. trend denotes trend component (Tau_t)
# 6. seasonal denotes seasonal component (S_t)
# 7. residual denotes residual component (R_t)
def generate_syn1(filename: str = "syn1.json", is_export=False):
    np.random.seed(0)
    N = 4000
    change_point = 2000
    M_1 = 60
    M_2 = 143

    Tau_t = np.linspace(0, 5, num=N)
    first_pattern = sinewave(change_point, M_1, 1)
    second_pattern = sinewave(change_point, M_2, 1)
    main_length_ts = np.concatenate((np.repeat(M_1, change_point), np.repeat(M_2, change_point)))
    S_t = np.concatenate((first_pattern, second_pattern))
    R_t = 0.03 * np.random.randn(len(Tau_t))
    Y_t = Tau_t + S_t + R_t

    data = {'main_length': [M_1, M_2],
            'sub_length': [],
            'change_point': [2000],
            'main_length_ts': main_length_ts.tolist(),
            'sub_length_ts': [],
            'ts': Y_t.tolist(),
            'trend': Tau_t.tolist(),
            'seasonal': S_t.tolist(),
            'residual': R_t.tolist()}

    if is_export:
        with open(filename, "w") as outfile:
            json.dump(data, outfile)

    return data


def generate_syn2(filename: str = "syn2.json", is_export=False):
    # dataset oneShotSTL
    np.random.seed(0)
    M_P = 100
    Tau_t = np.zeros(1200)  # avoid 5m for oneshot
    Tau_t = np.concatenate([Tau_t, np.ones(660)])
    Tau_t = np.concatenate([Tau_t, 2 * np.ones(1380)])
    Tau_t = np.concatenate([Tau_t, 3 * np.ones(930)])
    Tau_t = np.concatenate([Tau_t, 2 * np.ones(1030)])

    main_length_ts = np.repeat(M_P, len(Tau_t))
    S_t = square_wave(len(Tau_t), 100, 1)
    R_t = 0.03 * np.random.randn(len(Tau_t))
    Y_t = S_t + Tau_t + R_t

    data = {'main_length': [M_P],
            'sub_length': [],
            'changing_point': [],
            'main_length_ts': main_length_ts.tolist(),
            'sub_length_ts': [],
            'ts': Y_t.tolist(),
            'trend': Tau_t.tolist(),
            'seasonal': S_t.tolist(),
            'residual': R_t.tolist()}

    if is_export:
        with open(filename, "w") as outfile:
            json.dump(data, outfile)
    return data


def generate_syn3(filename: str = "syn3.json", is_export=False):
    np.random.seed(0)

    Tau_increase = np.linspace(0, 2, num=2200)
    Tau_stability = np.ones(600) + 1
    Tau_decrease = np.linspace(2, 0, num=2200)
    Tau_t = np.concatenate((Tau_increase, Tau_stability, Tau_decrease))

    M_1 = 50
    M_2 = 80
    M_main = 140
    main_pattern = sinewave(5000, M_main, 1.5)
    first_pattern = sinewave(1800, M_1, 1)
    second_pattern = sinewave(1800, M_2, 1)
    third_pattern = sinewave(1400, M_1, 1)
    sub_pattern = np.concatenate((first_pattern,
                                  second_pattern,
                                  third_pattern))

    main_length_ts = np.repeat(M_main, len(Tau_t))
    sub_length_ts = np.concatenate((np.repeat(M_1, 1800),
                                    np.repeat(M_2, 1800),
                                    np.repeat(M_1, 1400)))
    S_t = main_pattern + sub_pattern
    R_t = 0.03 * np.random.randn(len(Tau_t))
    Y_t = Tau_t + S_t + R_t

    data = {'main_length': [M_main],
            'sub_length': [M_1, M_2],
            'change_point': [1800, 3200],
            'main_length_ts': main_length_ts.tolist(),
            'sub_length_ts': sub_length_ts.tolist(),
            'ts': Y_t.tolist(),
            'trend': Tau_t.tolist(),
            'seasonal': S_t.tolist(),
            'main_seasonal': main_pattern.tolist(),
            'sub_seasonal': sub_pattern.tolist(),
            'residual': R_t.tolist()}

    if is_export:
        with open(filename, "w") as outfile:
            json.dump(data, outfile)

    return data


def generate_syn3_1(filename: str = "syn3.1.json", is_export=False):
    np.random.seed(0)

    Tau_increase = np.linspace(0, 2, num=2200)
    Tau_stability = np.ones(600) + 1
    Tau_decrease = np.linspace(2, 0, num=2200)
    Tau_t = np.concatenate((Tau_increase, Tau_stability, Tau_decrease))

    M_1 = 50
    M_2 = 80
    M_main = 140
    # main_pattern = sinewave(5000, M_main, 1.5)
    first_pattern = sinewave(1800, M_1, 1)
    second_pattern = sinewave(1800, M_2, 1)
    third_pattern = sinewave(1400, M_1, 1)
    sub_pattern = np.concatenate((first_pattern,
                                  second_pattern,
                                  third_pattern))

    main_length_ts = np.repeat(M_main, len(Tau_t))
    sub_length_ts = np.concatenate((np.repeat(M_1, 1800),
                                    np.repeat(M_2, 1800),
                                    np.repeat(M_1, 1400)))
    S_t = sub_pattern
    R_t = 0.03 * np.random.randn(len(Tau_t))
    Y_t = Tau_t + S_t + R_t

    data = {'main_length': [M_1, M_2],
            # 'sub_length': [M_1, M_2],
            'change_point': [1800, 3200],
            'main_length_ts': main_length_ts.tolist(),
            'sub_length_ts': sub_length_ts.tolist(),
            'ts': Y_t.tolist(),
            'trend': Tau_t.tolist(),
            'seasonal': S_t.tolist(),
            # 'main_seasonal': main_pattern.tolist(),
            'main_seasonal': sub_pattern.tolist(),
            'sub_seasonal': [],
            'residual': R_t.tolist()}

    if is_export:
        with open(filename, "w") as outfile:
            json.dump(data, outfile)

    return data


def generate_syn4(filename: str = "syn4.json", is_export=False):
    np.random.seed(0)

    total_cycle = 60
    temporal_cycle = 10
    M_normal = 80
    M_abnormal = np.random.choice(np.arange(40, 170), size=temporal_cycle, replace=False)
    normal_cycle = sinewave(M_normal, M_normal, 1)
    changing_index = np.random.choice(np.arange(10, total_cycle - 10),
                                      size=temporal_cycle, replace=False)
    S_t = []
    timestamp_changing = []
    answer_mp = []
    count = 0
    for idx in range(total_cycle):
        if idx in changing_index:
            timestamp_changing.append(len(S_t))
            answer_mp = answer_mp + ([int(M_abnormal[count])] * M_abnormal[count])
            anomaly_cycle = sinewave(M_abnormal[count], M_abnormal[count], 1)
            count = count + 1
            S_t = np.concatenate([S_t, anomaly_cycle])
        else:
            answer_mp = answer_mp + ([int(M_normal)] * M_normal)
            S_t = np.concatenate([S_t, normal_cycle])

    Tau_t = np.zeros(M_normal * 7)  # avoid 5m for oneshot
    remaining_len = round((len(S_t) - (M_normal * 7)) / 4)
    final_len = len(S_t) - (M_normal * 7) - (3 * remaining_len)
    Tau_t = np.concatenate([Tau_t, np.ones(remaining_len)])
    Tau_t = np.concatenate([Tau_t, 1.5 * np.ones(remaining_len)])
    Tau_t = np.concatenate([Tau_t, 1 * np.ones(remaining_len)])
    Tau_t = np.concatenate([Tau_t, np.zeros(final_len)])

    R_t = 0.03 * np.random.randn(len(Tau_t))
    Y_t = Tau_t + S_t + R_t

    data = {'main_length': [M_normal],
            'sub_length': [],
            'change_point': timestamp_changing,
            'main_length_ts': answer_mp,
            'sub_length_ts': [],
            'ts': Y_t.tolist(),
            'trend': Tau_t.tolist(),
            'seasonal': S_t.tolist(),
            'residual': R_t.tolist()}

    if is_export:
        with open(filename, "w") as outfile:
            json.dump(data, outfile)

    return data


# For testing : waiting for removing
if __name__ == '__main__':

    data = generate_syn3_1(is_export=False)
    # sr = np.array(data['seasonal']) + np.array(data['residual'])
    # plt.figure(figsize=(11, 4))  # Adjust the figure size as needed
    # plt.plot(sr)
    # # plt.title('Syn 1', fontsize = 20)
    # plt.xlabel('timestamps', fontsize = 18)
    # plt.ylabel('Value', fontsize = 18)
    # plt.xticks(fontsize=18)
    # plt.yticks(fontsize=18)
    # plt.tight_layout()
    # plt.show()

    #
    plot_lable = ['Raw data & Trend component', 'Seasonal component']
    tick_interval = 500
    plot_data = [data['ts'], data['seasonal']]
    fig, axes = plt.subplots(2, 1, figsize=(7, 5))
    for i, ax in enumerate(axes.ravel()):
        if i == 0:
            ax.plot(plot_data[0], label="raw")
            ax.plot(data['trend'], 'r', alpha=0.7, label="trend")
            # ax.legend(fontsize="17")
        else:
            ax.plot(plot_data[i])
        ax.set_title(plot_lable[i], fontdict={'fontsize': 18})
        xticks = np.arange(0, len(data['ts']), 1000)

        ax.set_xticks(xticks)
        ax.set_xticklabels([f'{tick:.0f}' for tick in xticks], fontsize=18)
        ax.set_yticklabels(ax.get_yticks(), fontsize=18)
    #
    #
    # plt.tight_layout()
    # plt.show()
    # plt.clf()
#     data = generate_syn3()
#     plot_data = [data['ts'], data['trend'], data['seasonal'], data['residual']]
#     fig, axes = plt.subplots(2, 2, figsize=(8, 6))
#     for i, ax in enumerate(axes.ravel()):
#         if i == 0:
#             ax.plot(plot_data[0], label="raw")
#             ax.plot(plot_data[1], 'r', alpha=0.7, label="trend")
#             ax.legend()
#         else:
#             ax.plot(plot_data[i])
#         ax.set_title(plot_lable[i])
#
#     fig.suptitle('RAW')
#     plt.tight_layout()
#     plt.show()
#     plt.clf()
#     data = generate_syn4()
#     plot_data = [data['ts'], data['trend'], data['seasonal'], data['residual']]
#     fig, axes = plt.subplots(2, 2, figsize=(8, 6))
#     for i, ax in enumerate(axes.ravel()):
#         if i == 0:
#             ax.plot(plot_data[0], label="raw")
#             ax.plot(plot_data[1], 'r', alpha=0.7, label="trend")
#             ax.legend()
#         else:
#             ax.plot(plot_data[i])
#         ax.set_title(plot_lable[i])
#
#     fig.suptitle('RAW')
#     plt.tight_layout()
#     plt.show()
