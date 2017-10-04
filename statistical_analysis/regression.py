import sys

import numpy as np
import pandas as pd
import math
from sklearn import linear_model
from sklearn.model_selection import LeaveOneOut
from sklearn import metrics

import matplotlib.pyplot as plt
import matplotlib.markers as ma

import dirs

def in_sample_fit(cols=['max_CRSI']):

    def SimpleLinearRegression_estimate(Covariates_train, Covariates_test, Dependent_train, Dependent_test):
        names_covariates = Covariates_train.columns.values
        lr = linear_model.LinearRegression(fit_intercept=True)
        lr.fit(Covariates_train, Dependent_train)
        intercept =  lr.intercept_
        coefficients = pd.DataFrame(np.hstack((names_covariates.reshape(len(names_covariates),1),lr.coef_.reshape(len(names_covariates),1))), columns=['covariates','coefficients'])
        MSE = np.mean((lr.predict(Covariates_test) - Dependent_test)**2)
        MAE = np.mean(abs(lr.predict(Covariates_test)-Dependent_test))
        R_squared = lr.score(Covariates_test, Dependent_test)
        return {'intercept':intercept, 'coefficients': coefficients, 'MSE': MSE, 'MAE': MAE,'R_squared': R_squared}

    data = pd.read_csv(dirs.regression_data, index_col=0)
    X_all = data[cols]
    salinity = data['salinity'].values.reshape((len(data['salinity']),1))
    results = SimpleLinearRegression_estimate(Covariates_train=X_all,Covariates_test=X_all,Dependent_train=salinity,Dependent_test=salinity)
    print(results)

    return results

def Leave_One_Out(cov_cols=['Field_ID', 'max_CRSI'], sal_cols = ['salinity', 'Field_ID']):

    def LOO_Regressions(Covariates, Salinity):
        lr = linear_model.LinearRegression(fit_intercept=True)
        loo = LeaveOneOut()
        field_indices = range(1, 23)
        predictions = pd.DataFrame(index = Covariates.index, columns = ['prediction', 'observation', 'residuals'])

        import ipdb; ipdb.set_trace()
        for train, test in loo.split(field_indices):
            covariates_train = Covariates[Covariates['Field_ID'].isin((train+1))].drop('Field_ID', axis=1)
            salinity_train = Salinity[Salinity['Field_ID'].isin((train+1))].drop('Field_ID', axis=1)
            covariates_test = Covariates[Covariates['Field_ID'] == test[0]+1].drop('Field_ID', axis=1)
            salinity_test = Salinity[Salinity['Field_ID'] == test[0]+1].drop('Field_ID', axis=1)
            
            lr.fit(covariates_train, salinity_train)
            prediction = pd.Series(lr.predict(covariates_test).flatten(), index=covariates_test.index)
            residuals = pd.Series(prediction-salinity_test['salinity'], index=covariates_test.index)
            dict_temp = pd.DataFrame.from_dict({'prediction': prediction, 'observation': salinity_test['salinity'], 'residuals': residuals})
            predictions.loc[salinity_test.index,:] = dict_temp

        R_squared = metrics.r2_score(predictions['observation'], predictions['prediction'])
        print(R_squared)

    data = pd.read_csv(dirs.regression_data, index_col=0)
    Covariates = data[cov_cols]
    Salinity = data[sal_cols]
    LOO_Regressions(Covariates=Covariates, Salinity=Salinity)

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print "Please include an argument."
        print "Current acceptable arguments are in_sample or leave_one_out"
        print "Example: python regression.py in_sample"
        sys.exit()

    command = sys.argv[1]

    if command == "in_sample": 
        in_sample_fit()
    if command == "leave_one_out": 
        Leave_One_Out()
