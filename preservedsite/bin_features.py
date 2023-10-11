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
    
    for feature in df.columns[1:]: # skipping 'PATIENT' column
        feature_df = df[[args.patient_col, feature]]
        binary_label_feature_col_name = feature + '_binary_label'
        feature_df[binary_label_feature_col_name] = pd.cut(feature_df[feature], args.n_bins, labels=False)
        
        if args.site_col:
            feature_df['SITE'] = feature_df[args.patient_col].apply(lambda x: x.split('-')[1])
        feature_df = feature_df.sort_values(by=[args.patient_col])
        # drop rows with missing values in feature column
        feature_df = feature_df.dropna(subset=[feature])

        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
        
        output_file = args.output_dir + f'/{feature}_binary_label.csv'
        
        feature_df.to_csv(output_file, index=False)
        print(f'Processed data saved to {output_file}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process data and create binary label CSV files.")
    parser.add_argument("--input-csv", type=str, help="Path to the input CSV file.")
    parser.add_argument("--n-bins", type=int, default=5, help="Number of bins for pd.qcut (default: 5)")
    parser.add_argument("--patient-col", type=str, default='PATIENT', help="Name of column containing patient IDs (default: PATIENT)")
    parser.add_argument("--site-col", action='store_true', help="Include this flag to extract SITE information from TCGA patient IDs (default: False)")
    parser.add_argument("--output-dir", type=str, default='./output', help="Output directory for processed CSV files (default: ./output)")
    
    args = parser.parse_args()

    main(args)