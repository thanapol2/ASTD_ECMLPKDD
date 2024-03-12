
# Dataset folder

- These are all datasets that are utilized in our paper


## Folder structure 
    .
    ├── 01_synthetic_dataset           # Two synthetics dataset
    └── 02_seasonal_changes_dataset    # Real-world datasets within seasonal length changes
    ├── 03_CRAN_dataset                # Real-world dataset from The Comprehensive R Archive Network (CRAN) 
    └── README.md                      


>  Note that our datasets were cleaned in the same format, but we give information to access the original sources.


## Original Source

### 01_synthetic_dataset
- The re-generataion synthetic dataset codes are available in "src/utilities/gen_synthetic.py"
- ## Data dic for each JSON file

Attribute Name   | Meaning
-------------    | -------------
main_length      | length of main seasonal component
changing_point   | answer of seasonal changing point
ts               | time series data (Y)
trend            | trend component (T)
seasonal         | seasonal component (S)
residual         | residual component (R)

### 02_seasonal_changes_dataset
- All URLs and details of original datasets are available "Reference" in our publication.
- List URL

Dataset Name    | URL
-------------   | -------------
WalkJogRun1     | [Matrix Profile VIII supplementary website](https://sites.google.com/site/onlinesemanticsegmentation/)
WalkJogRun2     | [Matrix Profile VIII supplementary website](https://sites.google.com/site/onlinesemanticsegmentation/)
Canadian lynx   | [fma package from CRAN](https://search.r-project.org/CRAN/refmans/fma/html/lynx.html)
SOI             | [Southern Oscillation Index (SOI) from National Oceanic and Atmospheric Administration](https://www.ncei.noaa.gov/access/monitoring/enso/soi)
Sunspot         | [Sunspot Index and Long-term Solar Observations](https://www.sidc.be/SILSO/datafiles)


### 03_CRAN_dataset
- We exported a list for each dataset and source in "cran_list.csv" 
- **Please be careful some libraries overwrite some datasets.**
- CRAN package URL:
    - [astsa](https://cran.r-project.org/web/packages/astsa/index.html) >= 2.1    ** CRAN dataset
    - [fpp2](https://cran.r-project.org/web/packages/fpp2/index.html) >= 2.5    ** CRAN dataset
    - [expsmooth](https://cran.r-project.org/web/packages/expsmooth/index.html) >= 2.3    ** CRAN dataset
    - [fma](https://cran.r-project.org/web/packages/fma/index.html) >= 2.5    ** CRAN dataset




## BibTex

