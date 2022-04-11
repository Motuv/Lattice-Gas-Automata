from PIL import Image

frames = []

ITERATIONS = 1000
SIZE = 128
CONDITION = 50
DIFFCOEF = 0.1

def condensation(kom):
    c = 0
    for k in range(4):
        c += kom[k]
    return c

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
        komorka[2] = gt[i][j][0]
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
    c = condensation(komorka)
    for k in range(4):
        komorka[k] = komorka[k]+(DIFFCOEF*(c/4-komorka[k]))
    return komorka

def threadFunction(img, gt, i, j):
    if i == 0 or j == 0 or i == SIZE - 1 or j == SIZE - 1 or (i==32 and (j<50 or j>70)):
        gt[i][j] = [2, 2, 2, 2]
        img.putpixel((2 * i, 2 * j), (255, 255, 255))
        img.putpixel(((2 * i) + 1, 2 * j), (255, 255, 255))
        img.putpixel((2 * i, (2 * j) + 1), (255, 255, 255))
        img.putpixel(((2 * i) + 1, (2 * j) + 1), (255, 255, 255))
    else:
        gt[i][j] = streaming(i, j, gasAutomata)
        gt[i][j] = collision(i, j, gt)
        c = condensation(gt[i][j])
        img.putpixel((2 * i, 2 * j), (int((c / 4 * 255)), 0, 0))
        img.putpixel(((2 * i) + 1, 2 * j), (int(c / 4 * 255), 0, 0))
        img.putpixel((2 * i, (2 * j) + 1), (int(c / 4 * 255), 0, 0))
        img.putpixel(((2 * i) + 1, (2 * j) + 1), (int(c / 4 * 255), 0, 0))


gasAutomata = [[[0 for k in range(4)] for j in range(SIZE)] for i in range(SIZE)]

for i in range(SIZE):
    for j in range(SIZE):
        for k in range(4):
            if i == 0 or j==0 or i == SIZE-1 or j == SIZE-1 or (i==32 and (j<50 or j>70)):
                gasAutomata[i][j][k] = 2
            else:
                if 0<i<30 and 0<j<SIZE-1:
                    #if k*random.randint(0,100) >= CONDITION:
                    gasAutomata[i][j][k] = 1


for z in range(ITERATIONS):
    gasTemp = [[[0 for k in range(4)] for j in range(SIZE)] for i in range(SIZE)]
    image_temp = Image.new('RGB', (2*SIZE, 2*SIZE), (0, 0, 0))
    threads = []
    for i in range(SIZE):
        for j in range(SIZE):
            threadFunction(image_temp, gasTemp, i, j)
    print(z)
    frames.append(image_temp)
    gasAutomata = gasTemp
    if z==1:
        image_temp.save('lga_start.jpg', format='jpeg')
frames[0].save('lbmbm.gif', format='GIF', append_images=frames[1:], save_all=True, duration=10, loop=0)
