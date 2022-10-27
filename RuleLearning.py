#!/usr/bin/env python3
import time
from DefaultStructure import *
from BackProp import *
import FuzzyControllerGuide as FCG
from threading import Thread


def controller(tempvalue, presvalue, objective):
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

    # print(DicTemp)
    # print(DicPres)

    DicVal = deepcopy(rules)

    for i in DicVal.keys():
        tempdic = {}
        for j in DicVal[i].keys():
            # print(DicPres[i])
            value1 = DicPres[i]
            value2 = DicTemp[j]
            tempdic[j] = [value1, value2]
        DicVal[i] = tempdic
    # print("DicVal\n \n ", DicVal, "\n")

    DicValIntersec = deepcopy(DicVal)
    # print(DicValIntersec)

    for i in DicVal.keys():
        for j in DicVal[i].keys():
            inter = Intersecciones.zadeh(DicValIntersec[i][j])
            DicValIntersec[i][j] = inter
    # print("DictValIntersec\n \n", DicValIntersec, "\n")

    # Dejando unicamente las reglas que se activan
    for i in DicValIntersec.copy():
        DicValIntersec[i] = {x: y for x, y in DicValIntersec[i].items() if y != 0}
        if not DicValIntersec[i]:
            DicValIntersec.pop(i)

    # print("New \n", DicValIntersec)
    # TODO Standarization of the output variables, lists and dictionaries

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

    AccionDict = dict(zip(aVar.labels, SalAcc))
    # print("AccionDict\n \n", AccionDict, "\n")

    rulesc = deepcopy(DicValIntersec)
    ruleslist = []

    for i in DicValIntersec.keys():
        for j in DicValIntersec[i].keys():
            rulesc[i][j] = [DicValIntersec[i][j]] * 7
            ruleslist.append([DicValIntersec[i][j]] * 7)
    # print(ruleslist)
    counter = 0
    # ex es una ejemplo de las posibles funciones de pertenencia a la salida
    ex = aVar.labels
    totalComb = []
    global totalError, cError, pError
    totalError = []
    cError = []
    pError = []
    print(len(ruleslist))
    # TODO cambiar el código para cuando las pertenencias son diferentes de 4
    for i in range(len(ruleslist[0])):
        # print(ruleslist[0])
        try:
            for j in range(len(ruleslist[1])):
                # print(ruleslist[1])
                try:
                    for k in range(len(ruleslist[2])):
                        # print(ruleslist[2])
                        try:
                            for m in range(len(ruleslist[3])):
                                # print(ruleslist[3])
                                Acc = deepcopy(AccionDict)
                                Acc[ex[i]].append(ruleslist[0][i])
                                Acc[ex[j]].append(ruleslist[1][j])
                                Acc[ex[k]].append(ruleslist[2][k])
                                Acc[ex[m]].append(ruleslist[3][m])
                                counter += 1
                                totalComb.append(Acc)
                                tcon = totalc(Acc, DictAccSal, objective)
                                pcon = partialc(Acc, DictAccSal, objective)
                                cError.append(tcon)
                                pError.append(pcon)
                                totError = tcon
                                totalError.append(totError)
                        except IndexError:
                            if tot <=175:
                                Acc = deepcopy(AccionDict)
                                Acc[ex[i]].append(ruleslist[0][i])
                                Acc[ex[j]].append(ruleslist[1][j])
                                Acc[ex[k]].append(ruleslist[2][k])
                                counter += 1
                                totalComb.append(Acc)
                                tcon = totalc(Acc, DictAccSal, objective)
                                pcon = partialc(Acc, DictAccSal, objective)
                                cError.append(tcon)
                                pError.append(pcon)
                                totError = tcon
                                totalError.append(totError)
                            else:
                                pass
                except IndexError:
                    if tot <=175:
                        Acc = deepcopy(AccionDict)
                        Acc[ex[i]].append(ruleslist[0][i])
                        Acc[ex[j]].append(ruleslist[1][j])
                        counter += 1
                        totalComb.append(Acc)
                        tcon = totalc(Acc, DictAccSal, objective)
                        pcon = partialc(Acc, DictAccSal, objective)
                        cError.append(tcon)
                        pError.append(pcon)
                        totError = tcon
                        totalError.append(totError)
                    else:
                        pass
        except IndexError:
            if tot <= 175:
                Acc = deepcopy(AccionDict)
                Acc[ex[i]].append(ruleslist[0][i])
                counter += 1
                totalComb.append(Acc)
                tcon = totalc(Acc, DictAccSal, objective)
                pcon = partialc(Acc, DictAccSal, objective)
                cError.append(tcon)
                pError.append(pcon)
                totError = tcon
                totalError.append(totError)
            else:
                pass

    rulesl = deepcopy(rulesc)
    # try:
    #     plotting()
    # except IndexError:
    #     pass
    for i in rulesl.keys():
        for j in rulesl[i].keys():
            rulesl[i][j] = []
    c = 0



    for i in range(len(totalError)):
        # print(i)
        # if totalError[i] <= np.mean(totalError):
        # if totalError[i] <= 0.1:
        objlist = [objective] * len(cError)
        rui = [np.abs(e1 - e2) for e1, e2 in zip(objlist, cError)]
        if np.sign(cError[i]) == np.sign(objective): # and np.abs(cError[i]-objective) <= np.quantile(rui, 0.05):
            oblist = [objective] * len(pError[i])
            res = [np.abs(e1 - e2) for e1, e2 in zip(oblist, pError[i])]
            for j in pError[i]:
                if np.sign(j) == np.sign(objective): # and np.abs(j-objective) <= np.quantile(rui, 0.025):
                    print(j, objective)
                    # print("change")
                    rulesl = getrule(i, ruleslist, rulesl, ex)
                    c += 1
    # print(c)
    # print(rulesl)
    # print(rules)

    for i in rulesl.keys():
        temp = deepcopy(rules[i])
        for j in rulesl[i].keys():
            # print(rules[i][j])
            if len(rulesl[i][j]) != 0:
                t = []
                for k in rulesl[i][j]:
                    if k in temp[j]:
                        t.append(k)
                if len(t) != 0:
                    temp[j] = t
        rules[i] = temp

    # print(rulesl)
    print(rules)



def plotting():
    fig, axs = plt.subplots(2, 2)
    fig.suptitle('Error distribution analysis')

    sns.lineplot(ax=axs[0, 0], x=range(len(totalError)), y=totalError)
    axs[0, 0].set_title("Total Error Lineplot")
    axs[0, 0].set_xlabel("Total Error")
    axs[0, 0].set_ylabel("Count")

    sns.histplot(ax=axs[0, 1], x=totalError, kde=True)
    axs[0, 1].axvline(x=np.mean(totalError), color='b', label='Mean Error')
    axs[0, 1].axvline(x=np.quantile(totalError, [0.25]), color='g', label='First Quantile')
    axs[0, 1].set_title("Total Error Distribution")
    axs[0, 1].set_xlabel("Combination")
    axs[0, 1].set_ylabel("Total Error")
    axs[0, 1].legend(bbox_to_anchor=(1.0, 1), loc='best')

    sns.boxplot(ax=axs[1, 0], y=totalError)
    axs[1, 0].set_title("Total Error Boxplot")
    axs[1, 0].set_xlabel("Array")
    axs[1, 0].set_ylabel("Total Error")

    sns.violinplot(ax=axs[1, 1], y=totalError)
    axs[1, 1].set_title("Total Error Violinplot")
    axs[1, 1].set_xlabel("Array")
    axs[1, 1].set_ylabel("Total Error")

    print("1st Quantile", np.quantile(totalError, [0.25]))
    print("media", np.mean(totalError))
    print(min(totalError))
    print(max(totalError))

    plt.show()


def getrule(ind, ruleslist, rulesl, ex):
    power = len(ruleslist)
    base = len(aVar.labels)
    cons = []
    for i in range(power-1, -1, -1):
        # print(i)
        val = ind/base**i
        val = int(np.ceil(val))-1
        cons.append(ex[val])
        ind = ind % base**i
    # print(cons)
    # print(rulesl)
    counter = 0
    for i in rulesl.keys():
        for j in rulesl[i].keys():
            if cons[counter] not in rulesl[i][j]:
                rulesl[i][j].append(cons[counter])
            counter += 1

    # print(rulesl)
    return rulesl


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
                AccDict[i] = TrapAbiertaIzquierda("TrapIzquierdaTruncada", Base.var, [Base.inicio, Base.medio, Base.fin],
                                                     AccionConorma[i])
            elif DictAccSal[i].type == "TrapAbiertaDerecha":
                Base = DictAccSal[i]
                AccDict[i] = TrapAbiertaDerecha("TrapDerechaTruncada", Base.var, [Base.inicio, Base.medio, Base.fin],
                                                   AccionConorma[i])
            elif DictAccSal[i].type == "Trapezoidal":
                Base = DictAccSal[i]
                AccDict[i] = Trapezoidal('TrapTruncada', Base.var, [Base.inicio, Base.medio1, Base.medio2, Base.fin],
                                            AccionConorma[i])
            elif DictAccSal[i].type == "Triangular":
                Base = DictAccSal[i]
                AccDict[i] = Triangular('TriangularTruncada', Base.var, [Base.inicio, Base.medio, Base.fin],
                                           AccionConorma[i])

    elif Tipo == "Truncado":
        for i in AccionConorma.keys():
            if DictAccSal[i].type == "TrapAbiertaIzquierda":
                Base = DictAccSal[i]
                medio = Base.evalx(AccionConorma[i])
                AccDict[i] = TrapAbiertaIzquierda("TrapIzquierdaTruncada", Base.var, [Base.inicio, medio, Base.fin],
                                                     altura=AccionConorma[i])
            elif DictAccSal[i].type == "TrapAbiertaDerecha":
                Base = DictAccSal[i]
                medio = Base.evalx(AccionConorma[i])
                AccDict[i] = TrapAbiertaDerecha("TrapDerechaTruncada", Base.var, [Base.inicio, medio, Base.fin],
                                                   altura=AccionConorma[i])
            elif DictAccSal[i].type == "Trapezoidal":
                Base = DictAccSal[i]
                medio1, medio2 = Base.evalx(AccionConorma[i])
                AccDict[i] = Trapezoidal('TrapTruncada', Base.var, [Base.inicio, medio1, medio2, Base.fin],
                                            altura=AccionConorma[i])
            elif DictAccSal[i].type == "Triangular":
                Base = DictAccSal[i]
                medio1, medio2 = Base.evalx(AccionConorma[i])
                AccDict[i] = Trapezoidal('TriangularTruncada', Base.var, [Base.inicio, medio1, medio2, Base.fin],
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

    cerror = value
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
        perror.append(i)

    return perror


def probe():
    ob = np.ones(25)
    length = np.zeros_like(ob)
    counter = 0
    for i in rules.keys():
        for j in rules[i].keys():
            val = len(rules[i][j])
            length[counter] = val
            counter += 1
    tot = np.dot(length, ob)
    print(np.dot(length, ob))
    return all(ob ==length)

def outerLoop():
    rul = deepcopy(rules)
    tRange = tVar.rang
    pRange = pVar.rang
    while probe() != True:
        tempValues = np.random.uniform(tRange[0], tRange[1])
        presValues = np.random.uniform(pRange[0], pRange[1])
        actionValues = FCG.controller(tempValues, presValues)
        controller(tempValues, presValues, actionValues)
    print(rul)
    print(rules)


def outerloop(samples):
    rul = deepcopy(rules)
    tRange = tVar.rang
    pRange = pVar.rang
    tempValues = np.random.randint(tRange[0], tRange[1], [samples])
    presValues = np.random.randint(pRange[0], pRange[1], [samples])
    actionValues = [FCG.controller(tempValues[i], presValues[i]) for i in range(samples)]
    #print(actionValues)
    for i in range(samples):
        controller(tempValues[i], presValues[i], actionValues[i])
        print("Loop", i)
    print(rul)
    print(rules)

# controller(150, 80, 31.443)
# outerloop(100)
# probe()

if __name__ == '__main__':
    start = time.time()
    global tot
    tot = 175
    tVar = FuzzyVariable(name="Temperature", rang=[100, 340], labels=["Fria", "Fresca", "Normal", "Tibia", "Caliente"])
    pVar = FuzzyVariable(name='Pressure', rang=[10, 250], labels=["Escasa", "Baja", "Bien", "Fuerte", "Alta"])
    aVar = FuzzyVariable(name='Action', rang=[-60, 60], labels=["NG", "NM", "NP", "CE", "PP", "PM", "PG"])
    Rules = RuleGenerator([pVar, tVar, aVar])
    rules = Rules.gencomb()
    # print(rules)
    # rules = {'Escasa': {'Fria': ['PM', 'PG'], 'Fresca': ['PM', 'PG'], 'Normal': ['PP', 'PM', 'PG'], 'Tibia': ['PP', 'PM', 'PG'], 'Caliente': ['CE', 'PP', 'NP']}, 'Baja': {'Fria': ['PP', 'PM', 'PG'], 'Fresca': ['PP', 'PM'], 'Normal': ['CE', 'PP'], 'Tibia': ['CE', 'NP'], 'Caliente': ['CE', 'PP', 'NP']}, 'Bien': {'Fria': ['CE', 'PP', 'NP'], 'Fresca': ['CE', 'NP'], 'Normal': ['CE', 'NP'], 'Tibia': ['NP', 'NM'], 'Caliente': ['NP', 'NM', 'NG']}, 'Fuerte': {'Fria': ['NM', 'NP', 'CE'], 'Fresca': ['NG', 'NM', 'NP'], 'Normal': ['NM', 'NP'], 'Tibia': ['NG', 'NM', 'NP'], 'Caliente': ['NG', 'PG']}, 'Alta': {'Fria': ['NG', 'NM', 'NP'], 'Fresca': ['NG', 'NM'], 'Normal': ['PG', 'NG', 'NM', 'NP'], 'Tibia': ['PG', 'NG'], 'Caliente': ['PG', 'NG', 'NM', 'NP']}}
    outerLoop()
    end = time.time()

    print("The execution time is :", (end - start)*10**3, "ms")
