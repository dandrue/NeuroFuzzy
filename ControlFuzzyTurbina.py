#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 00:43:30 2021

@author: diego
"""
# Se importan librerías
# import numpy as np
import matplotlib.pyplot as plt
from FuncionesPertenencia import TrapAbiertaIzquierda, TrapAbiertaDerecha, \
    Triangular, Trapezoidal, Intersecciones, Conorma
from copy import deepcopy
import seaborn as sns
sns.set_theme()

# Se establecen las etiquetas de los conjuntos difusos para Temperatura y Presión y se agrupan en dos diccionarios
Temp = {'name': 'Temperatura', 'labels': ["Fria", "Fresca", "Normal", "Tibia", "Caliente"]}
Pres = {'name': 'Presion', 'labels': ["Escasa", "Baja", "Bien", "Fuerte", "Alta"]}

# Se definen las funciones de pertenencia de los conjuntos difusos para la temperatura
TempFria = TrapAbiertaIzquierda(Temp['labels'][0], Temp['name'], [100, 140, 180])
TempFresca = Triangular(Temp['labels'][1], Temp['name'], [140, 180, 220])
TempNormal = Triangular(Temp['labels'][2], Temp['name'], [180, 220, 260])
TempTibia = Triangular(Temp['labels'][3], Temp['name'], [220, 260, 300])
TempCaliente = TrapAbiertaDerecha(Temp['labels'][4], Temp['name'], [260, 300, 340])

# Se agrupan en una lista las funciones de pertenencia para la Temperatura
Temperatura = [TempFria, TempFresca, TempNormal, TempTibia, TempCaliente]
fig, axs = plt.subplots(2, 2)
for i in Temperatura:
    axs[0, 0].plot(i.x, i.y)
axs[0, 0].set_ylim([0, 1.02])
axs[0, 0].grid(True)
axs[0, 0].set_title("Temperature")
axs[0, 0].set_xlabel("Temperature")
axs[0, 0].set_ylabel('Membership')

# Se definen las funciones de pertenencia de los conjuntos difusos para la presión
PreEscasa = TrapAbiertaIzquierda(Pres['labels'][0], Pres['name'], [10, 50, 90])
PreBaja = Triangular(Pres['labels'][1], Pres['name'], [50, 90, 130])
PreBien = Triangular(Pres['labels'][2], Pres['name'], [90, 130, 170])
PreFuerte = Triangular(Pres['labels'][3], Pres['name'], [130, 170, 210])
PreAlta = TrapAbiertaDerecha(Pres['labels'][4], Pres['name'], [170, 210, 250])

# Se agrupan en una lista las funciones de pertenencia para la Presión
Presion = [PreEscasa, PreBaja, PreBien, PreFuerte, PreAlta]

for i in Presion:
    axs[0, 1].plot(i.x, i.y)
axs[0, 1].grid(True)
axs[0, 1].set_ylim([0, 1.02])
axs[0, 1].set_title("Preassure")
axs[0, 1].set_xlabel("Preassure")
axs[0, 1].set_ylabel('Membership')

# Se Realizan las entradas del sistema con valores discretos
TempValue = 150
PreValue = 80

# Se crean dos listas vacias que almacenaran la activación correspondiente a
# cada función de pertenencia en temperatura y presión
ActTemp = []
ActPre = []


# Partiendo de que no necesariamente deben ser iguales el número de conjuntos
# de temp y presion se opta por separa el análisis de activación

# cada i representa una función de pertenencia, y cada función posee el método
# eval(param), que evalúa el valor de la función con respecto a el valor ingresado como parámetro

for i in Temperatura:
    ActTemp.append(i.eval(TempValue))

for i in Presion:
    ActPre.append(i.eval(PreValue))

# Se generan diccionarios que relacionan las etiquetas de los conjuntos difusos con los valores de activación

DicTemp = dict(zip(Temp['labels'], ActTemp))
DicPres = dict(zip(Pres['labels'], ActPre))
print(DicTemp)
print(DicPres)

# Se ingresan las reglas del modelo Fuzzy, utilizando un diccionario que para cada
# etiqueta de Presión relaciona a otro diccionario en donde se relaciona finalmente
# con el conjunto de salida

dic = {"Escasa": {"Fria": "PG", "Fresca": "PG", "Normal": "PM", "Tibia": "PM", "Caliente": "PP"},
       "Baja": {"Fria": "PM", "Fresca": "PM", "Normal": "PP", "Tibia": "PP", "Caliente": "PP"},
       "Bien": {"Fria": "PP", "Fresca": "CE", "Normal": "CE", "Tibia": "NP", "Caliente": "NM"},
       "Fuerte": {"Fria": "NP", "Fresca": "NM", "Normal": "NP", "Tibia": "NM", "Caliente": "NG"},
       "Alta": {"Fria": "NM", "Fresca": "NM", "Normal": "NM", "Tibia": "NG", "Caliente": "NG"}}

# Se copia el diccionario de las reglas para generar un diccionario con los valores
# de activación siguiendo las reglas del modelo

DicVal = deepcopy(dic)

# Se agrupan los valores de activación para cada regla del modelo y se generan listas
# con los valores de activación len([]) = 2, ya que son solo dos entradas
for i in DicVal.keys():
    for j in DicVal[i].keys():
        value1 = DicPres[i]
        value2 = DicTemp[j]
        DicVal[i][j] = [value1, value2]
print("DicVal\n \n ", DicVal, "\n")

# Se copia el diccionario anterior para generar un nuevo diccionario con el valor de
# activación final tras la realización de la intersección
# Este paso puede ser borrado y sobreescribir el diccionario copiado, pero para efectos
# de entendimiento del sistema se decide mantenerlo

DicValIntersec = deepcopy(DicVal)

# Se realiza un ciclo for que itera entre las keys del diccionario para generar el
# valor de intersección, pueden utilizarse los métodos Zadeh, Mean, Larsen, mediante
# la sintaxis Intersecciones.$Metodo$

# TODO: Optimize the number of computations to obtain the final membership of input functions

for i in DicVal.keys():
    for j in DicVal[i].keys():
        inter = Intersecciones.zadeh(DicValIntersec[i][j])
        DicValIntersec[i][j] = inter
print("DictValIntersec\n \n", DicValIntersec, "\n")
# Se definen las etiquetas para las funciones de salida
Accion = {'name': 'action', 'labels': ["NG", "NM", "NP", "CE", "PP", "PM", "PG"]}

# Se definen las funciones de salida
AccNG = TrapAbiertaIzquierda(Accion['labels'][0], Accion['name'], [-60, -40, -20])
AccNM = Triangular(Accion['labels'][1], Accion['name'], [-40, -20, -10])
AccNP = Triangular(Accion['labels'][2], Accion['name'], [-20, -10, 10])
AccCE = Triangular(Accion['labels'][3], Accion['name'], [-10, 0, 10])
AccPP = Triangular(Accion['labels'][4], Accion['name'], [-10, 10, 20])
AccPM = Triangular(Accion['labels'][5], Accion['name'], [10, 20, 40])
AccPG = TrapAbiertaDerecha(Accion['labels'][6], Accion['name'], [20, 40, 60])

# Se agrupan en una lista las funciones de pertenencia para el accionamiento del inyector
Salidas = [AccNG, AccNM, AccNP, AccCE, AccPP, AccPM, AccPG]

for i in Salidas:
    axs[1, 0].plot(i.x, i.y)
axs[1, 0].set_ylim([0, 1.02])
axs[1, 0].grid(True)
axs[1, 0].set_title("Accionamiento del Inyector (Entrada) [cm/s]")
axs[1, 0].set_xlabel("Accionamiento")
axs[1, 0].set_ylabel('Pertenencia')


# Se generan listas vacias para cada función de salida y se agrupan en la lista SalAcc
NG = []
NM = []
NP = []
CE = []
PP = []
PM = []
PG = []
SalAcc = [NG, NM, NP, CE, PP, PM, PG]

# Se genera un diccionario que relaciona las etiquetas de las funciones de salida y las
# funciones de pertenencia de la salida
DictAccSal = dict(zip(Accion['labels'], Salidas))

print("DictAccSal\n \n", DictAccSal, "\n")

# Se genera un diccionario que relaciona las etiquetas de las funciones de salida con
# las listas vacias que se cargaran con los valores de activación en el siguiente paso
AccionDict = dict(zip(Accion['labels'], SalAcc))
print("AccionDict\n \n", AccionDict, "\n")

# Mediante el ciclo for se itera dentro del diccionario que contiene las reglas difusas
# del modelo y el diccionario que contiene el valor de activación para cada caso, los
# datos se almacenan en el recién creado diccionario AccionDict
for i in dic.keys():
    for j in dic[i].keys():
        value = dic[i][j]
        AccionDict[value].append(DicValIntersec[i][j])
print("AccionDict\n \n", AccionDict, "\n")
# Se copia el diccionario ActionDict y se genera el calculo de la conorma sobre la
# lista de activaciones para cada conjunto de salida. Los metodos para la conorma son Max y Sum
AccionConorma = deepcopy(AccionDict)
for i in AccionConorma.keys():
    value = Conorma.max(AccionConorma[i])
    AccionConorma[i] = value

# El diccionario AccionConorma contiene el valor de corte para cada uno de los conjuntos difusos a la salida
print("AccionConorma\n \n", AccionConorma, "\n")

# Determinación del tipo de salida Escalado o Truncado
Tipo = "Truncado"
if Tipo == "Escalado":
    for i in AccionConorma.keys():
        if DictAccSal[i].type == "TrapAbiertaIzquierda":
            Base = DictAccSal[i]
            AccionDict[i] = TrapAbiertaIzquierda("TrapIzquierdaTruncada", Base.var, [Base.inicio, Base.medio, Base.fin],
                                                 AccionConorma[i])
        elif DictAccSal[i].type == "TrapAbiertaDerecha":
            Base = DictAccSal[i]
            AccionDict[i] = TrapAbiertaDerecha("TrapDerechaTruncada", Base.var, [Base.inicio, Base.medio, Base.fin],
                                               AccionConorma[i])
        elif DictAccSal[i].type == "Trapezoidal":
            Base = DictAccSal[i]
            AccionDict[i] = Trapezoidal('TrapTruncada', Base.var, [Base.inicio, Base.medio1, Base.medio2, Base.fin],
                                        AccionConorma[i])
        elif DictAccSal[i].type == "Triangular":
            Base = DictAccSal[i]
            AccionDict[i] = Triangular('TriangularTruncada', Base.var, [Base.inicio, Base.medio, Base.fin],
                                       AccionConorma[i])

elif Tipo == "Truncado":
    for i in AccionConorma.keys():
        if DictAccSal[i].type == "TrapAbiertaIzquierda":
            Base = DictAccSal[i]
            medio = Base.evalx(AccionConorma[i])
            AccionDict[i] = TrapAbiertaIzquierda("TrapIzquierdaTruncada", Base.var, [Base.inicio, medio, Base.fin],
                                                 altura=AccionConorma[i])
        elif DictAccSal[i].type == "TrapAbiertaDerecha":
            Base = DictAccSal[i]
            medio = Base.evalx(AccionConorma[i])
            AccionDict[i] = TrapAbiertaDerecha("TrapDerechaTruncada", Base.var, [Base.inicio, medio, Base.fin],
                                               altura=AccionConorma[i])
        elif DictAccSal[i].type == "Trapezoidal":
            Base = DictAccSal[i]
            medio1, medio2 = Base.evalx(AccionConorma[i])
            AccionDict[i] = Trapezoidal('TrapTruncada', Base.var, [Base.inicio, medio1, medio2, Base.fin],
                                        altura=AccionConorma[i])
        elif DictAccSal[i].type == "Triangular":
            Base = DictAccSal[i]
            medio1, medio2 = Base.evalx(AccionConorma[i])
            AccionDict[i] = Trapezoidal('TriangularTruncada', Base.var, [Base.inicio, medio1, medio2, Base.fin],
                                        altura=AccionConorma[i])

# for i in AccionConorma.keys():
#     print(AccionConorma[i])

for i in AccionDict.keys():
    axs[1, 1].plot(AccionDict[i].x, AccionDict[i].y)
axs[1, 1].set_xlim([-60, 60])
axs[1, 1].set_ylim([0, 1.02])
axs[1, 1].grid(True)
axs[1, 1].set_xlabel('Membership')
axs[1, 1].set_ylabel('Displacement')
axs[1, 1].set_title('Injector Displacement (Output) [cm/s]')
fig.suptitle('MEMBERSHIP FUNCTIONS')
plt.show()

Areas = []
Centroides = []

for i in AccionDict.keys():
    if AccionDict[i].type == "TrapAbiertaIzquierda":
        Base = AccionDict[i]
        area1 = 1/2*((Base.fin - Base.medio)*Base.altura)
        centroide1 = Base.medio + (1/3)*(Base.fin - Base.medio)
        area2 = ((Base.medio - Base.inicio)*Base.altura)
        centroide2 = Base.inicio + (1/2)*(Base.medio - Base.inicio)
        Areas.extend([area1, area2])
        Centroides.extend([centroide1, centroide2])

    elif AccionDict[i].type == "TrapAbiertaDerecha":
        Base = AccionDict[i]
        area1 = 1/2*((Base.medio - Base.inicio)*Base.altura)
        centroide1 = Base.inicio + (2/3)*(Base.medio - Base.inicio)
        area2 = ((Base.fin - Base.medio)*Base.altura)
        centroide2 = Base.medio + (1/2)*(Base.fin - Base.medio)
        Areas.extend([area1, area2])
        Centroides.extend([centroide1, centroide2])

    elif AccionDict[i].type == "Trapezoidal" or AccionDict[i].type == "Tringular":
        Base = AccionDict[i]
        area1 = 1/2*((Base.medio1 - Base.inicio)*Base.altura)
        centroide1 = Base.inicio + (2/3)*(Base.medio1 - Base.inicio)
        area2 = ((Base.medio2 - Base.medio1)*Base.altura)
        centroide2 = Base.medio1 + (1/2)*(Base.medio2 - Base.medio1)
        area3 = ((Base.fin - Base.medio2)*Base.altura)
        centroide3 = Base.medio2 + (1/2)*(Base.fin - Base.medio2)
        Areas.extend([area1, area2, area3])
        Centroides.extend([centroide1, centroide2, centroide3])

XA = [a * b for a, b in zip(Areas, Centroides)]
XA = sum(XA)
print(XA)
SA = sum(Areas)
print(SA)
value = round(XA/SA, 3)
print(value)