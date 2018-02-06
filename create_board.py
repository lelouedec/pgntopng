from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from math import *
from PIL import ImageOps

pieces = ["R","KN","B","K","Q","B","KN","R"]
pawns = "P"
positionb = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)]
positionpb = [(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]
positionw = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)]
positionpw = [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]
def drange(start, stop, step):
    while start < stop:
            yield start
            start += step

def draw_board():
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = Image.new( 'RGB', (800,800), "white") # create a new black image
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]):    # for every col:
        for j in range(img.size[1]):    # For every row
            if(floor(i/100)%2==0 and floor(j/100)%2==0 ):
                pixels[i,j] = (140, 140, 140) # set the colour accordingly
            if(floor(i/100)%2!=0 and floor(j/100)%2!=0 ):
                pixels[i,j] = (140, 140, 140) # set the colour accordingly


    #draw whites
    for i in range(0,8):
        img.paste(Image.open("./pieces/"+pieces[i]+"w.png"),(int('%d%d' % (positionw[i][0], 20)),int('%d%d' % (positionw[i][1], 10))),
        Image.open("./pieces/"+pieces[i]+"w.png"))
    for i in range(0,8):
        img.paste(Image.open("./pieces/Pw.png"),(int('%d%d' % (positionpw[i][0], 20)),int('%d%d' % (positionpw[i][1], 10))),
        Image.open("./pieces/Pw.png"))

    #draw blacks
    for i in range(0,8):
        img.paste(Image.open("./pieces/"+pieces[i]+"b.png"),(int('%d%d' % (positionb[i][0], 20)),int('%d%d' % (positionb[i][1], 10))),
        Image.open("./pieces/"+pieces[i]+"b.png"))
    for i in range(0,8):
        img.paste(Image.open("./pieces/Pb.png"),(int('%d%d' % (positionpb[i][0], 20)),int('%d%d' % (positionpb[i][1], 10))),
        Image.open("./pieces/Pb.png"))


    draw = ImageDraw.Draw(img)
    return img


image = Image.new( 'RGB', (1610,800), "white") # create a new black image
img1 = draw_board()
image.paste(img1,(0,0))
positionpb[3] = (positionpb[3][0],positionpb[3][1]+1)
img2 = draw_board()
image.paste(img2,(810,0))
image.show()
