# greedy game playing agent
# created by Bill Zhu for comp30024 project B
# Date: 05/09/2023
# Description: This agent uses a greedy strategy to play the game. It will
#              evaluate the score of each possible move and choose the move
#              that gives the highest score.
#              The score is calculated by the following formula:
#              score = 2 * (number of cells owned by the agent) +
#                      (number of cells owned by the agent that are adjacent to
#                       enemy cells) -
#                      (number of cells owned by the agent that are adjacent to
#                       friendly cells) +
#                      (number of cells owned by the agent that are adjacent to
#                       enemy cells that are adjacent to friendly cells) -
#                      (number of cells owned by the agent that are adjacent to
#                       friendly cells that are adjacent to enemy cells)
#              The agent will also check if it is in the endgame. If it is, it
#              will try to spread to the last enemy piece on the board.
#              If it is not in the endgame, it will try to spread to the
#              position that gives the highest score.
#              If it cannot spread, it will spawn a piece in the position that
#              gives the highest score.
# the above comments were made by an AI lol :)

import copy
from dataclasses import dataclass
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

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
        ######## calling minimax algorithm for next move ########
        if (self.board.checkEndGame(self.colour) == True and self.board.endgameAction(self.colour) != None):
                next_move = self.board.endgameAction(self.colour)
        else:
                next_move = self.greedy_strategy()
            
        if (next_move[0] == 'spread'):
                return SpreadAction(HexPos(next_move[1][0], next_move[1][1]), HexDir(next_move[2]))
        else:
                return SpawnAction(HexPos(next_move[1][0], next_move[1][1]))
       
                    
                   
    ### DOES IT ACCOUNT FOR OPPONENT"S SPAWNS AND SPREADS? AND PLAYER SPREADS THAT GOES OVER MAX POWER?
    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        Note: this updates your agent as well.
        """

        match action:
            case SpawnAction(cell):
                c = 'r'
                if (color == PlayerColor.BLUE):
                    c = 'b'
                self.board.spawn((cell.r, cell.q), c)
                return
            
            case SpreadAction(cell, direction):
                self.board.spread((cell.r, cell.q), (direction.value.r, direction.value.q))
                return
            
    def greedy_strategy(self):
        legal_moves = self.board.getLegalMoves(self.colour)
        best_move = None
        best_score = -float('inf')

        for move in legal_moves:
            next_state = copy.deepcopy(self.board)
            next_state = self.apply_move(move, next_state)
            score = self.evaluate_score(next_state.board, self.colour)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move
    
    def apply_move(self, move:tuple, boardcopy):
        if(move[0] == 'spread'):
            boardcopy.spread(move[1], move[2])
        else:
            boardcopy.spawn(move[1], self.colour)

        return boardcopy
    
    def evaluate_score(self, state:dict[tuple, tuple], colour):
        result = 0
        for piece in state.keys():
            if state.get(piece)[0] == colour:
                result += state.get(piece)[1]
            if state.get(piece)[0] == ENEMY[colour]:
                result -= state.get(piece)[1]
            for direction in DIRECTIONS:
                r = piece[0] + direction[0]
                q = piece[1] + direction[1]
                if (piece[0] + direction[0] < 0):
                    r = 6
                if (piece[0] + direction[0] > 6):
                    r = 0
                if (piece[1] + direction[1] < 0):
                    q = 6
                if (piece[1] + direction[1] > 6):
                    q = 0
                checkedpos = (r, q)
                #print(checkedpos)
                if checkedpos in state.keys() and state.get(checkedpos)[0] != colour:
                    result -= 1
                else:
                    result += 1
        return result
        
    def checkEndGame(self, colour):
        """ Checks if the game is about to end for the other player """
        c = 'r'
        if colour == 'r':
            c = 'b'
        
        if  countColour(self.board.board, c) == 0:
            return True
        else:
            return False
        
    def endgameAction(self, colour):
        """ Performs the action for the endgame """
        # find the last piece on the board
        c = 'r'
        if colour == 'r':
            c = 'b'
        temp = copy.deepcopy(self.board)
        for piece in self.board.board.keys():
            if self.board.board.get(piece)[0] == colour:
                # spread the piece in all directions
                for direction in DIRECTIONS:
                    temp.board.spread(piece, direction)
                    if countColour(temp.board.board, c) == 0:
                        return ('spread', piece, direction)
                    temp = copy.deepcopy(self) # reset temp to original state
        return None
    
    


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
    
    def getLegalMoves(self, colour):
        """ Returns a list of all legal moves """
        legalMoves = []
        for piece in self.board.keys():
            if self.board.get(piece)[0] == colour:
                for direction in DIRECTIONS:
                    legalMoves.append(('spread', piece, direction))

        for r in range(DIM):
            for q in range(DIM):
                if (r, q) not in self.board.keys() and getTotalPower(self.board) < MAX_BOARD_POW:
                    legalMoves.append(('spawn', (r, q)))
        
        return legalMoves



    
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


