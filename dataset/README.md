
# Dataset folder

- This is all datasets that utilized in our paper


## Folder structure 
    .
    ├── 01_synthetic_dataset           # Two synthetics dataset
    ├── 02_CRAN_dataset                # Real-world dataset from The Comprehensive R Archive Network (CRAN) 
    └── 03_Long_length_dataset         # Real-world dataset with long length.
    └── README.md                      


>  Note that our datasets were cleaned in the same format, but we give information to access the original sources.


## Data dic for each json file

## Original Source

### 01_synthetic_dataset
- The re-generataion synthetic dataset codes are availabled in "src/utilities/gen_synthetic.py"

### 02_CRAN_dataset
- We exported list for each dataset and source in "cran_list.csv" 
- **Please be careful some libraries overwrite some datasets.**
- CRAN package URL:
    - [astsa](https://cran.r-project.org/web/packages/astsa/index.html) >= 2.1    ** CRAN dataset
    - [fpp2](https://cran.r-project.org/web/packages/fpp2/index.html) >= 2.5    ** CRAN dataset
    - [expsmooth](https://cran.r-project.org/web/packages/expsmooth/index.html) >= 2.3    ** CRAN dataset
    - [fma](https://cran.r-project.org/web/packages/fma/index.html) >= 2.5    ** CRAN dataset


### 03_Long_length_dataset
- All urls and details of original datasets are availabled "Refernce" in our publication.
- List URL

Dataset Name    | URL
-------------   | -------------
WalkJogRun1     | Content Cell
WalkJogRun2     | 
Fetal2013       | 
Co2             |   
Oil price       |
Covid-19        |
SOI             |
Sunspot         |



## BibTex

