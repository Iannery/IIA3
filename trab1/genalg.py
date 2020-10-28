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

import random
import utils
import dados
a = []
b = []
numrandom = random.randint(1, 2)


class Algoritmo_Genetico():
    #########################################################
    # Inicialização da classe que roda o algoritmo genético #
    # com:                                                  #
    # - População de 20 genes                               #
    # - 10 genes criados com crossover + mutação            #
    # - Início e fim em 'BSB'                               #
    # - 50% de chance de rodar um dos tipos de crossover    #
    #########################################################
    def __init__(self):
        self.crossover_points = numrandom
        print('\nIniciando algoritmo genético com crossover de', self.crossover_points, 'ponto(s)')
        self.hash_distancia = utils.formar_hash_distancia()
        self.tam_pop= 20
        self.total_evolucoes = 10
        self.inicio = 'BSB'
        self.cidades_list = dados.cidades_list
        self.cidades_list.remove(self.inicio)
        self.genes = [] 
        self.gerar_genes()
    
    #########################################################
    # Unica função chamada pela inicialização da classe,    #
    # para gerar a lista de genes que será utilizada pelos  #
    # outros métodos da classe posteriormente. Gera uma     #
    # lista de genes a partir da lista de cidades importada #
    # como chaves do hash de distâncias.                    #
    #########################################################    
    def gerar_genes(self):
        for i in range(self.tam_pop):
            gene = [self.inicio]
            options = [k for k in self.cidades_list]
            while len(gene) < len(self.cidades_list)+1:
                cidade = random.choice(options)
                loc = options.index(cidade)                
                gene.append(cidade)
                del options[loc]
            gene.append(self.inicio)
            self.genes.append(gene)
        return self.genes
    
    #########################################################
    # Função que recebe a lista cujo primeiro índice é o    #
    # elemento de pontuação máxima da lista de fitness,     #
    # junto com o melhor caminho que gerou esse elemento de #
    # pontuação máxima.                                     #
    #########################################################
    def convergir_genes(self):
        flag_recebido = False
        for i in range(1000): #Numero de iterações
            valor_poda = self.podar_genes()
            pts_atual = valor_poda[0]
            melhor_gene_atual = valor_poda[1]
            a.append(int(1/pts_atual))
            b.append(int(i))
        # print(str(int(1/pts_atual)) + ' km')
        return melhor_gene_atual, pts_atual
    
    #############################################################
    # Função que utiliza a lista de 30 genes, dos quais 20      #
    # são da geração atual e 10 são gerados pela função de      #
    # evolução; deleta os 10 genes com menor pontuação de       #
    # fitness e retorna o gene com pontuação máxima da lista.   #
    #############################################################            
    def podar_genes(self):       
        for i in range(self.total_evolucoes):
            self.evoluir_genes()
        pts_fitness = self.avaliar_fitness()
        for i in range(self.total_evolucoes):
            pior_gene = pts_fitness.index(min(pts_fitness))
            del self.genes[pior_gene]
            del pts_fitness[pior_gene]
        return max(pts_fitness),self.genes[pts_fitness.index(max(pts_fitness))]

    #############################################################
    # Função que utiliza a lista de 20 genes, uma lista de      #
    # índices baseado nas cidades, e executa tanto o crossover  #
    # quanto a mutação no novo gene, e o insere na lista de     #
    # genes. Como a função é executada 10 vezes, 10 genes são   #
    # adicionados na lista de genes, resultando 30 genes que    #
    # seguirão para avaliação e poda para a escolha da geração  #
    # seguinte.                                                 #
    ############################################################# 
    def evoluir_genes(self):
        indice_map = {i:'' for i in range(0,len(self.cidades_list))}
        n_visitadas = [x for x in self.cidades_list]
        for i in range(self.crossover_points - 1):
            indices = [i for i in range(0,len(self.cidades_list))]
            n_visitadas = [x for x in self.cidades_list]
            for j in range(len(self.genes)-1):
                gene = self.genes[i]
                try:
                    indice_gene = random.choice(indices)
                    aux_gene = gene[indice_gene]
                    if aux_gene in n_visitadas:
                        indice_map[indice_gene] = aux_gene
                        loc = indices.index(indice_gene)
                        del indices[loc]
                        loc = n_visitadas.index(aux_gene)
                        del n_visitadas[loc]
                    else:
                        continue
                except:
                    # print('ERRO NO CROSSOVER')
                    pass
                      
        ultimo_gene = self.genes[-1]
        cidades_restantes = [x for x in ultimo_gene if x in n_visitadas]
        for k,v in indice_map.items():
            if v != '':
                continue
            else:
                cidade = cidades_restantes.pop(0)
                indice_map[k] = cidade
        novo_gene = [indice_map[i] for i in range(0,len(self.cidades_list))]
        novo_gene.insert(0,self.inicio)
        novo_gene.append(self.inicio)
        try:
            rand_gene = [x for x in novo_gene if x != self.inicio]
            cidade_a = random.choice(rand_gene)
            cidade_b = random.choice(rand_gene)
            indice_a = novo_gene.index(cidade_a)
            indice_b = novo_gene.index(cidade_b)
            novo_gene[indice_a] = cidade_b
            novo_gene[indice_b] = cidade_a
            self.genes.append(novo_gene)
        except:
            # print('ERRO NA MUTAÇÃO')
            pass
    
    #########################################################
    # Função que utiliza a lista de 30 genes, dos quais 20  #
    # são da geração atual e 10 são gerados pela função de  #
    # evolução; e retorna uma lista utilizando os mesmos    #
    # índices da lista de genes, para avaliar o fitness     #
    # a partir da soma das distâncias entre as cidades      #
    # de um gene.                                           #
    #########################################################
    def avaliar_fitness(self):
        pts_fitness = []
        for gene in self.genes:
            distancia_total = 0
            for i in range(1,len(gene)):
                cidade_b = gene[i]
                cidade_a = gene[i-1]
                # como o hash de distancias só possui as distancias do triangulo superior
                # da matriz euclideana, é necessário testar se existe a distância com
                # ambas as cidades em origem e destino. 
                try: 
                    distancia = self.hash_distancia[cidade_a][cidade_b]
                except:
                    distancia = self.hash_distancia[cidade_b][cidade_a]
                distancia_total += distancia
            fitness = 1/distancia_total
            pts_fitness.append(fitness)
        return pts_fitness
