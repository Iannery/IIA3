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
