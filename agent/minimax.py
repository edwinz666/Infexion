import math
from agent.program import evaluatePower, get_successors, is_terminal
from referee.game import board


class minimax:
    
    def __init__(self):
        self.game = board
        
        
    # minimax implementation

    # state: the current board state
    # game: game description
    # alpha: MAX score along the path to state
    # beta: MIN score along the path to state
    
    # depth: the depth of the search
    
    def max_value(state: dict[tuple, tuple], alpha, beta):
        if is_terminal(state):
            return evaluatePower(state) # evaluateAtkDef(state)
        
        v = -math.inf
        
        for s in get_successors(state):
            v = max(v, minimax.min_value(s, alpha, beta))
            alpha = max(alpha, v)
            if alpha >= beta:
                return beta
            
        return v
    
    def min_value(state, game, alpha, beta):
        if game.is_terminal(state):
            return evaluatePower(state) # evaluateAtkDef(state)
        
        v = math.inf
        
        for s in get_successors(state):
            v = min(v, minimax.max_value(game.result(s, alpha, beta)))
            if v <= alpha:
                return v
            beta = min(beta, v)
            
        return v
    
    def next_move(state, game):
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf
        next_move = None
        
        for s in game.actions(state):
            score = minimax.min_value(s , alpha, beta)
            if score > best_score:
                best_score = score
                next_move = s
            alpha = max(alpha, best_score)    
        return next_move