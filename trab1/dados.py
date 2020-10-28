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

#########################################################
# Essa lista foi criada a partir da matriz euclideana   #
# dada no roteiro do trabalho. Ela serve para mostrar   #
# todas as arestas de distância com origem e destino.   #
#########################################################
matriz_eucl = [
    ('BSB', 'SP', 9),
    ('BSB','BA',23),
    ('BSB','RJ',9),
    ('BSB','Lima',32),
    ('BSB','Bog',37),
    ('BSB','Sant',30),
    ('BSB','Carac',35),
    ('BSB','BH',6),
    ('BSB','PoA',16),
    ('PoA','SP',8),
    ('PoA','BA',8),
    ('PoA','RJ',11),
    ('PoA','Lima',33),
    ('PoA','Bog',46),
    ('PoA','Sant',19),
    ('PoA','Carac',48),
    ('PoA','BH',13),
    ('BH','SP',5),
    ('BH','BA',22),
    ('BH','RJ',3),
    ('BH','Lima',36),
    ('BH','Bog',43),
    ('BH','Sant',30),
    ('BH','Carac',42),
    ('Carac','SP',44),
    ('Carac','BA',51),
    ('Carac','RJ',45),
    ('Carac','Lima',27),
    ('Carac','Bog',10),
    ('Carac','Sant',49),
    ('Sant','SP',26),
    ('Sant','BA',11),
    ('Sant','RJ',29),
    ('Sant','Lima',25),
    ('Sant','Bog',43),
    ('Bog','SP',43),
    ('Bog','BA',47),
    ('Bog','RJ',45),
    ('Bog','Lima',19),
    ('Lima','SP',35),
    ('Lima','BA',31),
    ('Lima','RJ',38),
    ('RJ','SP',3),
    ('RJ','BA',20),
    ('BA','SP',17),
    ]

#########################################################
# Essa lista foi criada para termos todas as cidades    #
# presentes na matriz euclideana                        #
#########################################################
cidades_list = ['BSB','PoA','BH','Carac','Sant','Bog','Lima','RJ','BA','SP']