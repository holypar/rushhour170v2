from queue import PriorityQueue
#Parminder Singh

#rushhour(0,["--AABB", "--CDEF", "XXCDEF", "--GGHH", "------", "------"]) test case beginner


#Gets initial input board and outputs it all into one string.
def convertInput(currentStateArray):
    return ''.join(currentStateArray)


def isGoal(currentState):
    if currentState[16] == 'X' and currentState[17] == 'X':
        return True
    return False


#
def generatePossibleStates(currentBoard, boardLocations):
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
                # move left
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
                # move up
                if i > 5 and currentBoard[i-6] == '-':
                    newBoardStateList = list(currentBoard)
                    newBoardStateList[i-6] = name
                    newBoardStateList[i+(vehicleLength-1)*6] = '-'
                    newBoard.append(''.join(newBoardStateList))
                # move down
                if i < (36-vehicleLength*6) and currentBoard[i+vehicleLength*6] == '-':
                    newBoardStateList = list(currentBoard)
                    newBoardStateList[i+vehicleLength*6] = name
                    newBoardStateList[i] = '-'
                    newBoard.append(''.join(newBoardStateList))
        i += 1
    return newBoard



def updateStates(currentBoard, parentBoard, exploredBoard):
    # python disctionaries are a hash table implementation
    # checking existance of state is only O(1)
    if(currentBoard in exploredBoard):
        return False
    exploredBoard[currentBoard] = parentBoard
    return True




#CLASSES -------------------------------------------------------------------------------------------


class State:
    #g: g(n)
    #h: h(n)
    def __init__(self):
        self.id = ""
        self.g = 0
        self.h = 0
    #f(n) = g(n) + h(n)

    def __lt__(self, other):
        return self.h < other.h #python dunder method to define the less than operator

class vehicle:
    def __init__(self):
        # orientation: 0 = horizontal, 1 = vertical
        self.orientation = 0
        self.length = 0
        self.name = None

#add tile class
#'--AABB--CDEFXXCDEF--GGHH------------'
#A = currentstate[2]

# get the board vehicle locations
def boardLocations(currentState):
    board = {}
    for i in range(0, 36): #literally every tile of the board
        char = currentState[i]
        if char != '-' and char not in board: #if the character is basically any letter that hasnt been read yet, it will be added to the dict.
            board[char] = vehicle()
            board[char].name = char
            board[char].length = 1
            if i%6 < 5:  #0
                j = i+1 #1 #checks the right side of the current location
                if char == currentState[j]:  #checks if the car is horizontal 
                    board[char].orientation = 0    #0 means it is horizontal
                    while j%6 > 0:
                        if char == currentState[j]:
                            board[char].length = board[char].length+1
                            j = j+1
                        else:
                            break
            if i < 30: #everything above the last row of the game board
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


#Prints all states/boards to screen
def printState(currentState):
    i = 0
    while i < 36:
        print(currentState[i], end = '')
        if i%6 == 5:
            print("\n", end = '')
    i += 1


#Print all paths to screen
def printPath(path):
    i = 0
    n = len(path)
    while i < n:
        printState(path[i])
        print("\n", end = '')
    i += 1



#HEURISTICS --------------------------------------------
#hn is the number of pieces blocking the exit
def blockingHeuristic(currState):
    foundXXcar = False
    i = 12
    # find vehicles  on third row
    if isGoal(currState):
        return 0
    hn = 1
    while i < 18:
        if not foundXXcar and currState[i] == 'X':
            foundXXcar = True
        elif foundXXcar and currState[i] != '-' and currState[i] != 'X':
            hn = hn+1
    i += 1
    return hn
