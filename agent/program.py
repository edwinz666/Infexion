# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from dataclasses import dataclass
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from referee.utils import render_board

import random

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!


DIM = 7
MAX_POWER = DIM-1

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
        
        # algorithm goes here: 
        # pseudocode ...
        # MCTS(self.board, colour) ...
        #   tree = Starting from the root of the tree, use a selection strategy
        #          to choose successor states until we reach a leaf node of the tree
        #   while IsTimeRemaining:
        #       leaf = select(tree)
        #       child = expand(leaf)
        #       result = simulate(child)
        #       backPropogate(result, child)
        #       return the move in actions(state) whose node has the highest number of playouts


        # temperary random algorithm
        r = random.randint(0,6)
        q = random.randint(0,6)
        
                
        if (r,q) not in self.board.internalBoard:
            return SpawnAction(HexPos(r, q))
        else:
            for piece in self.board.internalBoard.keys():
                if self.board.internalBoard.get(piece)[0] == colour:
                    r = piece[0]
                    q = piece[1]
                    break
            return SpreadAction(HexPos(r, q), HexDir.Up)
                
                   

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        Note: this updates your agent as well.
        """
        
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                c = 'r'
                if (color == PlayerColor.BLUE):
                    c = 'b'
                self.board.spawn((cell.r, cell.q), c)
                return
                  
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self.board.spread((cell.r, cell.q), (1, -1))
                return


################################################################################
######################### Inetrnal Board Class #################################
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
        self.internalBoard: dict[tuple, tuple] = {}

    def spawn(self, position: tuple, color):
            """ Spawns a piece (its position) on the board """
            
            if position in self.internalBoard.keys():
                return False
            else:
                self.internalBoard[position] = (color, 1)
                return True
        
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
    
################################################################################
############################### End Program ####################################
################################################################################