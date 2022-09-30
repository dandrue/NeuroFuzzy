import matplotlib.pyplot as plt
from FuncionesPertenencia import TrapAbiertaIzquierda, TrapAbiertaDerecha, \
    Triangular, Trapezoidal, Intersecciones, Conorma
from copy import deepcopy
import seaborn as sns
sns.set_theme()

# Definition of a constructor for input variables


class FuzzyVariable:
    """
    Definition of an input variable using a template with 6 membership functions

    Parameters
    ----------
            name: String, The name of the input function
            rang: List, The universe discurse of the variable
            labels: List, labels of the membership functions

    Returns
    -------
            Fuzzy variable constructed by default

    """
    def __init__(self, name, rang, labels=None):
        if labels is None:
            labels = ["NB", "NM", "ZZ", "PM", "PB"]
        self.name = name
        self.labels = labels
        self.rang = rang
        self.dictFunctions = self.mfcreator()
        self.functions = list(self.dictFunctions.values())
        self.mfunctions = list(self.dictFunctions.keys())

    def get_info(self):
        print("------------------------------------------------")
        print("Name = " + str(self.name))
        print("Labels = " + str(self.labels))
        print("Range = " + str(self.rang))
        print("Functions = " + str(self.mfunctions))
        ranList = []
        for i in self.functions:
            ranList.append(i.type)
        print("Functions Type = " + str(ranList))
        print("------------------------------------------------\n")

    def varcon(self):
        mfn = len(self.labels)
        secn = mfn + 1
        rang = self.rang
        start = rang[0]
        end = rang[1]
        rng = end - start
        increment = rng / secn
        rangs = []
        start_range = start
        for i in range(mfn):
            middle_range = start_range + increment
            end_range = middle_range + increment
            rangs.append([start_range, middle_range, end_range])
            start_range = middle_range

        # print(list(zip(self.labels, rangs)))
        return rangs

    def mfcreator(self):
        pre = self.name
        mf_names = []
        labels = self.labels
        varrg = self.varcon()
        for i in labels:
            mf_names.append(pre + i)
        # print(mf_names)
        functions = {}

        for i in range(len(mf_names)):
            if i == 0:
                f = TrapAbiertaIzquierda(labels[i], self.name, varrg[i])
                namef = mf_names[i]
                functions[namef] = f

            elif i == len(mf_names)-1:
                f = TrapAbiertaDerecha(labels[i], self.name, varrg[i])
                namef = mf_names[i]
                functions[namef] = f

            else:
                f = Triangular(labels[i], self.name, varrg[i])
                namef = mf_names[i]
                functions[namef] = f
        return functions

    def plotting(self):
        # Plotting the membership functions
        fig, axs = plt.subplots()
        for i in self.functions:
            axs.plot(i.x, i.y)
        axs.set_ylim([0, 1.02])
        axs.grid(True)
        axs.set_title(self.name)
        axs.set_xlabel(self.name)
        axs.set_ylabel('Membership')
        axs.legend(self.mfunctions)
        plt.show()
