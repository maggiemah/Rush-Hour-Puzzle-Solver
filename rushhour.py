import copy

addedStates = [] # list of boards (list of 6 strings) already explored for a puzzle


# Program that solves a 6x6 Rush Hour puzzle.
# Inputs: (1) heuristic choice: 0 = simple blocking, 1 = better alt; used in calculateCost()
#         (2) the initial game board as a list of six 6-character strings
# Outputs: if the starting board is determined to have no solution immediately, prints "No solution" and returns
#          otherwise, calls bestfirstsearch(): prints board path, # of moves, # of states explored if solution found
def rushhour(h, start):
    # store vehicles and their positions/coordinates into dictionary
    vehicles = createDictionary(start) # char : {(x1,y1), (x2,y2), ...}

    # find the orientation of each vehicle and their rows/columns and store them in direction dictionary
    direction = {}  # char : tuple('r' if horizontal or 'c' if vertical, row/col);
                    # example: {'X' : ('r', 2)}
    for key in vehicles:
        if(min(vehicles[key])[0] == max(vehicles[key])[0]):
            direction[key] = ('r', min(vehicles[key])[0])
        else:
            direction[key] = ('c', min(vehicles[key])[1])

    hncost = calculateCost(start, vehicles, h, direction)
    initboardO = Board(start, [], hncost)
    if initboardO.hncost == float('inf'): # guaranteed that no solution exists
        print("No solution")
        return
    bestfirstsearch(initboardO, h, direction)
    addedStates.clear()

# Function that iteratively generates new states to explore generated states in the smallest to largest order
# of f(n) = heuristic cost (h(n)) + length of path (g(n)).
# Inputs: (1) the initial board as a Board object
#         (2) heuristic choice passed in by user when calling rushhour() (0 or 1)
#         (3) dictionary that stores orientation of each vehicle and their rows/columns (char : tuple(char, int))
# Outputs: if solution is found, prints the path to solution, total moves, and states explored and returns 1.
#          otherwise, returns 0
def bestfirstsearch(startBoard, h, direction):
    exploredCount = 1
    frontier = [startBoard] # list of Board objects that gets sorted by total cost
    while True:
        if frontier == []:
            return exploredCount
        # g(n) is the length of the path
        frontier.sort(key = lambda board: (board.hncost + len(board.path))) # sort frontier by total cost f(n) = h(n) + g(n)
        front = frontier[0] # choose node with smallest cost
        frontier.remove(front)
        if front.hncost == 0: # goal state reached
            front.printPath()
            print("Total moves: ", len(front.path)-1)
            print("Total states explored: ", exploredCount)
            return exploredCount
        else: # goal state not reached, so expand current node
            newStates = generateNewStates(front, h, direction)
            frontier = newStates + frontier
        exploredCount += 1

# Class to store board, path, and heuristic cost h(n) as one object.
# naming convention: boardO is obeject Board, boardS string list
# Inputs: (1) board represented as a list of six 6-character strings
#         (2) path represented as a list of boards like (1) leading to input board
#         (3) the heuristic cost of input board
# self.board: the inputted board represented as a list of six 6-character strings
# self.path: path represented as a list of boards like (1) including input board
# self.hncost: the heuristic cost of the input board
class Board:
    def __init__(self, board, path, hncost):
                         # Examples:
        self.board = board         # ["------","--B---","XXB---","--BAA-", "------","------"]
        self.path = path + [board] #  [["--B---","--B---","XXB---","--AA--", "------","------"],
                                   #   ["--B---","--B---","XXB---","---AA-", "------","------"]
                                   #   ["------","--B---","XXB---","--BAA-", "------","------"]]
        self.hncost = hncost

    # Function that prints all boards in the path
    # Called by instance.printPath()
    def printPath(self):
        for i, board in enumerate(self.path):
            printBoard(board)

    # Function that updates board (dictionary representation) by moving a chosen vehicle to the left one spot.
    # Inputs: (1) board represented as a dictionary of vehicle names to a set of
    #             tuples as coordinates {key : {(x1,y1), (x2,y2), ...}}
    #         (2) the key/character name of the vehicle to be moved (e.g. 'X', 'B')
    # Outputs: updates given dictionary (1) with correct corresponding tuples for each key
    def moveLeft(self, vehicles, key):
        # remove rightmost part of vehicle, add to left
        rCoor = max(vehicles[key]) #rightmost coordinate of vehicle
        vehicles['-'].add(rCoor)
        vehicles[key].remove(rCoor)
        lCoor = min(vehicles[key]) #leftmost coordinate of vehicle
        vehicles[key].add((lCoor[0], lCoor[1]-1))
        vehicles['-'].remove((lCoor[0], lCoor[1]-1))

    # Function that updates a board by moving a chosen vehicle to the right one spot.
    # Inputs: (1) board represented as a dictionary of vehicle names to a set of
    #             tuples as coordinates {key : {(x1,y1), (x2,y2), ...}}
    #         (2) the key/character name of the vehicle to be moved (e.g. 'X', 'B')
    # Outputs: updates given dictionary (1) with correct corresponding tuples for each key
    def moveRight(self, vehicles, key):
        # remove leftmost part of vehicle, add to right
        rCoor = min(vehicles[key]) #leftmost coordinate of vehicle
        vehicles['-'].add(rCoor)
        vehicles[key].remove(rCoor)
        lCoor = max(vehicles[key]) #rightmost coordinate of vehicle
        vehicles[key].add((lCoor[0], lCoor[1]+1))
        vehicles['-'].remove((lCoor[0], lCoor[1]+1))

    # Function that updates a board by moving a chosen vehicle down one spot.
    # Inputs: (1) board represented as a dictionary of vehicle names to a set of
    #             tuples as coordinates {key : {(x1,y1), (x2,y2), ...}}
    #         (2) the key/character name of the vehicle to be moved (e.g. 'X', 'B')
    # Outputs: updates given dictionary (1) with correct corresponding tuples for each key
    def moveDown(self, vehicles, key):
        # remove uppermost part of vehicle, add to bottom
        hCoor = min(vehicles[key]) #highest coordinate of vehicle
        vehicles['-'].add(hCoor)
        vehicles[key].remove(hCoor)
        lCoor = max(vehicles[key]) #lowest coordinate of vehicle
        vehicles['-'].remove((lCoor[0]+1, lCoor[1]))
        vehicles[key].add((lCoor[0]+1, lCoor[1]))

    # Function that updates a board by moving a chosen vehicle up one spot.
    # Inputs: (1) board represented as a dictionary of vehicle names to a set of
    #             tuples as coordinates {key : {(x1,y1), (x2,y2), ...}}
    #         (2) the key/character name of the vehicle to be moved (e.g. 'X', 'B')
    # Outputs: updates given dictionary (1) with correct corresponding tuples for each key
    def moveUp(self, vehicles, key):
        # remove lowermost part of vehicle, add to top
        hCoor = max(vehicles[key]) #lowest coordinate of vehicle
        vehicles['-'].add(hCoor)
        vehicles[key].remove(hCoor)
        lCoor = min(vehicles[key]) #highest coordinate of vehicle
        vehicles['-'].remove((lCoor[0]-1, lCoor[1]))
        vehicles[key].add((lCoor[0]-1, lCoor[1]))

# Function to find all possible boards by making any one legal move on a board.
# Inputs: (1) Board object containing a board from which to generate new states
#         (2) heuristic choice passed in by user when calling rushhour() (0 or 1)
#         (3) dictionary that stores orientation of each vehicle and their rows/columns (char : tuple(int, int))
# Output: a list of Board objects that can result from making 1 legal move on boardO
def generateNewStates(boardO, h, direction):
    newStates = []
    board = boardO.board # board (list of six strings representation)
    vehicles = createDictionary(board) # board (dictionary representation)
    for key in vehicles: # for all vehicles on the board (key is name of vehicle)
        if direction[key][0] == 'r': # if vehicle is horizontal
            row = max(vehicles[key])[0] # row of rightmost part of vehicle
            col = max(vehicles[key])[1] # col of rightmost part of vehicle
            if col < 5 and board[row][col+1] == '-': # vehicle has space to move right AND space not occupied
                copyVeh = copy.deepcopy(vehicles)
                boardO.moveRight(copyVeh, key)
                newBoard = getBoard(copyVeh)
                if newBoard not in addedStates: # board hasn't been added to frontier
                    addedStates.append(newBoard)
                    hncost = calculateCost(newBoard, copyVeh, h, direction)
                    newStates.append(Board(newBoard, boardO.path, hncost))
            row = min(vehicles[key])[0] # row of leftmost part of vehicle
            col = min(vehicles[key])[1] # col of leftmost part of vehicle
            if col > 0 and board[row][col-1] == '-': # vehicle has space to move left AND space not occupied
                copyVeh = copy.deepcopy(vehicles)
                boardO.moveLeft(copyVeh, key)
                newBoard = getBoard(copyVeh)
                if newBoard not in addedStates: # board hasn't been added to frontier
                    addedStates.append(newBoard)
                    hncost = calculateCost(newBoard, copyVeh, h, direction)
                    newStates.append(Board(newBoard, boardO.path, hncost))
        else: # if vehicle is vertical
            row = max(vehicles[key])[0] # row of bottommost part of vehicle
            col = max(vehicles[key])[1] # col of bottommost part of vehicle
            if row < 5 and board[row+1][col] == '-': # vehicle has space to move down AND space not occupied
                copyVeh = copy.deepcopy(vehicles)
                boardO.moveDown(copyVeh, key)
                newBoard = getBoard(copyVeh)
                if newBoard not in addedStates: # board hasn't been added to frontier
                    addedStates.append(newBoard)
                    hncost = calculateCost(newBoard, copyVeh, h, direction)
                    newStates.append(Board(newBoard, boardO.path, hncost))
            row = min(vehicles[key])[0] # row of uppermost part of vehicle
            col = min(vehicles[key])[1] # col of uppermost part of vehicle
            if row > 0 and board[row-1][col] == '-': # vehicle has space to move up AND space not occupied
                copyVeh = copy.deepcopy(vehicles)
                boardO.moveUp(copyVeh, key)
                newBoard = getBoard(copyVeh)
                if newBoard not in addedStates: # board hasn't been added to frontier
                    addedStates.append(newBoard)
                    hncost = calculateCost(newBoard, copyVeh, h, direction)
                    newStates.append(Board(newBoard, boardO.path, hncost))
    return newStates

# Function to calculate the h(n) cost of a board based on the heuristic chosen.
# Inputs: (1) board represented as a list of six 6-character strings
#         (2) board represented as a dictionary of vehicle names to a set of
#             tuples as coordinates {key : {(x1,y1), (x2,y2), ...}}
#         (3) heuristic choice passed in by user when calling rushhour() (0 or 1)
#         (4) dictionary that stores orientation of each vehicle and their rows/columns (char : tuple(int, int))
# Output: returns h(n) cost as an integer
def calculateCost(boardS, dic, heuristic, direction):
    row3 = boardS[2]
    if "XX" not in row3: #infinite cost if X car not in row with exit
        return float('inf')

    maxColX = max(dic['X'])[1] # rightmost column of 'X'

    # calculate cost using blocking heuristic
    if heuristic == 0:
        if maxColX == 5: # goal state reached
            return 0
        hn = 1
        for i in range(maxColX+1, 6):
            if row3[i] != '-':
                hn += 1
        return hn

    # calculate cost using alternate heuristic
    else:
        # Heuristic part 1:
        # Similar to blocking heuristic, but the closer X is to the goal, the lower the h(n).
        # This works better because the heuristic would choose to explore a board with row 3 "---XX-" over
        # "-XX---" for example, while these two boards could be the same cost in the blocking heuristic.
        if maxColX == 5: # goal state reached
            return 0
        hn = 6
        blocking = set() # names of vehicles blocking X car
        for i in range(maxColX+1, 6):
            if row3[i] != '-':
                hn += 1
                blocking.add(row3[i])
        if hn == 6: # if hn is 6, then no cars are blocking so return
            return hn-maxColX
        # Heuristic part 2:
        # h(n) increases based on how many vehicles are in the way of the vehicles in the way of X or potentially could be in the way in the future.
        # If the vehicles are in the same column as the blocking vehicle, h(n) increases based on how far away that vehicle is.
        # This works because it prioritizes boards where you can move the vehicles blocking X out of X's way.
        for key in blocking:
            if direction[key][0] == 'r' or len(dic[key]) > 3:
                return float('inf')
            column = direction[key][1]
            uppestRow = min(dic[key])[0]
            lowestRow = max(dic[key])[0]
            scale = 0.5
            while uppestRow > 0:
                if boardS[uppestRow-1][column] != '-':
                    hn += scale
                scale *= 0.6
                uppestRow -= 1
            scale = 0.5
            while lowestRow < 5:
                if boardS[lowestRow+1][column] != '-':
                    hn += scale
                scale *= 0.6
                lowestRow += 1
        return hn

# Function that converts board representation from a list of six strings to a dictionary
# Input: board represented as a list of six 6-character strings
# Output: board represented as a dictionary { char of vehicle : set{coordinates as tuples} }
def createDictionary(boardS):
    vehicles = {'X':set()}
    for i in range(0, 6):
        for j in range(0, 6):
            currChr = boardS[i][j]
            if currChr not in vehicles:
                vehicles[currChr] = {(i, j)}
            else:
                vehicles[currChr].add((i, j))
    return vehicles

# Function that converts board representation from a dictionary to a list of six strings
# Input: board represented as a dictionary { char of vehicle : set{coordinates as tuples} }
# Output: board represented as a list of six 6-character strings
def getBoard(vehicles):
    board = [['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-']]
    for key in vehicles:
        for row, col in vehicles[key]:
            board[row][col] = key
    for i in range(0, 6):
        board[i] = ''.join(board[i])
    return board

# Function to print the board neatly to the terminal
# Input: board represented as a list of six 6-character strings
# Output: prints board
def printBoard(boardS):
    for i, board in enumerate(boardS):
        print(' ', board)
    print()

'''
Recursive best first search
Recursion limit  reached for expert levels, so would have to increase Python recursion limit.
To use, replace line 107 in rushhour:
    exploredCount = [0] # initialized as list so that the argument passes by reference for recursive
    bestfirstsearch([initboardO], exploredCount, h, direction)
# Function that recursively calls itself to explore generated states in the smallest to largest order of
# heuristic cost + length of path.
# Inputs: (1) frontier of states as a list of Board objects that gets sorted by total cost
#         (2) a list of one integer representing number of states removed and explored from frontier
#         (3) heuristic choice passed in by user when calling rushhour() (0 or 1)
#         (4) dictionary that stores orientation of each vehicle and their rows/columns (char : tuple(int, int))
# Outputs: if solution is found, prints the path to solution, total moves, and states explored and returns 1.
#          otherwise, returns 0
def bestfirstsearch(frontier, exploredCount, h, direction):
    exploredCount[0] += 1
    # g(n) is len(boardO.path)
    frontier.sort(key = lambda board: (board.hncost + len(board.path))) # sort frontier by total cost f(n) = h(n) + g(n)
    if frontier == []:
        return 0
    front = frontier[0] # choose board with the lowest total cost
    frontier.remove(front)
    if(front.hncost == 0): # goal state reached
        front.printPath()
        print("Total moves: ", len(front.path)-1)
        print("Total states explored: ", exploredCount[0])
        return 1
    else:
        newStates = generateNewStates(front, h, direction)
        return bestfirstsearch(newStates + frontier, exploredCount, h, direction) # add new states to frontier
'''

rushhour(1,['AAABCD','EFFBCD','E-XXCD','GGH---','-IH-JJ','-IKKLL'])