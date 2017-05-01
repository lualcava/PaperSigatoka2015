# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 15:36:42 2017

@author: lcalvo
"""

import pandas as pd
import os
import matplotlib.pyplot as pl

pl.style.use('ggplot')

os.chdir("D:/Usuarios/Lcalvo/Documents/Cambios/Doctorado/PAPERS EN PROCESO/PaperSigatoka2015")
tArchivoEntrada = "Usado - 2017-04-30-Datos totales.xlsx"
tArchivoSalida = "Usado_2017_"

tDatos = pd.read_excel(tArchivoEntrada, header=0 )
tParte = tDatos[['RMSE', 'Techniques', 'Farm']] 

tBoxPlot = tDatos[['RMSE', 'Techniques', 'Farm']] 
tBoxPlot = tBoxPlot[tBoxPlot.Techniques == "ESN"]

fig, axes = pl.subplots(nrows=1, ncols=2, sharey=True)
'''
tParte1 = tParte[tParte.Farm == "28 Millas"]
tParte2 = tParte[tParte.Farm == "La Rita"]

tParte1 = pd.DataFrame(tParte1.groupby(['Techniques'])['RMSE'].mean())

tParte2 = tParte2[tParte2.Techniques != "ESN"]
tParte2 = pd.DataFrame(tParte2.groupby(['Techniques'])['RMSE'].mean())

ax1 = tParte1.plot(ax=axes[0], sort_columns=True,legend=True, kind="bar")
ax2 = tParte2.plot(ax=axes[1], sort_columns=True, kind="bar")

ax1.set(xlabel='28 Millas', ylabel='RMSE')
ax2.set(xlabel='La Rita', ylabel='RMSE')
pl.plot()
pl.tight_layout()
pl.savefig( tArchivoSalida+ ".pdf")
'''

#######################################################
# BoxPlot
#######################################################
tBox1 = tBoxPlot[tBoxPlot.Farm == "28 Millas"]
tBox2 = tBoxPlot[tBoxPlot.Farm == "La Rita"]

bx1 = tBox1.boxplot(ax=axes[0],column=['RMSE'], by='Techniques', fontsize =6)
bx2 = tBox2.boxplot(ax=axes[1],column=['RMSE'], by='Techniques', fontsize =6)
bx1.set(xlabel='28 Millas', ylabel='')
bx2.set(xlabel='La Rita', ylabel='')

bx1.set_xticklabels(tBox1.Techniques.unique(), rotation=70)
bx2.set_xticklabels(tBox2.Techniques.unique(), rotation=70)
pl.plot(title ="")
fig.suptitle('')
pl.tight_layout()
pl.savefig( "Boxplot_ESN.pdf")

