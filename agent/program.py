# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

import copy
from dataclasses import dataclass
from json.encoder import INFINITY
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from .utils import render_board
#from .minimax import minimax

import math
import random

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!


DIM = 7
MAX_POWER = DIM-1
MAX_BOARD_POW = 49
MAX_TURNS = 343

DIRECTIONS = ((1,-1), (1,0), (0,1), (-1,1), (-1,0), (0,-1))
ENEMY = {'r': 'b', 'b': 'r'}

def generateCoveragePositionPower():
    coveragePositionPower = {}

    for i in range(DIM):
        for j in range(DIM):
            position = (i, j)
            for power in range(1,4):
                covered = []
                for direction in DIRECTIONS:
                
                    """ Finds the destination of a node after a move in a direction """
                

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


################################################################################
############################## Agent Class #####################################
################################################################################

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self.board = InternalBoard()
        self.Minimax = minimax(self.board)
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        if self._color == PlayerColor.RED:
            colour = 'r'
        else:
            colour = 'b'

        ######## calling minimax algorithm for next move ########
        next_move = self.Minimax.next_move(self.board, colour)
        if (next_move[0] == 'spread'):
            return SpreadAction(HexPos(next_move[1][0], next_move[1][1]), HexDir(next_move[2]))
        else:
            return SpawnAction(HexPos(next_move[1][0], next_move[1][1]))
        


        # temperary random algorithm
        '''
        r = random.randint(0,6)
        q = random.randint(0,6)

        # dir already taken by Python ? 
        direction = None
        match random.randint(0,5):
            case 0:
                direction = HexDir.Up
            case 1:
                direction = HexDir.UpRight
            case 2:
                direction = HexDir.DownRight
            case 3:
                direction = HexDir.Down
            case 4:
                direction = HexDir.DownLeft
            case 5:
                direction = HexDir.UpLeft
        
        print(render_board(self.board.internalBoard))        
        if (r,q) not in self.board.internalBoard and self.board.totalPower < MAX_BOARD_POW:
            return SpawnAction(HexPos(r, q))
        else:
            myBoard = {}
            for piece in self.board.internalBoard.keys():
                if self.board.internalBoard.get(piece)[0] == colour:
                    myBoard[piece] = self.board.internalBoard.get(piece)
            position = random.choice(list(myBoard.keys()))
            return SpreadAction(HexPos(position[0], position[1]), direction)
        '''
                
                   
    ### DOES IT ACCOUNT FOR OPPONENT"S SPAWNS AND SPREADS? AND PLAYER SPREADS THAT GOES OVER MAX POWER?
    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        Note: this updates your agent as well.
        """
        self.board.turn+=1
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                c = 'r'
                if (color == PlayerColor.BLUE):
                    c = 'b'
                self.board.totalPower += 1
                self.board.spawn((cell.r, cell.q), c)
                return
            
            ### NEED TO RE-CALCULATE POWER for any SPREADS?
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self.board.spread((cell.r, cell.q), (direction.value.r, direction.value.q))
                self.board.totalPower = getTotalPower(self.board)
                return

################################################################################
########################### Ineternal Board Class ###############################
################################################################################

@dataclass
class InternalBoard:
    """
    A data structure to represent the internal state of the board.
    """
    
    def __init__(self):
        """
        Initialise the internal board.
        """
        self.totalPower: int = 0
        self.internalBoard: dict[tuple, tuple] = {}
        self.bluePieces: int = 0
        self.redPieces: int = 0
        self.turn: int = 0


    def spawn(self, position: tuple, color):
            """ Spawns a piece (its position) on the board """
            
            if position in self.internalBoard.keys():
                return False
            else:
                self.internalBoard[position] = (color, 1)
                return True
    
    def countPieces(self, color: str):
        """ Counts the number of pieces on the board for a given color """
        count = 0
        for piece in self.internalBoard.keys():
            if self.internalBoard.get(piece)[0] == color:
                count += 1
        return count

    '''helper functions for spreading a thingo'''
    def spread(self, piece: tuple, direction: tuple):
        """ Spreads a piece (its position) in a direction on the board """
        colour = self.internalBoard.get(piece)[0]
        spreadDistance = self.internalBoard.get(piece)[1]

        temp = piece 

        # go through all the spread distance
        while spreadDistance:
            newPosition = self.findNewPosition(temp, direction)
            self.spreadToNode(newPosition, colour)

            # set temp to new position to use again next iteration
            temp = newPosition

            spreadDistance -= 1

        # delete original piece from internalBoard
        del self.internalBoard[piece]
            

    def findNewPosition(self, position, direction):
        """ Finds the destination of a node after a move in a direction """

        newR = position[0] + direction[0]
        newQ = position[1] + direction[1]

        # require both r and q to be positive, and also less than the dimension
        if newR < 0:
            newR = DIM - 1
        elif newR >= DIM:
            newR = 0

        if newQ < 0:
            newQ = DIM - 1
        elif newQ >= DIM:
            newQ = 0

        return (newR, newQ)

    def spreadToNode(self, newPosition, colour):
            """ 
            Increments power of a node and changes its colour if it is an enemy node, 
            or removing the node if the max power is reached 
            """
            if newPosition not in self.internalBoard.keys():
                self.internalBoard[newPosition] = (colour, 1)    
            else:
                power = self.internalBoard.get(newPosition)[1]
                if power == MAX_POWER:
                    self.internalBoard.pop(newPosition)
                else:
                    self.internalBoard[newPosition] = (colour, 1 + power)
            return
    
    def getValues(self):
        return self.internalBoard.values()
    
    def getKeys(self):
        return self.internalBoard.keys()


    # could use game_over(board), in board.py
    def is_terminal(self):
        # if maximum number of turns is reached
        if(self.turn >= MAX_TURNS):
            return True
        
        # else if no blue or red pieces left
        elif(self.countPieces('b') == 0 or self.countPieces('r') == 0):
            return True
        
        # else continue
        return False
    
    
# get the successors, possible states we should explore
def get_successors(board: InternalBoard, colourToMove):
    successors = []
    state = copy.deepcopy(board)
    temp = copy.deepcopy(board)
    
    # loop through the board and find all player's piece
    # when you land on a piece perform a spread in 6 directions
    # if it is empty spawn a piece
    # add to the successors list
    
    
    for position in state.internalBoard.keys():
        if(state.internalBoard.get(position)[0] == colourToMove):
        # if(state.get(position)[0] == colourToMove):
            # print(state.get(position)[0])
            # spread in all directions
            for direction in DIRECTIONS:
                temp.spread(position, direction)
                successors.append((temp.internalBoard, ('spread', position, direction)))
                temp = copy.deepcopy(board) # reset temp to original state

    # random spawn
    # 
    coverages = getCoverages(board.internalBoard) 

    for i in range(3):
        r = random.randint(0,6)
        q = random.randint(0,6)
        
        if((r, q) not in state.internalBoard.keys()):
            temp.spawn((r, q), colourToMove)
            successors.append((temp.internalBoard, ('spawn', (r, q), colourToMove)))
            temp = copy.deepcopy(board)
    
    
    
    return successors

    """

    for r in range(DIM):
        for q in range(DIM):
            position = (r, q)
        
            if position in state.internalBoard.keys():
                if(state.internalBoard.get(position)[0] == colourToMove):
                    # print(state.get(position)[0])
                    # spread in all directions
                    for direction in DIRECTIONS:
                        temp.spread(position, direction)
                        successors.append((temp.internalBoard, ('spread', position, direction)))
                        temp = copy.deepcopy(board) # reset temp to original state

            else:
                temp.spawn(position, colourToMove)
                successors.append((temp.internalBoard, ('spawn', position, colourToMove)))
                temp = copy.deepcopy(board) # reset temp to original state
    
    return successors
    
    """

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

################################################################################
############################### End Program ####################################
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
            
        # if this_state.is_terminal():
        if depth == 0 or self.board.is_terminal():
            return evaluateAtkDef(state, new_colour) # evaluatePower(state) # 
        
        v = -math.inf
           
        for s in get_successors(this_state, colour):
            v = max(v, self.min_value(s[0], alpha, beta, new_colour, depth - 1))
            alpha = max(alpha, v)
            if alpha >= beta:
                return beta
            
        return v
    
    def min_value(self, state: dict[tuple, tuple], alpha, beta, colour, depth):
        
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
        if self.board.is_terminal():
            ### if no red pieces:
                return INFINITY
            ### if no blue pieces:
                return NEGATIVE INFINITY

        if depth == 0:
            return evaluatePower(state) # evaluateAtkDef(state, colour) # 

        
        v = math.inf
                
        for s in get_successors(this_state, new_colour):
            v = min(v, self.max_value(s[0], alpha, beta, new_colour, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
            
        return v
    
    # colour should affect this algorithm
    def next_move(self, board: InternalBoard, colour):
        self.board = board
        # self.state = board.internalBoard
        
        #best_score = -math.inf
        alpha = -math.inf
        beta = math.inf
        next_move = None
        
        if colour == 'r':
            best_score = -math.inf
            for s in get_successors(self.board, colour):
                print("successor : ", s)
            
                score = self.min_value(s[0], alpha, beta, colour, 2)
                if score > best_score:
                    best_score = score
                    next_move = s
                alpha = max(alpha, best_score)
        
        else:
            best_score = math.inf
            for s in get_successors(self.board, colour):
                print("successor : ", s)
            
                score = self.max_value(s[0], alpha, beta, colour, 2)
                if score < best_score:
                    best_score = score
                    next_move = s
                beta = min(beta, best_score)
        
        
        if next_move is None:
            print("well you lost")
            return None
        
        print(next_move[1])   
        return next_move[1]