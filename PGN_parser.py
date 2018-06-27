from create_board import draw_board
from PIL import Image
from Utils import *
#from create_gif import *
import sys
import re
import os 
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
    gameboard = []
    gameboard.append(positions)
    images = []
    check  = []
    if(int(arg1)):
        if(arg2):
            image = Image.new( 'RGB', (800,800), (181,136,99)) # create a new black image
        else:
            image = Image.new( 'RGB', (1400,800), (181,136,99)) # create a new black image
        img1 = draw_board(positions,image)
        image.paste(img1,(0,0))
        images.append(image)
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
                positions[moved[0]][moved[1]] = coord ##regler probleme de pions qui avance mais pas sur sa colone
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

            if(int(arg1)):
                if(arg2):
                    image = Image.new( 'RGB', (800,800), (181,136,99)) # create a new black image
                else:
                    image = Image.new( 'RGB', (1400,800), (181,136,99)) # create a new black image
                img1 = draw_board(positions,image)
                image.paste(img1,(0,0))
                images.append(image)



    return images,check
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_images(path,images):
    list_j = []
    list_i = []

    for i in range(0,len(images)):
        list_i.append(images[i].size[0])
        list_j.append(images[i].size[1])

    pad = 0

    for j in range(0,len(images)):
        new_im = Image.new('RGB', (max(list_i)+pad,max(list_j)+pad),(255,255,255))
        new_im.paste(images[j], (0+pad,0+pad))
        if(j<10):
            new_im.save(path+"00"+str(j)+".png", "PNG")
        elif(j>=10 and j<100):
            new_im.save(path+"0"+str(j)+".png", "PNG")
        else:
            new_im.save(path+str(j)+".png", "PNG")

def load_games(start,nb,file):
    lines = []
    count = 0
    with open(file) as infile:
        for line in infile:
            val =re.sub(r' {[^}]*}','',line)
            if(val[0] =='1'):
                if(count >= start):
                    lines.append(val)
                    if(count>nb):
                        break
                count = count + 1
    return lines
if __name__ == '__main__':
    arg1 = 0
    arg2 = 0
    game_string = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6 23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5 hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33. f3 Bc8 34. Kf2 Bf5 35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6 Nf2 42. g4 Bd3 43. Re6 1/2-1/2"
    game2_string = "1. e4 c6 2. c4 d5 3. exd5 cxd5 4. cxd5 Nf6 5. Nc3 g6 6. Bc4 Bg7 7. Nf3 O-O 8. O-O Nbd7 9. d3 Nb6 10. Qb3 Bf5 11. Re1 h6 12. a4 Nfd7 13. Be3 a5 14. Nd4 Nxc4 15. dxc4 Nc5 16. Qa3 Nd3 17. Nxf5 gxf5 18. Red1 Ne5 19. b3 Ng4 20. Qc1 f4 21. Bd4 Bxd4 22. Rxd4 e5 23. Rd2 Qh4 24. h3 Nf6 25. Qe1 Qg5 26. Ne4 Nxe4 27. Qxe4 f5 28. Qxe5 Rae8 29. h4 Qxh4 30. Qc3 Re4 31. d6 Qg5 32. f3 Re3 33. Qxa5 Rfe8 34. Rf2 Qf6 35. Rd1 R3e5 36. d7  1-0"
    if(len(sys.argv)>1):
        arg1 = sys.argv[1]
    if(len(sys.argv)>2):
        arg2 = sys.argv[2]

    # game = create_game_array(game_string)
    # images = generate(game)
    # path = "./images/game1/configs/"
    # ensure_dir(path)
    # save_images(path,images)
    #
    #
    # positions = [[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)],[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
    #              [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)],[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]]
    # game = create_game_array(game2_string)
    # images = generate(game)
    # path = "./images/game2/configs/"
    # ensure_dir(path)
    # save_images(path,images)

    start = 0
    nb = start + 2000
    mines = load_games(start,nb,"./marchgames2017.pgn")
    game_counter = start

    for games in mines:
        positions = [[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)],[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
                     [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)],[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]]
        print(games)
        try:
            game = create_game_array(games)
            images,checks = generate(game)
            if(images !=None):
                if(game_counter<10):
                    path = "./images/game000"+str(game_counter)+"/configs/"
                elif(game_counter>=10 and game_counter<100):
                    path = "./images/game00"+str(game_counter)+"/configs/"
                elif(game_counter>=100 and game_counter<1000):
                    path = "./images/game0"+str(game_counter)+"/configs/"
                else:
                    path = "./images/game"+str(game_counter)+"/configs/"
                ensure_dir(path)
                save_images(path,images)
                with open(path[:-8]+"/checks.txt", 'w') as file_handler:
                    for item in checks:
                        file_handler.write("{}\n".format(item))
                game_counter = game_counter + 1
        except KeyError:
            print("wrong format")
