# Preserved Site Cross Validation
Provides optimal stratification for deep learning on datasets with samples from multiple sites
<br>
<img src="https://github.com/fmhoward/PreservedSiteCV/blob/main/PreservedSitesCV.png?raw=true" width="600">

## Installation
The associated files can be downloaded to a project directory. Installation takes < 5 minutes on a standard desktop computer. All software was tested on Windows 10 version 1909, with a Intel Core i5-10210U processor with integrated Intel UHD graphics processor.

Requirements:
* python 3.7
* pandas 1.0.5
* cvxpy 1.1.7
* numpy 1.19.0
* IBM's CPLEX 12.10.0 and <a href='https://www.ibm.com/support/knowledgecenter/en/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html'>CPLEX's python API</a>

## Overview
Stratification can be performed by loading data from an annotations file into a DataFrame. Stratification can be performed with the following function:
```python
def generate(data, category, values, crossfolds = 3, target_column = 'CV3', patient_column = 'submitter_id', site_column = 'SITE', timelimit = 100):
    ''' Generates 3 site preserved cross folds with optimal stratification of category
    Input:
        data: dataframe with slides that must be split into crossfolds.
        category: the column in data to stratify by
        values: a list of possible values within category to include for stratification
        crossfolds: number of crossfolds to split data into
        target_column: name for target column to contain the assigned crossfolds for each patient in the output dataframe
        patient_column: column within dataframe indicating unique identifier for patient
        site_column: column within dataframe indicating designated site for a patient
        timelimit: maximum time to spend solving
    Output:
        dataframe with a new column, 'CV3' that contains values 1 - 3, indicating the assigned crossfold
    '''
```

## Example
Please see test.py for example use applied to the accompanying 'example.csv' data file.  In our tests on above hardware, execution of this code takes 0.34 seconds.
```python
import preservedsite.crossfolds as cv
import pandas as pd

data = pd.read_csv("example.csv", dtype=str)
data = cv.generate(data, "feature", ["A", "B"], crossfolds=3, patient_column='patient', site_column='site')
```

The resulting segregation of sites into crossfolds is printed as follows, with the appropriate assignment of patients to folds for cross validation appended to the dataframe.
```
Crossfold 1: A - 54 B - 251  Sites: ['Site 0', 'Site 7', 'Site 9', 'Site 10', 'Site 11', 'Site 13', 'Site 19', 'Site 28']
Crossfold 2: A - 54 B - 250  Sites: ['Site 1', 'Site 2', 'Site 4', 'Site 5', 'Site 8', 'Site 14', 'Site 15', 'Site 18', 'Site 20', 'Site 21', 'Site 22', 'Site 23', 'Site 25', 'Site 26', 'Site 30', 'Site 32', 'Site 34', 'Site 36']
Crossfold 3: A - 54 B - 250  Sites: ['Site 3', 'Site 6', 'Site 12', 'Site 16', 'Site 17', 'Site 24', 'Site 27', 'Site 29', 'Site 31', 'Site 33', 'Site 35', 'Site 37']
```

## Reproduction
To recreate our cross validation setup for <a href="https://www.biorxiv.org/content/10.1101/2020.12.03.410845v2">our work describing batch effect in TCGA</a>, clinical annotations should be downloaded from https://www.cbioportal.org/ for TCGA datasets for the six cancers of interest. Immune subtype annotations were obtained from the work of <a href="https://pubmed.ncbi.nlm.nih.gov/29628290/">Thorsson et al</a>, and genomic ancestry annotations were obtained from <a href="https://www.cell.com/cancer-cell/pdfExtended/S1535-6108(20)30211-7">Carrot-Zhang et al</a>. The CSV files with annotations from cbioportal can then be loaded into a dataframe as per the above example to generate 3 groups of sites for preserved site cross validation.

To generate the folds used for cross validation, we ran our preserved site cross validation tool for each feature of interest:
```
data = cv.generate(data, "ER status", ["Positive", "Negative"], crossfolds=3, patient_column='patient', site_column='site')
data = cv.generate(data, "BRCA mutation", ["Present", "Absent"], crossfolds=3, patient_column='patient', site_column='site')
...
```
