import os
import json
import numpy as np
from scipy.fft import fft, fftfreq
import src.utilities.utility_frequency_analysis as sDFT
import src.utilities.utility_stl as utility_stl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

FOLDER_DATASET = os.path.expanduser("~/source_code/ESTL/dataset/01_synthetic_dataset")
result_folder = 'synthetic_result'
files_name = ['syn1', 'syn2', 'syn3', 'syn3.1', 'syn4']
folder_path = 'synthetic_result'
algorithms = ['rec', 'rec', 'rec', 'rec', 'hann']
estimators = ['non', 'quin2', 'qse', 'haqse', 'grandke']
save_result = 'accuracy_ratio_results.csv'

if __name__ == '__main__':
    plot_results = []
    for algo_name,estimator_name in zip(algorithms,estimators):
        print (f'{algo_name},{estimator_name}')
        for file_name in files_name:
            data_directory = os.path.join(FOLDER_DATASET, file_name)
            print(f'{data_directory}')
            with open(f'{data_directory}.json') as f:
                syn_data = json.load(f)

            S = np.array(syn_data['seasonal'])
            R = np.array(syn_data['residual'])
            ts_data = S + R
            ts_data = utility_stl.Znormalization(ts_data)
            freq = int(max(syn_data['main_length']))
            if file_name in ['syn3', 'syn3.1']:
                answer_window = np.array(syn_data['sub_length_ts'])
            else:
                answer_window = np.array(syn_data['main_length_ts'])

            window_sizes = np.arange(2 * freq, 6 * freq, 6)
            for window_size in window_sizes:
                results = []
                buffer = ts_data[:window_size]
                start_fft = fft(buffer)
                xfreq, periodogram_den = sDFT.peridogram(window_size, start_fft, algo_name)
                frequency_range = abs(xfreq[0] - xfreq[1])
                location, peak_index = sDFT.get_period_hints(periodogram_den)
                if peak_index > 1:
                    if estimator_name == 'non':
                        frequency_tone = xfreq[peak_index]
                    elif estimator_name == 'quin2':
                        k_peak, frequency_tone = sDFT.quin2_estimator(start_fft, peak_index, xfreq[1] - xfreq[0])
                    elif estimator_name == 'qse':
                        k_peak, frequency_tone = sDFT.qse(buffer, peak_index, xfreq[1] - xfreq[0])
                    elif estimator_name == 'haqse':
                        k_peak, frequency_tone = sDFT.haqse(buffer, peak_index, xfreq[1] - xfreq[0])
                    else:
                        k_peak, frequency_tone = sDFT.grandke_estimator(start_fft, peak_index,
                                                                          frequency_range)
                    sdft_result = round(1 / frequency_tone)
                else:
                    sdft_result = 1

                results.append({'idx_win': window_size,
                                'answer': answer_window[window_size - 1],
                                'result': sdft_result})

                for idx, newest_x in enumerate(ts_data[window_size:]):
                    oldest_x = buffer[0]
                    buffer = utility_stl.update_array(buffer, newest_x)

                    start_fft = sDFT.update_sDFT(start_fft, oldest_x, newest_x)
                    xfreq, periodogram_den = sDFT.peridogram(window_size, start_fft, algo_name)
                    location, peak_index = sDFT.get_period_hints(periodogram_den)
                    if peak_index > 1:
                        if estimator_name == 'non':
                            frequency_tone = xfreq[peak_index]
                        elif estimator_name == 'quin2':
                            k_peak, frequency_tone = sDFT.quin2_estimator(start_fft, peak_index, xfreq[1] - xfreq[0])
                        elif estimator_name == 'qse':
                            k_peak, frequency_tone = sDFT.qse(buffer, peak_index, xfreq[1] - xfreq[0])
                        elif estimator_name == 'haqse':
                            k_peak, frequency_tone = sDFT.haqse(buffer, peak_index, xfreq[1] - xfreq[0])
                        else:
                            k_peak, frequency_tone = sDFT.grandke_estimator(start_fft, peak_index,
                                                                            frequency_range)
                        sdft_result = round(1 / frequency_tone)
                    else:
                        sdft_result = 1

                    results.append({'idx_win': 1 + window_size + idx,
                                    'answer': answer_window[window_size + idx],
                                    'result': sdft_result})

                plot_results = plot_results + utility_stl.result_aggregation(file_name,
                                                                             f'{algo_name},{estimator_name}',
                                                                             window_size, results)
    df_results = pd.DataFrame(plot_results, columns=['dataset_name',
                                                     'algorithms',
                                                     'error_bound', 'window_size', 'accuracy_ratio'])

    filtered_df = df_results[(df_results['error_bound'] == 2) & (df_results['dataset_name'] == 'syn3.1')]
    plt.figure(figsize=(12, 8))
    b = sns.lineplot(data=df_results, x='window_size', y='accuracy_ratio', hue='algorithms', style='algorithms',
                     markers=False, linewidth=3, dashes=False)
    plt.show()

    if os.path.exists(save_result):
        df_results.to_csv(save_result, mode='a', header=False, index=False)
    else:
        df_results.to_csv(save_result, index=False)
