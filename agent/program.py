# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from dataclasses import dataclass
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from .utils import render_board

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

        ############## ALGORITHM STRATEGY ###########################
        # general strategy for making a move:
        # consider all moves: spreads from a node, and spawns of player colour
        # each move, consider territories occupied by each player after all possible captures can be mode ...
        # each move played should have something stored somewhere as (movePlayed, territoryEvaluation)
        # check for winning positions too?

        # We will check all SPREAD actions first ... 
        # for each SPREAD action possible in position:
        #   if capture made by that SPREAD action: (define function to check for captures)?
        #       do MINIMAX recursion, but ONLY capture moves by both players moving forward in this MINIMAX algorithm
        #       --> this will result in a final board position after captures --> return the territory evaluation for this board
        #      (root node of the minimax will be the board after the player makes a move, AKA opponent's move)
        #      (that root node recursively expands into all boards THAT INVOLVE A CAPTURE etc based on whose turn it is)
        #      (we only consider territories after captures have ended)
        #   if no capture made by that SPREAD action:
        #       --> simply return the territory evaluation
        #
        # After checking all SPREAD actions ... do we consider SPAWN actions?
        # if the best territory evaluation after considering all SPREAD moves is better than original evaluation:
        #     SKIP checking spawn actions? (is it possible to have a better spawn move if a 
        #                                   spread move results in an improvement of territory?)
        #      --> just return and play the best spread move we found then?
        # otherwise (AKA SPREAD moves don't improve our position, then we consider SPAWN moves):
        #   for each SPAWN action possible in position:
        #       get evaluations for the SPAWN action
        # 
        #   NOW have list of ALL moves and their evaluations ...
        #   pick the move with best evaluation and play
        #
        # try to pick the move that generates such that:
        #   player nodes have more attackers than some enemy nodes defenders
        #   and also player nodes have more defenders than enemy nodes attackers
        #
        # MAYBE instead if a player chooses a move:
        #   each node goes to a certain player based on attackers vs defenders
        #   
        
        

        ######## calling minimax algorithm for next move ########
        next_move = self.minimax.next_move(self.current_state)
        


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
                return

################################################################################
########################### Inetrnal Board Class ###############################
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
def is_terminal(board):
    # if maximum number of turns is reached
    if(board.turns >= MAX_TURNS):
        return True
    
    # else if no blue or red pieces left
    elif(board.countPieces('b') == 0 or board.countPieces('r') == 0):
        return True
    
    # else continue
    return False
    
    
# get the successors, possible states we should explore
def get_successors(state, colourToMove):
    successors = []
    
    # loop through the board and find all player's piece
    # when you land on a piece perform a spread in 6 directions
    # if it is empty spawn a piece
    # add to the successors list
    for r in range(DIM):
        for q in range(DIM):
            position = (r, q)
        
            if position in state.keys():
                if(state.get(position)[0] == colourToMove):
                    # spread in all directions
                    for direction in HexDir:
                        successors.append(state.spread(position, direction))
                
            else:
                successors.append(state.spawn(position, colourToMove))
    
    return successors

# higher power favours red, lower power favours blue
def evaluatePower(board):
    totalPower = 0
    for (colour, power) in board.values():
        if colour == 'r':
            totalPower += power
        else:
            totalPower -= power
    return totalPower
        
def generateCoverageDict():
    coverage = {}

    for i in range(DIM):
        for j in range(DIM):
            coverage[(i,j)] = 0

    return coverage

# gives each node's power (or something else?) to a certain player based on
# the node's colour and 
def evaluateAtkDef(board, colourToMove):
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
            if colourToMoveCoverage > colourJustPlayedCoverage:
                colourToMoveScores.append(power)
            else:
                colourJustPlayedScores.append(power)
        else:
            if colourJustPlayedCoverage > colourToMoveCoverage:
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



################################################################################
############################### End Program ####################################
################################################################################