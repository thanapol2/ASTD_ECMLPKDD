
# Adaptive Seasonal-Trend Decomposition (ASTD)

- This is an official implementation of "Adaptive Seasonal-Trend Decomposition for Streaming Time Series Data with Transitions and Fluctuations in Seasonality" (ASTD).
- ASTD was implemented using Python 3.9.2.
- Existing methods were implemented using Python 3.9.2 and R 4.3.0

- If you have any more questions or need further suggestions, don't hesitate to email me.

## Document material
- [Supplementary websit](https://sites.google.com/view/astd-ecmlpkdd/)


## Folder structure 
    .
    ├── dataset                            # Datasets were utilized in this paper. 
    │   ├── 01_synthetic_datasets           
    │   ├── 02_Real1_datasets             
    │   └── 03_Real2_datasets
    │   └── README.md                      # Readme for dataset folder
    ├── evaluation                         # All source codes for reproduction
    │   ├── Numerical_error_computation 
    │   ├── 01_synthetic_datasets          # Reproduction for synthetic datasets
    │   ├── 02_Real1_datasets              # Reproduction for Real1
    │   ├── utility_evaluation.R           # Utility function for evaluation with R
    │   ├── README.MD                      # Readme for evaluation folder
    ├── src                                # Source files
    │   ├── utilities                      # Utility functions
    │   └── online_decomposition           # Online Time series decomposition
    └── README.md

>  Note that our datasets were cleaned in the same format, but we give information to access the original sources.


## Dependencies
### Python
- [numpy] >=1.26.4
- [scipy] >= 1.12.0
- [pandas] >= 2.2.1
- [matplotlib] >= 3.8.2
- [tqdm](https://tqdm.github.io) >= 4.64.1
- [statsmodel](https://www.statsmodels.org/stable/index.html) >= 0.14.1
- [periodicity-detection](https://periodicity-detection.readthedocs.io/en/latest/) >= 0.1.1    ** For existing SLE methods
- [scikit-learn](https://scikit-learn.org/stable/) >= 1.4.1   ** For mean square error computation in STD evaluations.  

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

