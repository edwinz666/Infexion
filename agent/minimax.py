import copy
from json.encoder import INFINITY
from .internalBoard import InternalBoard

import math

PRINT_COUNT = 0

DIM = 7
MAX_POWER = DIM-1
MAX_BOARD_POW = 49
MAX_TURNS = 343

DIRECTIONS = ((1,-1), (1,0), (0,1), (-1,1), (-1,0), (0,-1))
ENEMY = {'r': 'b', 'b': 'r'}

################################################################################
############################# Minimax Class ####################################
################################################################################

class minimax:
    
    def __init__(self, board: InternalBoard):
        self.board = board
        self.state = board.internalBoard
        
        
    # minimax implementation

    # state: the current board state
    # game: game description
    # alpha: MAX score along the path to state
    # beta: MIN score along the path to state
    
    # depth: the depth of the search
    
    def max_value(self, state: dict[tuple, tuple], alpha, beta, colour, depth):
        
        this_state = InternalBoard()
        this_state.internalBoard = copy.deepcopy(state)
        
        if(colour == 'r'):
            new_colour = 'b'
        else: 
            new_colour = 'r'
        
        if self.board.turn >= MAX_TURNS:
            return 0 
        
        if self.board.turn > 1: #self.board.is_terminal():
            if self.board.countPieces('r') == 0:
                return -1000
            elif self.board.countPieces('b') == 0:
                return 1000

        if depth == 0:
            return evaluateAtkDef(state, new_colour) # evaluatePower(state) # 
        
        v = -math.inf
           
        for s in get_successors(this_state, new_colour):
            #print("successor again: = ",s)
            v = max(v, self.min_value(s[0], alpha, beta, new_colour, depth - 1))

            #if v == math.inf:
                #print("value of v is ",v)
            alpha = max(alpha, v)
            if alpha >= beta:
                return beta
            
        return v
    
    def min_value(self, state: dict[tuple, tuple], alpha, beta, colour, depth):
        global PRINT_COUNT
        
        this_state = InternalBoard()
        this_state.internalBoard = copy.deepcopy(state)
        
        if(colour == 'r'):
            new_colour = 'b'
        else: 
            new_colour = 'r'
            
        # if this_state.is_terminal():  
        # ----> TERMINAL STATES NEEDS TO RETURN EVALUATION INFINITY OR NEGATIVE INFINITY
        # E.g. if there is no BLUE pieces --> Red wins. therefore infinity evaluation
        #      if there is no RED pieces --> Blue wins, therefore negative infinity evaluation
        # is_terminal() whether no blue or no red pieces remains, and assign the above evaluations accordingly,
        # rather than considering whether either no blue or red pieces

        if self.board.turn >= MAX_TURNS:
            return 0

        if self.board.turn > 1: #self.board.is_terminal():
            if self.board.countPieces('r') == 0:
                return -1000
            elif self.board.countPieces('b') == 0:
                return 1000

        if depth == 0:
            return evaluateAtkDef(state, new_colour) # evaluatePower(state) # 

        
        v = math.inf
                
        for s in get_successors(this_state, new_colour):
            v = min(v, self.max_value(s[0], alpha, beta, new_colour, depth - 1))
            """
            if PRINT_COUNT < 2 and (self.max_value(s[0], alpha, beta, new_colour, depth - 1) == math.inf):
                print("successor is infinity with board below")
                print(render_board(s[0]))
                PRINT_COUNT += 1
            """
            if v <= alpha:
                return v
            beta = min(beta, v)
        
        #if v == math.inf:
        #    print("v is still", v)
        return v
    
    # colour should affect this algorithm
    def next_move(self, board: InternalBoard, colour):
        self.board = board
        # self.state = board.internalBoard
        
        #best_score = -math.inf
        best_score = None
        alpha = -math.inf
        beta = math.inf
        next_move = None
        
        if colour == 'r':
            best_score = -math.inf
            for s in get_successors(self.board, colour):
                #print("successor : ", s)
                
                #print("calling minvalue for child")
                score = self.min_value(s[0], alpha, beta, colour, 3)

                #print(f"score is {score}")
                if score > best_score:
                    best_score = score
                    next_move = s
                alpha = max(alpha, best_score)
        
        else:
            best_score = math.inf
            for s in get_successors(self.board, colour):
                #print("successor : ", s)
                
                #print("calling maxvalue for child")
                score = self.max_value(s[0], alpha, beta, colour, 3)

                #print(f"score is {score}")
                if score < best_score:
                    best_score = score
                    next_move = s
                beta = min(beta, best_score)
        
        
        if next_move is None:
            print("well you lost")
            return None
        
        print(next_move[1])   
        return next_move[1]
    
################################################################################
######################## Minimax Helper Functions ##############################
################################################################################
    
def generateCoveragePositionPower():
    coveragePositionPower = {}

    for i in range(DIM):
        for j in range(DIM):
            position = (i, j)
            for power in range(1,4):
                covered = []
                for direction in DIRECTIONS:
                
                    # Finds the destination of a node after a move in a direction 
                    tempPower = power
                    tempR = position[0]
                    tempQ = position[1]

                    while tempPower:
                        newR = tempR + direction[0]
                        newQ = tempQ + direction[1]

                        # require both r and q to be positive, and also less than the dimension
                        if newR < 0:
                            newR = DIM - 1
                        elif newR >= DIM:
                            newR = 0

                        if newQ < 0:
                            newQ = DIM - 1
                        elif newQ >= DIM:
                            newQ = 0 
                        if (newR, newQ) not in covered:
                            covered.append((newR, newQ))
                    
                        tempR = newR
                        tempQ = newQ

                        tempPower -= 1
                
                coveragePositionPower[(position, power)] = covered
                if power == 3:
                    for restPower in range(4, 7):
                        coveragePositionPower[(position, restPower)] = covered
    return coveragePositionPower

coveragePositionPower = generateCoveragePositionPower()
   
    
# get the successors, possible states we should explore
def get_successors(board: InternalBoard, colourToMove):

    global PRINT_COUNT
    successors = []

    # do we need to copy board into state? just use the board argument
    state = copy.deepcopy(board)
    temp = copy.deepcopy(board)
    
    # loop through the board and find all player's piece
    # when you land on a piece perform a spread in 6 directions
    # if it is empty spawn a piece
    # add to the successors list
    
    coverages = getCoverages(board.internalBoard)
    colourToMoveCoverage = None
    colourJustPlayedCoverage = None

    if colourToMove == 'r':
        colourToMoveCoverage = coverages[0]
        colourJustPlayedCoverage = coverages[1]
    else:
        colourToMoveCoverage = coverages[1]
        colourJustPlayedCoverage = coverages[0]
    
    for position in state.internalBoard.keys():
        if(state.internalBoard.get(position)[0] == colourToMove):
            
            # spread in all directions
            for direction in DIRECTIONS:
                temp.spread(position, direction)

                if temp.countPieces(ENEMY[colourToMove]) >= board.countPieces(ENEMY[colourToMove]):
                    temp = copy.deepcopy(board)
                    continue


                successors.append((temp.internalBoard, ('spread', position, direction)))
                temp = copy.deepcopy(board) # reset temp to original state

    if getTotalPower(state.internalBoard) < MAX_BOARD_POW:
        temp = copy.deepcopy(board)
        for r in range(DIM):
            for q in range(DIM):
                if (r,q) not in state.internalBoard.keys():
                    playerCoverage = colourToMoveCoverage[r,q]
                    if (playerCoverage > 0 or board.turn < 2) and playerCoverage >= colourJustPlayedCoverage[(r,q)]:
                        temp.spawn((r, q), colourToMove)
                        successors.append((temp.internalBoard, ('spawn', (r, q), colourToMove)))
                        temp = copy.deepcopy(board)
    # fail safe
    if not successors:
        temp = copy.deepcopy(board)
        found = False

        if getTotalPower(state.internalBoard) < MAX_BOARD_POW:
            temp = copy.deepcopy(board)
            found = False
            for r in range(DIM):
                if found:
                    break
                for q in range(DIM):
                    if (r,q) not in state.internalBoard.keys():
                        found = True
                        temp.spawn((r, q), colourToMove)
                        successors.append((temp.internalBoard, ('spawn', (r, q), colourToMove)))
                        break
        else:
            for position in state.internalBoard.keys():                
                if(state.internalBoard.get(position)[0] == colourToMove):
                    temp.spread(position, (0,1))
                    successors.append((temp.internalBoard, ('spread', position, (0,1))))
                    break
    
    return successors

# higher power favours red, lower power favours blue
def evaluatePower(board: dict[tuple, tuple]):
    totalPower = 0
    for v in board.values():
        if v[0] == 'r':
            totalPower += v[1]
        else:
            totalPower -= v[1]
    return totalPower

def getTotalPower(board):
    power = 0
    for (_, (_, k)) in board.items():
        power += k
    return power

def generateCoverageDict():
    coverage = {}

    for i in range(DIM):
        for j in range(DIM):
            coverage[(i,j)] = 0

    return coverage

# gives each node's power (or something else?) to a certain player based on
# the node's colour and 
def evaluateAtkDef(board: dict[tuple, tuple], colourToMove):
    # 1. generate two arrays 7x7 ? for both colours
    # 2. go over every node, and add to covered squares in array based on colour
    # 3. go over every node again, but compare array coverages based on colour
    # 4.    for every node ... add power based on who wins
    # 5. if colourToMove is RED ... remove blue's best capture if available

    # 1. 
    colourToMoveCoverage = generateCoverageDict()
    colourJustPlayedCoverage = generateCoverageDict()

    # MAYBE ONLY NEED LIST FOR colourJustPlayed ... to remove the best capture for that colour
    colourToMoveScores = []
    colourJustPlayedScores = []

    # 2.
    for (position, (colour, power)) in board.items():
        for covered in coveragePositionPower[(position, power)]:
            if colour == colourToMove:
                colourToMoveCoverage[covered] += 1
            else:
                colourJustPlayedCoverage[covered] += 1
    
    # 3.
    for (position, (colour, power)) in board.items():
        if colour == colourToMove:
            if colourToMoveCoverage[position] > colourJustPlayedCoverage[position]:
                colourToMoveScores.append(power)
            else:
                colourJustPlayedScores.append(power)
        else:
            if colourJustPlayedCoverage[position] > colourToMoveCoverage[position]:
                colourJustPlayedScores.append(power)
            else:
                colourToMoveScores.append(power)
    
    # 4.
    sortJustPlayedScores = sorted(colourJustPlayedScores)
    
    if sortJustPlayedScores:
        sortJustPlayedScores.pop()

    if colourToMove == 'r':
        return sum(colourToMoveScores) - sum(sortJustPlayedScores)
    else:
        return sum(sortJustPlayedScores) - sum(colourToMoveScores)

def getCoverages(board):
    redCoverage = generateCoverageDict()
    blueCoverage = generateCoverageDict()

    # 2.
    for (position, (colour, power)) in board.items():
        for covered in coveragePositionPower[(position, power)]:
            if colour == 'r':
                redCoverage[covered] += 1
            else:
                blueCoverage[covered] += 1

    return (redCoverage,blueCoverage)