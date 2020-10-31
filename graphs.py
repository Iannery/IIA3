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
import os
import shap
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree, DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report, roc_auc_score
from category_encoders import *

import scikitplot as skplt
import matplotlib.pyplot as plt


script_dir = os.path.dirname(__file__)
def create_roc(data):
    skplt.metrics.plot_roc(data[0], data[1])
    plt.savefig(script_dir + '/task1/roc_curve.png')
    plt.close()   
    
def create_shap(data, task):
    plt.clf()
    explainer = shap.TreeExplainer(data[0])
    shap_values = explainer.shap_values(data[1], approximate=True)
    if(task == 1):
        shap.summary_plot(shap_values[1],
                          data[1],
                          show=False,
                          max_display=10)
        plt.savefig(script_dir + '/task1/shap_graph.png', bbox_inches='tight')
        plt.close()   
        create_dependence_plot(data, shap_values, task,'Leukocytes')
        create_dependence_plot(data, shap_values, task,'Platelets')
        create_dependence_plot(data, shap_values, task,'Monocytes')
    elif(task == 2):        
        shap.summary_plot(shap_values[-1],
                          data[1],
                          show=False,
                          max_display=5)
        plt.savefig(script_dir + '/task2/shap_graph.png', bbox_inches='tight')
        plt.close()
        create_dependence_plot(data, shap_values, task,'Patient age quantile')
        create_dependence_plot(data, shap_values, task,'Proteina C reativa mg/dL')
        create_dependence_plot(data, shap_values, task,'Neutrophils')
    
def create_dependence_plot(data, shap_values,task,name):
    plt.clf()
    
    shap.dependence_plot(name,
                         shap_values[1],
                         data[1], 
                         show=False,
                         interaction_index=None)
    if(name != 'Proteina C reativa mg/dL'):
        plt.savefig(script_dir + '/task'+str(task)+'/' + name + '.png', bbox_inches='tight')
    else:
        plt.savefig(script_dir + '/task'+str(task)+'/Proteina C reativa.png', bbox_inches='tight')
    plt.close()
    
