# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 10:42:31 2015

@author: luis
"""

import pandas as pd
import numpy as np
import os
import math


tTamTotal1 = 55
tTamUsar1 = 50
tTamTotal2 = 105
tTamUsar2 = 100
tDirectorio = "D:\Cambios\Doctorado\CORRIDAS DEL PROGRAMA\Corbana\Sigatoka - Semanal - EstadoEvolucion\\2016-02-17"
tArchivos = [   ["2016-02-16-Sigatoka - La Rita=01= - 55",tTamTotal1, tTamUsar1],
                ["2016-02-16-Sigatoka - La Rita=02= - 55",tTamTotal1, tTamUsar1],
                ["2016-02-16-Sigatoka - La Rita=03= - 55",tTamTotal1, tTamUsar1],
                ["2016-02-16-Sigatoka - La Rita=04= - 105",tTamTotal2, tTamUsar2],
                ["2016-02-16-Sigatoka - 28 Millas=05= - 55",tTamTotal1, tTamUsar1],
                ["2016-02-16-Sigatoka - 28 Millas=06= - 55",tTamTotal1, tTamUsar1],
                ["2016-02-16-Sigatoka - 28 Millas=07= - 105",tTamTotal2, tTamUsar2],
                ["2016-02-16-Sigatoka - 28 Millas=08= - 105",tTamTotal2, tTamUsar2],
                ["2016-02-16-Sigatoka - 28 Millas=09= - 55",tTamTotal1, tTamUsar1],
                ["2016-02-16-Sigatoka - 28 Millas=10= - 105",tTamTotal2, tTamUsar2],
                ["2016-02-16-Sigatoka - 28 Millas=11= - 55",tTamTotal1, tTamUsar1],
                ["2016-02-16-Sigatoka - 28 Millas=12= - 105",tTamTotal2, tTamUsar2],
                ["2016-02-16-Sigatoka - 28 Millas=13= - 55",tTamTotal1, tTamUsar1],
                ["2016-02-16-Sigatoka - 28 Millas=14= - 105",tTamTotal2, tTamUsar2],
                ["2016-02-16-Sigatoka - 28 Millas=15= - 55",tTamTotal2, tTamUsar2],
                ["2016-02-16-Sigatoka - La Rita=16= - 55",tTamTotal2, tTamUsar2],
                ["2015-01-27-Sigatoka - 28 Millas - Semanal - Validacion-ESN - 54",54,50],
                ["2015-01-27-Sigatoka - La Rita - Semanal - Validacion-SVR - 54",54,50],
                ["2015-01-27-Sigatoka - La Rita - Semanal - Validacion-SVR - 105",105,100],
                ["2016-02-03-Sigatoka - La Rita - Semanal - ValidacionERL - 54",54,50],
                ["2016-02-03-Sigatoka - La Rita - Semanal - ValidacionERL - 105",105,100],
                ["2016-02-03-Sigatoka - La Rita - Semanal - ValidacionESN - 53",53,50],
                ["2016-02-03-Sigatoka - La Rita - Semanal - ValidacionESN - 105",105,100],
                ["2015-01-27-Sigatoka - 28 Millas - Semanal - Validacion-ESN - 105",105,100],
                ["2015-01-27-Sigatoka - 28 Millas - Semanal - Validacion-REL - 54",54,50],
                ["2015-01-27-Sigatoka - 28 Millas - Semanal - Validacion-REL - 105",105,100],
                ["2015-01-27-Sigatoka - 28 Millas - Semanal - Validacion-SVR - 54",54,50],
                ["2015-01-27-Sigatoka - 28 Millas - Semanal - Validacion-SVR - 105",105,100],
                ["2015-01-27-Sigatoka - La Rita - Semanal - Validacion-ESN - 54",54,50],
                ["2015-01-27-Sigatoka - La Rita - Semanal - Validacion-ESN - 105",105,100],
                ["2015-01-27-Sigatoka - La Rita - Semanal - Validacion-REL - 54",54,50],
                ["2015-01-27-Sigatoka - La Rita - Semanal - Validacion-REL - 105",105,100]
        ]
os.chdir(tDirectorio)
tArchSalida = "2016-02-19- Resumen - Validacion - semanal - Sigatoka"


tTempDic = { "tipo": {}, "patron": {}, "algoritmo": {}, "disc_cont": {}, 
            "variables": {}, "r2": {}, "rmse": {}, "antes": {}, "despues": {},
            "configuracion": {}, "escalax": {}, "escalay": {}, "lugar": {},
            "metodoescalar": {}, "num_train": {}
            }
tSalida = pd.DataFrame(tTempDic)

print("Cantidad de archivos a procesar: ", len(tArchivos))
for tArch in range(len(tArchivos)):
    print("Archivo: ", tArchivos[tArch][0])
    tDatos = pd.read_excel(tArchivos[tArch][0]+".xlsx")       
    tDatos = tDatos.sort(["Discretizacion", "APatron", "Algoritmo", "EscalaX",
                          "Lugar", "Metodo", "Num_Validacion"], ascending=True)
    tVoyPor = 0
    tLargo = len(tDatos) - 1
    while tVoyPor < tLargo:
        tDatosnp = np.array(tDatos[tVoyPor:(tVoyPor+tArchivos[tArch][2])])
        tVoyPor = tVoyPor + tArchivos[tArch][1]   
        tMedia = np.mean(tDatosnp[:,-2],axis=0)
        tsse = 0
        tssr = 0
        tN = len(tDatosnp)
        for i in range(tN):
            tsse = tsse + pow(tDatosnp[i][-2]-tDatosnp[i][-1], 2)
            tssr = tssr + pow(tDatosnp[i][-2]-tMedia, 2)        
        tsse = tsse / tN
        tssr = tssr / tN
        tsst = tsse + tssr
        tr2 = tssr / tsst
        trmse = math.sqrt(tsse)
        # APatron 	Algoritmo	Detalles	   Discretizacion	 EscalaX	  EscalaY	
        # Lugar	Metodo	MetodoEscalar	Num_Train	Num_Validacion	
        # Valor1Real	Valor2Predicho    
        tUno = { "tipo": [tArchivos[tArch][2]], "patron": [tDatosnp[0][0]], 
                    "algoritmo": [tDatosnp[0][1]], "disc_cont": [tDatosnp[0][3]], 
                    "variables": [tDatosnp[0][7]], "r2": [tr2], "rmse": [trmse], 
                    "antes": [int(tDatosnp[0][0][0:2])], "despues": [int(tDatosnp[0][0][13:15])],
                    "configuracion": [tDatosnp[0][2]], "escalax": [tDatosnp[0][4]], 
                    "escalay": [tDatosnp[0][5]], "lugar": [tDatosnp[0][6]],
                    "metodoescalar": [tDatosnp[0][8]], "num_train": [tDatosnp[0][9]]
                }
        tUno2 = pd.DataFrame.from_dict(tUno)
        tSalida = tSalida.append(tUno2)
#tSalida = tSalida.sort(["r2"], ascending=True)        
tSalida.to_excel(tArchSalida + ".xlsx",sheet_name="Resultado", engine="openpyxl")    



