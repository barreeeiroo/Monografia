#!/usr/bin/python3
# -*- coding: utf-8 -*-


##############################################################################################
#                                         RECOMENDADO                                        #
#                  Se recomienda leer la siguiente iPython notebook, ya que                  #
#                     contiene el mismo código pero mucho más comentado.                     #
#   https://github.com/barreeeiroo/Monografia/blob/master/fourFactors/Four%20Factors.ipynb   #
##############################################################################################



# Se hacen todos los imports
import os
from random import randint
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Se carga el archivo CSV
wdir = os.path.dirname(__file__)
data = pd.read_csv(wdir+'/fourFactors.csv')

# Se declaran los ejes de la función
x = data[['efg', 'ftr', 'orb', 'tov']]
y = data['scr']
# Y los del equipo contrario
x_opp = data[['efg_opp', 'ftr_opp', 'orb_opp', 'tov_opp']]
y_opp = data['scr_opp']

# Se designa un número aleatorio para generar la muestra
random = randint(0, 99)
# Se separan los datos, para no sobrealimentar el modelo
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=random)
x_train_opp, x_test_opp, y_train_opp, y_test_opp = train_test_split(x_opp, y_opp, random_state=random)

# Se inicia el método de regresión linear
estimate = LinearRegression()
estimate_opp = LinearRegression()

# ENTRENAMIENTO DEL MODELO
estimate.fit(x_train, y_train)
estimate_opp.fit(x_train_opp, y_train_opp)

# Se muestran los coeficientes y el valor independiente
print(estimate.coef_)
print(estimate_opp.coef_)
# print(estimate.intercept_)
# print(estimate_opp.intercept_)
print("\n")

y_pred = estimate.predict(x_test)
# print(y_test)
# print(y_pred)

y_pred_opp = estimate_opp.predict(x_test_opp)
# print(y_test_opp)
# print(y_pred_opp)

# Muestra de errores para debug del programa
# print(mean_squared_error(y_test, y_pred))
# print(r2_score(y_test, y_pred))

# Hace falta migrar el formato int64 de numpy a una lista para poder iterarla
p_results = y_pred.tolist()
p_results_opp = y_pred_opp.tolist()
results = y_test.tolist()
results_opp = y_test_opp.tolist()

# Se inician las listas conteniendo las victorias
p_won = []
won = []

counter = 0
while counter < len(p_results):
    p_won.append(1 if p_results[counter]>p_results_opp[counter] else 0)
    won.append(1 if results[counter]>results_opp[counter] else 0)
    counter += 1

# Se muestran los resultados de las predicciones
print(p_won)
print(won)
