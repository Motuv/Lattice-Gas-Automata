import random
from PIL import Image

frames = []

ITERATIONS = 1000
SIZE = 100
CONDITION = 10
def streaming(i, j, gt):
    ax = i - 1
    bx = i + 1
    ay = j - 1
    by = j + 1
    komorka = [0, 0, 0, 0]
    if gt[ax][j][2] == 2:
        komorka[0] = gt[i][j][2]
    else:
        komorka[0] = gt[ax][j][0]

    if gt[bx][j][2] == 2:
        komorka[2] = gt[i][j][0] == 1
    else:
        komorka[2] = gt[bx][j][2]

    if gt[i][ay][2] == 2:
        komorka[1] = gt[i][j][3]
    else:
        komorka[1] = gt[i][ay][1]

    if gt[i][by][2] == 2:
        komorka[3] = gt[i][j][1]

    else:
        komorka[3] = gt[i][by][3]
    return komorka


def collision(i, j, gt):
    komorka = gt[i][j]
    if gt[i][j][0] == 1 and gt[i][j][2] == 1 and gt[i][j][1] == 0 and gt[i][j][3] == 0:
        komorka[0] = 0
        komorka[2] = 0
        komorka[1] = 1
        komorka[3] = 1
    elif gt[i][j][0] == 0 and gt[i][j][2] == 0 and gt[i][j][1] == 1 and gt[i][j][3] == 1:
        komorka[0] = 1
        komorka[2] = 1
        komorka[1] = 0
        komorka[3] = 0
    return komorka


gasAutomata = [[[0 for k in range(4)] for j in range(SIZE)] for i in range(SIZE)]

for i in range(SIZE):
    for j in range(SIZE):
        for k in range(4):
            if i == 0 or j==0 or i == SIZE-1 or j == SIZE-1 or (i==32 and (j<50 or j>70)):
                gasAutomata[i][j][k] = 2
            else:
                if 0<i<30 and 0<j<SIZE-1:
                    if k*random.randint(0,100) >= CONDITION:
                        gasAutomata[i][j][k] = 1


for z in range(ITERATIONS):
    gasTemp = [[[0 for k in range(4)] for j in range(SIZE)] for i in range(SIZE)]
    image_temp = Image.new('RGB', (2*SIZE, 2*SIZE), (0, 0, 0))
    for i in range(SIZE):
        for j in range(SIZE):
            if i==0 or j==0 or i==SIZE-1 or j==SIZE-1 or (i==32 and  (j<50 or j>70)):
                gasTemp[i][j] = [2,2,2,2]
                image_temp.putpixel((2 * i, 2 * j), (255,255,255))
                image_temp.putpixel(((2 * i) + 1, 2 * j), (255,255,255))
                image_temp.putpixel((2 * i, (2 * j) + 1), (255,255,255))
                image_temp.putpixel(((2 * i) + 1, (2 * j) + 1), (255,255,255))
            else:
                gasTemp[i][j] = streaming(i, j, gasAutomata)
                gasTemp[i][j] = collision(i, j, gasTemp)
                image_temp.putpixel((2 * i, 2 * j), (gasTemp[i][j][0] * 255, 0, 0))
                image_temp.putpixel(((2 * i) + 1, 2 * j), (gasTemp[i][j][1] * 255, 0, 0))
                image_temp.putpixel((2 * i, (2 * j) + 1), (gasTemp[i][j][2] * 255, 0, 0))
                image_temp.putpixel(((2 * i) + 1, (2 * j) + 1), (gasTemp[i][j][3] * 255, 0, 0))

    frames.append(image_temp)
    gasAutomata = gasTemp
    if z==1:
        image_temp.save('lga_start.jpg', format='jpeg')
frames[0].save('lga.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)