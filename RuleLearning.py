#!/usr/bin/env python3
import time
start = time.time()
from DefaultStructure import *
from BackProp import *

tVar = FuzzyVariable(name="Temperature", rang=[100, 340], labels=["Fria", "Fresca", "Normal", "Tibia", "Caliente"])
pVar = FuzzyVariable(name='Pressure', rang=[10, 250], labels=["Escasa", "Baja", "Bien", "Fuerte", "Alta"])
aVar = FuzzyVariable(name='Action', rang=[-60, 60], labels=["NG", "NM", "NP", "CE", "PP", "PM", "PG"])


def controller(tempvalue, presvalue, objective):

    Rules = RuleGenerator([pVar, tVar, aVar])
    rules = Rules.gencomb()
    print(rules)

    # rules = {"Escasa": {"Fria": "PG", "Fresca": "PG", "Normal": "PM", "Tibia": "PM", "Caliente": "PP"},
    #        "Baja": {"Fria": "PM", "Fresca": "PM", "Normal": "PP", "Tibia": "PP", "Caliente": "PP"},
    #        "Bien": {"Fria": "PP", "Fresca": "CE", "Normal": "CE", "Tibia": "NP", "Caliente": "NM"},
    #        "Fuerte": {"Fria": "NP", "Fresca": "NM", "Normal": "NP", "Tibia": "NM", "Caliente": "NG"},
    #        "Alta": {"Fria": "NM", "Fresca": "NM", "Normal": "NM", "Tibia": "NG", "Caliente": "NG"}}

    # TODO Estandarize the evaluation of functions and creation of dictionaries

    tempValues = [i.eval(tempvalue) for i in tVar.functions]
    presValues = [i.eval(presvalue) for i in pVar.functions]

    DicTemp = dict(zip(tVar.mfunctions, tempValues))
    DicPres = dict(zip(pVar.mfunctions, presValues))

    print(DicTemp)
    print(DicPres)

    DicVal = deepcopy(rules)

    for i in DicVal.keys():
        tempdic = {}
        for j in DicVal[i].keys():
            # print(DicPres[i])
            value1 = DicPres[i]
            value2 = DicTemp[j]
            tempdic[j] = [value1, value2]
        DicVal[i] = tempdic
    print("DicVal\n \n ", DicVal, "\n")

    DicValIntersec = deepcopy(DicVal)
    # print(DicValIntersec)

    for i in DicVal.keys():
        for j in DicVal[i].keys():
            inter = Intersecciones.zadeh(DicValIntersec[i][j])
            DicValIntersec[i][j] = inter
    print("DictValIntersec\n \n", DicValIntersec, "\n")

    # Dejando unicamente las reglas que se activan
    for i in DicValIntersec.copy():
        DicValIntersec[i] = {x: y for x, y in DicValIntersec[i].items() if y != 0}
        if not DicValIntersec[i]:
            DicValIntersec.pop(i)

    print("New \n", DicValIntersec)

    NG = []
    NM = []
    NP = []
    CE = []
    PP = []
    PM = []
    PG = []
    SalAcc = [NG, NM, NP, CE, PP, PM, PG]
    DictAccSal = aVar.dictFunctions
    print("DictAccSal\n \n", DictAccSal, "\n")

    AccionDict = dict(zip(aVar.labels, SalAcc))
    print("AccionDict\n \n", AccionDict, "\n")

    rulesc = deepcopy(DicValIntersec)
    ruleslist = []

    for i in DicValIntersec.keys():
        for j in DicValIntersec[i].keys():
            rulesc[i][j] = [DicValIntersec[i][j]] * 7
            ruleslist.append([DicValIntersec[i][j]] * 7)
    print("rules c\n \n", rulesc, "\n")
    print(ruleslist)
    counter = 0
    # ex es una ejemplo de las posibles funciones de pertenencia a la salida
    ex = aVar.labels
    print('ex', ex)
    totalComb = []
    totalValue = []
    totalError = []
    for i in range(len(ruleslist[0])):
        for j in range(len(ruleslist[1])):
            for k in range(len(ruleslist[2])):
                for m in range(len(ruleslist[3])):
                    Acc = deepcopy(AccionDict)
                    print(ex[i], ex[j], ex[k], ex[m])
                    Acc[ex[i]].append(ruleslist[0][i])
                    Acc[ex[j]].append(ruleslist[1][j])
                    Acc[ex[k]].append(ruleslist[2][k])
                    Acc[ex[m]].append(ruleslist[3][m])
                    counter += 1
                    # print("Acc ", Acc)
                    # entry1 = Acc
                    # print(counter)
                    totalComb.append(Acc)
                    # print("before", DictAccSal)
                    # print(Acc)
                    tcon = totalc(Acc, DictAccSal, objective)
                    # print("after", DictAccSal)
                    # print(Acc)
                    pcon = partialc(Acc, DictAccSal, objective)
                    totError = (tcon + pcon)/2
                    totalError.append(totError)
                    # print('Entry 1', entry1)
                    # totalValue.append(tcon)
                    print('Ciclo ', counter, " Finalizado")
                    print(totError)
                    # print("Acc 2", Acc)

    # print(totalError)
    # print(len(totalError))
    print(min(totalError))
    print(max(totalError))


    # TODO modificar las reglas para iniciar la depuración

def getrule(ind, ruleslist, rulesc):
    power = len(ruleslist)
    base = len(aVar.labels)

    pass

def totalc(AccionDict, DictAccSal, objective):
    # print('total contribution')
    AccionConorma = deepcopy(AccionDict)
    AccDict = deepcopy(AccionDict)
    # print("AccionConorma",AccionConorma)
    for i in AccionConorma.keys():
        value = Conorma.max(AccionConorma[i])
        AccionConorma[i] = value
    # print("AccionConorma post", AccionConorma)

    # El diccionario AccionConorma contiene el valor de corte para cada uno de los conjuntos difusos a la salida
    # print("AccionConorma\n \n", AccionConorma, "\n")

    # Determinación del tipo de salida Escalado o Truncado
    Tipo = "Truncado"
    if Tipo == "Escalado":
        for i in AccionConorma.keys():
            if DictAccSal[i].type == "TrapAbiertaIzquierda":
                Base = DictAccSal[i]
                AccDict[i] = TrapAbiertaIzquierda("TrapIzquierdaTruncada", Base.var,
                                                     [Base.inicio, Base.medio,
                                                      Base.fin],
                                                     AccionConorma[i])
            elif DictAccSal[i].type == "TrapAbiertaDerecha":
                Base = DictAccSal[i]
                AccDict[i] = TrapAbiertaDerecha("TrapDerechaTruncada", Base.var,
                                                   [Base.inicio, Base.medio, Base.fin],
                                                   AccionConorma[i])
            elif DictAccSal[i].type == "Trapezoidal":
                Base = DictAccSal[i]
                AccDict[i] = Trapezoidal('TrapTruncada', Base.var,
                                            [Base.inicio, Base.medio1, Base.medio2, Base.fin],
                                            AccionConorma[i])
            elif DictAccSal[i].type == "Triangular":
                Base = DictAccSal[i]
                AccDict[i] = Triangular('TriangularTruncada', Base.var,
                                           [Base.inicio, Base.medio, Base.fin],
                                           AccionConorma[i])

    elif Tipo == "Truncado":
        for i in AccionConorma.keys():
            if DictAccSal[i].type == "TrapAbiertaIzquierda":
                Base = DictAccSal[i]
                medio = Base.evalx(AccionConorma[i])
                AccDict[i] = TrapAbiertaIzquierda("TrapIzquierdaTruncada", Base.var,
                                                     [Base.inicio, medio, Base.fin],
                                                     altura=AccionConorma[i])
            elif DictAccSal[i].type == "TrapAbiertaDerecha":
                Base = DictAccSal[i]
                medio = Base.evalx(AccionConorma[i])
                AccDict[i] = TrapAbiertaDerecha("TrapDerechaTruncada", Base.var,
                                                   [Base.inicio, medio, Base.fin],
                                                   altura=AccionConorma[i])
            elif DictAccSal[i].type == "Trapezoidal":
                Base = DictAccSal[i]
                medio1, medio2 = Base.evalx(AccionConorma[i])
                AccDict[i] = Trapezoidal('TrapTruncada', Base.var,
                                            [Base.inicio, medio1, medio2, Base.fin],
                                            altura=AccionConorma[i])
            elif DictAccSal[i].type == "Triangular":
                Base = DictAccSal[i]
                medio1, medio2 = Base.evalx(AccionConorma[i])
                AccDict[i] = Trapezoidal('TriangularTruncada', Base.var,
                                            [Base.inicio, medio1, medio2, Base.fin],
                                            altura=AccionConorma[i])
    Areas = []
    Centroides = []

    for i in AccDict.keys():
        Base = AccDict[i]
        Areas.extend(Base.areas())
        Centroides.extend(Base.centroides())

    XA = [a * b for a, b in zip(Areas, Centroides)]
    XA = sum(XA)
    # print(XA)
    SA = sum(Areas)
    # print(SA)
    value = round(XA / SA, 3)

    cerror = np.abs(value-objective)/aVar.rng
    # print(cerror)
    return cerror

def partialc(AccionDict, DictAccSal, objective):
    # print('Partial contribution')
    AccionConorma = deepcopy(AccionDict)
    AccDict = deepcopy(AccionDict)
    # print("AccionConorma", AccionConorma)

    # El diccionario AccionConorma contiene el valor de corte para cada uno de los conjuntos difusos a la salida
    # print("AccionConorma\n \n", AccionConorma, "\n")

    # Determinación del tipo de salida Escalado o Truncado
    Tipo = "Truncado"
    if Tipo == "Escalado":
        for i in AccionConorma.keys():
            for j in AccionConorma[i]:
                if DictAccSal[i].type == "TrapAbiertaIzquierda":
                    Base = DictAccSal[i]
                    AccDict[i][j] = TrapAbiertaIzquierda("TrapIzquierdaTruncada", Base.var,
                                                         [Base.inicio, Base.medio,
                                                          Base.fin],
                                                         AccionConorma[i][j])
                elif DictAccSal[i].type == "TrapAbiertaDerecha":
                    Base = DictAccSal[i]
                    AccDict[i][j] = TrapAbiertaDerecha("TrapDerechaTruncada", Base.var,
                                                       [Base.inicio, Base.medio, Base.fin],
                                                       AccionConorma[i][j])
                elif DictAccSal[i].type == "Trapezoidal":
                    Base = DictAccSal[i]
                    AccDict[i][j] = Trapezoidal('TrapTruncada', Base.var,
                                                [Base.inicio, Base.medio1, Base.medio2, Base.fin],
                                                AccionConorma[i][j])
                elif DictAccSal[i].type == "Triangular":
                    Base = DictAccSal[i]
                    AccDict[i][j] = Triangular('TriangularTruncada', Base.var,
                                               [Base.inicio, Base.medio, Base.fin],
                                               AccionConorma[i][j])

    elif Tipo == "Truncado":
        for i in AccionConorma.keys():
            # print("here ", AccionConorma[i])
            # print(DictAccSal[i])
            for j in range(len(AccionConorma[i])):
                # print(j)
                if DictAccSal[i].type == "TrapAbiertaIzquierda":
                    Base = DictAccSal[i]
                    # print(AccionConorma[i][j])
                    medio = Base.evalx(AccionConorma[i][j])
                    AccDict[i][j] = TrapAbiertaIzquierda("TrapIzquierdaTruncada", Base.var,
                                                         [Base.inicio, medio, Base.fin],
                                                         altura=AccionConorma[i][j])
                elif DictAccSal[i].type == "TrapAbiertaDerecha":
                    Base = DictAccSal[i]
                    medio = Base.evalx(AccionConorma[i][j])
                    AccDict[i][j] = TrapAbiertaDerecha("TrapDerechaTruncada", Base.var,
                                                       [Base.inicio, medio, Base.fin],
                                                       altura=AccionConorma[i][j])
                elif DictAccSal[i].type == "Trapezoidal":
                    Base = DictAccSal[i]
                    medio1, medio2 = Base.evalx(AccionConorma[i][j])
                    AccDict[i][j] = Trapezoidal('TrapTruncada', Base.var,
                                                [Base.inicio, medio1, medio2, Base.fin],
                                                altura=AccionConorma[i][j])
                elif DictAccSal[i].type == "Triangular":
                    Base = DictAccSal[i]
                    medio1, medio2 = Base.evalx(AccionConorma[i][j])
                    AccDict[i][j] = Trapezoidal('TriangularTruncada', Base.var,
                                                [Base.inicio, medio1, medio2, Base.fin],
                                                altura=AccionConorma[i][j])
    Areas = []
    Centroides = []

    for i in AccDict.keys():
        for j in range(len(AccDict[i])):
            # print(j)
            Base = AccDict[i][j]
            Areas.extend(Base.areas())
            Centroides.extend(Base.centroides())

    perror = []
    for i in Centroides:
        perror.append(np.abs(objective - i)/aVar.rng)
    # print(Centroides)
    # print(sum(perror))

    # XA = [a * b for a, b in zip(Areas, Centroides)]
    # XA = sum(XA)
    # # print(XA)
    # SA = sum(Areas)
    # # print(SA)
    # value = round(XA / SA, 3)
    # print(value)
    # return value
    return np.mean(perror)


controller(150, 80, 31.443)
end = time.time()

print("The time of execution of above program is :", (end - start)*10**3, "ms")
