from math import *


piecesb =  {'Q': 4 ,'K' : 3}
piecesw = {'K': 4,'Q' : 3}
dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

def transform_board_to_screen(val):
    x = dict[val[0]]
    y = 8-int(val[1])
    return (x,y)
def get_case_color(case):
    if(case[0]%2==0 and case[1]%2!=0):
        return 0
    else:
        return 1
def something_in_middle_h(coord,goal,positions):
    for i in range (0,len(positions)):
        for j in range(0,8):
            if(positions[i][j][0] != -1):
                if(positions[i][j][1] == coord[1]):
                    if(coord[0] > goal[0]):
                        if(positions[i][j][0]> goal[0] and positions[i][j][0] < coord[0] ):
                            return True
                    else:
                        if(positions[i][j][0] < goal[0] and positions[i][j][0] > coord[0] ):
                            return True
    return False

def something_in_middle_v(coord,goal,positions):
    for i in range (0,len(positions)):
        for j in range(0,8):
            if(positions[i][j][0] == coord[0]):
                if(coord[1] > goal[1]):
                    if(positions[i][j][1]> goal[1] and positions[i][j][1] < coord[1] ):
                        return True
                else:
                    if(positions[i][j][0] < goal[1] and positions[i][j][1] > coord[1] ):
                        return True
    return False

def get_piece_index(letter,but,color,positions):
    if(letter=='R'):#no possible ambiguity
        if(color):
            if(positions[0][0] == (-1,-1) and positions[0][7] == (-1,-1)):
                return -1
            elif(positions[0][0] == (-1,-1)):
                return 7
            elif(positions[0][7] == (-1,-1)):
                return 0
            else:
                coord = positions[0][0]
                goal = transform_board_to_screen(but)
                if(coord[0]==goal[0]):
                    if(something_in_middle_v(coord,goal,positions)):
                        return 7
                    else:
                        return 0
                elif(coord[1]==goal[1]):
                    if(something_in_middle_h(coord,goal,positions)):
                        return 7
                    else:
                        return 0
                else:
                    return 7
        else:
            if(positions[1][0] == (-1,-1) and positions[1][7] == (-1,-1)):
                return -1
            elif(positions[1][0] == (-1,-1)):
                return 7
            elif(positions[1][7] == (-1,-1)):
                return 0
            else:
                coord = positions[1][0]
                goal = transform_board_to_screen(but)
                if(coord[0]==goal[0]):
                    if(something_in_middle_v(coord,goal,positions)):
                        return 7
                    else:
                        return 0
                elif(coord[1]==goal[1]):
                    if(something_in_middle_h(coord,goal,positions)):
                        return 7
                    else:
                        return 0
                else:
                    return 7
    elif (letter=='N'):#if this is a knight moving
        if (color):
            if(positions[0][1] == (-1,-1) and positions[0][6] == (-1,-1)):#no knight to move
                return -1
            else:
                if(positions[0][1] == (-1,-1)):#only one knight to move
                    return 6
                elif (positions[0][6] == (-1,-1)):#only one knight to move
                    return 1
                else:#decide which one can be moved here
                    coord = positions[0][1]
                    goal = transform_board_to_screen(but)
                    if(goal == (coord[0]+1,coord[1]+2)):
                        return 1
                    elif (goal == (coord[0]+2,coord[1]+1)):
                        return 1
                    elif (goal == (coord[0]+2,coord[1]-1)):
                        return 1
                    elif (goal == (coord[0]+1,coord[1]-2)):
                        return 1
                    elif (goal == (coord[0]-1,coord[1]-2)):
                        return 1
                    elif (goal == (coord[0]-2,coord[1]-1)):
                        return 1
                    elif (goal == (coord[0]-2,coord[1]+1)):
                        return 1
                    elif (goal == (coord[0]-1,coord[1]+2)):
                        return 1
                    else:
                        return 6
        else:
            if(positions[1][1] == (-1,-1) and positions[1][6] == (-1,-1)):#no knight to move
                return -1
            else:
                if(positions[1][1] == (-1,-1)):#only one knight to move
                    return 6
                elif (positions[1][6] == (-1,-1)):#only one knight to move
                    return 1
                else:#decide which one can be moved here
                    coord = positions[1][1]
                    goal = transform_board_to_screen(but)
                    if(goal == (coord[0]+1,coord[1]+2)):
                        return 1
                    elif (goal == (coord[0]+2,coord[1]+1)):
                        return 1
                    elif (goal == (coord[0]+2,coord[1]-1)):
                        return 1
                    elif (goal == (coord[0]+1,coord[1]-2)):
                        return 1
                    elif (goal == (coord[0]-1,coord[1]-2)):
                        return 1
                    elif (goal == (coord[0]-2,coord[1]-1)):
                        return 1
                    elif (goal == (coord[0]-2,coord[1]+1)):
                        return 1
                    elif (goal == (coord[0]-1,coord[1]+2)):
                        return 1
                    else:
                        return 6

    elif (letter =='B'):
        if(color):
            if(positions[0][2]== (-1,-1) and positions[0][5]== (-1,-1)):
                return -1
            elif (positions[0][2]== (-1,-1)):
                return 5
            elif positions[0][5]== (-1,-1):
                return 2
            else:
                goal = transform_board_to_screen(but)
                case_color = get_case_color(goal)#0 black, 1 white
                if(case_color): #white bishop
                    return 5
                else:
                    return 2
        else:
            if(positions[1][2]== (-1,-1) and positions[1][5]== (-1,-1)):
                return -1
            elif (positions[1][2]== (-1,-1)):
                return 5
            elif positions[1][5]== (-1,-1):
                return 2
            else:
                goal = transform_board_to_screen(but)
                case_color = get_case_color(goal)#0 black, 1 white
                if(case_color): #white bishop
                    return 2
                else:
                    return 5
    else:
        if(color):
            return piecesw[letter]
        else:
            return piecesb[letter]
