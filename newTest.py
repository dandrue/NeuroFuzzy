#!/usr/bin/env python3
from DefaultStructure import *
from BackProp import *

xVar = FuzzyVariable(name='x', rang=[-10, 10])
yVar = FuzzyVariable(name='y', rang=[-12, 10])
Rules = RuleGenerator([xVar, yVar])
rules = Rules.gencomb()
print(rules)
print(list(zip(rules)))

xVar.plotting()
yVar.plotting()
