# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 20:55:32 2021

@author: Bárbara Carnaúba

O objetivo deste programa é:
    1) encontrar todos os arquivos python da máquina local de quem executa o
    código
    2) Lista todos os arquivos python por data do arquivo
    3) Exportar dados para uma planilha excel
"""

### Bibliotecas

import glob # encontra nomes dos caminhos de acordo com um padrão
import os # uso de funcionalidades dependentes do sistema operacional
from datetime import datetime # manipulação de datas e tempo
import pandas as pd

### Buscando caminhos de todos os arquivos python na diretório Documents e em 
# 4 camadas de subpastas

path_name = 'C:/Users/User/Documents/'
file_list  = glob.glob(path_name + "/*/*.py") # /* significa camada de busca 

### Nomes dos arquivos sem caminho completo

file_name = []
for file in file_list:
    file_name.append(file.split('\\')[-1])
    
### Datas de ultima modifcação

datas_ultima_modificacao = []
for file in file_list:
    t_mod = os.path.getmtime(file)
    datas_ultima_modificacao.append(datetime.fromtimestamp(t_mod))

### Datas de criações dos arquivos python
    
datas_criacao = []
for file in file_list:
    t_cria = os.path.getctime(file)
    datas_criacao.append(datetime.fromtimestamp(t_cria))
    
### Duração da modificação nos arquivos
    
duracao_modificacao_files = [datas_ultima_modificacao[i] - 
                              datas_criacao[i] for i in range(len(file_list))]
# Observação: Alguns intervalos de datas estão negativos, o que não faz sentido,
# pois a data de modificação é obrigatoriamente maior ou igual à data de 
# criação. Provavelmente, esses arquivos são arquivos baixados e não criados
# nesta máquina.

### Ordenando todas as listas por data de criação

datas_criacao_ordenada = sorted(datas_criacao)
indices = [datas_criacao.index(x) for x in sorted(datas_criacao)]

file_name_ordenada = [file_name[y] for y in indices]
file_list_ordenada = [file_list[y] for y in indices]
datas_ultima_modificacao_ordenada = [datas_ultima_modificacao[y] for y in indices]
duracao_modificacao_files_ordenada = [duracao_modificacao_files[y] for y in indices]

### Exportando resultados para .xlsx

nomes_colunas = ['Nome do Arquivo', 'Data de Criação', 
                 'Data da Última Modificação', 'Duração Modificações','Caminho do Arquivo']

valores_colunas = list(zip(file_name_ordenada,
                           datas_criacao_ordenada,
                           datas_ultima_modificacao_ordenada,
                           duracao_modificacao_files_ordenada,
                           file_list_ordenada))

df = pd.DataFrame(valores_colunas, columns = nomes_colunas)

df.to_excel('Lista de Arquivos Python.xlsx', index = False)