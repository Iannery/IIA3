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

import dados

hash_distancia = {x:{} for x in dados.cidades_list}
#########################################################
# Função que mapeia a distância entre as cidades        #
# a partir da cidade de origem e destino, olhando pela  #
# lista de arestas.                                     #
#########################################################
def mapear_dist(cidade_a, cidade_b):
    for i in range(0, len(dados.matriz_eucl)):
        if dados.matriz_eucl[i][0] == cidade_a and dados.matriz_eucl[i][1] == cidade_b:
            return dados.matriz_eucl[i][2]


#########################################################
# Função que cria um hash de distâncias a partir de uma #
# cidade específica com suas respectivas distâncias a   #
# todas as outras cidades.                              #
#########################################################    
def formar_hash_distancia(): 
    for i in range(0,len(dados.cidades_list)-1):
        for j in range(i+1,len(dados.cidades_list) ):
            cidade_a = dados.cidades_list[i]
            cidade_b = dados.cidades_list[j]
            distancia = mapear_dist(cidade_a,cidade_b)
            hash_distancia[cidade_a][cidade_b] = distancia
    return hash_distancia