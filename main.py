# dependencies - numpy and pillow
# after running the generator, results are stored in the output folder in root directory.
# area and copynumbers are only inputs


from itertools import product
from collections import defaultdict
import numpy as np
import random
import time
import math
from PIL import Image
from pathlib import Path


fields = [rc for rc in product(range(20), range(20))]
label = dict()
for a, b in fields:
    label[a, b] = 0

deset = dict()
for a, b in fields:
    c = a//2 * 10 + b//2
    deset[a, b] = c

desetsort = defaultdict(list)
for key, val in deset.items():
    desetsort[val].append(key)
desetsort = dict(desetsort)

pet = dict()
for a in range(100):
    c = (a//10)//2 * 5 + (a%10)//2
    pet[a] = c

petsort = defaultdict(list)
for key, val in pet.items():
    petsort[val].append(key)
petsort = dict(petsort)


def add_cells_around(mapa):
    x,y = mapa.shape
    mapa = np.reshape(mapa, (x, y))
    mapa = np.insert(mapa, 0, 0, axis=1)
    mapa = np.insert(mapa, 0, 0, axis=0)
    mapa = np.insert(mapa, x+1, 0, axis=1)
    mapa = np.insert(mapa, y+1, 0, axis=0)
    return mapa


def remove_cells_around(array):
    x,y = array.shape
    array = np.delete(array, x - 1, 0)
    array = np.delete(array, y - 1, 1)
    array = np.delete(array, 0, 0)
    array = np.delete(array, 0, 1)
    return array


def five_by_five_map(area_num):
    map_5by5 = np.zeros((5, 5), dtype=int)
    map_5by5[2, 2] = 16
    percent_of_corner_cells = math.floor(area_num * 0.6 - 15)
    list_Cn = []
    for i in range(4):
        x = random.random()
        list_Cn.append(x)
    sum_Cn = sum(list_Cn)
    placeing_Cn = list(map(lambda x: math.floor(x/sum_Cn * percent_of_corner_cells), list_Cn))
    placeing_Cn[3] = percent_of_corner_cells - sum(placeing_Cn[0:3])
    minind = placeing_Cn.index(min(placeing_Cn))
    for i in range(4):
        if placeing_Cn[i] > 49:
            placeing_Cn[i] = 49
            placeing_Cn[minind] += placeing_Cn[i] - 49
    listax = [[], [], [], []]
    if area_num > 220:
        dvaitri = 16
    else:
        dvaitri = 12
    for i in range(4):
        if placeing_Cn[i] < 17:
            listax[i] = [placeing_Cn[i],0,0,0]
        elif placeing_Cn[i] < 17 + dvaitri:
            listax[i] = [16, placeing_Cn[i]-16, 0, 0]
        elif placeing_Cn[i] < 17 + 2 * dvaitri:
            listax[i] = [16, dvaitri, placeing_Cn[i] - 16 - dvaitri, 0]
        else:
            listax[i] = [16, dvaitri, dvaitri, placeing_Cn[i] - 16 - 2 * dvaitri]
        if random.random() > 0.5:
            listax[i] = [listax[i][0],listax[i][2],listax[i][1],listax[i][3]]

    lista1 = listax[0][::-1]
    lista2 = listax[1][2:4]+listax[1][0:2]
    lista3 = (listax[2][2:4]+listax[2][0:2])[::-1]
    lista4 = listax[3]

    map_5by5[0, 0:2], map_5by5[1, 0:2] = lista1[0:2], lista1[2:4]
    map_5by5[0, 3:5], map_5by5[1, 3:5] = lista2[0:2], lista2[2:4]
    map_5by5[3, 0:2], map_5by5[4, 0:2] = lista3[0:2], lista3[2:4]
    map_5by5[3, 3:5], map_5by5[4, 3:5] = lista4[0:2], lista4[2:4]

    for i in range(1,4):
        for j in range(1,4):
            if map_5by5[i,j] == 0 and map_5by5[i+1,j] == 16 and map_5by5[i-1,j] == 16:
                if area_num - np.sum(map_5by5) > 16:                    map_5by5[i, j] = 16
                else:                    map_5by5[i,j] = 0
            elif map_5by5[i,j] == 0 and map_5by5[i,j+1] == 16 and map_5by5[i,j-1] == 16:
                if area_num - np.sum(map_5by5) > 16:                    map_5by5[i, j] = 16
                else:                    map_5by5[i, j] = 0
            elif map_5by5[i,j] == 0 and map_5by5[i+1,j] + map_5by5[i-1,j] + map_5by5[i,j+1] + map_5by5[i,j-1] > 32:
                if area_num - np.sum(map_5by5) > 12:                    map_5by5[i, j] = 12
                else:                    map_5by5[i, j] = 0
            elif map_5by5[i,j] == 0:
                if area_num - np.sum(map_5by5) > 8:                    map_5by5[i, j] = 8
                else:                    map_5by5[i, j] = 0

    map_5by5 = add_cells_around(map_5by5)
    list_of_zeros = []
    listaoko = []
    for i in range(1,6):
        for j in range(1,6):
            if map_5by5[i,j] == 0:
                list_of_zeros.append([i,j])
                listaoko.append(map_5by5[i + 1, j] + map_5by5[i - 1, j] + map_5by5[i, j + 1] + map_5by5[i, j - 1])
    nulice = {listaoko[i]: list_of_zeros[i] for i in range(len(listaoko))}
    nulice_items = nulice.items()
    sorted_nulice = sorted(nulice_items, reverse=True)
    ostatak = area_num - np.sum(map_5by5)
    nesto = [12, 8, 8, 8, 8,  4, 4, 4, 4, 2, 2, 4, 4, 4]
    nesto1 = [16, 12, 12, 8, 8, 8, 4, 4, 4, 4, 4, 4]
    nesto2 = [16, 16, 16, 12, 12, 12, 12, 12, 12, 12]
    nesto3 = [16, 16, 16, 16, 16, 16, 16, 16, 16]
    if ostatak > sum(nesto[:len(sorted_nulice)]):
        nesto = nesto1
        if ostatak > sum(nesto[:len(sorted_nulice)]):
            nesto = nesto2
            if ostatak > sum(nesto[:len(sorted_nulice)]):
                nesto = nesto3
    listaostatak = []
    for i in range(len(sorted_nulice)):
        if ostatak < nesto[i]:
            listaostatak.append(ostatak)
            ostatak = 0
        elif ostatak > 0:
            ostatak -= nesto[i]
            listaostatak.append(nesto[i])
        else:
            listaostatak.append(0)

    for i in range(len(listaostatak)):
        map_5by5[sorted_nulice[i][1][0], sorted_nulice[i][1][1]] =listaostatak[i]
    map_5by5 = remove_cells_around(map_5by5)
    if map_5by5[1,2] < 16 and map_5by5[0,2] > 0:
        x = 16 - map_5by5[1,2]
        map_5by5[1,2] = 16
        map_5by5[0,2] = map_5by5[0,2] - x
    if map_5by5[2,1] < 16 and map_5by5[2,0] > 0:
        x = 16 - map_5by5[2,1]
        map_5by5[2,1] = 16
        map_5by5[2,0] = map_5by5[2,0] - x
    if map_5by5[2, 3] < 16 and map_5by5[2, 4] > 0:
        x = 16 - map_5by5[2, 3]
        map_5by5[2, 3] = 16
        map_5by5[2, 4] = map_5by5[2, 4] - x
    if map_5by5[3, 2] < 16 and map_5by5[4, 2] > 0:
        x = 16 - map_5by5[3, 2]
        map_5by5[3, 2] = 16
        map_5by5[4, 2] = map_5by5[4, 2] - x
    print(map_5by5, np.sum(map_5by5))
    return map_5by5


def ispitivanje(a,i,j):
    a2 = []
    a2.append(a[i-1,j])
    a2.append(a[i,j+1])
    a2.append(a[i,j-1])
    a2.append(a[i+1,j])
    nule = a2.count(0)
    nuleind = []
    for i in range(4):
        if a2[i] == 0:            nuleind.append(i)
    minind = a2.index(min(a2))
    maxind = a2.index(max(a2))
    t1 = [1, 2, 3, 4]
    t2 = [1, 3, 2, 4]
    t3 = [2, 4, 1, 3]
    t4 = [3, 4, 1, 2]
    t5 = [4, 2, 3, 1]
    t = t1
    if nule == 3:
        if maxind == 1:            t = t3
        elif maxind == 2:            t = t2
        elif maxind == 3:            t = t4
    elif nule == 2:
        if nuleind == [1, 2]:            t = t2
        elif nuleind == [0, 2]:            t = t5
        elif nuleind == [0, 1]:            t = t4
        elif nuleind == [2, 3]:            t = t3
    elif nule == 1 or nule == 0:
        if minind == 0:            t = t4
        elif minind == 1:            t = t2
        elif minind == 2:            t = t3
        elif minind == 3:            t = t1
    else:
        t = t1
    return t


def division_10(a):
    a2 = a % 8
    x = a2 % 4
    y = a2 - x
    if a == 16:        t = [4, 4, 4, 4]
    elif a == 0:        t = [0, 0, 0, 0]
    elif a > 7:        t = [4, 4, x, y]
    elif a > 3:        t = [y, x, 0, 0]
    else:        t = [x, y, 0, 0]
    t.sort(reverse=True)
    return t


def division_20(a):
    t = a * [1] + 4 * [0]
    t = t[:4]
    return t


def checking_for_problems(array):
    x, y = array.shape
    array = add_cells_around(array)
    list_of_possibilities = []
    k = 0
    for n in range(x):
        i = n+1
        for m in range(x):
            j = m +1
            if array[i, j] == 4 and array[i + 1, j] + array[i - 1, j] + array[i, j + 1] + array[i, j - 1] == 4:
                list_of_possibilities.append([i,j])
                random.shuffle(list_of_possibilities)
    for n in range(x):
        i = n+1
        for m in range(x):
            j = m +1
            if array[i + 1, j] + array[i - 1, j] + array[i, j + 1] + array[i, j - 1] == 0:
                if array[i + 1, j + 1] > 0:                    array[i + 1, j] = array[i, j]
                if array[i + 1, j - 1] > 0:                    array[i + 1, j] = array[i, j]
                if array[i - 1, j - 1] > 0:                    array[i - 1, j] = array[i, j]
                if array[i - 1, j + 1] > 0:                    array[i - 1, j] = array[i, j]
                array[i, j] = 0
            if array[i, j] ==0 and array[i + 1, j] != 0 and array[i - 1, j] != 0 and array[i, j + 1] != 0 and array[i, j - 1] != 0:
                array[i, j] = 4
                array[list_of_possibilities[k][0], list_of_possibilities[k][1]] = 0
                k += 1

    array = remove_cells_around(array)
    return array


def desetka(broj):
    mapa5x = add_cells_around(five_by_five_map(broj))
    mapa10 = []
    for i in range(5):
        m = i + 1
        for j in range(5):
            n = j + 1
            listaokoline = ispitivanje(mapa5x,m,n)
            sorta = division_10(mapa5x[m, n])
            lis = [-1,-1,-1,-1]
            for s in range(4):
                lis[listaokoline[s]-1] = sorta[s]
            mapa10.append(lis)

    desetrecnik = dict()
    for i in range(25):
        mapiranje = petsort.get(i)
        unosi = mapa10[i]
        for n in range(4):
            desetrecnik[mapiranje[n]] = unosi[n]

    desetrecnik = dict(sorted(desetrecnik.items()))
    mapadeset = list(desetrecnik.values())
    mapadeset = np.array(mapadeset).reshape((10,10))
    mapadeset = checking_for_problems(mapadeset)
    print(mapadeset, np.sum(mapadeset))
    return mapadeset


def connected_components(slik1):
    # analiziranje slike da li su oznake prostorija povezane (da se spreci dve odvojene dnevne sobe npr)
    tags = []
    # current  tag (remember 1 and 0 are already in image so start from 2)
    tag = 20
    # counter
    cntr = 0
    for i in range(20):
        for j in range(20):
            if slik1[i][j] != 0:
                if i != 0 and j != 0 and slik1[i][j - 1] != 0 and slik1[i - 1][j] != 0 and slik1[i - 1][j] != slik1[i][j - 1]:
                    slik1[i][j] = slik1[i][j - 1]
                    tags.remove(slik1[i - 1][j])
                    cntr -= 1
                    slik1[slik1 == slik1[i - 1][j]] = slik1[i][j]
                elif i != 0 and slik1[i - 1][j] != 0:
                    slik1[i][j] = slik1[i - 1][j]
                elif j != 0 and slik1[i][j - 1] != 0:
                    slik1[i][j] = slik1[i][j - 1]
                else:
                    slik1[i][j] = tag
                    tags.append(tag)
                    tag += 1
                    cntr += 1
    if cntr < 2:
        m1 = True
    else:
        m1 = False
    return m1


def dvadesetka(broj=170):
    mapa10x = add_cells_around(desetka(broj))
    mapa20 = []
    for i in range(10):
        m = i + 1
        for j in range(10):
            n = j + 1
            listaokoline = ispitivanje(mapa10x, m, n)
            sorta = division_20(mapa10x[m, n])
            lis = [-1, -1, -1, -1]
            for s in range(4):
                lis[listaokoline[s] - 1] = sorta[s]
            mapa20.append(lis)

    dvadesetrecnik = dict()
    for i in range(100):
        mapiranje = desetsort.get(i)
        unosi = mapa20[i]
        for n in range(4):
            dvadesetrecnik[mapiranje[n]] = unosi[n]

    dvadesetrecnik = dict(sorted(dvadesetrecnik.items()))
    mapadvadeset = list(dvadesetrecnik.values())
    mapadvadeset = np.array(mapadvadeset).reshape((20, 20))
    mapadvadeset = checking_for_problems(mapadvadeset)
    print(mapadvadeset, np.sum(mapadvadeset))
    if np.sum(mapadvadeset) == broj and connected_components(mapadvadeset) == True:
        return mapadvadeset, 1
    else:
        return mapadvadeset, 0


def plot(broj):
    for i in range(100):
        mp = dvadesetka(broj)
        mapa,mapab = mp[0],mp[1]
        if mapab != 0:
            break
        else:
            continue


    mapa[mapa > 0] = 1
    zbir = np.sum(mapa)
    mapa1 = np.zeros((20, 20, 3), dtype=np.uint8)
    for i in range(20):
        for j in range(20):
            if mapa[i,j] == 0:
                mapa1[i,j] = [255, 255, 255]
            else:    mapa1[i,j] = [0, 0, 0]
    img = Image.fromarray(mapa1, "RGB")
    return img, mapa, zbir





def jedna_slika(k=150, rang=100):
    for i in range(rang):
        print(f"Krug {i}.")
        Path(f"output/dir{k}/data").mkdir(parents=True, exist_ok=True)
        plot1 = plot(k)
        x = plot1[0]
        y = plot1[1]
        z = plot1[2]
        f = open(f"output/dir{k}/data/slika {i} - {z}.txt","w+")
        f.write(np.array2string(y,separator=", "))
        #x.save(f"output/dir{k}/data/slika {i}.png")
        y = x.resize((400,400), Image.NEAREST)
        y.save(f"output/dir{k}/slika {i}.png")


area = [50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350]
# list of numbers representing area of the building.
copynumber = 100
# number of copies per area.

lista_vremena = []
for i in range(len(area)):
    start = time.time()
    lista_vremena.append(area[i])
    jedna_slika(area[i], copynumber)
    end = time.time()
    lista_vremena.append(end-start)

print(f"time: {end-start} s.")

