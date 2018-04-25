from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from math import *
from PIL import ImageOps

piecesw = ["R","KN","B","Q","K","B","KN","R"]
piecesb = ["R","KN","B","Q","K","B","KN","R"]

pawns = "P"


def draw_board(positions,image):
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = image
    pixels = img.load() # create the pixel map

    for i in range(0,800):    # for every col:
        for j in range(0,800):    # For every row
            if(floor(i/100)%2==0 and floor(j/100)%2==0 ):
                pixels[i,j] = (240, 217, 181) # set the colour accordingly
            elif(floor(i/100)%2!=0 and floor(j/100)%2!=0 ):
                pixels[i,j] = (240, 217, 181) # set the colour accordingly
            #else:
                #pixels[i,j] = (240, 217, 181) # set the colour accordingly

    positionw = positions[0]
    positionb = positions[1]
    positionpw = positions[2]
    positionpb = positions[3]
    dead_index_x = 900
    dead_index_y = 20


    #draw whites
    for i in range(0,8):
        if(positionw[i] == (-1,-1)):
            img.paste(Image.open("./pieces/"+piecesw[i]+"w.png").resize((100,100),Image.BILINEAR),(dead_index_x,dead_index_y)
            ,Image.open("./pieces/"+piecesw[i]+"w.png").resize((100,100),Image.BILINEAR))
            if(dead_index_y == 720):
                dead_index_y = 20
                dead_index_x = dead_index_x + 100
            else:
                dead_index_y = dead_index_y +100
        else:
            img.paste(Image.open("./pieces/"+piecesw[i]+"w.png").resize((100,100),Image.BILINEAR),(positionw[i][0]*100,positionw[i][1]*100),
            Image.open("./pieces/"+piecesw[i]+"w.png").resize((100,100),Image.BILINEAR))
    for i in range(0,8):
        if(positionpw[i] == (-1,-1)):
            img.paste(Image.open("./pieces/Pw.png"),(dead_index_x,dead_index_y),Image.open("./pieces/Pw.png"))
            if(dead_index_y == 720):
                dead_index_y = 20
                dead_index_x = dead_index_x + 100
            else:
                dead_index_y = dead_index_y +100
        else:
            img.paste(Image.open("./pieces/Pw.png").resize((100,100),Image.BILINEAR),(positionpw[i][0]*100,positionpw[i][1]*100),
            Image.open("./pieces/Pw.png").resize((100,100),Image.BILINEAR))

    #draw blacks
    for i in range(0,8):
        if(positionb[i] == (-1,-1)):
            img.paste(Image.open("./pieces/"+piecesb[i]+"b.png"),(dead_index_x,dead_index_y),Image.open("./pieces/"+piecesb[i]+"b.png"))
            if(dead_index_y == 720):
                dead_index_y = 20
                dead_index_x = dead_index_x + 100
            else:
                dead_index_y = dead_index_y +100
        else:
            img.paste(Image.open("./pieces/"+piecesb[i]+"b.png").resize((100,100),Image.BILINEAR),(positionb[i][0] *100 ,positionb[i][1] *100),
            Image.open("./pieces/"+piecesb[i]+"b.png").resize((100,100),Image.BILINEAR))
    for i in range(0,8):
        if(positionpb[i] == (-1,-1)):
            img.paste(Image.open("./pieces/Pb.png"),(dead_index_x,dead_index_y),Image.open("./pieces/Pb.png"))
            if(dead_index_y == 720):
                dead_index_y = 20
                dead_index_x = dead_index_x + 100
            else:
                dead_index_y = dead_index_y +100
        else:
            img.paste(Image.open("./pieces/Pb.png").resize((100,100),Image.BILINEAR),(positionpb[i][0] *100,positionpb[i][1] *100),
            Image.open("./pieces/Pb.png").resize((100,100),Image.BILINEAR))


    draw = ImageDraw.Draw(img)
    return img
