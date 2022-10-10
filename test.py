#!/usr/bin/env python3
import BackProp
import FuzzyControllerGuide
import TestDefault

TempValue = 150
PresValue = 80

o_d = FuzzyControllerGuide.controller(TempValue, PresValue)
activation, o_f, variables, act_accion = TestDefault.controller(TempValue, PresValue)
rang = 60 - (-60)
# print(rang)
print(round(o_d - o_f, 2))
print(o_d)
print(o_f)
bperror = BackProp.ErrorComputation()
E = bperror.error(o_d, o_f, 2, rang)
s = bperror.sgn(o_f, o_d)
print(E, s)
print(activation)
print(act_accion)
only_act = {}
acr = {}
for key, val in variables.items():
    if val.ind is None:
        continue
    else:
        print(key)
        print(val.ind)
        only_act[key] = act_accion[key]
        acr[key] = val.ind
        # print(val.centroides())
        # print(val.areas())
print(only_act)
print(acr)

print((o_f - acr['PM'])/rang, (o_f - acr['PG'])/rang)
