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
#               EXECUTE ESSE ARQUIVO!                   #
#########################################################   

import man_data
import random
import os
import graphs

#########################################################
# Parte que faz a execução do algoritmo em si           #
#########################################################
main = man_data.Manipulador_de_Dados()
data_for_plot, data_for_shap = main.init_algo1()
print('Task 1: Criando gráficos ...')
graphs.create_shap(data_for_shap, 1)
graphs.create_roc(data_for_plot)
print('Task 1: Gráficos criados!')

data_for_plot, data_for_shap = main.init_algo2()
print('Task 2: Criando gráficos ...')
graphs.create_shap(data_for_shap, 2)
print('Task 2: Gráficos criados!')


# print("\nA melhor rota encontrada pelo algoritmo, partindo de BSB e visitando todas as cidades é: ")
# print(*rota, sep=' -> ')
# print("Com distância total igual a " + str(int(1/pontuacao)) + ' km\n')

# #########################################################
# # Parte que gera a análise de dados provenientes da     #
# # execução do algoritmo, que então são gerados gráficos #
# # e seus valores, bem como as imagens dos gráficos, são #
# # salvas nas pastas do projeto.                         #
# #########################################################
# import matplotlib.pyplot as plt
# randarq = random.randint(0, 10000)
# script_dir = os.path.dirname(__file__)
# a = man_data.a
# b = man_data.b
# rand_method = man_data.numrandom

# fig, ax = plt.subplots()
# ax.plot(b, a)

# ax.set(xlabel='Iterações', ylabel='Distância (Km)',
#        title='Caixeiro Viajante')
# ax.grid()
# fig.savefig(script_dir + '/img/' + str(rand_method) + '/' + str(randarq) + '.png')
# plt.show()

# valorkm = a.pop(len(a) - 1)
# with open(script_dir + '/txt/valores/' + str(rand_method) + '/' + str(randarq) + '.txt', 'w') as f:
#     f.write(str(valorkm))
# with open(script_dir + '/txt/rotas/' + str(rand_method) + '/' + str(randarq) + '_rota.txt', 'w') as f:
#     f.write(str(rota))