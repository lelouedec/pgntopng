from create_board import draw_board
from PIL import Image
from Utils import *
from create_gif import *
import sys

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

def generate(game,game_name):
    gameboard = []
    gameboard.append(positions)
    images = []
    for i in range(0,len(game)-1):
        print(i)
        if(int(arg1)):
            if(arg2):
                image = Image.new( 'RGB', (800,800), (181,136,99)) # create a new black image
            else:
                image = Image.new( 'RGB', (1400,800), (181,136,99)) # create a new black image
            img1 = draw_board(positions,image)
            image.paste(img1,(0,0))
            images.append(image)
        ###WHITE MOVE

        for j in range(0,2):
            if(game[i][j][-1] == "+" or game[i][j][-1] == "+"):#check
                a = list(game[i])
                a[j] = a[j][:-1]
                print(a)
                game[i] = tuple(a)
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
                if(game[i][j][1] =='x'):#cxb5 Nxd6
                    piece_index = get_piece_index(game[i][j][0],(game[i][j][2],game[i][j][3]),j,positions)
                    goal = transform_board_to_screen( (game[i][j][2],game[i][j][3]) )
                    if(piece_index == -1):#cxb5
                        dead_piece = get_dying_piece((game[i][j][2],game[i][j][3]),positions)
                        if(j==0):
                            moved = get_pawn_moved((dict[game[i][j][0]],goal[1]+1),positions)
                        else:
                            moved = get_pawn_moved((dict[game[i][j][0]],goal[1]-1),positions)
                        positions[moved[0]][moved[1]] = goal
                        positions[dead_piece[0]][dead_piece[1]] = (-1,-1)
                    else:#Nxd6
                        piece_dead_indices = get_dying_piece((game[i][j][2],game[i][j][3]),positions)
                        positions[piece_dead_indices[0]][piece_dead_indices[1]] = (-1,-1)
                        positions[j][piece_index] = goal
                else:#Nbd7
                    piece_index = get_piece_concurrence(game[i][j][0],game[i][j][1],j,positions)
                    goal = transform_board_to_screen((game[i][j][2],game[i][j][3]))
                    positions[j][piece_index] = goal
            else:
                if(game[i][j][0]=='O'):#O-O-O
                    positions[j][0] = (positions[j][0][0]+3,positions[j][0][1])
                    positions[j][4] = (positions[j][4][0]-2,positions[j][4][1])
                else:
                    print(game[i])

            if(int(arg1)):
                if(arg2):
                    image = Image.new( 'RGB', (800,800), (181,136,99)) # create a new black image
                else:
                    image = Image.new( 'RGB', (1400,800), (181,136,99)) # create a new black image
                img1 = draw_board(positions,image)
                image.paste(img1,(0,0))
                images.append(image)



    return images
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

if __name__ == '__main__':
    arg1 = 0
    arg2 = 0
    game_string = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6 23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5 hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33. f3 Bc8 34. Kf2 Bf5 35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6 Nf2 42. g4 Bd3 43. Re6 1/2-1/2"
    game2_string = "1. e4 c6 2. c4 d5 3. exd5 cxd5 4. cxd5 Nf6 5. Nc3 g6 6. Bc4 Bg7 7. Nf3 O-O 8. O-O Nbd7 9. d3 Nb6 10. Qb3 Bf5 11. Re1 h6 12. a4 Nfd7 13. Be3 a5 14. Nd4 Nxc4 15. dxc4 Nc5 16. Qa3 Nd3 17. Nxf5 gxf5 18. Red1 Ne5 19. b3 Ng4 20. Qc1 f4 21. Bd4 Bxd4 22. Rxd4 e5 23. Rd2 Qh4 24. h3 Nf6 25. Qe1 Qg5 26. Ne4 Nxe4 27. Qxe4 f5 28. Qxe5 Rae8 29. h4 Qxh4 30. Qc3 Re4 31. d6 Qg5 32. f3 Re3 33. Qxa5 Rfe8 34. Rf2 Qf6 35. Rd1 R3e5 36. d7  1-0"
    game3_string = "1. e4 e6 2. d4 d5 3. Nd2 c5 4. exd5 Qxd5 5. Ngf3 cxd4 6. Bc4 Qd6 7. Qe2 Nf6 8. Nb3 Nc6 9. Bg5 Qb4+ 10. Bd2 Qb6 11. O-O-O Bd7 12. Bg5 Bc5 13. Kb1 O-O-O 14. Ne5 Nxe5 15. Qxe5 Bd6 16. Qe2 h6 17. Bd2 Bb4 18. Bxb4 Qxb4 19. Nxd4 Kb8 20. f4 Qc5 21. Nf3 Ng4 22. Rd4 Bc8 23. Rhd1 Rxd4 24. Nxd4 e5 25. h3 exd4 26. hxg4 Bxg4 27. Qxg4 Qxc4 28. Qxg7 Rc8 29. Qe5+ Ka8 30. Qe4 a6 31. b3 Qc6 32. Qxc6 Rxc6 33. f5 Rd6 34. Kc1 Ka7 35. Kd2 Kb6 36. Re1 Rd8 37. g4 Rg8 38. Re4 Kc5 39. Kd3 h5 40. gxh5 Rg3+ 41. Kd2 Rh3 42. f6 Rxh5 43. Re7 Rf5 44. Rxf7 b5 45. Rf8 Kc6 46. Kd3 Rf4 47. a3 Kc7 48. a4 Kb6 49. Ke2 Rf5 50. Kd3 Rf4 51. axb5 axb5 52. c3 dxc3 53. Kxc3 Kc6 54. b4 Kc7 55. f7 Kb7 56. Kd3 Rf3+ 57. Ke4 Rf1 58. Ke5 Rf2 59. Ke6 Re2+ 60. Kd6  Rf2 61. Kc5 1/2-1/2"
    game_file = ""
    if(len(sys.argv)>1):
        arg1 = sys.argv[1]
    if(len(sys.argv)>2):
        arg2 = sys.argv[2]

    # game = create_game_array(game_string)
    # images = generate(game,"game1")
    # path = "./images/game1/configs/"
    # ensure_dir(path)
    # save_images(path,images)
    # positions = [[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)],[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
    #             [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)],[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]]
    # game = create_game_array(game2_string)
    # images = generate(game,"game2")
    # path = "./images/game2/configs/"
    # ensure_dir(path)
    # save_images(path,images)


    positions = [[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)],[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
                 [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)],[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]]
    game = create_game_array(game3_string)
    images = generate(game,"game3")
    path = "./images/game3/configs/"
    ensure_dir(path)
    save_images(path,images)
