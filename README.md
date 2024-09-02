

![alt text](https://github.com/thanapol2/Mean_EBinning/blob/082cd9447659d9d140acc38d5d4c11db9187d06c/Documents/shizuoka%20bannar.png)


# Adaptive Seasonal-Trend Decomposition (ASTD)
[![ECML](https://img.shields.io/badge/ECML-2024-blue.svg?style=flat-square)](https://2024.ecmlpkdd.org/)
- This is an official implementation of "Adaptive Seasonal-Trend Decomposition for Streaming Time Series Data with Transitions and Fluctuations in Seasonality" (ASTD).
- This paper was accepted in ECML-PKDD 2024: [https://doi.org/10.1007/978-3-031-70344-7_25](https://doi.org/10.1007/978-3-031-70344-7_25)
- ASTD was implemented using Python 3.9.2.
- Existing methods were implemented using Python 3.9.2 and R 4.3.0

- If you have any more questions or need further suggestions, don't hesitate to email me.

## Document material
- [Supplementary website](https://sites.google.com/view/astd-ecmlpkdd/)


## Folder structure 
    .
    ├── datasets                            # Datasets were utilized in this paper. 
    │   ├── 01_synthetic_datasets           
    │   ├── 02_Real1_datasets             
    │   ├── 03_Real2_datasets
    │   └── README.md                      # Readme for dataset folder
    ├── document                           # Supplmentary file
    ├── evaluation                         # All source codes for reproduction
    │   ├── 00_HAQSE                       # Reproduction for HAQSE estimator
    │   ├── 01_synthetic_datasets          # Reproduction for synthetic datasets
    │   ├── 02_Real1_datasets              # Reproduction for Real1
    │   └── utility_evaluation.R           # Utility function for evaluation with R
    ├── figures                            # Reproduction for Figures in this paper 
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
- [rpy2](https://rpy2.github.io/) >= 3.5.16 ** For R running in python

### R
- [sazedR](https://cran.r-project.org/web/packages/sazedR/index.html) >= 2.0.2    ** SAZED method
- [astsa](https://cran.r-project.org/web/packages/astsa/index.html) >= 2.1    ** CRAN dataset
- [fpp2](https://cran.r-project.org/web/packages/fpp2/index.html) >= 2.5    ** CRAN dataset
- [expsmooth](https://cran.r-project.org/web/packages/expsmooth/index.html) >= 2.3    ** CRAN dataset
- [fma](https://cran.r-project.org/web/packages/fma/index.html) >= 2.5    ** CRAN dataset

** Please be careful some libraries overwrite some datasets. 

## BibTex
- If you plan to use or apply our source code, please cite our published paper.
```
@InProceedings{10.1007/978-3-031-70344-7_25,
	author="Phungtua-eng, Thanapol and Yamamoto, Yoshitaka",
	editor="Bifet, Albert and Davis, Jesse and Krilavi{\v{c}}ius, Tomas and Kull, Meelis and Ntoutsi, Eirini and {\v{Z}}liobait{\.{e}}, Indr{\.{e}}",
	title="Adaptive Seasonal-Trend Decomposition for Streaming Time Series Data with Transitions and Fluctuations in Seasonality",
	booktitle="Machine Learning and Knowledge Discovery in Databases. Research Track",
	year="2024",
	publisher="Springer Nature Switzerland",
	address="Cham",
	pages="426--443",
	isbn="978-3-031-70344-7"
}
```

## Link
- [Our laboraory at Shizuoka University](http://lab.inf.shizuoka.ac.jp/yamamoto/)

## Contact
If you have any question, please contact thanapol@yy-lab.info

## Acknowledgements

We would like to thank the community and everyone who made their datasets and source codes publicly accessible. These datasets are valuable and have greatly facilitated this research. 

