#########################################################
#   Trabalho 1 - Introdução à Inteligência Artificial   #
#                                                       #
#   Integrantes:                                        #
#   André Carvalho Marques - 15/0005491                 #
#   Ian Nery Bandeira - 17/0144739                      #
#                                                       #
#   Python Versão 3.7.2                                 #
#   Executado em Windows 10                             #
#                                                       #
#########################################################   

import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree, DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report, roc_auc_score
from category_encoders import OrdinalEncoder


class Manipulador_de_Dados():
    def __init__(self):
        self.data = pd.read_excel('dataset.xlsx')
    def init_algo(self):
        self.filter_data()
        self.random_forest()
    def filter_data(self):
        self.data['SARS-Cov-2 exam result'] = self.data['SARS-Cov-2 exam result'].map(dict(negative=0, positive=1))
        self.data['Urine - pH'] = self.data['Urine - pH'].map(lambda x: -100 if isinstance(x, str) else x).astype(float)
        self.data['Urine - Leukocytes'] = self.data['Urine - Leukocytes'].map(lambda x: 500 if x == '<1000' else x).astype(float)
        self.exams = self.data.drop('Patient ID', 
                               'Patient age quantile', 
                               'SARS-Cov-2 exam result', 
                               'Patient addmited to regular ward (1=yes, 0=no)', 
                               'Patient addmited to semi-intensive unit (1=yes, 0=no)', 
                               'Patient addmited to intensive care unit (1=yes, 0=no)')
        self.exams['Patient age quantile'] = self.data['Patient age quantile']
    def random_forest(self):        
        kf = KFold(2, shuffle=True, random_state=0)
    
        for tr, ts in kf.split(self.exams):
            exams_training = self.exams.iloc[tr]
            exams_test_set = self.exams.iloc[ts]
            y_training = self.data.iloc[tr]['SARS-Cov-2 exam result']
            y_test_set = self.data.iloc[ts]['SARS-Cov-2 exam result']
            
            exams_training, exams_test_set = self.encode_fill_NaN(exams_training, exams_test_set)

            rforest_model = RandomForestClassifier(random_state=0,
                                        criterion='gini',
                                        n_estimators=500,
                                        bootstrap=True,
                                        min_samples_leaf=10)
            rforest_model.fit(exams_training, y_training)
            
            p = rforest_model.predict_proba(exams_test_set)[:,1]
            
            print("AUC= ", roc_auc_score(y_test_set,p))
    def encode_fill_NaN(self, training, test_set):
        enc = OrdinalEncoder()
        training = enc.fit_transform(training).fillna(-10)
        test_set = enc.transform(test_set).fillna(-10)
        return training, test_set
        