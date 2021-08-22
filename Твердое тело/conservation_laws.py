from matplotlib import pyplot as plt
with open('output.txt') as f:
    data = f.read().split(' ')

with open('energy.txt') as f:
    energy_pot = f.read().split(' ')

with open('kin_en.txt') as f:
    energy_kin = f.read().split(' ')

with open('impulses.txt') as f:
    imps = f.read().split(' ')
num = int(data[0])
dt = float(data[1])
t = int((len(data) - 2)/num/3)
time = [dt*i for i in range(t)]
imp_x = [float(imps[3*i]) for i in range(t)]
imp_y = [float(imps[1 + 3*i]) for i in range(t)]
imp_z = [float(imps[2 + 3*i]) for i in range(t)]
energy_pot = [float(energy_pot[i]) for i in range(t)]
energy_kin = [float(energy_kin[i]) for i in range(t)]
energy = [energy_pot[i] + energy_kin[i] for i in range(t)]
plt.subplot(2, 2, 1)
plt.xlabel('T')
plt.ylabel('p')
plt.plot(time, imp_x, time, imp_y, time, imp_z)
plt.subplot(2, 2, 2)
plt.plot(time, energy, label='Общая энергия')
plt.plot(time, energy_kin, label='Кинетическая энергия')
plt.plot(time, energy_pot, label='Потенциальная энергия')
plt.xlabel('T')
plt.ylabel('E')
plt.legend(loc='lower right')
energy = [(energy[i] - energy[0])/energy[0] for i in range(t)]
plt.subplot(2, 2, 3)
plt.plot(time, energy, label='Относительное изменение энергии')
plt.legend(loc='lower right')
plt.subplot(2, 2, 4)
imp_x = [(imp_x[i] - imp_x[0])/imp_x[0] for i in range(t)]
imp_y = [(imp_y[i] - imp_y[0])/imp_y[0] for i in range(t)]
imp_z = [(imp_z[i] - imp_z[0])/imp_z[0] for i in range(t)]
plt.plot(time, imp_x, time, imp_y, time, imp_z)
plt.show()
