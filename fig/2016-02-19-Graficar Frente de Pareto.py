# -*- coding: utf-8 -*-
"""
Created on Thu Feb 04 18:38:48 2016

@author: lcalvo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
import operator
import os


#########################################################################    
def guarde_Frente_Pareto(pDatos, pTipos, maxX, maxY, pCategX, pCategY, pCol):
# maxX : Si True es porque se quiere maximizar, si False se desea minimizar
# maxY : Si True es porque se quiere maximizar, si False se desea minimizar    
    global gNombreGlobal  
    for tL in pTipos:
        tParte = pDatos[(pDatos[pCol] == tL )]
        if len(tParte) > 0:    
            myListX =  tParte.sort([pCategX], ascending=(not maxX)) 
            myListY =  tParte.sort([pCategY], ascending=(not maxY)) 
            p_front= pd.DataFrame({})
            if maxX:
                p_front = myListY.head(1)
                orden = myListY
            else:
                p_front = myListX.head(1)
                orden = myListX                
            tLargo = len(orden)
            for pair in range(1,tLargo):
                if maxY:
                    if maxX:
                        if (orden.iloc[pair][pCategX] >= p_front.tail(1).iloc[-1][pCategX]) : 
                            p_front = p_front.append(orden.iloc[pair]) 
                    else: # if maxX
                        if (orden.iloc[pair][pCategY] >= p_front.tail(1).iloc[-1][pCategY]):                             
                            p_front = p_front.append(orden.iloc[pair])                 
                else: # if maxY
                    if maxX:
                        if (orden.iloc[pair][pCategY] <= p_front.tail(1).iloc[-1][pCategY]):
                            p_front = p_front.append(orden.iloc[pair])                     
                    else: # if maxX
                        if (orden.iloc[pair][pCategX] <= p_front.tail(1).iloc[-1][pCategX]): 
                            p_front = p_front.append(orden.iloc[pair]) 
        else:
            print("No se pudo calcular frente de pareto para: ", tL)
        p_front.to_excel(gNombreGlobal+" - Frende de Pareto - " + tL+ ".xlsx",sheet_name="Resultado", engine="openpyxl")        
    

#########################################################################    
def pareto_frontier(Xs, Ys, maxX , maxY ):
    # Calcula el frente de pareto
    myListX = sorted([[Xs[i], Ys[i]] for i in range(len(Xs))], reverse=maxX)
    myListY = sorted([[Xs[i], Ys[i]] for i in range(len(Ys))], reverse=maxY, key=operator.itemgetter(1)) 
    if maxX:
        p_front = [myListY[0]] 
        orden = myListY[:]
    else:
        p_front = [myListX[0]]         
        orden = myListX[:]
    for pair in orden[1:]:
        if maxY:
            if maxX:
                if (pair[0] >= p_front[-1][0]) : 
                    p_front.append(pair) 
            else: # if maxX
                if (pair[1] >= p_front[-1][1]): 
                    p_front.append(pair)        
        else: # if maxY
            if maxX:
                if (pair[1] <= p_front[-1][1]):
                    p_front.append(pair)                     
            else: # if maxX
                if (pair[0] <= p_front[-1][0]): 
                    p_front.append(pair)     
    p_frontX = [pair[0] for pair in p_front]
    p_frontY = [pair[1] for pair in p_front]    
    return p_frontX, p_frontY

#########################################################################
def genereUnGrafico(pDatos, pColores, pTipos, pCol, pTipoGraf, pX, pY, pLoc, pNombre, 
                    pPareto, pTitulo):
    # Imprime y archiva un gráfico
    global gMaxEnX, gMaxEnY
    tColor = 0
    tElmarker = '.'
    pl.clf()
    if len(pDatos>0):
        for tL in pTipos:
            tParte = pDatos[(pDatos[pCol] == tL )]
            if len(tParte) > 0:     
                if tColor == 0:                    
                    tAx = tParte.plot( title= pTitulo, kind=pTipoGraf, x=pX, y=pY, color=pColores[tColor], label=tL, marker=tElmarker)
                    tColor += 1 
                else:
                    tParte.plot(ax=tAx, kind=pTipoGraf, x=pX, y=pY, color=pColores[tColor], label=tL, marker=tElmarker)
                if pPareto:
                    pXequis = list(tParte[pX])
                    pYes = list(tParte[pY])
                    p_front = pareto_frontier(pXequis, pYes, maxX = False, maxY = True)
                    tDFrame = pd.DataFrame({pX: p_front[0],  pY: p_front[1]})
                    tDFrame.plot(ax=tAx, color="Darkred", linewidth =3, kind='line', x=pX, y=pY,legend =False)                    
                    if len(p_front[0])==1:  # Solo hay un punto
                        pl.plot(p_front[0], p_front[1], 'ro')
            else:
                print("No se pudo graficar: ", tL)
            if tColor >= len(pColores):
                tColor = 0                    
        tGrafActual = pl.gcf()     
        tAx.set_xlim([0, gMaxEnX])
        tAx.set_ylim([0, gMaxEnY])
        #pl.legend(loc=pLoc)
        pl.plot()
        tGrafActual.savefig(pNombre , format="pdf")

####################################################################################################
#  Programa principal
####################################################################################################


os.chdir("D:\Cambios\Doctorado\CORRIDAS DEL PROGRAMA\Graficacion")

tArchivoEntrada = "2016-02-04-datos para dispersion - Fase 1.csv"
tArchivoEntrada = "2016-02-20- Datos- Validacion - Fase 2.csv"
gNombreGlobal = "Fase 2"
tCuantosHead = 55000
tRMSEMenorQue = 1200
gMaxEnX = tRMSEMenorQue
gMaxEnY = 0.70



tMatrizDatos = pd.io.parsers.read_csv(tArchivoEntrada, sep=";", header = 0)  # En fila 0 títulos




tMatrizDatos = tMatrizDatos.sort(["rmse" ], ascending=True)
tMatrizDatos = tMatrizDatos.head(tCuantosHead)
tMatrizDatos = tMatrizDatos[(tMatrizDatos ["rmse"] < tRMSEMenorQue )]


tNumFilas = len(tMatrizDatos.index)
tNumColumnas = len(tMatrizDatos.columns)
tMatrizDatos.index = list(range(0,tNumFilas)) 

tColores = ["blue", "green", "red", "cyan", "magenta", "yellow", "black", 
                    "DarkBlue", "DarkGreen", "DarkRed"]  
tTipos = [ "28 Millas", "La Rita"]
tTip = "lugar"
tGra = ['rmse','r2']
tLocG = 4
tNombre = gNombreGlobal+ " - R2 - RMSE"
tQPareto = True
##################################
tTitulo = "Pareto Frontier"
tTitulo = ""
##################################
                    
genereUnGrafico(tMatrizDatos, tColores, tTipos, tTip, 'scatter',tGra[0], tGra[1], 
                tLocG, tNombre, tQPareto, tTitulo) 



#genereUnGrafico(tMatrizDatos[(tMatrizDatos ["Lugar"] == "28 Millas" )], tColores, tTipos, tTip, 'scatter',tGra[0], tGra[1], tLocG, tNombre+"-1", tQPareto) 

#genereUnGrafico(tMatrizDatos[(tMatrizDatos ["Lugar"] == "La Rita" )], tColores, tTipos, tTip, 'scatter',tGra[0], tGra[1], tLocG, tNombre+"-2", tQPareto) 

guarde_Frente_Pareto(tMatrizDatos, tTipos, False, True, tGra[0], tGra[1], tTip)



