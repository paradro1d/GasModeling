import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from celluloid import Camera

with open('output.txt') as f:
    data = f.read().split(' ')

with open('speeds.txt') as f:
    speeds = f.read().split(' ')

num = int(data[0])
dt = float(data[1])
t= int((len(data) - 2)/num/3)

sp_data = [[0 for i in range(num)] for i in range(t)]

a = 0 
b = 40 
for i in range(t):
    for j in range(num):
        sp_data[i][j] = abs(float(speeds[i*num + j]))

fig = plt.figure()
camera = Camera(fig)

def hist(arr, num, a, b):
    l = len(arr)
    output = [0 for i in range(num)]
    for j in range(num):
        for i in arr:
            if (a + (b - a)/num*j <= i < a + (b - a)/num*(j+1)):
                output[j] += 1
    k = 1/l/(b-a)*num
    for i in range(num):
        output[i] = output[i]*k
    return output

n = 13

x = [a + (b-a)/n*(0.5 + i) for i in range(n)]
x1 = np.linspace(a, b, 100)

def maxwell(x, a):
    return 4*a**1.5/np.sqrt(np.pi)*x*x*np.exp(-a*x**2)

x2 = [dt*i for i in range(0, t, 50)]
count = []
al_arr = []

for i in range(0, t, 50):
    plt.subplot(3, 2, 1)
    out = hist(sp_data[i], n, a, b)
    alpha = curve_fit(maxwell, x, out, p0=0)[0][0]
    al_arr.append(alpha)
    y1 = [maxwell(x1[j], alpha) for j in range(len(x1))]
    plt.plot(x, out,'ro', x1, y1, 'b')
    count.append(0)
    for j in range(n):
        count[int(i/50)] += (out[j] - maxwell(x[j], alpha))**2
    plt.subplot(3, 1, 2)
    plt.plot(x2[0:int(i/50)+1], count, 'b')
    plt.subplot(3, 2, 2)
    x_ = [k*k*np.exp(-alpha*k**2) for k in x]
    x1_ = [k*k*np.exp(-alpha*k**2) for k in x1]
    plt.plot(x_, out, 'ro', x1_, y1, 'b')
    plt.subplot(3, 1, 3)
    plt.plot(x2[0:int(i/50)+1], al_arr, 'b')
    camera.snap()


an = camera.animate(interval=int(dt*50000))
an.save('Распределение_по_скоростям.gif')
