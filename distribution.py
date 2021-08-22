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

a = 15
b = 150 
for i in range(t):
    for j in range(num):
        sp_data[i][j] = abs(float(speeds[i*num + j]))

fig = plt.figure()
camera = Camera(fig)

def hist(arr, num, a, b):
    output = [0 for i in range(num)]
    for j in range(num):
        for i in arr:
            if (a + (b - a)/num*j < i < a + (b - a)/num*(j+1)):
                output[j] += 1
    k = 1/sum(output)/(b-a)*num
    for i in range(num):
        output[i] = output[i]/k
    return output
n = 15

x = [a + (b-a)/num*(0.5 + i) for i in range(n)]
x1 = np.linspace(a, b)

def maxwell(x, a):
    return 4*a**1.5/3/sqrt(np.pi)*x*x*np.exp(-ax^2)

for i in range(0, t, 50):
    out = hist(sp_data[i], n, a, b)
    alpha, = curve_fit(maxwell, x, out)
    y1 = [maxwell(x1[i], alpha) for i in range(len(x1))]
    plt.plot(x, out,'ro', x1, y1)
    camera.snap()
    


an = camera.animate(interval=int(dt*50000))
an.save('Распределение_по_скоростям.gif')
