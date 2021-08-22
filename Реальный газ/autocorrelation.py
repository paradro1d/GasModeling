from matplotlib import pyplot as plt
with open('output.txt') as f:
    data = f.read().split(' ')

with open('speeds.txt') as f:
    speeds = f.read().split(' ')

with open('speed_prods.txt') as f:
    sp_pr = f.read().split(' ')

num = int(data[0])
dt = float(data[1])
t = int((len(data) - 2)/num/3)

cut = int(t*8/10)
t_0 = t - cut

sp_x = [[0 for i in range(num)] for i in range(cut)]
sp_y = [[0 for i in range(num)] for i in range(cut)]
sp_z = [[0 for i in range(num)] for i in range(cut)]

a = 15
b = 150

for i in range(cut):
    for j in range(num):
        sp_x[i][j] = float(sp_pr[i*num*3 + 3*j])
        sp_y[i][j] = float(sp_pr[1 + i*num*3 + 3*j])
        sp_z[i][j] = float(sp_pr[2+ i*num*3 + 3*j])

time = [dt*i for i in range(cut)]

out = [0 for i in range(cut)]

integral = 0

for i in range(cut):
    for j in range(num):
        out[i] += sp_x[i][j]*sp_x[0][j] + sp_y[i][j]*sp_y[0][j] + sp_z[i][j]*sp_z[0][j]
    out[i] = out[i]/num
    integral += out[i]*dt/3

plt.plot(time, out, label='D = ' + str(integral))
plt.legend(loc='lower right')
plt.show()
