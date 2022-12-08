import math
import numpy as np
from scipy.stats import rankdata
import pandas as pd

#importa tabelas de referencia para os testes estatísticos e seu kit de conversões
import tabelas
import tabelastoolkit


def t_cochran(dados, alfa=0.05, uni_bi=1, somaquadrados=0):
    """
    :param dados: lista contendo listas com os valores dos grupos.
    :param alfa: nivel de signficancia adotado
    :param uni_bi: teste unilateral (1) ou bilateral (2), por padrão 2.
    :return: o valor z calculado, alpha e a hipotese favorecida.
    :eg. Num estudo sobre modo de entrevista 3 grupos de 18 pessoas foram expostas a 3 tipos de entrevistas, polida, neutra
    e truculenta respondendo positivamente ou negativamente. Esses dados estão na lista 'a' e para realizar esse teste com
    0.001 de significancia a chamada para esse teste é t_cochran(a, 0.05).
    Nesse caso a  função retornará (16.6667, 5.99, 0.001, 'h1'), ou seja, o valor Q calculado, o valor z tabelado,  alpha
    e a hipótese favorecida.

    :Erro de soma dos quadrados: Você parece ter informado a soma dos grupos e não a tabela de dados, como é
    necessário tanto obter a soma dos grupos quanto a soma dos quadrados das linhas não é possivel realizar os calculos
    assim. Para informar a soma dos quadrados use o argumento 'somaquadrados = n', onde n é a soma dos quadrados.
    """
    l = pd.DataFrame(dados)
    if l.shape[1] == 1:
        return print('Erro na soma dos quadrados, consulte a ajuda.')
    k = l.shape[1]

    grupos = pd.DataFrame(l.sum(axis=0))
    somaquadgrupos = (grupos ** 2).sum()
    somagrupos = l.sum(axis=1)
    somaquadrados = somagrupos ** 2

    somagrupos = sum(somagrupos)
    somaquadrados = sum(somaquadrados)

    Q = (((k-1)*(( k * somaquadgrupos)-(somagrupos ** 2))) / ((k * somagrupos) - somaquadrados)).round(4)[0]
    gl = k -1
    alf = tabelastoolkit.alfaconvert(alfa, 'c' )
    z = float(tabelas.C[gl][alf])
    if Q >= z:
        return (Q, z, alfa, 'H1')
    else:
        return (Q, z, alfa, 'H0')


def t_anova_friedman_postos():
    pass


def t_page_alt_ord(dados, alfa = 0.05, uni_bi=2):
    """
    :param dados: pode receber um dicionário no formato {'condição A':[lista de valores],'condição B':[lista de valores]...}
     ou uma tabela pandas de valores organizados em i linhas de experimentações e j colunas de condições.
    :param alfa: nivel de signficancia adotado
    :param uni_bi: teste unilateral (1) ou bilateral (2), por padrão 2.
    :return: o valor F calculado, o valor z de corte,  alfa e a hipotese favorecida.
    :eg.
    :erro de formato da tabela: A tabela deve estar no formato informado acima no campo param:dados como tabela pandas ou
    dicionário, além disso o numero de dados em cada grupo deve ser o mesmo.
    """
    if str(type(dados)) == "<class 'dict'>":
        print('é dicio')
        dados = pd.DataFrame(dados).T
    elif str(type(dados)) == "<class 'pandas.core.frame.DataFrame'>":
        print('é panda')
    else:
        print('Erro de formato da tabela, consulte a ajuda.')



a = [[0,0,0],
    [1,1,0],
    [0,1,0],
    [0,0,0],
    [1,0,0],
    [1,1,0],
    [1,1,0],
    [0,1,0],
    [1,0,0],
    [0,0,0],
    [1,1,1],
    [1,1,1],
    [1,1,0],
    [1,1,0],
    [1,1,0],
    [1,1,1],
    [1,1,0],
    [1,1,0]]

b =  {"A": [0.797, 0.876, 0.888, 0.923, 0.942, 0.956],
      "B": [0.794, 0.772, 0.908, 0.982, 0.976, 0.913],
      "C": [0.838, 0.801, 0.853, 0.951, 0.883, 0.837],
      "D": [0.815, 0.801, 0.747, 0.857, 0.887, 0.902]}
b = pd.DataFrame(b).T

#print(t_cochran(a))
print(t_page_alt_ord(b))