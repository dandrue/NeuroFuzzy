from DefaultStructure import *

# Temperature input variable
tVar = FuzzyVariable(name="Temp", rang=[100, 340])
Temperatura = list(tVar.functions.values())
# keys = list(tVar.functions.keys())
print(Temperatura)

# Pressure input variable
pVar = FuzzyVariable(name='Pre', rang=[10, 250], labels=["Escasa", "Baja", "Bien", "Fuerte", "Alta"])
Pressure = list(pVar.functions.values())
print(Pressure)

# Plotting the membership functions
fig, axs = plt.subplots(2, 2)
for i in Temperatura:
    axs[0, 0].plot(i.x, i.y)
axs[0, 0].set_ylim([0, 1.02])
axs[0, 0].grid(True)
axs[0, 0].set_title("Temperature")
axs[0, 0].set_xlabel("Temperature")
axs[0, 0].set_ylabel('Membership')

for i in Pressure:
    axs[0, 1].plot(i.x, i.y)
axs[0, 1].grid(True)
axs[0, 1].set_ylim([0, 1.02])
axs[0, 1].set_title("Pressure")
axs[0, 1].set_xlabel("Pressure")
axs[0, 1].set_ylabel('Membership')

plt.show()
