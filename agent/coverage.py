DIM = 7
DIRECTIONS = ((1,-1), (1,0), (0,1), (-1,1), (-1,0), (0,-1))
POWER_DISTANCE_COVERAGE = {1: (1,0,0), 2: (2,2,0), 3: (2,3,2), 4: (2,3,3), 5: (2,3,3), 6: (2,3,3)}


def generateCoverageDict():
    """
    Initializes coverage of each position on the board for a particular player
    """

    coverage = {}

    for i in range(DIM):
        for j in range(DIM):
            coverage[(i,j)] = 0

    return coverage


def generateCoveragePositionPower():
    """
    Generates a dictionary where the keys are each (position, power) pairs for every 
    position on the 7x7 board, and for every power from 1 to 6.

    The output is what nodes are covered, and how many times it is covered.
    """
    coveragePositionPower = {}

    for i in range(DIM):
        for j in range(DIM):
            position = (i, j)
            for power in range(1,DIM):
                positionCoverage = {} 
                toAddBasedOnDistanceFromNode = POWER_DISTANCE_COVERAGE[power]

                for direction in DIRECTIONS:
                    tempPower = 0 
                    tempR = position[0]
                    tempQ = position[1]

                    while tempPower < 3:
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
                        
                        positionCoverage[(newR, newQ)] = toAddBasedOnDistanceFromNode[tempPower]
                    
                        tempR = newR
                        tempQ = newQ

                        tempPower += 1
                
                coveragePositionPower[(position, power)] = positionCoverage

    return coveragePositionPower



COVERAGE_POSITION_POWER = generateCoveragePositionPower()


def getCoverages(board):
    """
    Returns coverage for each colour for each position on the 7x7 board
    """

    redCoverage = generateCoverageDict()
    blueCoverage = generateCoverageDict()

    for (position, (colour, power)) in board.items():
        for (coveredPosition, coveredTimes) in COVERAGE_POSITION_POWER[(position, power)].items():
            if colour == 'r':
                redCoverage[coveredPosition] += coveredTimes
            else:
                blueCoverage[coveredPosition] += coveredTimes

    return (redCoverage, blueCoverage)



def peaceful(board):
    """
    Checks if any captures can be made in a position
    """

    redCoverage = {}
    blueCoverage = {}

    # get coverages for each colour
    for (position, (colour, power)) in board.items():
        for (coveredPosition, coveredTimes) in COVERAGE_POSITION_POWER[(position, power)].items():
            if colour == 'r':
                if coveredPosition in redCoverage.keys():
                    redCoverage[coveredPosition] += coveredTimes
                else:
                    redCoverage[coveredPosition] = coveredTimes
            else:
                if coveredPosition in blueCoverage.keys():
                    blueCoverage[coveredPosition] += coveredTimes
                else:
                    blueCoverage[coveredPosition] = coveredTimes
    
    # if a piece is covered by the opponent, a capture is available
    for (position, (colour, _)) in board.items():
        if (position in redCoverage.keys() and colour == 'b' or 
            position in blueCoverage.keys() and colour == 'r'):
            return False
    
    # no captures are available
    return True



def evaluateAtkDef(board: dict[tuple, tuple], colourToMove):
    """
    Evaluation function of a position, based on coverage of nodes for each colour.

    Primary evaluation assigns the power of each piece on the board to a colour, 
    and adjusts for whose move it is.

    Secondary evaluation is used in the case of a tie in the primary evaluation,
    favouring the side who covers any node on the board more times overall.
  
    # 1. generate two arrays 7x7 ? for both colours
    # 2. go over every node, and add to positions covered and how many times based on colour
    # 3. go over every node again, but compare array coverages based on colour
            and add power based on who wins
    # 4. evaluate by the overall power of pieces covered first, but then after by overall coverage numbers
    """

    # 1. 
    colourToMoveCoverage = generateCoverageDict()
    colourJustPlayedCoverage = generateCoverageDict()


    colourToMoveScore = 0
    maxJustPlayedPowerCoverage = 0
    secondaryOverlappingScore = 0

    # 2.
    for (position, (colour, power)) in board.items():
        for (coveredPosition, coveredTimes) in COVERAGE_POSITION_POWER[(position, power)].items():
            if colour == colourToMove:
                colourToMoveCoverage[coveredPosition] += coveredTimes
            else:
                colourJustPlayedCoverage[coveredPosition] += coveredTimes

    # 3.
    for (position, (defendingColour, power)) in board.items():
        secondaryOverlappingScore += (colourToMoveCoverage[position] - colourJustPlayedCoverage[position])

        if defendingColour == colourToMove:           
            if colourToMoveCoverage[position] >= colourJustPlayedCoverage[position]:
                colourToMoveScore += power
            # defending colour is the colour to move and a favourable capture can be made by the colour that just played
            else:
                colourToMoveScore -= power
                if power > maxJustPlayedPowerCoverage:
                    maxJustPlayedPowerCoverage = power

        # defendingColour is the colour who just played
        else: 
            if colourJustPlayedCoverage[position] >= colourToMoveCoverage[position]:
                colourToMoveScore -= power
            else:
                colourToMoveScore += power

    # 4. 
    if colourToMove == 'r':
        return (colourToMoveScore + maxJustPlayedPowerCoverage, secondaryOverlappingScore)
    else:
        return (-colourToMoveScore - maxJustPlayedPowerCoverage, -secondaryOverlappingScore)