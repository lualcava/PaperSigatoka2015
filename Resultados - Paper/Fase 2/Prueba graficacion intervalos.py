# -*- coding: utf-8 -*-
"""
Created on Mon Feb 01 17:14:08 2016

@author: lcalvo
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier

###############################################################################
# Calcula el R2  - Coeficiente de determinación
def calculeR2(pXorig, pYpred):
    tn = len(pXorig)
    ybar = np.sum(pXorig)/ tn
    sse = np.sum((pXorig - pYpred)**2)  # Suma de cuadrados del error o residual
    ssr = np.sum((pYpred - ybar)**2)  # Suma de Cuadrados debido a la regresión
    sst = sse + ssr   # Suma de cuadrados total
    results =  (ssr / sst)       
    return results

def demeLista(l):
    res = []
    for e in l:
        res.append(e)
    return res
    
    
    
np.random.seed(1)
nValidar = 52

todos = np.genfromtxt('Sigatoka.csv', delimiter=';', skip_header =1)
todos = todos.astype(np.float32)

X = todos[1:-nValidar,:-1]
# Observations
y = todos[1:-nValidar,-1]
xx = todos[-nValidar:,:-1]
realesxx = todos[-nValidar:,-1]


alpha = 0.95

clf = GradientBoostingRegressor(loss='quantile', alpha=alpha,
                                n_estimators=850, max_depth=3,
                                learning_rate=.1, min_samples_leaf=9,
                                min_samples_split=9)
clf.fit(X, y)
# Make the prediction on the meshed x-axis
y_upper = clf.predict(xx)

clf.set_params(alpha=1.0 - alpha)
clf.fit(X, y)

# Make the prediction on the meshed x-axis
y_lower = clf.predict(xx)


clf.set_params(loss='ls')
clf.fit(X, y)

# Make the prediction on the meshed x-axis
y_pred = clf.predict(xx)

# Plot the function, the prediction and the 90% confidence interval based on
# the MSE
xxg = range(nValidar)
fig = plt.figure()
plt.plot(xxg, realesxx, 'k:', label=u'$reales$')
plt.plot(xxg, realesxx, 'b.', markersize=10, label=u'Observations')
plt.plot(xxg, y_pred, 'r-', label=u'Prediction')
plt.plot(xxg, y_upper, 'k-')
plt.plot(xxg, y_lower, 'k-')
plt.fill(np.concatenate([xxg, xxg[::-1]]),
         np.concatenate([y_upper, y_lower[::-1]]),
         alpha=.5, fc='c', ec='None', label='90% prediction interval')
plt.xlabel('$x$')
plt.ylabel('$reales$')
plt.ylim(0, 8000)
plt.legend(loc='lower left')
plt.show()
print("El R2 es: ", calculeR2(realesxx, y_pred))


X = todos[:,:-1]
y = todos[:,-1]
'''
clf = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0)
scores = cross_val_score(clf, X, y)
print( scores.mean() )


clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)
scores = cross_val_score(clf, X, y)
print( scores.mean() )



clf = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)
scores = cross_val_score(clf, X, y)
print( scores.mean() > 0.999 )
'''

