import math
import numpy as np
from scipy.stats import rankdata
import pandas as pd

#importa tabelas de referencia para os testes estatísticos e seu kit de conversões
import tabelas
import tabelastoolkit

b =  {"A": [0.797, 0.876, 0.888, 0.923, 0.942, 0.956],
      "B": [0.794, 0.772, 0.908, 0.982, 0.976, 0.913],
      "C": [0.838, 0.801, 0.853, 0.951, 0.883, 0.837],
      "D": [0.815, 0.801, 0.747, 0.857, 0.887, 0.902]}
b = pd.DataFrame(b)

tabela_postos = pd.DataFrame(dados.rank(method='max')).T

print(c)