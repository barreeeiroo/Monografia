#!/usr/bin/python3
# -*- coding: utf-8 -*-


##############################################################################################
#                                         RECOMENDADO                                        #
#                  Se recomienda leer la siguiente iPython notebook, ya que                  #
#                     contiene el mismo código pero mucho más comentado.                     #
#      https://github.com/barreeeiroo/Monografia/blob/master/clustering/Clustering.ipynb     #
##############################################################################################



# Se hacen todos los imports
import os
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn import datasets


# Carga de datos del CSV
wdir = os.path.dirname(__file__)
leb_oro = pd.read_csv(wdir+'/../scrapper/clustering/out.csv')


# Selección de las columnas útils (todas menos las de datos no estadísticos por defecto)
data = leb_oro[['GP', 'MPG', 'FGM', 'FGA', 'FG%', '3PM', '3PA',
       '3P%', 'FTM', 'FTA', 'FT%', 'TOV', 'PF', 'ORB', 'DRB', 'RPG', 'APG',
       'SPG', 'BPG', 'PPG', 'TS%', 'eFG%', 'Total S %', 'ORB%', 'DRB%', 'TRB%',
       'AST%', 'TOV%', 'STL%', 'BLK%', 'USG%', 'PPR', 'PPS', 'ORtg', 'DRtg',
       'eDiff', 'FIC', 'PER', 'POS']]



# Normalización de los datos
data_norm = (data-data.min())/(data.max()-data.min())
data_norm.head()


# CLUSTERING JERÁRQUICO
clus = AgglomerativeClustering(n_clusters=5, linkage="ward").fit(data_norm)

# Obtención de los valores predecidos
md = pd.Series(clus.labels_)


# CLUSTERING K-MEANS
model = KMeans(n_clusters=5)
model.fit(data_norm)

# Obtención de los valores predecidos
md_k = pd.Series(model.labels_)


# Adición de las nuevas columnas a la tabla original
leb_oro['clust_j'] = md
leb_oro['clust_k'] = md_k
print(leb_oro.groupby('POS').mean())
