# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from json.encoder import INFINITY
#from turtle import color
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from .utils import render_board
from .internalBoard import InternalBoard
from .minimax import minimax
from .minimax import getTotalPower  

import math
import random

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

PRINT_COUNT = 0

DIM = 7
MAX_POWER = DIM-1
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
        self.board.turn += 1
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
                self.board.totalPower = getTotalPower(self.board.internalBoard)
                return
            
################################################################################
############################### End Program ####################################
################################################################################
