# Z-score normalization function
Znormalization <- function(X) {
  mean_X <- mean(X, na.rm = TRUE)
  sd_X <- sd(X, na.rm = TRUE)
  
  if (sd_X == 0) {
    warning("Standard deviation is zero. Z-normalization not possible.")
    return(X)
  }
  
  Z <- (X - mean_X) / sd_X
  return(Z)
}

# Function to calculate rate of change
calculate_rate_of_change <- function(ts, seasonality_length) {
  n <- length(ts)
  num_cycles <- ceiling(n / seasonality_length)
  padding_size <- num_cycles * seasonality_length - n
  
  # Pad ts with NA
  ts <- c(ts, rep(NA, padding_size))
  
  results <- numeric(0)
  
  for (cycle_index in 1:seasonality_length) {
    subseasonality_ts <- sapply(1:num_cycles, function(i) ts[cycle_index + (i - 1) * seasonality_length])
    subseasonality_ts <- subseasonality_ts[!is.na(subseasonality_ts)]
    
    differences <- diff(subseasonality_ts)
    time_diff <- diff(seq_along(subseasonality_ts))
    
    rate_of_change <- differences / time_diff
    results <- c(results, rate_of_change)
  }
  
  return(c(mean(results, na.rm = TRUE),sd(results)))
}

# Function to update sDFT (sliding Discrete Fourier Transform)
# 
# References:
#   [1] E. Jacobsen and R. Lyons, "The sliding DFT," in IEEE Signal Processing Magazine,
#       vol. 20, no. 2, pp. 74-80, March 2003, doi: 10.1109/MSP.2003.1184347.
#   [2] E. Jacobsen and R. Lyons, "An update to the sliding DFT," in IEEE Signal Processing Magazine,
#       vol. 21, no. 1, pp. 110-111, Jan. 2004, doi: 10.1109/MSP.2004.1516381.
update_sDFT <- function(fft_X, old_x, new_x) {
  N <- length(fft_X)
  k <- seq(0, N - 1)
  twiddle <- exp(2i * pi * k / N)
  new_fft_X <- (fft_X - old_x + new_x) * twiddle
  
  return(new_fft_X)
}

# Function for result aggregation
result_aggregation <- function(dataset_name, algo_name, window_size, input_results) {
  error_bounds = c(0, 2, 5, 10, 15, 20)
  output_results <- c()
  
  for (error_bound in error_bounds) {
    count_result <- 0
    
    for (i in 1:nrow(input_results))  {
      row <- input_results[i, ]
      if (error_bound == 0) {
        lb <- row$answer
        ub <- row$answer
      } else {
        lb <- row$answer * ((100 - error_bound) / 100)
        ub <- row$answer * ((100 + error_bound) / 100)
      }
      
      pred_result <- row$result
      
      if (lb <= pred_result && pred_result <= ub) {
        count_result <- count_result + 1
      }
    }
    
    accuracy_ratio <- count_result / nrow(input_results)
    
    output_row <- data.frame(
      dataset_name = dataset_name,
      algorithms = algo_name,
      error_bound = error_bound,
      window_size = window_size,
      accuracy_ratio = accuracy_ratio
    )
    output_results <- rbind(output_results, output_row)
  }
  
  return(output_results)
}
