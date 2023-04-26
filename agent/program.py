# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

import random

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

MAX_POWER = 6
DIM = 6

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        r = random.randint(0,6)
        q = random.randint(0,6)
        _board = {} # {(r, q): (colour, power))}
        match self._color:          
            case PlayerColor.RED:
                r = random.randint(0,6)
                q = random.randint(0,6)

                exists = False
               
                if spawn(_board, (r,q), 'r') == True:
                    exists = False
                else:
                    exists = True
                            
                if exists:
                    for piece in _board.values():
                        if piece[0] == 'r':
                            spread(_board, piece, (1, -1))
                            break
                    return SpreadAction(HexPos(r, q), HexDir.Up)
                else:
                    return SpawnAction(HexPos(r, q))
            case PlayerColor.BLUE:
                r = random.randint(0,6)
                q = random.randint(0,6)

                exists = False
                
                if spawn(_board, (r,q), 'b') == True:
                    exists = False
                else:
                    exists = True
                            
                if exists:
                    for piece in _board.values():
                        if piece[0] == 'b':
                            spread(_board, piece, (1, -1))
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
                pass
                
                # idk
                #self._board[cell] = (self._color, 1)
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
                
                # we can use method from Project A
                # update the self._board with spread(cell, direction)

def spawn(board: dict[tuple, tuple], position: tuple, color):
        """ Spawns a piece (its position) on the board """
        print(board)
        if position in board.keys():
            print("---------------------------hi")
            return  False
        else:
            print("no\n\n\n")
            board[position] = (color, 1)
            return True
    
'''helper functions for spreading a thingo'''
def spread(board: dict[tuple, tuple], piece: tuple, direction: tuple):
        """ Spreads a piece (its position) in a direction on the board """

        colour = board.get(piece)[0]
        spreadDistance = board.get(piece)[1]

        temp = piece 
        
        # go through all the spread distance
        while spreadDistance:
            newPosition = findNewPosition(temp, direction)
            spreadToNode(newPosition, board, colour)

            # set temp to new position to use again next iteration
            temp = newPosition

            spreadDistance -= 1

        # spreading piece leaves an empty node
        board.pop(piece)

def findNewPosition(position, direction):
        """ Finds the destination of a node after a move in a direction """

        newR = position[0] + direction[0]
        newQ = position[1] + direction[1]


        # get new coordinates using modulus, returns remainder
        """ 
        # newR = ( position[0] + direction[0] ) % DIM
        # newQ = ( position[1] + direction[1] ) % DIM
        """
        
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

def spreadToNode(newPosition, board, colour):
        """ 
        Increments power of a node and changes its colour if it is an enemy node, 
        or removing the node if the max power is reached 
        """

        if newPosition not in board.keys():
            board[newPosition] = (colour, 1)
        else:
            power = board.get(newPosition)[1]
            if power == MAX_POWER:
                board.pop(newPosition)
            else:
                board[newPosition] = (colour, 1 + power)
        return