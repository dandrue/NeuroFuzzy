#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Mon Oct 10

@author: Diego A. Rueda

"""
from typing import Dict, Union

from DefaultStructure import *
import numpy as np

theta_var = FuzzyVariable(name="Theta", rang=[0, 2*np.pi])
theta_dot_var = FuzzyVariable(name='Theta_dot', rang=[-np.pi/4, np.pi/4])
torque_var = FuzzyVariable(name='Torque', rang=[-3, 3])


def controller(theta_value, theta_dot_value):
    # Temperature input variable
    # theta_var = FuzzyVariable(name="Theta", rang=[0, 2*np.pi])
    # Temperatura = list(theta_var.functions)
    # keys = list(theta_var.functions.keys())
    # print(Temperatura)

    # Pressure input variable
    # theta_dot_var = FuzzyVariable(name='Theta_dot', rang=[-np.pi/4, np.pi/4])
    # Pressure = list(theta_dot_var.functions)
    # print(Pressure)

    # torque_var = FuzzyVariable(name='Torque', rang=[-3, 3])
    # Action = list(torque_var.functions)
    # print(list(torque_var.mfunctions))
    # variables = [theta_var, theta_dot_var, torque_var]

    # theta_var.get_info()
    # theta_dot_var.get_info()
    # torque_var.get_info()

    # Rules = RuleGenerator([theta_var, theta_dot_var, torque_var])
    # rules = Rules.gencomb()
    # linrepr(rules)
    # print(rules)

    # TempValue = 150
    # presValue = 80

    theta_values = [i.eval(theta_value) for i in theta_var.functions]
    theta_dot_values = [i.eval(theta_dot_value) for i in theta_dot_var.functions]

    DictTheta = dict(zip(theta_var.mfunctions, theta_values))
    DictTheta_dot = dict(zip(theta_dot_var.mfunctions, theta_dot_values))

    # Fuzzy Rules
    dic = {"NB": {"NB": "PB", "NM": "PB", "ZZ": "PB", "PM": "PM", "PB": "PB"},
           "NM": {"NB": "PM", "NM": "PB", "ZZ": "PM", "PM": "PM", "PB": "PM"},
           "ZZ": {"NB": "ZZ", "NM": "PM", "ZZ": "ZZ", "PM": "NM", "PB": "ZZ"},
           "PM": {"NB": "NM", "NM": "ZZ", "ZZ": "NM", "PM": "NM", "PB": "NM"},
           "PB": {"NB": "NB", "NM": "ZZ", "ZZ": "NB", "PM": "NB", "PB": "NB"}}

    # Se copia el diccionario de las reglas para generar un diccionario con los valores
    # de activación siguiendo las reglas del modelo

    DicVal: Dict[str, Union[Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str]]] = \
        deepcopy(dic)

    # Se agrupan los valores de activación para cada regla del modelo y se generan listas
    # con los valores de activación len([]) = 2, ya que son solo dos entradas

    # TODO: Combine DicVal and DictValIntersec, make the computations only in two loops

    for i in DicVal.keys():
        j: str
        for j in DicVal[i].keys():
            value1 = DictTheta_dot[i]
            value2 = DictTheta[j]
            DicVal[i][j] = [value1, value2]
    # print("DicVal\n \n ", DicVal, "\n")

    # Se copia el diccionario anterior para generar un nuevo diccionario con el valor de
    # activación final tras la realización de la intersección
    # Este paso puede ser borrado y sobreescribir el diccionario copiado, pero para efectos
    # de entendimiento del sistema se decide mantenerlo

    DicValIntersec = deepcopy(DicVal)

    # Se realiza un ciclo for que itera entre las keys del diccionario para generar el
    # valor de intersección, pueden utilizarse los métodos Zadeh, Mean, Larsen, mediante
    # la sintaxis Intersecciones.$Metodo$

    for i in DicVal.keys():
        for j in DicVal[i].keys():
            inter = Intersecciones.zadeh(DicValIntersec[i][j])
            DicValIntersec[i][j] = inter
    # print("DictValIntersec\n \n", DicValIntersec, "\n")

    # Salidas = torque_var.functions

    # Se generan listas vacias para cada función de salida y se agrupan en la lista SalAcc
    NB = []
    NM = []
    ZZ = []
    PM = []
    PB = []
    # PM = []
    # PG = []
    SalAcc = [NB, NM, ZZ, PM, PB]
    DictAccSal = torque_var.dictFunctions
    # print("DictAccSal\n \n", DictAccSal, "\n")

    # Se genera un diccionario que relaciona las etiquetas de las funciones de salida con
    # las listas vacias que se cargaran con los valores de activación en el siguiente paso
    AccionDict = dict(zip(torque_var.labels, SalAcc))
    # print("AccionDict\n \n", AccionDict, "\n")

    # Mediante el ciclo for se itera dentro del diccionario que contiene las reglas difusas
    # del modelo y el diccionario que contiene el valor de activación para cada caso, los
    # datos se almacenan en el recién creado diccionario AccionDict
    for i in dic.keys():
        for j in dic[i].keys():
            value = dic[i][j]
            AccionDict[value].append(DicValIntersec[i][j])
    # print("AccionDict\n \n", AccionDict, "\n")
    # Se copia el diccionario ActionDict y se genera el calculo de la conorma sobre la
    # lista de activaciones para cada conjunto de salida. Los metodos para la conorma son Max y Sum
    AccionConorma = deepcopy(AccionDict)
    for i in AccionConorma.keys():
        value = Conorma.max(AccionConorma[i])
        AccionConorma[i] = value

    # El diccionario AccionConorma contiene el valor de corte para cada uno de los conjuntos difusos a la salida
    # print("AccionConorma\n \n", AccionConorma, "\n")

    # Determinación del tipo de salida Escalado o Truncado
    Tipo = "Truncado"
    if Tipo == "Escalado":
        for i in AccionConorma.keys():
            if DictAccSal[i].type == "TrapAbiertaIzquierda":
                Base = DictAccSal[i]
                AccionDict[i] = TrapAbiertaIzquierda("TrapIzquierdaTruncada", Base.var, [Base.inicio, Base.medio,
                                                                                         Base.fin],
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
    Areas = []
    Centroides = []

    for i in AccionDict.keys():
        Base = AccionDict[i]
        Areas.extend(Base.areas())
        Centroides.extend(Base.centroides())

    XA = [a * b for a, b in zip(Areas, Centroides)]
    XA = sum(XA)
    # print(XA)
    SA = sum(Areas)
    # print(SA)
    value = round(XA/SA, 3)
    print(value)

    # torque_var.plotting()
    # return [theta_values, theta_dot_values], value, AccionDict, AccionConorma
    return value


# T = controller(theta, theta_d)
