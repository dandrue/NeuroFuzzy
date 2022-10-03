#!/usr/bin/env python3
from DefaultStructure import *


def controller(tempvalue, presvalue):
    # Temperature input variable
    tVar = FuzzyVariable(name="Temperature", rang=[100, 340], labels=["Fria", "Fresca", "Normal", "Tibia", "Caliente"])
    # Temperatura = list(tVar.functions)
    # keys = list(tVar.functions.keys())
    # print(Temperatura)

    # Pressure input variable
    pVar = FuzzyVariable(name='Pressure', rang=[10, 250], labels=["Escasa", "Baja", "Bien", "Fuerte", "Alta"])
    # Pressure = list(pVar.functions)
    # print(Pressure)

    aVar = FuzzyVariable(name='Action', rang=[-60, 60], labels=["NG", "NM", "NP", "CE", "PP", "PM", "PG"])
    # Action = list(aVar.functions)
    # print(list(aVar.mfunctions))
    # variables = [tVar, pVar, aVar]

    # tVar.get_info()
    # pVar.get_info()
    # aVar.get_info()

    # Rules = RuleGenerator([tVar, pVar, aVar])
    # rules = Rules.gencomb()
    # linrepr(rules)
    # print(rules)

    # TempValue = 150
    # presValue = 80

    tempValues = [i.eval(tempvalue) for i in tVar.functions]
    presValues = [i.eval(presvalue) for i in pVar.functions]

    DicTemp = dict(zip(tVar.mfunctions, tempValues))
    DicPres = dict(zip(pVar.mfunctions, presValues))
    # print(DicTemp)
    # print(DicPres)

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

    # TODO: Combine DicVal and DictValIntersec, make the computations only in two loops

    for i in DicVal.keys():
        for j in DicVal[i].keys():
            value1 = DicPres[i]
            value2 = DicTemp[j]
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

    # Salidas = aVar.functions

    # Se generan listas vacias para cada función de salida y se agrupan en la lista SalAcc
    NG = []
    NM = []
    NP = []
    CE = []
    PP = []
    PM = []
    PG = []
    SalAcc = [NG, NM, NP, CE, PP, PM, PG]
    DictAccSal = aVar.dictFunctions
    # print("DictAccSal\n \n", DictAccSal, "\n")

    # Se genera un diccionario que relaciona las etiquetas de las funciones de salida con
    # las listas vacias que se cargaran con los valores de activación en el siguiente paso
    AccionDict = dict(zip(aVar.labels, SalAcc))
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
    # print(value)

    # aVar.plotting()
    return [tempValues, presValues], value, AccionDict, AccionConorma
