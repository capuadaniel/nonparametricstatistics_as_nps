import math
import numpy as np
from scipy.stats import rankdata

#importa tabelas de referencia para os testes estatísticos e seu kit de conversões
import tabelas
import tabelastoolkit

def t_mudancaMcNemar(ab, ba, alfa=0.05):
    '''
    Para usar o teste de mudança de McNemar deve-se separar os dados em variaveis de 3 tipos, as que tiveram alteração
    de a para b as que se alteraram no sentido inverso e as que não tiveram alteração.
    :param ab: numero de mudanças na direção a para b
    :param ba: numero de mudanças na direção b para a
    :param alfa: valor de significancia adotado, 0.05 por padrão
    :return: o valor z calculado, sua referencia na tabela e a hipotese favorecida.
    '''
    N = ab + ba
    alf = tabelastoolkit.alfaconvert(alfa, 'C')
    c = tabelas.C[1][alf]
    z = (abs(ab - ba) - 1) **2 /(ab+ba)
    if N/2 <= 5:
        return f'O valor de N {N}/2, ou seja, valor esperado da frenquencia, é muito baixo, considere usar o teste binomial'

    if z < c:
        return f'O valor z = {z} é menor do que o valor crítico {c}, para alfa = {alfa}. Favorecendo H0.'
    else:
        return f'O valor z = {z} é maior ou igual ao valor crítico {c}, para alfa = {alfa}. Favorecendo H1'

def t_sinal(mais,menos, alfa=0.05, uni_bi=2):
    '''
    O teste do sinal recebe valores + e - associados a duplas relacionadas como 'antes e depois' muitas vezes convertendo
    valores de investigação numa variavel mais simples +, - e 0 para empates quando esse resumo não poder informação
    relevante (caso a magnitude das diferenças seja importante recomenda-se o teste t_postocomsinal() ).
    :param mais: n de sinais +
    :param menos: n de sinais -
    :param alfa: valor de significancia adotado, 0.05 por padrão
    :param uni_bi: teste unilateral ou bilateral, por padrão 2, bilateral.
    :return: o valor z calculado, sua referencia na tabela e a hipotese favorecida.
    exemplo: investigando a tomada de decisão por casais se o casal concordava em ambos terem poder de decisão na compra de uma
    casa era registrado o valor 0, enquanto quando a discordancia ia no sentido de que o marido deveria tomar a decisão era anotado
    o valor - para o casal e quando a tendencia era para a esposa o valor +. Nesse caso tivemos 14 casais discordantes, 3 + e 11 -.
    t_sinal(3,11) como 14 < 35 usamos a função para pequenas amostras indo direto para a tabela D onde um valor critico de 0.029 nos
    mostra que sendo menor que 0.05 (nosso alfa e região de rejeição) devemos rejeitar H0 em favor de H1. Há tendencia entre casais
    de deixar essa decisão analisada mais nas mãos do marido.
    Num estudo com N maior as mudanças foram calculadas t_sinal(26,59), resultando em 0.006 como valor critico dentro do estipulado
    de 0.05, rejeitando H0 em favor de H1.
    '''
    N = mais + menos
    menor = min(mais, menos)
    uni_bi_valor = 'bilateral'
    if uni_bi == 1: uni_bi_valor = 'unilateral'

    if N < 35:
        z = float(tabelas.D[N][menor])/1000

        if z < alfa:
            return f'O valor z = {z} é menor do que o valor crítico alfa = {alfa}. Favorecendo H0.'
        else:
            return f'O valor z = {z} é maior ou igual ao valor crítico alfa = {alfa}. Favorecendo H1'
    else:
        h = 1
        if N/2 < menor:
            h = -1
        z = abs((2 * menor + h - N) / math.sqrt(N))
        c = tabelastoolkit.alfaconvert(z, 'a') * uni_bi

        if c <= alfa:
            return f'O valor crítico {c} ({uni_bi_valor}) é menor ou igual que o valor de significancia escolhido alfa = {alfa}. Favorecendo H0.'
        else:
            return f'O valor crítico {c} ({uni_bi_valor}) é maior que o valor de significancia escolhido alfa = {alfa}. Favorecendo H1.'

def t_sinalcomposto(listaA, listaB, alfa = 0.05, uni_bi = 2):
    '''
    O tesde de sinal com posto testa a diferença entra as listas A e B relacionadas. Se o pesquisador tiver as diferenças
    em mãos pode informar elas na lista A e preencher a lista B com zeros.
    :param listaA: Observações na condição A para a dupla de observações relacionadas
    :param listaB: Observações na condição B para a dupla de observações relacionadas
    :param alfa: valor de significancia adotado, 0.05 por padrão
    :param uni_bi: teste unilateral ou bilateral, por padrão 2, bilateral.
    :return: o valor z calculado, sua referencia na tabela e a hipotese favorecida.
    exemplo: Investigando





    '''
    N = len(listaA)
    if len(listaB) != N:
        return "As listas A e B não possuem o mesmo comprimento"
    listaA = np.array(listaA)
    listaB = np.array(listaB)
    d = listaB - listaA
    lista = rankdata(abs(d), method='ordinal')
    lista_sinal = []
    for elemento in d:
        if elemento >= 0 :
            lista_sinal.append('+')
        else:
            lista_sinal.append('-')
    lista_sinal = np.array(lista_sinal)
    for k,v in enumerate(lista):
        if lista_sinal[k] == '-':
            lista[k] = -v

    T_positivos = T_negativos = 0
    for elemento in lista:
        if elemento >= 0:
            T_positivos += elemento
        else:
            T_negativos += elemento

    if N <= 15: #talvez trocar por um try
        #pequenas amostras consultam N e T_positivos na tabela H
        z = tabelas.H[T_positivos][N] * uni_bi
    else:
        #grandes amostras calculam z
        z = (T_positivos - (N*(N+1)/4)) / math.sqrt(N*(N+1)*((2*N)+1)/24)

    if z <= alfa:
        return f'O valor crítico {z} é menor ou igual que o valor de significancia escolhido alfa = {alfa}. Favorecendo H1.'
    else:
        return f'O valor crítico {z} é maior que o valor de significancia escolhido alfa = {alfa}. Favorecendo H1.'


#dados para testes
a = (20.3,17,6.5,25,5.4,29.2,2.9,6.6,15.8,8.3,34,8)
b = (50.4,87,25.1,28.5,26.9,36.6,1,43.8,44.2,10.4,29.9,27.7)
c = ( 0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0, 0,0,0,0,0,0, 0, 0,0,0,0,0,0, 0)
d = (-2,0,0,1,0,0,4,4,1,1,5,3,5,3,-1,1,-1,5,8,2,2,2,-3,-2,1,4,8,2,3,-1)

#print(t_mudancaMcNemar(13,7), '/// esperado z=1.25, critico=3.84. H0')
#print(t_sinal(11,3), '/// esperado z=0.29, critico=alfa. H0') #pequenas amostras
#print(t_sinal(26,59), '/// esperado z=0.0006 < alfa 0.01 H0') #grandes amostras
print(t_sinalcomposto(a, b), '/// z = 0.048 ') #pequenas amostras
#print(t_sinalcomposto(c,d), '/// z = 3.11') #grandes amostras