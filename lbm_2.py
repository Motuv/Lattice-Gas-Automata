from math import sqrt
from PIL import Image

frames = []

ITERATIONS = 100
SIZE = 128
CONDITION = 50
DIFFCOEF = 0.1

ci = [[0,0], [1,0], [-1,0], [0,1], [0,-1], [1,1], [-1,1], [-1,-1], [1,-1]]
wi = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36]

class komorka:
    barrier = 0
    v = [0,0]
    d = 1
    fin = [0,0,0,0,0,0,0,0,0]
    fout = [0,0,0,0,0,0,0,0,0]
    feq = [0,0,0,0,0,0,0,0,0]

def eq(kom):
    c = [0,0,0,0,0,0,0,0,0]
    for k in range(9):
        help = ci[k][0]*kom.v[0]+ci[k][1]*kom.v[1]
        u2 = kom.v[0]*kom.v[0]+kom.v[1]*kom.v[1]
        c[k] = wi[k]*kom.d*(1+(3*help)+(4.5*help*help)-(1.5*u2))
    return c

#streaming zarówno gęstości jak i prędkości
def streaming(i, j, gt, ga):
    ax = i - 1
    bx = i + 1
    ay = j - 1
    by = j + 1
    if ga[i][j].barrier == 1:
        gt[i][j].fin[0] = 1
        gt[i][j].fin[1] = 1
        gt[i][j].fin[2] = 1
        gt[i][j].fin[3] = 1
        gt[i][j].fin[4] = 1
        gt[i][j].fin[5] = 1
        gt[i][j].fin[6] = 1
        gt[i][j].fin[7] = 1
        gt[i][j].fin[8] = 1
    else:
        gt[i][j].fin[0] = ga[i][j].fout[0]
        gt[i][j].fin[1] = ga[ax][j].fout[1]
        gt[i][j].fin[2] = ga[bx][j].fout[2]
        gt[i][j].fin[3] = ga[i][by].fout[3]
        gt[i][j].fin[4] = ga[i][ay].fout[4]
        gt[i][j].fin[5] = ga[ax][by].fout[5]
        gt[i][j].fin[6] = ga[bx][by].fout[6]
        gt[i][j].fin[7] = ga[bx][ay].fout[7]
        gt[i][j].fin[8] = ga[ax][by].fout[8]


def collision(kom):
    for k in range(9):
        kom.fout[k]=kom.fin[k]+DIFFCOEF*(kom.feq[k]-kom.fin[k])


#glowny program
gasAutomata = [[komorka for j in range(SIZE)] for i in range(SIZE)]

for i in range(SIZE):
    for j in range(SIZE):
        if i == 0 or j==0 or i == SIZE-1 or j == SIZE-1:
            gasAutomata[i][j].barrier = 1
            gasAutomata[i][j].v[0] = 0
            gasAutomata[i][j].v[1] = 0.02-((i/SIZE)*0.02)

for i in range(SIZE):
    for j in range(SIZE):
        gasAutomata[i][j].fin = eq(gasAutomata[i][j])


gasTemp = [[komorka for j in range(SIZE)] for i in range(SIZE)]
for z in range(ITERATIONS):
    image_temp = Image.new('RGB', (SIZE, SIZE), (0, 0, 0))
    threads = []
    for i in range(SIZE):
        for j in range(SIZE):
            gasTemp[i][j].d = sum(gasTemp[i][j].fin)
            u = [0, 0]
            for y in range(9):
                u[0] += gasTemp[i][j].fin[y] * ci[y][0]
                u[1] += gasTemp[i][j].fin[y] * ci[y][1]
            gasTemp[i][j].v[0] = u[0] / gasTemp[i][j].d
            gasTemp[i][j].v[1] = u[1] / gasTemp[i][j].d
            gasTemp[i][j].feq = eq(gasTemp[i][j])

            collision(gasTemp[i][j])
            streaming(i, j, gasTemp, gasAutomata)
            image_temp.putpixel((i, j), (int((gasTemp[i][j].v[1]) * 255 * 50), 0, 0))
    print(z)
    frames.append(image_temp)
    gasAutomata = gasTemp

frames[0].save('lbm_2.gif', format='GIF', append_images=frames[1:], save_all=True, duration=10, loop=0)
