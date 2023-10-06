#import pandas as pd
#import numpy as np
#
#file_path = './voom_DEGs_tumour_t_prognostic_incl_samples.csv'
#
#df = pd.read_csv(file_path)
#print(df.head())
#
#for gene in df.columns[1:]:
#    gene_df = df[['PATIENT', gene]]
#    binary_label_gene_col_name = gene + '_binary_label'
#    gene_df[binary_label_gene_col_name] = pd.qcut(gene_df[gene], q=5, labels=False)
#    gene_df['SITE'] = gene_df['PATIENT'].apply(lambda x: x.split('-')[1])
#    gene_df.to_csv(f'./voom_DEGs_tumour_t_{gene}_binary_label.csv', index=False)


import argparse
import pandas as pd
import os

def main(args):

    """
    Bin continuous clinical features data for cross-validation stratification and extract TSS from TCGA patient ID

    Input:
        input_csv: CSV file containing continuous clinical features data, where the first column is patient IDs and the rest are features
        cv_col: name of column containing cross-validation fold numbers
        output_file: output file name

    Output:
        CSV file containing binned clinical features data
    """
    df = pd.read_csv(args.input_csv)
    
    for gene in df.columns[1:]:
        gene_df = df[[args.patient_col, gene]]
        binary_label_gene_col_name = gene + '_binary_label'
        gene_df[binary_label_gene_col_name] = pd.qcut(gene_df[gene], q=args.n_bins, labels=False)
        # to do: make SITE column optional
        gene_df['SITE'] = gene_df[args.patient_col].apply(lambda x: x.split('-')[1])
        gene_df = gene_df.sort_values(by=[args.patient_col])

        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
        
        output_file = args.output_dir + f'/{gene}_binary_label.csv'
        
        gene_df.to_csv(output_file, index=False)
        print(f'Processed data saved to {output_file}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process data and create binary label CSV files.")
    parser.add_argument("--input-csv", type=str, help="Path to the input CSV file.")
    parser.add_argument("--n-bins", type=int, default=5, help="Number of bins for pd.qcut (default: 5)")
    parser.add_argument("--patient-col", type=str, default='PATIENT', help="Name of column containing patient IDs (default: PATIENT)")
    parser.add_argument("--output-dir", type=str, default='./output', help="Output directory for processed CSV files (default: ./output)")
    
    args = parser.parse_args()

    main(args)