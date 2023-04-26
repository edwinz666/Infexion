# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from dataclasses import dataclass
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

import random

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!



class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self.internalBoard = InternalBoard()
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        
        match self._color:          
            case PlayerColor.RED:
                r = random.randint(0,6)
                q = random.randint(0,6)
                print(internalBoard)
                exists = False
               
                if self.internalBoard.spawn((r,q), 'r') == True:
                    exists = False
                else:
                    exists = True
                            
                if exists:
                    for piece in internalBoard.keys():
                        if internalBoard.get(piece)[0] == 'r':
                            #print("true")
                            self.internalBoard.spread(piece,  (1,-1))
                            break
                    return SpreadAction(HexPos(r, q), HexDir.Up)
                else:
                    return SpawnAction(HexPos(r, q))
            case PlayerColor.BLUE:
                r = random.randint(0,6)
                q = random.randint(0,6)

                exists = False
               
                if self.internalBoard.spawn((r,q), 'b') == True:
                    exists = False
                else:
                    exists = True
                            
                if exists:
                    for piece in internalBoard.keys():
                        if internalBoard.get(piece)[0] == 'b':
                            self.internalBoard.spread(piece, (1,-1))
                            break
                    return SpreadAction(HexPos(r, q), HexDir.Up)
                else:
                    return SpawnAction(HexPos(r, q))

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                c = 'r'
                if (color == PlayerColor.BLUE):
                    c = 'b'
                self.internalBoard.spawn((cell.r, cell.q), c)
                
                # idk
                #self._board[cell] = (self._color, 1)
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self.internalBoard.spread((cell.r, cell.q), (1,-1))
                
                # we can use method from Project A
                # update the self._board with spread(cell, direction)

internalBoard: dict[tuple, tuple] = {}
@dataclass
class InternalBoard:
    """
    A data structure to represent the internal state of the board.
    """
    DIM = 7
    MAX_POWER = 6
    
    def __init__(self):
        """
        Initialise the internal board.
        """

    def spawn(self, position: tuple, color):
            """ Spawns a piece (its position) on the board """
            
            if position in internalBoard.keys():
                return False
            else:
                internalBoard[position] = (color, 1)
                return True
        
    '''helper functions for spreading a thingo'''
    def spread(self, piece: tuple, direction: tuple):
            """ Spreads a piece (its position) in a direction on the board """

            colour = internalBoard.get(piece)[0]
            spreadDistance = internalBoard.get(piece)[1]

            temp = piece 
            
            # go through all the spread distance
            while spreadDistance:
                newPosition = self.findNewPosition(temp, direction)
                self.spreadToNode(newPosition, internalBoard, colour)

                # set temp to new position to use again next iteration
                temp = newPosition

                spreadDistance -= 1

            # spreading piece leaves an empty node
            internalBoard.pop(piece)

    def findNewPosition(self, position, direction):
            """ Finds the destination of a node after a move in a direction """

            newR = position[0] + direction[0]
            newQ = position[1] + direction[1]

            # require both r and q to be positive, and also less than the dimension
            if newR < 0:
                newR = self.DIM - 1
            elif newR >= self.DIM:
                newR = 0

            if newQ < 0:
                newQ = self.DIM - 1
            elif newQ >= self.DIM:
                newQ = 0

            return (newR, newQ)

    def spreadToNode(self, newPosition, board, colour):
            """ 
            Increments power of a node and changes its colour if it is an enemy node, 
            or removing the node if the max power is reached 
            """

            if newPosition not in board.keys():
                board[newPosition] = (colour, 1)
            else:
                power = board.get(newPosition)[1]
                if power == self.MAX_POWER:
                    board.pop(newPosition)
                else:
                    board[newPosition] = (colour, 1 + power)
            return
    
    def getValues(self):
        return internalBoard.values()
    
    def getKeys(self):
        return internalBoard.keys()