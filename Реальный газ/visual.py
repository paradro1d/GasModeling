import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from celluloid import Camera

with open('output.txt') as f:
    data = f.read().split(' ')

with open('speeds.txt') as f:
    speeds = f.read().split(' ')

num = int(data[0])
dt = float(data[1])
t= int((len(data) - 2)/num/3)
x_coord = [[0 for i in range(num)]  for i in range(t)]
y_coord = [[0 for i in range(num)]  for i in range(t)]
z_coord = [[0 for i in range(num)]  for i in range(t)]

for i in range(t):
    for j in range(num):
        x_coord[i][j] = float(data[2+ num*3*i + 3*j])
        y_coord[i][j] = float(data[3+ num*3*i + 3*j])
        z_coord[i][j] = float(data[4+ num*3*i + 3*j])

fig = plt.figure()
ax = p3.Axes3D(fig)

camera = Camera(fig)
for i in range(0, t, 50):
    plt.plot(x_coord[i], y_coord[i], z_coord[i], 'ro')
    camera.snap()

an = camera.animate(interval=int(dt*50000))
an.save('Анимация_движения.gif')
