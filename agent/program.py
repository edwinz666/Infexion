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

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._board = {}
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


        match self._color:          
            case PlayerColor.RED:
                r = random.randint(0,6)
                q = random.randint(0,6)

                exists = False
                for i in range(0,6):
                    for j in range(0,6):
                        if (r,q) in self._board.keys():
                            exists = True
                            
                if exists:
                    return SpreadAction(HexPos(r, q), HexDir(Up))
                else:
                    return SpawnAction(HexPos(r, q))
            case PlayerColor.BLUE:
                r = random.randint(0,6)
                q = random.randint(0,6)

                exists = False
                for i in range(0,6):
                    for j in range(0,6):
                        if (r,q) in self._board.keys():
                            exists = True
                if exists:
                    return SpreadAction(HexPos(r, q), HexDir(Up))
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
                self._board[cell] = (self._color, 1)
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
                
                # we can use method from Project A
                # update the self._board with spread(cell, direction)

   