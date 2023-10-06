import pandas as pd
import numpy as np
import argparse
import os
import torch

def genrate_pt(input_csv, cv_col, output_path):

    """
    Generate a PT file containing a tuple of indices for each fold

    Input:
        input_csv: CSV file containing clinical data
        cv_col: name of column containing cross-validation fold numbers
        output_file: output file name
    Output:
        PT file containing a tuple of indices for each fold
    """

    data_df = pd.read_csv(input_csv)
    cv_column = data_df[cv_col]
    n_folds = np.unique(cv_column)

    patient_indices_tuple = tuple(
        (np.where(cv_column != fold)[0], np.where(cv_column == fold)[0]) for fold in n_folds
    )

    #print(patient_indices_tuple)
    
    torch.save(patient_indices_tuple, os.path.join(output_path, 'folds.pt'))

    # Further operations with patient_indices_tuple if needed

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract preserved folds from clinical data')
    parser.add_argument('--input-csv', type=str, help='CSV generates from crossfolds.py')
    parser.add_argument('--cv-col', type=str, help='Name of column containing cross-validation fold numbers', default='CV3')
    parser.add_argument('--output-path', type=str, help='Output file name', default='./')

    args = parser.parse_args()

    genrate_pt(args.input_csv, args.cv_col, args.output_path)
    