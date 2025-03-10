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


def move_forward():
    pass

def turn_left():
    pass

def turn_right():
    pass

def move_backward():
    turn_left()
    turn_left()
    move_forward()
    turn_left()
    turn_left()

def findGoal(): #the user-function to find the coordinates of the goal
    for row in range(row_size):
        for col in range(col_size): #loop through each cell and row in the array
            if arr_map[row][col] == 99:
                return row,col #return the coordinates of the goal


def findRobot(): #the user-function to find the coordinates of the robot
    for row in range(row_size):
        for col in range(col_size): #loop through each cell and row in the array
            if arr_map[row][col] == 2:
                arr_map[row][col] = -99 #change symbol for robot position so as not to be confused with other symbols
                return row,col #return the coordinates of the robot


    
def waveShoot(): #the user-function to shoot waves marking incrementing steps spreading outward from one cell to its adjacent cells, marking and replacing the value of each cell with the wavestep number indicating how many steps it takes for the robot to reach said cell if it starts from the goal
    row_goal, col_goal = findGoal() #run the function to find the coordinates of the goal
    next = [(row_goal, col_goal)] #An array of tuples storing the coordinates (rows and columns) of the cells in the current wavestep. Initialized with the cooridnates of the goal because the first wavestep is shot outward from the goal to its adjacent cells
    x = 1 #marks the wavestep (how many steps taken to reach a cell from the goal)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    while next: #continue until all the cells in the current step has been accounted for
        new_position = [] #initialize an array to store the cells in the new wavestep
        count = 0 #variable to store the number of cells in the current wavestep that already shot waves to adjacent cells
        for row, col in next: #loop through each cell in the current wavestep
            for row_direct, col_direct in directions: #loop through each of the 4 directions possible in which the wave can shoot
                new_row = row + row_direct
                new_col = col + col_direct  #coordinates of each adjacent cells the wave can shoot to
                if (0 <= new_row < row_size) and (0 <= new_col < col_size) and arr_map[new_row][new_col] != -1 and (arr_map[new_row][new_col] == 0): #ensure the adjacent cell is still within the map, is not a barrier, and is an open space
                    new_position.append((new_row, new_col)) #if the condition above is satisfied, add the adjacent cell to the next wavestep
                    arr_map[new_row][new_col] = x #marks the cell with the corresponding wavestep
            count += 1  #increment for each cell in the current wavestep that already shot waves to adjacent cells
        if count == len(next): #only move on to the cells in the next wavestep if all the cells in the current wavestep have shot wave to adjacent cells
            next = new_position  #replace cells in the current wavestep with its valid adjacent cells for the next wavestep
            x += 1  #an extra step is taken
        
waveShoot()
for row in arr_map:
    print(row)   
              
def wavefrontSearch(): #the robot traces the lowest-numbered cells back to the goal to ensure it reaches the goal in the most efficient path (least steps taken) 
    row_robot, col_robot = findRobot() #run the function to find the coordinates of the robot
    waveShoot() #run the function to shoot waves
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
   
    while arr_map[row_robot][col_robot] != 99: #continue while the goal has not been reached
        move = () #the tuple containing coordinates that indicate the direction in which the robot should move
        min_val = 300 #a hypothetical value to initialize the current lowest-numbered adjacent cell

        for row_direct, col_direct in directions: #loop through each of the 4 directions possible in which the wave can shoot
            new_row = row_robot + row_direct
            new_col = col_robot + col_direct #coordinates of each adjacent cells the wave can shoot to
            if 0 <= new_row < row_size and 0 <= new_col < col_size and arr_map[new_row][new_col] != -1: #ensure the adjacent cell is still within the map and is not a barrier
                if arr_map[new_row][new_col] < min_val and arr_map[new_row][new_col] > 0: #find the next lowest-numbered cell
                    min_val = arr_map[new_row][new_col] 
                    move = (row_direct, col_direct) #if is the new lowest-numbered cell, replace the current lowest-numbered cell and store the direction to reach that adjacent cell
        
        if move:
            row_robot += move[0]
            col_robot += move[1] 
            if move == directions[0]:
                move_backward()
            elif move == directions[1]:
                move_forward()
            elif move == directions[2]:
                turn_left()
                move_forward()
                turn_right()
            elif move == directions[3]:
                turn_right()
                move_forward()
                turn_left()
            #the robot goes to the lowest-adjacent cell. update the coordinates of the robot


        
    

