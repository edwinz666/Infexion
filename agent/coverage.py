from calendar import c


DIM = 7
DIRECTIONS = ((1,-1), (1,0), (0,1), (-1,1), (-1,0), (0,-1))
POWER_DISTANCE_COVERAGE = {1: (1,0,0), 2: (2,2,0), 3: (2,3,2), 4: (2,3,3), 5: (2,3,3), 6: (2,3,3)}

def generateCoverageDict():
    coverage = {}

    for i in range(DIM):
        for j in range(DIM):
            coverage[(i,j)] = 0

    return coverage
#def generateCoveragePositionPower():
#    coveragePositionPower = {}

#    for i in range(DIM):
#        for j in range(DIM):
#            position = (i, j)
#            for power in range(1,4):
#                #toAddBasedOnDistanceFromNode = POWER_DISTANCE_COVERAGE[power]
#                # list of positions covered for each (position, power) pair AND how many times its covered?
#                covered = []
#                for direction in DIRECTIONS:
#                    tempPower = power # tempPower = 0 .... while tempPower < 3 ... tempPower += 1
#                    tempR = position[0]
#                    tempQ = position[1]

#                    while tempPower:
#                        newR = tempR + direction[0]
#                        newQ = tempQ + direction[1]

#                        # require both r and q to be positive, and also less than the dimension
#                        if newR < 0:
#                            newR = DIM - 1
#                        elif newR >= DIM:
#                            newR = 0

#                        if newQ < 0:
#                            newQ = DIM - 1
#                        elif newQ >= DIM:
#                            newQ = 0 
#                        if (newR, newQ) not in covered:
#                            covered.append((newR, newQ))
                    
#                        tempR = newR
#                        tempQ = newQ

#                        tempPower -= 1
                
#                coveragePositionPower[(position, power)] = covered
#                if power == 3:
#                    for restPower in range(4, 7):
#                        coveragePositionPower[(position, restPower)] = covered
#    return coveragePositionPower


def generateCoveragePositionPower():
    coveragePositionPower = {}

    for i in range(DIM):
        for j in range(DIM):
            position = (i, j)
            for power in range(1,DIM):
                positionCoverage = {} #generateCoverageDict()
                toAddBasedOnDistanceFromNode = POWER_DISTANCE_COVERAGE[power]
                # list of positions covered for each (position, power) pair AND how many times its covered?

                for direction in DIRECTIONS:
                    tempPower = 0 # tempPower = 0 .... while tempPower < 3 ... tempPower += 1
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



#def getCoverages(board):
#    redCoverage = generateCoverageDict()
#    blueCoverage = generateCoverageDict()

#    # 2.
#    for (position, (colour, power)) in board.items():
#        for covered in COVERAGE_POSITION_POWER[(position, power)]:
#            if colour == 'r':
#                redCoverage[covered] += 1
#            else:
#                blueCoverage[covered] += 1

#    return (redCoverage, blueCoverage)

def getCoverages(board):
    redCoverage = generateCoverageDict()
    blueCoverage = generateCoverageDict()

    # 2.
    for (position, (colour, power)) in board.items():
        for (coveredPosition, coveredTimes) in COVERAGE_POSITION_POWER[(position, power)].items():
            if colour == 'r':
                redCoverage[coveredPosition] += coveredTimes
            else:
                blueCoverage[coveredPosition] += coveredTimes

    return (redCoverage, blueCoverage)

#def peaceful(board):
#    redCoverage = {}
#    blueCoverage = {}

#    # 2.
#    for (position, (colour, power)) in board.items():
#        for covered in COVERAGE_POSITION_POWER[(position, power)]:
#            if colour == 'r':
#                redCoverage[covered] = 1
#            else:
#                blueCoverage[covered] = 1
    
#    # 3.
#    for (position, (colour, power)) in board.items():
#        if (position in redCoverage.keys() and colour == 'b' or 
#            position in blueCoverage.keys() and colour == 'r'):
#            return False
    
#    return True

def peaceful(board):
    redCoverage = {}
    blueCoverage = {}

    # 2.
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
    
    # 3.
    for (position, (colour, _)) in board.items():
        if (position in redCoverage.keys() and colour == 'b' or 
            position in blueCoverage.keys() and colour == 'r'):
            return False
    
    return True


# gives each node's power (or something else?) to a certain player based on
# the node's colour and 
def evaluateAtkDef(board: dict[tuple, tuple], colourToMove):
    # 1. generate two arrays 7x7 ? for both colours
    # 2. go over every node, and add to covered squares in array based on colour
    # 3. go over every node again, but compare array coverages based on colour
    # 4.    for every node ... add power based on who wins
    # 5. if colourToMove is RED ... remove blue's best capture if available

    # 1. 
    colourToMoveCoverage = generateCoverageDict()
    colourJustPlayedCoverage = generateCoverageDict()

    # MAYBE ONLY NEED LIST FOR colourJustPlayed ... to remove the best capture for that colour
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
            else:
                colourToMoveScore -= power
                if power > maxJustPlayedPowerCoverage:
                    maxJustPlayedPowerCoverage = power
        else: # defendingColour is the colour who just played
            if colourJustPlayedCoverage[position] >= colourToMoveCoverage[position]:
                colourToMoveScore -= power
            else:
                colourToMoveScore += power

    ### add component that sorts by this first, but then after by overlapping territory?
    if colourToMove == 'r':
        return (colourToMoveScore + maxJustPlayedPowerCoverage, secondaryOverlappingScore)
    else:
        return (-colourToMoveScore - maxJustPlayedPowerCoverage, -secondaryOverlappingScore)