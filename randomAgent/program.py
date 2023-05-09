import copy
from dataclasses import dataclass
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
import random

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

BREADTH = 7
DEPTH = 4

DIM = 7
MAX_POWER = DIM - 1
MAX_BOARD_POW = 49
MAX_TURNS = 343

DIRECTIONS = ((1,-1), (1,0), (0,1), (-1,1), (-1,0), (0,-1))
ENEMY = {'r': 'b', 'b': 'r'}

################################################################################
############################## Agent Class #####################################
################################################################################

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
          
        self.colour = None
        self.board = Board()
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
                self.colour = 'r'
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")
                self.colour = 'b'

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        r = random.randint(0,6)
        q = random.randint(0,6)
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
        if (r,q) not in self.board.board and getTotalPower(self.board.board) < MAX_BOARD_POW:
            return SpawnAction(HexPos(r, q))
        else:
                myBoard = {}
                for piece in self.board.board.keys():
                    if self.board.board.get(piece)[0] == self.colour:
                        myBoard[piece] = self.board.board.get(piece)
                position = random.choice(list(myBoard.keys()))
                return SpreadAction(HexPos(position[0], position[1]), direction)
       
                    
                   
    ### DOES IT ACCOUNT FOR OPPONENT"S SPAWNS AND SPREADS? AND PLAYER SPREADS THAT GOES OVER MAX POWER?
    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        Note: this updates your agent as well.
        """

        match action:
            case SpawnAction(cell):
                #print(f"Testing: {color} SPAWN at {cell}")
                c = 'r'
                if (color == PlayerColor.BLUE):
                    c = 'b'
                #self.board.totalPower += 1
                self.board.spawn((cell.r, cell.q), c)
                return
            
            ### NEED TO RE-CALCULATE POWER for any SPREADS?
            case SpreadAction(cell, direction):
                #print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self.board.spread((cell.r, cell.q), (direction.value.r, direction.value.q))
                #self.board.totalPower = getTotalPower(self.board.board)
                return

################################################################################
########################### Ineternal Board Class ##############################
################################################################################

@dataclass
class Board:
    """
    A data structure to represent the internal state of the board.
    """
    
    def __init__(self):
        # Initialise the internal board.
        self.board: dict[tuple, tuple] = {}

    def spawn(self, position: tuple, color):
        """ Spawns a piece (its position) on the board """
        self.board[position] = (color, 1)
    

    def countPieces(self, color: str):
        """ Counts the number of pieces on the board for a given color """
        count = 0
        for piece in self.board.keys():
            if self.board.get(piece)[0] == color:
                count += 1
        return count

    def spread(self, piece: tuple, direction: tuple):
        """ Spreads a piece (its position) in a direction on the board """
        colour = self.board.get(piece)[0]
        spreadDistance = self.board.get(piece)[1]

        temp = piece 

        # go through all the spread distance
        while spreadDistance:
            newPosition = self.findNewPosition(temp, direction)
            self.spreadToNode(newPosition, colour)

            # set temp to new position to use again next iteration
            temp = newPosition

            spreadDistance -= 1

        # delete original piece from board
        del self.board[piece]
            

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
            if newPosition not in self.board.keys():
                self.board[newPosition] = (colour, 1)    
            else:
                power = self.board.get(newPosition)[1]
                if power == MAX_POWER:
                    self.board.pop(newPosition)
                else:
                    self.board[newPosition] = (colour, 1 + power)
            return
    
    def getValues(self):
        return self.board.values()
    
    def getKeys(self):
        return self.board.keys()
    
    def checkEndGame(self, colour):
        """ Checks if the game is about to end for the other player """
        c = 'r'
        if colour == 'r':
            c = 'b'
        
        if  countColour(self.board, c) == 1:
            return True
        else:
            return False
    
    def endgameAction(self, colour):
        """ Performs the action for the endgame """
        # find the last piece on the board
        c = 'r'
        if colour == 'r':
            c = 'b'
        temp = copy.deepcopy(self)
        for piece in self.board.keys():
            if self.board.get(piece)[0] == colour:
                # spread the piece in all directions
                for direction in DIRECTIONS:
                    temp.spread(piece, direction)
                    if countColour(temp.board, c) == 0:
                        return ('spread', piece, direction)
                    temp = copy.deepcopy(self) # reset temp to original state
        return None

def evaluatePower(board: dict[tuple, tuple]):
    """"""
    totalPower = 0
    for v in board.values():
        if v[0] == 'r':
            totalPower += v[1]
        else:
            totalPower -= v[1]
    return totalPower

def getTotalPower(board):
    power = 0
    for (_, k) in board.values():
        power += k
    return power

def countColour(board, colour):
    total = 0
    for (_, (c, _)) in board.items():
        if c == colour:
            total += 1

    return total
