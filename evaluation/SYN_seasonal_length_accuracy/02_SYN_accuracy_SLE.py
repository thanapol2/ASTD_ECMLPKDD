import os
import json
import numpy as np
import periodicity_detection as period
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import src.utilities.utility_stl as utility_stl

FOLDER_DATASET = os.path.expanduser("~/source_code/ESTL/dataset/01_synthetic_dataset")
result_folder = 'synthetic_result'
files_name = ['syn1','syn2','syn3','syn3.1', 'syn4']
folder_path = 'synthetic_result'
algorithms = ['find_length', 'autoPeriod', 'ACF']
save_result = 'accuracy_ratio_results.csv'

if __name__ == '__main__':
    plot_results = []
    for algo_name in algorithms:
        print(algo_name)
        for file_name in files_name:
            results = []
            data_directory = os.path.join(FOLDER_DATASET, file_name)
            print(f'{data_directory}')
            with open(f'{data_directory}.json') as f:
                syn_data = json.load(f)
            S = np.array(syn_data['seasonal'])
            R = np.array(syn_data['residual'])
            ts_data = S + R
            ts_data = utility_stl.Znormalization(ts_data)
            main_length = int(max(syn_data['main_length']))
            if file_name in ['syn3', 'syn3.1']:
                answer_window = np.array(syn_data['sub_length_ts'])
            else:
                answer_window = np.array(syn_data['main_length_ts'])

            window_sizes = np.arange(2 * main_length, 6 * main_length, 6)
            # sliding
            for window_size in window_sizes:
                results = []
                for idx in range(len(ts_data) - window_size + 1):
                    buffer = ts_data[idx:window_size + idx]
                    if algo_name == 'find_length':
                        SLE_result = period.find_length(buffer)
                    elif algo_name == 'autoPeriod':
                        SLE_result = period.autoperiod(buffer)
                    else:
                        SLE_result = period.autocorrelation(buffer)

                    results.append({'idx_win': window_size + idx,
                                    'answer': answer_window[window_size + idx - 1],
                                    'result': SLE_result})

                plot_results = plot_results + utility_stl.result_aggregation(file_name,
                                                                algo_name,
                                                                window_size, results)

    df_results = pd.DataFrame(plot_results, columns=['dataset_name',
                                                     'algorithms',
                                                     'error_bound', 'window_size', 'accuracy_ratio'])
    filtered_df = df_results[(df_results['error_bound'] == 2) & (df_results['dataset_name'] == 'syn3.1')]
    plt.figure(figsize=(12, 8))
    b = sns.lineplot(data=filtered_df, x='window_size', y='accuracy_ratio', hue='algorithms', style='algorithms',
                     markers=False, linewidth=3, dashes=False)
    plt.show()

    if os.path.exists(save_result):
        df_results.to_csv(save_result, mode='a', header=False, index=False)
    else:
        df_results.to_csv(save_result, index=False)