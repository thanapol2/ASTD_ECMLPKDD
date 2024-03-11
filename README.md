
# Streamlined Seasonal-Trend Decomposition (SSTD)

- This is an official implementation of "Streamlined Seasonal-Trend Decomposition (SSTD) for Online Time Series Decomposition with Seasonal Transitions and Fluctuations" (SSTD).
- SSTD was implemented using Python 3.9.2.
- Existing methods were implemented using Python 3.9.2 and R 4.3.0

- If you have any more questions or need further suggestions, don't hesitate to email me.

## Document material
- [Supplementary material](https:)


## Folder structure 
    .
    ├── dataset                            # Datasets were utilized in this paper. 
    │   ├── 01_synthetic_dataset           
    │   ├── 02_CRAN_dataset               
    │   └── 03_Long_length_dataset
    │   └── README.md                      # Readme for dataset folder
    ├── evaluation                         # All source codes for reproduction
    │   ├── Numerical_error_computation 
    │   ├── Time_complexity    
    │   ├── utility_evaluation.R           # Utility function for evaluation with R
    │   ├── README.MD                      # Readme for evaluation folder
    ├── src                                # Source files
    │   ├── utilities                      # Utility functions
    │   └── online_decomposition           # Online Time series decomposition
    └── README.md

>  Note that our datasets were cleaned in the same format, but we give information to access the original sources.


## Dependencies
### Python
- [numpy](http://www.numpy.org/) >=1.26.4
- [scipy] >= 1.12.0
- [statsmodel] >= 0.14.1
- [matplotlib] >= 3.8.2
- [periodicity-detection](https://periodicity-detection.readthedocs.io/en/latest/) >= 0.1.1    ** For existing SLE methods

### R
- [sazedR](https://cran.r-project.org/web/packages/sazedR/index.html) >= 2.0.2    ** SAZED method
- [astsa](https://cran.r-project.org/web/packages/astsa/index.html) >= 2.1    ** CRAN dataset
- [fpp2](https://cran.r-project.org/web/packages/fpp2/index.html) >= 2.5    ** CRAN dataset
- [expsmooth](https://cran.r-project.org/web/packages/expsmooth/index.html) >= 2.3    ** CRAN dataset
- [fma](https://cran.r-project.org/web/packages/fma/index.html) >= 2.5    ** CRAN dataset

** Please be careful some libraries overwrite some datasets. 
## Citing


## BibTex


## Link

## Contact

