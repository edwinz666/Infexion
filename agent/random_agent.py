# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Random Playing Agent
'''
 """
        else:
            r = random.randint(0,6)
            q = random.randint(0,6)
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
            if (r,q) not in self.board.board and getTotalPower(self.board.board) < MAX_BOARD_POW:
                return SpawnAction(HexPos(r, q))
            else:
                myBoard = {}
                for piece in self.board.board.keys():
                    if self.board.board.get(piece)[0] == self.colour:
                        myBoard[piece] = self.board.board.get(piece)
                position = random.choice(list(myBoard.keys()))
                return SpreadAction(HexPos(position[0], position[1]), direction)
                """
'''
   