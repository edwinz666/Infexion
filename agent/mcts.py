import random
import math
from program import InternalBoard

class Node:
    def __init__(self, state: dict[tuple, tuple]):
        self.state = state
        self.children = []
        self.wins = 0
        self.visits = 0
    
    def add_child(self, child):
        childNode = Node(child)
        self.children.append(childNode)
        return childNode
    
    def update(self, result):
        self.visits += 1
        self.wins += result

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def get_best_child(self, exploration_parameter):
        best_score = -1
        best_child = None
        for child in self.children:
            exploitation_score = child.wins / child.visits
            exploration_score = math.sqrt(2 * math.log(self.visits) / child.visits)
            uct_score = exploitation_score + exploration_parameter * exploration_score
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child
    

class MonteCarloTreeSearch:
    def __init__(self, exploration_parameter=1):
        self.exploration_parameter = exploration_parameter

    def get_best_move(self, state, simulations_number):
        root_node = Node(state)
        for i in range(simulations_number):
            node = root_node
            state_copy = state.copy()
            # Selection phase
            while node.is_fully_expanded() and not state_copy.is_game_over():
                node = node.get_best_child(self.exploration_parameter)
                state_copy.apply_move(node.state.get_last_move())
            # Expansion phase
            if not state_copy.is_game_over():
                untried_move = random.choice(state_copy.get_legal_moves())
                state_copy.apply_move(untried_move)
                node = node.add_child(state_copy)
            # Simulation phase
            while not state_copy.is_game_over():
                state_copy.apply_move(random.choice(state_copy.get_legal_moves()))
            # Backpropagation phase
            result = state_copy.get_result(state.get_current_player_id())
            while node is not None:
                node.update(result)
                node = node.parent
        best_child = root_node.get_best_child(0)
        return best_child.state.get_last_move()