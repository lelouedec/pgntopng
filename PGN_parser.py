from create_board import draw_board
from PIL import Image
from Utils import *

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
            game.append((game_array2[i],end))

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




game_string = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6 23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5 hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33. f3 Bc8 34. Kf2 Bf5 35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6 Nf2 42. g4 Bd3 43. Re6 1/2-1/2"

game = create_game_array(game_string)
img = draw_board(positions)
gameboard = []
gameboard.append(positions)
for i in range(0,9):
    print(game[i])
    ###WHITE MOVE
    if(len(game[i][0])==2):#can only be a pawn moving vertically
        coord = transform_board_to_screen(game[i][0])
        positions[2][dict[game[i][0][0]]] = coord
    elif(len(game[i][0])==3):
        if(game[i][0][0] =='O'):#no possible ambiguity
            positions[0][7] = (positions[0][7][0]-2,positions[0][7][1])
            positions[0][4] = (positions[0][4][0]+2,positions[0][4][1])
        else:
            piece_index = get_piece_index(game[i][0][0],(game[i][0][1],game[i][0][2]),1,positions)
            positions[0][piece_index] = transform_board_to_screen((game[i][0][1],game[i][0][2]))
    else:
        print("")


    ###BLACK MOVE
    if(len(game[i][1])==2):
        coord = transform_board_to_screen(game[i][1])
        positions[3][dict[game[i][1][0]]] = coord
    elif(len(game[i][1])==3):
        if(game[i][1][0] =='O'):#no possible ambiguity
            positions[1][7] = (positions[1][7][0]-2,positions[1][7][1])
            positions[1][4] = (positions[1][4][0]+2,positions[1][4][1])
        else:
            piece_index = get_piece_index(game[i][1][0],(game[i][1][1],game[i][1][2]),0,positions)
            positions[1][piece_index] = transform_board_to_screen((game[i][1][1],game[i][1][2]))
    else:
        print("")
    gameboard.append(positions)
    # print(positions)
    # print("\n")
#print(gameboard)


image = Image.new( 'RGB', (800,800), "white") # create a new black image
img1 = draw_board(positions)
image.paste(img1,(0,0))
image.show()
