library("jsonlite")
library('sazedR')
library('forecast')
rm(list = ls())
# source('utils.R')

source('/Users/thanapolphungtua-eng/source_code/R_programming/evaluation_ESTL/utils.R')



result_df <- data.frame(
  package_name= character(),
  dataset_name = character(),
  length_total = numeric(),
  frequency_ans = numeric(),
  algorithms  = character(),
  size_buffer = character(),
  idx_win = numeric(),
  result_predi = numeric())

json_files <- c('syn4.json')
# algorithms <- c('S', 'SA', 'AZED', 'findfrequency', 'SAZED')
algorithms <- c('S')
plot_results <- c()
for (algo_name in algorithms){
  for (json_file in json_files) {
    json_data <- fromJSON(txt = json_file)
    file_name <- basename(json_file)
    dataset_name <- tools::file_path_sans_ext(file_name)
    seasonal_ts <- json_data$seasonal
    residual_ts <- json_data$residual
    ts <- seasonal_ts + residual_ts
    ts <- Znormalization(ts)
    
    if (dataset_name %in% c('syn3', 'syn3.1')) {
      answer_window <- json_data$sub_length_ts
    } else {
      answer_window <- json_data$main_length_ts
    }
    frequency_val <- max(json_data$main_length)
    
    window_sizes <- seq(2*frequency_val, 6*frequency_val, by = 20)
    
    for (window_size in window_sizes) {
      print(paste0('algo:',algo_name,' size',window_size,':',json_file))
      results <- c()
      pb <- txtProgressBar(min = 0,      # Minimum value of the progress bar
                           max = length(ts) - window_size +1, # Maximum value of the progress bar
                           style = 3,    # Progress bar style (also available style = 1 and style = 2)
                           width = 50,   # Progress bar width. Defaults to getOption("width")
                           char = "=") 
      for (idx in 1:(length(ts) - window_size +1)) {
        buffer <- ts[idx:(window_size + idx - 1)]
        if(algo_name == 'S'){
          SLE_result <- S(buffer, preprocess=FALSE)
        }else if (algo_name == 'SA'){
          SLE_result <- Sa(buffer, preprocess=FALSE)
        }else if (algo_name == 'AZED'){
          SLE_result <- azed(buffer, preprocess=FALSE)
        }else if (algo_name == 'SAZED'){
          SLE_result <- sazed(buffer)
        }else{
          SLE_result <- findfrequency(buffer)
        }
        SLE_result <- replace(SLE_result, is.infinite(SLE_result), 1)
        result_row <- data.frame(
          idx_win = idx + window_size -1,
          answer = answer_window[idx + window_size -1],
          result = SLE_result)
        results <- rbind(results, result_row)
        setTxtProgressBar(pb, idx)
      }
      aggregate_row <- result_aggregation(dataset_name,
                            algo_name,
                            window_size, results)
      plot_results <- rbind(plot_results,aggregate_row)
    }
  }
}
write.csv(plot_results, file = "test.csv", row.names = TRUE)
