from queue import PriorityQueue
#Parminder Singh

#rushhour(0,["--AABB", "--CDEF", "XXCDEF", "--GGHH", "------", "------"]) test case beginner


#Gets initial input board and outputs it all into one string.
def convertInput(currentStateArray):
    return ''.join(currentStateArray)

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




