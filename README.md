AI Project Part B
-----------------

To design and implement an agent program that plays the game "Infexion"

Using the given information about the evolving state of the game, 
the program will decide on an action to take on each of its turns.
The 'agent' and 'agent2' packages contain agents that implement 
minimax search with alpha-beta pruning, using a complex game state
evaluation metric derived from original strategic insights into the game.
These agents test different breadth/depth of the minimax search to compare
effectiveness of these parameters. The 'greedyAgent' and 'randomAgent' are
included for comparison

Game specifications found in the file:
    AI_2023_Project_PartB.pdf

A game sample of agents 'agent' and 'agent2' playing can be conducted using
the following command:
    python -m referee agent agent2

