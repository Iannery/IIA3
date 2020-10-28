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
#               EXECUTE ESSE ARQUIVO!                   #
#########################################################   

import genalg
import random
import os

#########################################################
# Parte que faz a execução do algoritmo em si           #
#########################################################
main = genalg.Algoritmo_Genetico()
rota, pontuacao = main.convergir_genes()

print("\nA melhor rota encontrada pelo algoritmo, partindo de BSB e visitando todas as cidades é: ")
print(*rota, sep=' -> ')
print("Com distância total igual a " + str(int(1/pontuacao)) + ' km\n')

#########################################################
# Parte que gera a análise de dados provenientes da     #
# execução do algoritmo, que então são gerados gráficos #
# e seus valores, bem como as imagens dos gráficos, são #
# salvas nas pastas do projeto.                         #
#########################################################
import matplotlib.pyplot as plt
randarq = random.randint(0, 10000)
script_dir = os.path.dirname(__file__)
a = genalg.a
b = genalg.b
rand_method = genalg.numrandom

fig, ax = plt.subplots()
ax.plot(b, a)

ax.set(xlabel='Iterações', ylabel='Distância (Km)',
       title='Caixeiro Viajante')
ax.grid()
fig.savefig(script_dir + '/img/' + str(rand_method) + '/' + str(randarq) + '.png')
plt.show()

valorkm = a.pop(len(a) - 1)
with open(script_dir + '/txt/valores/' + str(rand_method) + '/' + str(randarq) + '.txt', 'w') as f:
    f.write(str(valorkm))
with open(script_dir + '/txt/rotas/' + str(rand_method) + '/' + str(randarq) + '_rota.txt', 'w') as f:
    f.write(str(rota))