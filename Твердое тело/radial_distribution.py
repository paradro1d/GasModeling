from matplotlib import pyplot as plt
from tqdm import tqdm
with open('output.txt') as f:
    data = f.read().split(' ')

num = int(data[0])
dt = float(data[1])
t = int((len(data) -2)/num/3)
cut = int(t*17/40)
t_0 = t - cut
x_coord = [[0 for i in range(num)] for i in range(cut)]
y_coord = [[0 for i in range(num)] for i in range(cut)]
z_coord = [[0 for i in range(num)] for i in range(cut)]

for i in range(cut):
    for j in range(num):
        x_coord[i][j] = float(data[2+num*3*(i+t_0) + 3*j])
        y_coord[i][j] = float(data[3+num*3*(i+t_0) + 3*j])
        z_coord[i][j] = float(data[4+num*3*(i+t_0) + 3*j])
output = []
weis = []

for i in tqdm(range(0, cut, 7)):
    for j in range(1, num):
        for l in range(-1, 2):
            for m in range(-1, 2):
                for n in range(-1, 2):
                    x = x_coord[i][j] + 100*l
                    y = y_coord[i][j] + 100*m
                    z = z_coord[i][j] + 100*n
                    r = ((x - x_coord[i][0])**2 + (y - y_coord[i][0])**2 + (z - z_coord[i][0])**2)**0.5
                    output.append(r)
                    weis.append(1/r/r)

plt.hist(output, bins = 500, range = (0, 100), weights = weis)
plt.show()
