#!/usr/bin/python3
# -*- coding: utf-8 -*-


##############################################################################################
#                                         RECOMMENDED                                        #
#                It is highly advised to read the following iPython notebook,                #
#                     as it contains the same code but better commented.                     #
#   https://github.com/barreeeiroo/Monografia/blob/master/fourFactors/Four%20Factors.ipynb   #
###############################################################################################



# We make all required imports
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# We load the CSV file containing all stats
wdir = os.path.dirname(__file__)
data = pd.read_csv(wdir+'/fourFactors.csv')

# Declare the desired team axes
x = data[['efg', 'ftr', 'orb', 'tov']]
y = data['scr']
# And the opponent one
x_opp = data[['efg_opp', 'ftr_opp', 'orb_opp', 'tov_opp']]
y_opp = data['scr_opp']

# We split the data, so we keep some of them for testing purposes
random = 7
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=random)
x_train_opp, x_test_opp, y_train_opp, y_test_opp = train_test_split(x_opp, y_opp, random_state=random)

# Initialize the LinearRegression method
estimate = LinearRegression()
estimate_opp = LinearRegression()

# MODEL TRAINING
estimate.fit(x_train, y_train)
estimate_opp.fit(x_train_opp, y_train_opp)

# Print the weight of each factor
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

# Some error output for debugging purposes
# print(mean_squared_error(y_test, y_pred))
# print(r2_score(y_test, y_pred))

# We have to migrate the int64 format from numpy to a list so we can iterate it
p_results = y_pred.tolist()
p_results_opp = y_pred_opp.tolist()
results = y_test.tolist()
results_opp = y_test_opp.tolist()

# Initialize the array containing the victories
p_won = []
won = []

counter = 0
while counter < len(p_results):
    p_won.append(1 if p_results[counter]>p_results_opp[counter] else 0)
    won.append(1 if results[counter]>results_opp[counter] else 0)
    counter += 1

# We print the results of the predictions
print(p_won)
print(won)
