import pandas as pd
import numpy as np
import cvxpy as cp
import argparse
import cplex

def generate(data, category, values, n_folds, target_column, patient_column , site_column, timelimit, randomseed, output_csv):
    ''' Generates 3 site preserved cross folds with optimal stratification of category
    Input:
        data: dataframe with slides that must be split into n_folds.
        category: the column in data to stratify by
        values: a list of possible values within category to include for stratification
        n_folds: number of n_folds to split data into
        target_column: name for target column to contain the assigned n_folds for each patient in the output dataframe
        patient_column: column within dataframe indicating unique identifier for patient
        site_column: column within dataframe indicating designated site for a patient
        timelimit: maximum time to spend solving
    Output:
        dataframe with a new column, 'CV3' that contains values 1 - 3, indicating the assigned crossfold
    '''
    submitters = data[patient_column].unique()
    newData = pd.merge(pd.DataFrame(submitters, columns=[patient_column]), data[[patient_column, category, site_column]], on=patient_column, how='left')
    newData.drop_duplicates(inplace=True)
    uniqueSites = data[site_column].unique()
    n = len(uniqueSites)
    listSet = []
    # if elements of values are not strings, convert them to strings
    if not isinstance(values[0], str):
        values = [str(v) for v in values]
    # convert category column elements to strings
    newData[category] = newData[category].astype(str)
    for v in values:
        listOrder = []
        for s in uniqueSites:
            listOrder += [len(newData[(newData[site_column] == s) & (newData[category] == v)].index)]
        listSet += [listOrder]
    gList = []
    for i in range(n_folds):
        gList += [cp.Variable(n, boolean=True)]
    A = np.ones(n)
    constraints = [sum(gList) == A]
    error = 0
    for v in range(len(values)):
        for i in range(n_folds):
            error += cp.square(cp.sum(n_folds * cp.multiply(gList[i], listSet[v])) - sum(listSet[v]))
    prob = cp.Problem(cp.Minimize(error), constraints)
    prob.solve(solver='CPLEX', cplex_params={"timelimit": timelimit, "randomseed": randomseed})
    gSites = []
    for i in range(n_folds):
        gSites += [[]]
    for i in range(n):
        for j in range(n_folds):
            if gList[j].value[i] > 0.5:
                gSites[j] += [uniqueSites[i]]
    for i in range(n_folds):
        str1 = "Crossfold " + str(i+1) + ": "
        j = 0
        for s in listSet:
            str1 = str1 + values[j] + " - " + str(int(np.dot(gList[i].value, s))) + " "
            j = j + 1
        str1 = str1 + " Sites: " + str(gSites[i])
        print(str1)
    bins = pd.DataFrame()
    for i in range(n_folds):
        data.loc[data[site_column].isin(gSites[i]), target_column] = str(i+1)

    data.to_csv(output_csv, index=False)
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate crossfolds')
    parser.add_argument('--data-csv', type=str, help='path to data file', default='example.csv')
    parser.add_argument('--category', type=str, help='column to stratify by', default='feature')
    parser.add_argument('--values', type=list , help='possible values within category to include for stratification', default=['A', 'B'])
    parser.add_argument('--n-folds', type=int, help='number of crossfolds to split data into', default=3)
    parser.add_argument('--target-column', type=str, help='name for target column to contain the assigned crossfolds for each patient in the output dataframe', default='CV3')
    parser.add_argument('--patient-column', type=str, help='column within dataframe indicating unique identifier for patient', default='patient')
    parser.add_argument('--site-column', type=str, help='column within dataframe indicating designated site for a patient', default='site')
    parser.add_argument('--timelimit', type=int, help='maximum time to spend solving', default=100)
    parser.add_argument('--randomseed', type=int, help='random seed for solver', default=0)
    parser.add_argument('--output-csv', type=str, help='path to output csv', default='crossfolds.csv') 

    args = parser.parse_args()

    generate(pd.read_csv(args.data_csv), args.category, args.values, args.n_folds, args.target_column, args.patient_column, args.site_column, args.timelimit, args.randomseed, args.output_csv)