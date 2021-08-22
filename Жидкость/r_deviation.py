import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

with open('output.txt') as f:
    data = f.read().split(' ')

with open('speeds.txt') as f:
    speeds = f.read().split(' ')

with open('real_output.txt') as f:
    data_real = f.read().split(' ')

avg = 0

for i in range(len(speeds) - 1):
    avg += abs(float(speeds[i]))

avg = avg/len(speeds)

num = int(data[0])
dt = float(data[1])
t = int((len(data) - 2)/num/3)
cut = int(t*3/5)
t_0 = t - cut
x_coord = [[0 for i in range(num)] for i in range(cut)]
y_coord = [[0 for i in range(num)] for i in range(cut)]
z_coord = [[0 for i in range(num)] for i in range(cut)]

for i in range(cut):
    for j in range(num):
        x_coord[i][j] = float(data_real[num*3*i + 3*j + num*3*t_0])
        y_coord[i][j] = float(data_real[1+num*3*i + 3*j + num*3*t_0])
        z_coord[i][j] = float(data_real[2+num*3*i + 3*j + num*3*t_0])

time = [dt*i for i in range(cut)]
sred_sq = [0 for i in range(cut)]

for i in range(cut):
    for j in range(num):
        sred_sq[i] += (x_coord[i][j] - x_coord[0][j])**2 +(y_coord[i][j] - y_coord[0][j])**2 + (z_coord[i][j] - z_coord[0][j])**2
    sred_sq[i] = (sred_sq[i]/num)**(0.5)

coords_x = [x_coord[i][0] for i in range(cut)]
coords_y = [y_coord[i][0] for i in range(cut)]
coords_z = [z_coord[i][0] for i in range(cut)]

fig = plt.figure()
ax = Axes3D(fig)
plt.plot(coords_x, coords_y, coords_z)
plt.show()

plt.subplot(1, 2, 1)
plt.plot(time, sred_sq)
plt.xlabel('T')
plt.ylabel('$\sigma = \sqrt{<x^2>}$')
plt.subplot(1, 2, 2)
time = [time[i]**(0.5) for i in range(cut)]
plt.plot(time, sred_sq)
plt.xlabel('$\sqrt{T}$')
plt.ylabel('$\sigma = \sqrt{<x^2>}$')
k = np.polyfit(time, sred_sq, 1)
pol = np.poly1d(k)
sred_sq = [pol(time[i]) for i in range(cut)]
plt.plot(time, sred_sq, label='$\sqrt{6D}$ = '+str(round(k[0], 1)) + ' $\Rightarrow \lambda$ = ' + str(round(k[0]**2/2/avg, 1)))
plt.legend(loc='lower right')
plt.show()

