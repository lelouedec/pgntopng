import sys
import re
from math import *
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import ImageGrid
from Utils import *
import copy
from create_board import draw_board
from PIL import Image


def create_game_array(gamestring):
    game_array = gamestring.split(" ")
    game_array2 = []
    for i,val in enumerate(game_array):
        if(i%3 !=0):
            game_array2.append(val)

    game = []
    for i in range(0,len(game_array2),2):
        if(i!=len(game_array2)-1):
            game.append((game_array2[i],game_array2[i+1]))
        else:
            game.append((game_array2[i],"end"))

    return game



dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
piecesb =  {'Q': 3 ,'K' : 4}
piecesw = {'K': 4,'Q' : 3}
positions = [[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)],[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
            [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)],[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]]
#positions[0] = main pieces whites
#positions[1] = main pieces blacks
#positions[2] = pawns pieces white
#positions[3] = pawns pieces blacks
arg1 = 1
arg2 = 1
def generate(game):
    positions = [[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)],[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
                [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)],[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]]
    gameboard = []
    images = []
    check  = []
    # if(int(arg1)):
    #     if(arg2):
    #         image = Image.new( 'RGB', (800,800), (181,136,99)) # create a new black image
    #     else:
    #         image = Image.new( 'RGB', (1400,800), (181,136,99)) # create a new black image
    #     img1 = draw_board(positions,image)
    #     image.paste(img1,(0,0))
    #     images.append(image)
    images.append(copy.deepcopy(positions))
    for i in range(0,len(game)-1):
        for j in range(0,2):
            if(game[i][j][-1] == "+" or game[i][j][-1] == "#"):#check
                a = list(game[i])
                a[j] = a[j][:-1]
                game[i] = tuple(a)
                if(j==0):
                    check.append((i,j, positions[1][4] ))
                else:
                    check.append((i,j, positions[0][4] ))
            if(len(game[i][j])==2):#can only be a pawn moving vertically
                coord = transform_board_to_screen(game[i][j])
                if(j==0):
                    moved = get_pawn_moved((coord[0],coord[1]+1),positions)
                    if(moved == None):
                        moved = get_pawn_moved((coord[0],coord[1]+2),positions)
                else:
                    moved = get_pawn_moved((coord[0],coord[1]-1),positions)
                    if(moved == None):
                        moved = get_pawn_moved((coord[0],coord[1]-2),positions)
                positions[moved[0]][moved[1]] = coord
            elif(len(game[i][j])==3):
                if(game[i][j][0] =='O'):#no possible ambiguity
                    positions[j][7] = (positions[j][7][0]-2,positions[j][7][1])
                    positions[j][4] = (positions[j][4][0]+2,positions[j][4][1])
                else:
                    piece_index = get_piece_index(game[i][j][0],(game[i][j][1],game[i][j][2]),j,positions)
                    positions[j][piece_index] = transform_board_to_screen((game[i][j][1],game[i][j][2]))
            elif(len(game[i][j])==4):#Nbd7 cxb5 Nxd6
                if('=' in game[i][j]):
                    print("Pawn promotion, exiting game")
                    return images,checks
                if(game[i][j][1] =='x'):#cxb5 Nxd6
                    piece_index = get_piece_index(game[i][j][0],(game[i][j][2],game[i][j][3]),j,positions)
                    goal = transform_board_to_screen( (game[i][j][2],game[i][j][3]) )
                    if(piece_index == -1):#cxb5
                        dead_piece = get_dying_piece((game[i][j][2],game[i][j][3]),positions)
                        if(dead_piece == None):
                            return images,check
                        if(j==0):
                            moved = get_pawn_moved((dict[game[i][j][0]],goal[1]+1),positions)
                        else:
                            moved = get_pawn_moved((dict[game[i][j][0]],goal[1]-1),positions)
                        positions[moved[0]][moved[1]] = goal
                        positions[dead_piece[0]][dead_piece[1]] = (-1,-1)
                    else:#Nxd6
                        dead_piece = get_dying_piece((game[i][j][2],game[i][j][3]),positions)
                        if(dead_piece == None):
                            return images,check
                        positions[dead_piece[0]][dead_piece[1]] = (-1,-1)
                        positions[j][piece_index] = goal
                else:#Nbd7
                    piece_index = get_piece_concurrence(game[i][j][0],game[i][j][1],j,positions)
                    goal = transform_board_to_screen((game[i][j][2],game[i][j][3]))
                    positions[j][piece_index] = goal
            else:
                if('=' in game[i][j]):
                    print("Pawn promotion, exiting game")
                    return images,check
                elif(game[i][j][0]=='O'):#O-O-O
                    positions[j][0] = (positions[j][0][0]+3,positions[j][0][1])
                    positions[j][4] = (positions[j][4][0]-2,positions[j][4][1])
                elif(game[i][j][2]=='x'):
                    move = game[i][j]
                    move = move[:2]+move[3:]
                    ##find which piece to move
                    piece_index = get_piece_concurrence(move[0],move[1],j,positions)
                    ##goal to reach
                    goal = transform_board_to_screen((move[2],move[3]))
                    ##find dead piece
                    dead_piece = get_dying_piece((move[2],move[3]),positions)
                    if(dead_piece == None):
                        return images,check
                    ##kill it
                    positions[dead_piece[0]][dead_piece[1]] = (-1,-1)
                    ##change killer position
                    positions[j][piece_index] = goal
                else:
                    print(" failed " + str(game[i]))

            images.append(copy.deepcopy(positions))

            image = Image.new( 'RGB', (800,800), (181,136,99)) # create a new black image
            img1 = draw_board(positions,image)
            image.paste(img1,(0,0))
            #     images.append(image)
            plt.imshow(image)
            plt.show()


    return images,check

val ="1. e4 e5 2. a4 a5 3. Ra3 Ra6 4. Rb3 Rb6 5. Re3 Re6 6. b4 b5"

try:
    game = create_game_array(val)
    images,checks = generate(game)
    print(images)
    if(images !=None):
        print("")

except KeyError:
    print("wrong format")
