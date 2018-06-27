from create_board import draw_board
from PIL import Image
from Utils import *
import sys
import re
import numpy
import glob,os
import matplotlib.pyplot as plt
import numpy as np
from math import *
import matplotlib as matp


def flip_line(image):
    copy =  []
    for i in range(len(image),0,-100):
        copy.append(image[i-100:i])

    copy = np.concatenate(copy,0)
    copy = np.swapaxes(copy,0,1)
    copy2 = []

    for i in range(len(copy),0,-100):
        copy2.append(copy[i-100:i])

    copy2 = np.concatenate(copy2,0)
    copy = np.swapaxes(copy2,0,1)
    # plt.imshow(copy)
    # plt.show()
    return copy

def get_check(id,checks_turn,check):
    cnt = 0
    for i in checks_turn:
        if i == id:
            return check[cnt]
        cnt = cnt +1

def gaussian(x0,y0, sigma=1):

    x, y = np.arange(800), np.arange(800)

    gx = np.exp(-(x-x0)**2/(2*sigma**2))
    gy = np.exp(-(y-y0)**2/(2*sigma**2))
    g = np.outer(gx, gy)
    #g /= np.sum(g)  # normalize, if you want that

    return g.astype('float')

def interpolate(center):
    espacement = 50
    #print(center)
    if(len(center)==2):
        distance_x = round(center[1][0]-center[0][0])
        distance_y = round(center[1][1]-center[0][1])
        # print(distance_x )
        # print(distance_y)
        if(distance_x == 0):#vertical move
            start = center[0][1]
            gauss = gaussian(start,center[0][0],sigma=40)
            while(start+espacement<= center[1][1] - espacement):
                gauss = gauss + gaussian(start+espacement,center[0][0],sigma=40)
                start = start + espacement
        else:##diagonal or knight or horizontal move
            if(distance_y == 0):#horizontal
                if(distance_x <0): #to the left
                    start = center[0][0]
                    gauss = gaussian(center[0][1],start-espacement,sigma=40)
                    while(start+espacement>= center[1][0] + espacement):
                        gauss = gauss + gaussian(center[0][1],start-espacement,sigma=40)
                        start = start - espacement
                else:#to the right
                    start = center[0][0]
                    gauss = gaussian(center[0][1],start+espacement,sigma=40)
                    while(start+espacement<= center[1][0] - espacement):
                        gauss = gauss + gaussian(center[0][1],start+espacement,sigma=40)
                        start = start + espacement
            elif(distance_y == abs(distance_x)):#diagonal move
                start_x = center[0][1]
                start_y = center[0][0]
                if(distance_x<0):# diagonal to the left
                    gauss = gaussian(start_x+espacement,start_y-espacement,sigma=40)
                    while(start_x+espacement<= center[1][1] - espacement):
                        start_x = start_x + espacement
                        start_y = start_y - espacement
                        gauss = gauss + gaussian(start_x+espacement,start_y-espacement,sigma=40)
                else:#diagonal to the right
                    gauss = gaussian(start_x+espacement,start_y+espacement,sigma=40)
                    while(start_x+espacement<= center[1][1] - espacement):
                        start_x = start_x + espacement
                        start_y = start_y + espacement
                        gauss = gauss + gaussian(start_x+espacement,start_y+espacement,sigma=40)
            else: #knight move
                start_x = center[0][1]
                start_y = center[0][0]
                if(distance_y<0):# knight to the left
                    print("left")
                    if(abs(distance_x)>distance_y):#horizontal L
                        gauss =  gaussian(start_x+espacement,start_y,sigma=40)
                        gauss = gauss +  gaussian(start_x+(2*espacement),start_y,sigma=40)
                        start_x = start_x+(2*espacement)
                        while(start_y >= center[1][0] + espacement):
                            gauss = gauss + gaussian(start_x,start_y-espacement,sigma=40)
                            start_y = start_y - espacement
                    else:#vertical L
                        gauss =  gaussian(start_x,start_y-(espacement),sigma=40)
                        gauss = gauss +  gaussian(start_x,start_y-(2*espacement),sigma=40)
                        start_y = start_y-(2*espacement)
                        while(start_x >= center[1][1] - espacement):
                            gauss = gauss + gaussian(start_x- espacement,start_y,sigma=40)
                            start_x = start_x - espacement
                else:#knight to the right
                    if(distance_x>distance_y):#horizontal R
                        gauss =  gaussian(start_x+(espacement),start_y,sigma=40)
                        gauss =  gauss + gaussian(start_x+(2*espacement),start_y,sigma=40)
                        start_x = start_x+(2*espacement)
                        while(start_y <= center[1][0] - espacement):
                            gauss = gauss + gaussian(start_x,start_y + espacement,sigma=40)
                            start_y = start_y + espacement
                    else:#vertical R
                        gauss =  gaussian(start_x,start_y+(espacement),sigma=40)
                        gauss =  gauss + gaussian(start_x,start_y+(2*espacement),sigma=40)
                        start_y = start_y+(2*espacement)
                        while(start_x <= center[1][1] - espacement):
                            gauss = gauss + gaussian(start_x + espacement,start_y,sigma=40)
                            start_x = start_x + espacement

    return gauss

def find_coord(im3):
    coord = [] #[x,y]
    a = 0
    while(a<len(im3)):
        if(np.sum(im3[a])>0):
            pos = []
            pos.append(a)
            d=0
            ins = 0
            while(d<len(im3) and ins == 0):
                if(np.sum(im3[a][d])>0):
                    pos.append(d)
                    ins= 1
                d = d+1
            coord.append(pos)
            b = a
            while(b<len(im3)):
                if(np.sum(im3[b])==0):
                    pos = []
                    pos.append(b)
                    d = 0
                    b = b - 1
                    ins = 0
                    while(d<len(im3) and ins == 0):
                        if(np.sum(im3[b][d])>0):
                            pos.append(d)
                            ins = 1
                        d = d+1
                    coord.append(pos)
                    a = b + 1
                    break
                b = b+1
        a = a + 1
    return coord

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

path = "./images/"

if(len(sys.argv)>1):
    path_compute = int(sys.argv[1])
else:
    path_compute = 0



paths = sorted(glob.glob(path+"*"))
paths_values =  []
for i in paths:
    paths_values.append(sorted(glob.glob(i+"/*/"))[0])

#print(paths_values)
inputs = []
for i in paths_values:
    inputs.append(sorted(glob.glob(i+"/*.png")))

for games in inputs:#every games
    counter = 0
    print(games[0][:-15])
    with  open(games[0][:-15]+"checks.txt") as f:
         checks = f.readlines()
    checks = [eval(x.strip('\n')) for x in checks]
    if( len(checks)>0):
        checks_turn = [ (x[0]*2)+1 if x[1] else  x[0]*2  for x in checks]
    else:
        checks_turn = []
    for j in range(0,len(games)-1):#every configs from the game
        im1 = np.asarray(Image.open(games[j]))
        im2 = np.asarray(Image.open(games[j+1]))
        if (j%2!=0 and j!=0):
            im1 = flip_line(im1)
            Image.fromarray(im1,'RGB' ).save(games[j], "PNG")
            im2 = flip_line(im2)
            # plt.imshow(im1)
            # plt.show()
        im3 = im2 - im1
        im3 = np.squeeze(im3[:,:,:1],2)
        # plt.imshow(im3)
        # plt.show()

        coord = find_coord(im3)

        if (len(coord)>2):
            #print(coord)
            center = []
            for u in range(0,len(coord),2):
                center.append( (coord[u][1] + floor( (coord[u+1][1] - coord[u][1]) /2 ) , coord[u][0] + floor( (coord[u+1][0] - coord[u][0]) /2 ) )   )

        else:
            coord = find_coord(np.swapaxes(im3,0,1))
            center = []
            for u in range(0,len(coord),2):
                center.append( (coord[u][0] + floor( (coord[u+1][0] - coord[u][0]) /2 ) , coord[u][1] + floor( (coord[u+1][1] - coord[u][1]) /2 ) )   )

        if(path_compute):
            if(len(center)==2):
                gauss = gaussian(center[0][1],center[0][0], sigma=40)
                gauss = gauss + gauss
                gauss2 = gaussian(center[1][1],center[1][0], sigma=40)
                gauss2 = gauss2 +  interpolate(center)
                gauss = gauss + gauss2
            else:
                gauss = gaussian(center[0][1],center[0][0], sigma=40)
                for i in range(1,len(center)):
                    gauss = gauss  + gaussian(center[i][1],center[i][0], sigma=40)
        else:
            try:
                gauss = gaussian(center[0][1],center[0][0], sigma=40)
                for g in range(1,len(center)):
                    gauss = gauss +  gaussian(center[1][1],center[1][0], sigma=40)
            except IndexError:
                print("IndexError" + str(len(center)))


        if j in checks_turn:
            #print("check at " + str(j) + str(get_check(j,checks_turn,checks)))
            val = get_check(j,checks_turn,checks)
            if(val[1]):
                gauss = gauss + gaussian(len(im1)-(val[2][1]*100)-50,len(im1)-(val[2][0]*100)-50,sigma=40)
            else:
                gauss = gauss + gaussian((val[2][1]*100)+50,(val[2][0]*100)+50,sigma=40)
            # plt.imshow(gauss)
            # plt.show()
        # gauss3 = np.expand_dims(gauss,0)
        # gauss3 = np.concatenate( (gauss3,gauss3,gauss3),0)
        # gauss3 = np.swapaxes(np.swapaxes(gauss3,0,1),1,2)
        # plt.imshow(np.multiply(gauss3,im2/255))
        # plt.show()

        gauss = (gauss * 255 / np.max(gauss)).astype('uint8')
        path = games[j][:-15]+"saliency/"
        ensure_dir(path)
        gauss = gauss
        Image.fromarray(gauss,'L' ).save(games[j][:-15]+"saliency/"+  games[j][-7:], "PNG")
        counter = counter +1
