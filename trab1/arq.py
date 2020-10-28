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

import matplotlib.pyplot as plt
import random
import os
from numpy.core import sort

#########################################################
# Função utilizada para determinar elementos únicos     #
# de uma lista.                                         #
#########################################################
def unique(list1): 
      
    list_set = set(list1) 
    unique_list = (list(list_set)) 
    return unique_list

#########################################################
# O código abaixo recebe em uma lista todos os valores  #
# presentes nos resultados das execuções do algoritmo,  #
# salvos em arquivo, para criar uma lista de quantas    #
# vezes tal resultado ocorreu nas inúmeras execuções do #
# algoritmo.                                            #
#########################################################
script_dir = os.path.dirname(__file__)
lista_valores_1 = []
lista_valores_2 = []
lista_ocorrencias_1 = []
lista_ocorrencias_2 = []
for i in range(10000):
    if os.path.exists(script_dir + '/txt/valores/1/'+ str(i) + '.txt'):
        with open(script_dir + '/txt/valores/1/'+ str(i) + '.txt', 'r') as f:
            lista_valores_1.append(int(f.read()))

for x in sort(unique(lista_valores_1)):
    lista_ocorrencias_1.append(lista_valores_1.count(x))
for i in range(10000):
    if os.path.exists(script_dir + '/txt/valores/2/'+ str(i) + '.txt'):
        with open(script_dir + '/txt/valores/2/'+ str(i) + '.txt', 'r') as f:
            lista_valores_2.append(int(f.read()))
for x in sort(unique(lista_valores_2)):
    lista_ocorrencias_2.append(lista_valores_2.count(x))

#########################################################
# A parte de código abaixo cria o histograma utilizado  #
# no relatório do trabalho.                             #
######################################################### 
x1 = lista_valores_1
x2 = lista_valores_2
y = lista_ocorrencias_2

fig, axs = plt.subplots(1, 2)
axs[0].set(xlabel='Distância(Km)', ylabel='Ocorrências',
       title='Crossover de um ponto')
axs[1].set(xlabel='Distância(Km)', ylabel='Ocorrências',
       title='Crossover de dois pontos')
axs[0].hist(x1, bins=20)
axs[1].hist(x2, bins=20)
plt.show()