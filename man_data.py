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
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree, DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import *
from category_encoders import *
from sklearn.impute import SimpleImputer

import scikitplot as skplt
import matplotlib.pyplot as plt


class Manipulador_de_Dados():
    def __init__(self):
        self.data = pd.read_excel('dataset.xlsx')
        self.random_state = 25
        self.samples = 5
        self.estimators = 500
        self.sample_per_leaf = 10
        self.filter_data1()
        
    def init_algo1(self):
        self.random_forest('SARS-Cov-2 exam result')
        return self.data_for_plot, self.data_for_shap
    
    def init_algo2(self):
        self.filter_data2()
        self.random_forest('Admitted')
        return self.data_for_plot, self.data_for_shap
    
    def filter_data1(self):
        self.data['SARS-Cov-2 exam result'] = self.data['SARS-Cov-2 exam result'].map(dict(negative=0, positive=1))
        self.data['Urine - pH'] = self.data['Urine - pH'].map(lambda x: -100 if isinstance(x, str) else x).astype(float)
        self.data['Urine - Leukocytes'] = self.data['Urine - Leukocytes'].map(lambda x: 500 if x == '<1000' else x).astype(float)
        self.exams = self.data.drop(['Patient ID', 
                               'SARS-Cov-2 exam result',
                               'Patient addmited to regular ward (1=yes, 0=no)', 
                               'Patient addmited to semi-intensive unit (1=yes, 0=no)', 
                               'Patient addmited to intensive care unit (1=yes, 0=no)'], axis = 1)
        teste = self.exams.drop('Patient age quantile', axis = 1)
        self.full_nan = teste.isnull().mean(axis=1) == 1
    
    def filter_data2(self):
        self.data['Patient addmited to regular ward (1=yes, 0=no)'] *= 1
        self.data['Patient addmited to semi-intensive unit (1=yes, 0=no)'] *= 2
        self.data['Patient addmited to intensive care unit (1=yes, 0=no)'] *= 3
        self.data['Admitted'] = self.data[['Patient addmited to regular ward (1=yes, 0=no)', 
                                            'Patient addmited to semi-intensive unit (1=yes, 0=no)', 
                                            'Patient addmited to intensive care unit (1=yes, 0=no)']].max(axis=1)
    def random_forest(self, y_result):
        iterator = 0
        if(y_result == 'Admitted'):
            task = '2'
        else:
            task = '1'
        for tr, ts in KFold(n_splits=self.samples).split(self.exams):
            iterator += 1
            print("Task " + task +": Rodando a random forest para sample", iterator, "de", self.samples, "...")
            y_training = self.data.iloc[tr][y_result]
            y_test_set = self.data.iloc[ts][y_result]
            exams_training = self.exams.iloc[tr]
            exams_test_set = self.exams.iloc[ts]
            
            exams_training, exams_test_set = self.encode_fill_NaN(exams_training, exams_test_set)

            rforest_model = RandomForestClassifier(
                                        criterion='gini',
                                        n_estimators=self.estimators,
                                        bootstrap=True,
                                        min_samples_leaf=self.sample_per_leaf)
            rforest_model.fit(exams_training, y_training)
            
            if(y_result == 'Admitted'):
                y_pred = rforest_model.predict(exams_test_set)
            else:
                y_pred = rforest_model.predict_proba(exams_test_set)
        if(y_result == 'Admitted'):
            print('O accuracy score da task 2 foi de', accuracy_score(y_test_set, y_pred))
        self.data_for_plot = [y_test_set, y_pred]
        self.data_for_shap = [rforest_model, exams_training]

    def encode_fill_NaN(self, training, test_set):
        enc = OrdinalEncoder()
        training = enc.fit_transform(training).fillna(-6)
        test_set = enc.transform(test_set).fillna(-6)
        return training, test_set
        