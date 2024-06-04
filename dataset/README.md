
# Dataset folder

- These are all datasets that are utilized in our paper


## Folder structure 
    .
    ├── 01_synthetic_datasets          # Two synthetics dataset
    ├── 02_Real1_datasets              # Real-world datasets with seasonality transitions and fluctuations
    ├── 03_Real2_datasets              # Real-world dataset from The Comprehensive R Archive Network (CRAN) 
    └── README.md                      


>  Note that our datasets were cleaned in the same format, but we give information to access the original sources.

## Data dictionary for each JSON file

Attribute Name   | Meaning
-------------    | -------------
main_length      | Main season length of seasonal component
transition_points| Starting point of seasonality transitions
main_length_ts   | Season length for each timestamp
ts               | Time series data (Y)
trend            | Trend component (T)
seasonal         | Seasonal component (S)
residual         | Residual component (R)


## Data Source

### 01_synthetic_datasets
- The code for generating synthetic datasets can be found in "src/utilities/gen_synthetic.py".

### 02_Real1_datasets
- All URLs and details of the original datasets can be found in the 'Experimental Settings' section of our publication.
- List URLs:

Dataset Name    | URL
-------------   | -------------
WalkJogRun1     | [Matrix Profile VIII supplementary website](https://sites.google.com/site/onlinesemanticsegmentation/)
WalkJogRun2     | [Matrix Profile VIII supplementary website](https://sites.google.com/site/onlinesemanticsegmentation/)
CO2             | [Trends in Atmospheric Carbon Dioxide from National Oceanic and Atmospheric Administration](https://doi.org/10.15138/9N0H-ZH07)
Canadian lynx   | [fma package from CRAN](https://search.r-project.org/CRAN/refmans/fma/html/lynx.html)
SOI             | [Southern Oscillation Index (SOI) from National Centers for Enviromental Information](https://www.ncei.noaa.gov/access/monitoring/enso/soi)
Sunspot         | [Sunspot Index and Long-term Solar Observations](https://www.sidc.be/SILSO/datafiles)


### 03_Real2_datasets
- We exported a list for each dataset and source in "cran_list_datasets.csv" 
- **Please be careful some libraries overwrite some datasets.**
- CRAN package URLs:
    - [astsa](https://cran.r-project.org/web/packages/astsa/index.html) >= 2.1    ** CRAN dataset
    - [fpp2](https://cran.r-project.org/web/packages/fpp2/index.html) >= 2.5    ** CRAN dataset
    - [expsmooth](https://cran.r-project.org/web/packages/expsmooth/index.html) >= 2.3    ** CRAN dataset
    - [fma](https://cran.r-project.org/web/packages/fma/index.html) >= 2.5    ** CRAN dataset




## Acknowledgements

We would like to thank the community and everyone who made their datasets publicly accessible. These datasets are valuable and have greatly facilitated this research. 

