from DefaultStructure import *
from BackProp import *

# Temperature input variable
tVar = FuzzyVariable(name="Temperature", rang=[100, 340], labels=["Fria", "Fresca", "Normal", "Tibia", "Caliente"])
Temperatura = list(tVar.functions)
# keys = list(tVar.functions.keys())
# print(Temperatura)

# Pressure input variable
pVar = FuzzyVariable(name='Pressure', rang=[10, 250], labels=["Escasa", "Baja", "Bien", "Fuerte", "Alta"])
Pressure = list(pVar.functions)
# print(Pressure)

aVar = FuzzyVariable(name='Action', rang=[-60, 60], labels=["NG", "NM", "NP", "CE", "PP", "PM", "PG"])
Action = list(aVar.functions)
# print(list(aVar.mfunctions))

tVar.get_info()
pVar.get_info()
aVar.get_info()

Rules = RuleGenerator([tVar, pVar, aVar])
antecedent, totalrule = Rules.gencomb()

tVar.plotting()
pVar.plotting()
aVar.plotting()
