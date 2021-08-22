#Parminder Singh
#RUSH HOUR

#rushhour(0,["--AABB", "--CDEF", "XXCDEF", "--GGHH", "------", "------"])

from queue import PriorityQueue


#This is the main function that runs the program, it asks for the heursitic type which is 0 for blocking and 1 for custom
#Does not return anything, it prints out our Total Moves and Total States explored.
def rushhour(heuristicType,originalBoard):
    startState = convertInput(originalBoard) #checked
    board = boardLocations(startState) #checked
    path, statesExplored = stateSearch(heuristicType,startState,board)
    if path == None:
        print("NO SOLUTION")
    printPath(path)
    print("Total moves:", len(path)-1) 
    print("Total states explored:", statesExplored)


# Returns the whole board for example ["--AABB", "--CDEF", "XXCDEF", "--GGHH", "------", "------"] becomes
# '--AABB--CDEFXXCDEF--GGHH------------'

def convertInput(currentStateArray):
    return ''.join(currentStateArray)

#check if goalstate is reached
def isGoal(currentState):
    if currentState[16] == 'X' and currentState[17] == 'X':
        return True
    return False


# Iterative ASTAR implemenation using priority queue wihch is basically best first search
#The function takes in the heuristicType, what the currentState is in the board game, and what all the location of the vehicles are.
#Returns the states and the whole path explored
def stateSearch(heuristicType, inputState, mappedBoard):
    path = []
    queue = PriorityQueue()
    exploredBoard = {}
    currState = ""
    statesExplored = 0
    startState = State()
    startState.fullBoard = inputState
    if updateStates(startState.fullBoard, "", exploredBoard):
        queue.put((0, startState))
    while not queue.empty():
        statesExplored = statesExplored + 1
        currentStatePair = queue.get()
        currentState = currentStatePair[1]
        if isGoal(currentState.fullBoard):
            currState = currentState.fullBoard
            break
        newStateList = createNewStates(currentState.fullBoard, mappedBoard)
        n = len(newStateList)
        for i in range(0,n):
            if heuristicType == 0:
                heuristicValue = blockingHeuristic(newStateList[i])
            elif heuristicType == 1:
                heuristicValue = customHeuristic(newStateList[i], mappedBoard)
            if updateStates(newStateList[i], currentState.fullBoard, exploredBoard):
                # place new states in priority queue
                newState = State()
                newState.fullBoard = newStateList[i]
                newState.h = heuristicValue
                newState.g = currentState.g + 1
                f = newState.g + newState.h
                queue.put((f, newState))
                
    # Back track through explored board to get to the path
    path.append(currState)
    currState = exploredBoard.get(currState, "")
    while currState != "":
        path.append(currState)
        currState = exploredBoard.get(currState, "")
    # reverse path so it goes start to goal
    path.reverse()
    # validate path
    if path[0] == inputState:
        return path, statesExplored
    return None, None


#Move generations located here; the inputs are the currentBoard and the board with all locations of the vehiciles mapped out
#Again this function takes in the currentBoard state and the the locations of the vehicles 
#Returns a new board to look at
def createNewStates(currentBoard, boardLocations):
    newBoard = []
    spaceVisited = {}
    i = 0
    while i < 36:
        name = currentBoard[i]
        # not blank and piece not already visited
        if name != '-' and name not in spaceVisited:
            spaceVisited[name] = True
            vehicleOrientation = boardLocations[name].orientation
            vehicleLength = boardLocations[name].length
            # vehicle is horizontal
            if vehicleOrientation == 0:
                if i%6 > 0 and currentBoard[i-1] == '-':
                    newBoardStateList = list(currentBoard)
                    newBoardStateList[i-1] = name
                    newBoardStateList[i+vehicleLength-1] = '-'
                    newBoard.append(''.join(newBoardStateList))
                # move right
                if i%6 < (6-vehicleLength) and currentBoard[i+vehicleLength] == '-':
                    newBoardStateList = list(currentBoard)
                    newBoardStateList[i+vehicleLength] = name
                    newBoardStateList[i] = '-'
                    newBoard.append(''.join(newBoardStateList))
            # vehicle is vertical
            elif vehicleOrientation == 1:
                # go up
                if i > 5 and currentBoard[i-6] == '-':
                    newBoardStateList = list(currentBoard)
                    newBoardStateList[i-6] = name
                    newBoardStateList[i+(vehicleLength-1)*6] = '-'
                    newBoard.append(''.join(newBoardStateList))
                # go down
                if i < (36-vehicleLength*6) and currentBoard[i+vehicleLength*6] == '-':
                    newBoardStateList = list(currentBoard)
                    newBoardStateList[i+vehicleLength*6] = name
                    newBoardStateList[i] = '-'
                    newBoard.append(''.join(newBoardStateList))
        i += 1
    return newBoard



# Marks a state as visited and checks if it has already been visited.
# Returns False if previously visited a true if first visit
#Takes in the currentBoard state and the parent board and the total board
#returns True or false based on whether there is a cycle
def updateStates(currentBoard, parentBoard, exploredBoard):  #updatestates
    if(currentBoard in exploredBoard): #checks cycle 
        return False
    exploredBoard[currentBoard] = parentBoard
    return True


class State:

    def __init__(self):
        self.fullBoard = ""
        # g =  g(n) , h = heuristic value h(n)
        self.g = 0 
        self.h = 0

    # WHEN THE H(N) VALUES ARE THE SAME WE ARBRITARILY CHOOSE LEFT! I had to change the dunder method for that to work.
    def __lt__(self, other):
        return self.h < other.h

# this class contains the info of vehicle's: orientation, length, name 
class vehicle:

    def __init__(self):
        # orientation: 0 = horizontal, 1 = vertical
        # used for computing available movements
        self.orientation = 0
        self.length = 0
        # The name is the single letter character identifier on the board
        self.name = ""


#This function returns the locations of every vehicle on the current board state.
#The only input is the currentState so it can locate the locations of the vehicles
def boardLocations(currentState):
    # create a dictionary of pieces
    board = {}
    for i in range(0, 36):
        char = currentState[i]
        if char != '-' and char not in board:
            board[char] = vehicle()
            board[char].name = char
            board[char].length = 1
            # follow the piece
            if i%6 < 5:
                # check right
                j = i+1
                if char == currentState[j]:
                    board[char].orientation = 0
                    while j%6 > 0:
                        if char == currentState[j]:
                            board[char].length = board[char].length+1
                            j = j+1
                        else:
                            break
            if i < 30:
                # check down
                j = i+6
                if char == currentState[j]:
                    board[char].orientation = 1
                    while j < 36:
                        if char == currentState[j]:
                            board[char].length = board[char].length+1
                            j = j+6
                        else:
                            break
    return board    
    

#prints each state in the end
#input is currentBoard state
def printState(currState):
    for i in range(0, 36):
        print(currState[i], end = '')
        if i%6 == 5:
            print("\n", end = '')
#prints each path at the end
def printPath(path):
    n = len(path)
    for i in range(0, n):
        printState(path[i])
        print("\n", end = '')


#HEURISTICS ---------------------------------------------------------------------------------------------

# blocking heuristic
#checks all blocking vehicles in the third row of the board, adds 1 to h(n) for each vehicle
#hn is h(n) value
def blockingHeuristic(currState):
    foundXXcar = False
    i = 12
    # find pieces on third row
    if isGoal(currState):
        return 0
    hn = 1
    while i < 18:  #car is only located on on row 3 which is slot 12 to 18 in my string
        if not foundXXcar and currState[i] == 'X':
            foundXXcar = True
        elif foundXXcar and currState[i] != '-' and currState[i] != 'X':
            hn = hn+1
        i += 1
    return hn


#My approach for my custom heuristic was that if a car is blocking  the xx car, h(n) value goes up by 1 if THAT car itself is being blocked in any way, h(n) value goes up by 2
#This way the blocking car will be able to escape faster due to all the blocking vehicles moving out of the way faster because each car is being checked in all directions
#for another blocking vehicle.
def customHeuristic(currState, states): 
    foundXXcar = False
    blockingCarsSeen = {}
    i = 12
    # find pieces on third row
    if isGoal(currState):
        return 0
    hn = 1
    while i < 18:  #car is only located on on row 3 which is slot 12 to 18 in my string
        if not foundXXcar and currState[i] == 'X':
            foundXXcar = True
            blockingCarsSeen["X"] = True

        elif foundXXcar and currState[i] != '-' and (currState[i] not in blockingCarsSeen):  # if i found the x car already, AND the current location has a vehicle that i havent seen
            #before, add it to my dictionary called blockingCarsSeen
            blockingCarsSeen[currState[i]] = True
            hn += 1
            if currState[i+6] not in blockingCarsSeen:
                blockingCarsSeen[currState[i+6]] = True
                hn += 2

            elif currState[i-6] not in blockingCarsSeen:
                blockingCarsSeen[currState[i-6]] = True
                hn += 2
            
            elif (currState[i-6] not in blockingCarsSeen) and (currState[i+6] not in blockingCarsSeen):
               blockingCarsSeen[currState[i+6]] = True
               blockingCarsSeen[currState[i-6]] = True
               hn += 2
        
        
        elif foundXXcar and currState[i] != '-' and currState[i] in blockingCarsSeen: 
            
            if currState[i+6] not in blockingCarsSeen:
                blockingCarsSeen[currState[i+6]] = True
                hn += 2

            elif currState[i-6] not in blockingCarsSeen:
                blockingCarsSeen[currState[i-6]] = True
                hn += 2
            
            elif (currState[i-6] not in blockingCarsSeen) and (currState[i+6] not in blockingCarsSeen):
               blockingCarsSeen[currState[i+6]] = True
               blockingCarsSeen[currState[i-6]] = True
               hn += 2
        
        i += 1
    return hn

