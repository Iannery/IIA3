#########################################################
#   Trabalho 3 - Introdução à Inteligência Artificial   #
#                                                       #
#   Integrantes:                                        #
#   André Carvalho Marques - 15/0005491                 #
#   Ian Nery Bandeira - 17/0144739                      #
#                                                       #
#   Python Versão 3.7.2                                 #
#   Executado em Windows 10                             #
#                                                       #
#########################################################   

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from category_encoders import OrdinalEncoder



class Manipulador_de_Dados():
    #########################################################
    # Inicializa as variáveis de contexto da classe, como   #
    # o dataset do xlsx provido, as variáveis de controle   #
    # da random forest, e chama o método que faz a          #
    # primeira filtragem dos dados.                         #
    #########################################################
    def __init__(self):
        self.data = pd.read_excel('dataset.xlsx')
        self.random_state = 25
        self.samples = 5
        self.estimators = 500
        self.sample_per_leaf = 10
        self.fillna_param = -6
        self.filter_data1()
    
    #########################################################
    # Inicia o algoritmo da task 1, que consiste em         #
    # construir uma random forest com parâmetro de          #
    # resultado y como o resultado do exame de covid, para  #
    # que seja possível prever novos casos a partir dos     #
    # dados. Retorna os dados para o gráfico da curva ROC e #
    # dos summary plots e dependency plots do SHAP.         # 
    #########################################################
    def init_algo1(self):
        self.task = 1 # seta flag para dizer qual task está sendo executada.
        self.random_forest('SARS-Cov-2 exam result')
        return self.data_for_plot, self.data_for_shap
    
    #########################################################
    # Filtra dos dados sensíveis para essa task, e inicia o #
    # algoritmo da task 2, que consiste em construir uma    #
    # random forest com parâmetro de resultado y como o     #
    # parâmetro de se a pessoa foi internada no hospital    #
    # de alguma forma. Retorna os dados para o summary plot #
    # e dependency plots do SHAP.                           # 
    #########################################################
    def init_algo2(self):
        self.task = 2 # seta flag para dizer qual task está sendo executada.
        # executa a segunda filtragem de dados, agora somente para a task 2
        self.filter_data2() 
        self.random_forest('Admitted')
        return self.data_for_shap
    
    #########################################################
    # Filtra dos dados sensíveis para ambas a task 1 e 2,   #
    # que são transformar o resultado dos exames de covid   #
    # em 0's e 1's, e fazer um dataset de exames que possui #
    # apenas os dados dos exames e do quantil de idade      #
    #########################################################
    def filter_data1(self):
        self.data['SARS-Cov-2 exam result'] = self.data['SARS-Cov-2 exam result'].map(dict(negative = 0, positive = 1))
        self.exams = self.data.drop(['Patient ID',
                                     'Patient age quantile',
                                     'SARS-Cov-2 exam result',
                                     'Patient addmited to regular ward (1=yes, 0=no)', 
                                     'Patient addmited to semi-intensive unit (1=yes, 0=no)', 
                                     'Patient addmited to intensive care unit (1=yes, 0=no)'], axis = 1)
    
    #########################################################
    # Filtra dos dados sensíveis para a task 2, que trata   #
    # da internação. Cria uma nova coluna no dataset        #
    # original, que possui o resultado de qual internação o #
    # paciente teve, entre 0, 1, 2 e 3; sendo que 0 não foi #
    # internado e 3 foi internado na UTI.                   #
    #########################################################
    def filter_data2(self):
        # Coloca peso 1 para pacientes internados na sala regular
        self.data['Patient addmited to regular ward (1=yes, 0=no)'] *= 1
        # Coloca peso 2 para pacientes internados na unidade semi intensiva de tratamento
        self.data['Patient addmited to semi-intensive unit (1=yes, 0=no)'] *= 2
        # Coloca peso 3 para pacientes internados na UTI
        self.data['Patient addmited to intensive care unit (1=yes, 0=no)'] *= 3
        # Cria a coluna com o resultado de 'mais severidade' entre os 3 para cada linha.
        self.data['Admitted'] = self.data[['Patient addmited to regular ward (1=yes, 0=no)', 
                                           'Patient addmited to semi-intensive unit (1=yes, 0=no)', 
                                           'Patient addmited to intensive care unit (1=yes, 0=no)']].max(axis = 1)
    
    #########################################################
    # Executa o algoritmo de estimativa de random forest    #
    # para um dos resultados necessários por uma das duas   #
    # tasks. Utiliza duas listas de indices para dividir o  #
    # dataset, o tr e o ts são o training set e o test set, #
    # enquanto o y é o resultado das linhas presentes no    #
    # tr e ts, porém no dataset original, para a coluna     #
    # do resultado. Cria o modelo de random forest com as   #
    # listas de treino e depois testa acuracia com as       #
    # listas de teste.                                      #
    #########################################################
    def random_forest(self, y_result):
        iterator = 0
        # Utiliza o KFold para criar as listas de indices para teste e treino,
        # para que seja feita a validação cruzada com 5 amostras.
        for tr, ts in KFold(n_splits=self.samples).split(self.exams):
            iterator += 1
            print("Task " + str(self.task) +": Rodando a random forest para sample", iterator, "de", self.samples, "...")
            # Recebe a coluna do resultado do dataset original, para as linhas do tr e ts 
            y_training = self.data.iloc[tr][y_result]
            y_test_set = self.data.iloc[ts][y_result]
            # Recebe o dataset de exames para as linhas do tr e ts
            exams_training = self.exams.iloc[tr]
            exams_test_set = self.exams.iloc[ts]
            exams_training, exams_test_set = self.encode_fill_NaN(exams_training, exams_test_set)
            rforest_model = RandomForestClassifier(
                                        criterion='gini',
                                        n_estimators=self.estimators,
                                        bootstrap=True,
                                        min_samples_leaf=self.sample_per_leaf)
            rforest_model.fit(exams_training, y_training)
            # Como para a task 1 o resultado está entre 0 e 1, e a task 2 está entre 0 e 3,
            # foi necessário utilizar duas funções de predição diferentes para analisar os dados
            # diferentemente.
            if(self.task == 2):
                # como utilizamos o accuracy score para a task 2, é necessário utilizar o predict().
                y_pred = rforest_model.predict(exams_test_set)
            else:
                # como criamos uma curva ROC, é necessário utilizar o predict_proba.
                y_pred = rforest_model.predict_proba(exams_test_set)
        if(self.task == 2):
            print('Task 2: O accuracy score foi de', accuracy_score(y_test_set, y_pred))
        # retorna os dados para a plotagem no arquivo graphs.py
        # para a curva ROC, é necessário o test set e a predição do resultado
        self.data_for_plot = [y_test_set, y_pred]
        # para o shap, é necessário passar o classifier de floresta e um dos datasets de treino.  
        self.data_for_shap = [rforest_model, exams_training]
    
    #########################################################
    # Gera o encoding dos training e test sets, para tratar #
    # as strings não tratadas anteriormente, e trocar os    #
    # np.NaN por parâmetros reconhecíveis pelo classifier e #
    # que não alterem a análise dos dados.                  #
    #########################################################
    def encode_fill_NaN(self, training, test_set):
        enc = OrdinalEncoder()
        training = enc.fit_transform(training).fillna(self.fillna_param)
        test_set = enc.transform(test_set).fillna(self.fillna_param)
        return training, test_set
        