from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from math import *
from PIL import ImageOps

piecesw = ["R","KN","B","Q","K","B","KN","R"]
piecesb = ["R","KN","B","Q","K","B","KN","R"]

pawns = "P"


def draw_board(positions):
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = Image.new( 'RGB', (800,800), (140,140,140)) # create a new black image
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]):    # for every col:
        for j in range(img.size[1]):    # For every row
            if(floor(i/100)%2==0 and floor(j/100)%2==0 ):
                pixels[i,j] = (255, 255, 255) # set the colour accordingly
            if(floor(i/100)%2!=0 and floor(j/100)%2!=0 ):
                pixels[i,j] = (255, 255, 255) # set the colour accordingly

    positionw = positions[0]
    positionb = positions[1]
    positionpw = positions[2]
    positionpb = positions[3]

    #draw whites
    for i in range(0,8):
        img.paste(Image.open("./pieces/"+piecesw[i]+"w.png"),(int('%d%d' % (positionw[i][0], 20)),int('%d%d' % (positionw[i][1], 10))),
        Image.open("./pieces/"+piecesw[i]+"w.png"))
    for i in range(0,8):
        img.paste(Image.open("./pieces/Pw.png"),(int('%d%d' % (positionpw[i][0], 20)),int('%d%d' % (positionpw[i][1], 10))),
        Image.open("./pieces/Pw.png"))

    #draw blacks
    for i in range(0,8):
        img.paste(Image.open("./pieces/"+piecesb[i]+"b.png"),(int('%d%d' % (positionb[i][0], 20)),int('%d%d' % (positionb[i][1], 10))),
        Image.open("./pieces/"+piecesb[i]+"b.png"))
    for i in range(0,8):
        img.paste(Image.open("./pieces/Pb.png"),(int('%d%d' % (positionpb[i][0], 20)),int('%d%d' % (positionpb[i][1], 10))),
        Image.open("./pieces/Pb.png"))


    draw = ImageDraw.Draw(img)
    return img


# image = Image.new( 'RGB', (1610,800), "white") # create a new black image
# img1 = draw_board()
# image.paste(img1,(0,0))
# positionpb[3] = (positionpb[3][0],positionpb[3][1]+1)
# img2 = draw_board()
# image.paste(img2,(810,0))
# image.show()
