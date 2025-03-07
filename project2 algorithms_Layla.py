""" Created on Wed Mar 5 11:48:38 2025

@author: Layla Le
"""

# Global variables
row_size = 9
col_size = 6

# Global array representing the map
arr_map = [
    [0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [-1, 0, 0, 0, 0, -1],
    [0, 0, 0, 0, -1, -1],
    [0, 0, 0, 0, 0, -1],
    [0, 0, 0, 0, 0, 0],
    [-1, -1, -1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [99, 0, 0, 0, 0, 0],
]  # 0 is empty space, -1 is barrier, 2 is robot, 99 is goal

def move_forward(blocks):
    pass

def turn_left():
    pass

def turn_right():
    pass

def findGoal():
    for row in range(row_size):
        for col in range(col_size):
            if arr_map[row][col] == 99:
                return row,col


def findRobot():
    for row in range(row_size):
        for col in range(col_size):
            if arr_map[row][col] == 2:
                arr_map[row][col] = -99 #change symbol for robot position
                return row,col


    
def waveShoot():
    row_goal, col_goal = findGoal()
    row_robot, col_robot = findRobot()
    next = [(row_goal, col_goal)]
    x = 1
    directions = [(-1,0), (1, 0), (0, -1), (0, 1)] #Up, down, right, left
    count = 0
    while next:
        new_position = []
        for row, col in next:
            for row_direct, col_direct in directions:
                new_row = row + row_direct
                new_col = col + col_direct
                if (0 <= new_row < row_size) and (0 <= new_col < col_size) and (arr_map[new_row][new_col] != "x") and (arr_map[new_row][new_col] == 0):
                    new_position.append((new_row, new_col))
                    arr_map[new_row][new_col] = x
            count += 1
        if count == len(next):
            next = new_position
            x += 1
        print(arr_map)
        
def wavefrontSearch():
    row_goal, col_goal = findGoal()
    row_robot, col_robot = findRobot()
    waveShoot()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    min_val = None
    move = ()
    while arr_map[row_robot][col_robot] != 99: 
        for row_direct, col_direct in directions:
            new_row = row_robot + row_direct
            new_col = col_robot + col_direct
            if 0 <= new_row < row_size and 0 <= new_col < col_size and arr_map[new_row][new_col] != -1:
                if arr_map[new_row][new_col] < min_val and arr_map[new_row][new_col] > 0:
                    min_val = arr_map[new_row][new_col]
                    move = (row_direct, col_direct)
        if move == directions[1]:
            move_forward()
        elif move == directions[2]:
            turn_left()
            move_forward
        elif move == directions[3]:
            turn_right()
            move_forward
        print(arr_map)

        
    

