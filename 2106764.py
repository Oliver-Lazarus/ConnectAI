import board
import random
import math


# The aim of this coursework is to implement the minimax algorithm to determine the next move for a game of Connect.
# The goal in Connect is for a player to create a line of the specified number of pieces, either horizontally, vertically or diagonally.
# It is a 2-player game with each player having their own type of piece, "X" and "O" in this instantiation.
# You will implement the strategy for the first player, who plays "X". The opponent, who always goes second, plays "O".
# The number of rows and columns in the board varies, as does the number of pieces required in a line to win.
# Each turn, a player must select a column in which to place a piece. The piece then falls to the lowest unfilled location.
# Rows and columns are indexed from 0. Thus, if at the start of the game you choose column 2, your piece will fall to row 0 of column 2. 
# If the opponent also selects column 2 their piece will end up in row 1 of column 2, and so on until column 2 is full (as determined
# by the number of rows). 
# Note that board locations are indexed in the data structure as [row][column]. However, you should primarily be using checkFull(), 
# checkSpace() etc. in board.py rather than interacting directly with the board.gameBoard structure.
# It is recommended that look at the comments in board.py to get a feel for how it is implemented. 
#
# Your task is to complete the two methods, 'getMove()' and 'getMoveAlphaBeta()'.
#
# getMove() should implement the minimax algorithm, with no pruning. It should return a number, between 0 and (maxColumns - 1), to
# select which column your next piece should be placed in. Remember that columns are zero indexed, and so if there are 4 columns in
# you must return 0, 1, 2 or 3. 
#
# getMoveAlphaBeta() should implement minimax with alpha-beta pruning. As before, it should return the column that your next
# piece should be placed in.
#
# The only imports permitted are those already imported. You may not use any additional resources. Doing so is likely to result in a 
# mark of zero. Also note that this coursework is NOT an exercise in Python proficiency, which is to say you are not expected to use the
# most "Pythonic" way of doing things. Your implementation should be readable and commented appropriately. Similarly, the code you are 
# given is intended to be readable rather than particularly efficient or "Pythonic".
#
# IMPORTANT: You MUST TRACK how many nodes you expand in your minimax and minimax with alpha-beta implementations.
# IMPORTANT: In your minimax with alpha-beta implementation, when pruning you MUST TRACK the number of times you prune.
class Player:
	
    def __init__(self, name):
        self.name = name
        self.numExpanded = 0 # Use this to track the number of nodes you expand
        self.numPruned = 0 # Use this to track the number of times you prune 
        self.transpositionTable = {} #Hashmap of gamestates and according values
        self.count = 0
     
        
        
    def getMove(self, gameBoard): 
        move = self.minimax(gameBoard,3,True)[1]
        return move

    def getMoveAlphaBeta(self, gameBoard):
        move = self.AlphaBeta(gameBoard,6,-math.inf,math.inf,True)[1]
        return move
    
    
    
    #Generates a unique Zorbist key based on the gamestate
    def generateZorbistKey(self,gameBoard):
        key = ""
        #Iterates through the game board and appends value to the string to generate the key
        for row in gameBoard:
            for char in row:
                if char.value == None:
                    key+=" "
                else:
                    key += char.value
        return key
    
    #Borad Evaluation function, looks at all possible search windows of size gameBoard.winNum and determines a value
    def board_evaluate(self,gameBoard,isPlayer):
        value = 0
        b = []
        #Generates the gameboard as just values as opposed to the objects they represent
        for row in gameBoard.gameBoard:
            b.append([i.value for i in row])
        
        #Transposes the array and assigns the values of the gameboard state
        bCol = []  
        
        for col in range(gameBoard.numColumns):
            bCol.append([row[col] for row in b])
        
        #Looks at the centre column and assigns a value for number of players pieces in the centre
        #This allows for more winning opportunities as it maximises the number of ways to win
        centerCol = bCol[len(bCol)//2]
        #Assigns a value of 6 for every piece found in the centre of this game state
        if isPlayer:
            value += centerCol.count(self.name) * 6 
        else:
            value += centerCol.count("O") * 6
    
        
        #Searches all possible windows and calculates the value of each search space
        
        ##Horizontal Search
        for row in b:
            for col in range(0,gameBoard.numColumns - gameBoard.winNum +1):
                
                search_space = [i for i in row[col:col+gameBoard.winNum]] 
                value += self.Eval(search_space,gameBoard, isPlayer)
                
        
        #Vertical
        
        for col in bCol:
            for row in range(gameBoard.numRows - gameBoard.winNum +1):
                search_space = [i for i in col[row:row+gameBoard.winNum]]
                
                value += self.Eval(search_space,gameBoard,isPlayer)
               
                    
                    
        #y=x Diagonal
        for row in range(gameBoard.numRows - gameBoard.winNum +1):
            for col in range(gameBoard.numColumns - gameBoard.winNum +1):
                
                search_space = [b[row+i][col+i] for i in range(gameBoard.winNum)]
             
                value += self.Eval(search_space,gameBoard,isPlayer)
                
                
                
        #Y = -x Diagonal
        
        for row in range(gameBoard.numRows - gameBoard.winNum +1):
            for col in range(gameBoard.numColumns - gameBoard.winNum +1):
                search_space = [b[row+gameBoard.winNum-1 -i][col +i] for i in range(gameBoard.winNum)]
                value += self.Eval(search_space,gameBoard,isPlayer)
                
                
                
         
        
        
        
        return value
    
    #This function determines all coloumns that aren't full and returns a list of them
    def possibleMoves(self,gameBoard):
        pM = []
        for i in range(0,gameBoard.numColumns):
            if gameBoard.colFills[i] < gameBoard.numRows: #This is how the board class checks if the column is full
                pM.append(i)
        return pM
            
    
    #This function takes in the board and the search_space to determine the value of each search space
    def Eval(self,search_space,gameBoard,isPlayer):
        value = 0
        
        for i in range(2,len(search_space)):#Checks if there are 2 or more in a row in each search space
            
            if isPlayer:
                if search_space.count(self.name) == gameBoard.winNum: #If there is a win
                    value +=50
                 
                #Checks to see how many of the players pieces are in the search space and if there are a correct amount of empty spaces 
                if search_space.count(self.name) == i and search_space.count(" ") == (gameBoard.winNum - i):
                    value += 5*i
                
                #Checks to see if the opponent could potentially win next turn
                if search_space.count('O') == (len(search_space) -1) and search_space.count(" ") == 1:
                    value -= 10*gameBoard.winNum
            else:
                #Does the same checks but for the opposing player, used for the minmax algorithm
                if search_space.count("O") == gameBoard.winNum:
                    value +=50
                if search_space.count("O") == i and search_space.count(" ") == (gameBoard.winNum - i):
                    value += 5*i
                if search_space.count("X") == (len(search_space) -1) and search_space.count(" ") == 1:
                    value -= 10*gameBoard.winNum
                
                
               
        return value
        
    
    
    def pickMove(self,gameBoard):
        
        positions = self.possibleMoves(gameBoard) 
        HValue = -100000
        HCol = 0
        for col in positions:
            temp = gameBoard.copy()
            temp.addPiece(col,self.name)
            k = self.generateZorbistKey(gameBoard.gameBoard)
            if self.checkIfKeyExists(k):
                value = self.transpositionTable[k]
            else:
                value = self.board_evaluate(temp,True)
                self.transpositionTable[k] = value
            
            value = self.board_evaluate(gameBoard, True)

            if value > HValue:
                HValue = value
                HCol = col
     
        return HCol
            
    #Checks if it is a terminal node
    def isFinished(self,gameBoard):
        return gameBoard.checkWin() or gameBoard.checkFull() #Returns true if the board is full or a win
            
    #Minmax algorith according to Wikipedia's pseudocode
    def minimax(self,gameBoard, depth, maximisingPlayer):
        
        validPos = self.possibleMoves(gameBoard) #Determine all valid positions
        
        #Determines which player last moved
        currentPlayer = gameBoard.lastPlay[2]
        
        if currentPlayer == " ":
            currentPlayer = self.name
        elif currentPlayer == "O":
            currentPlayer = self.name
        else:
            currentPlayer = "O"
        #Base Cases
        
        if depth == 0 or self.isFinished(gameBoard):
            
            if self.isFinished(gameBoard):#Checks if the board is full or there is a win
                
                if gameBoard.checkWin() and currentPlayer == self.name: #If the player does not win, return a large negative value
                    return (-100000,None)
                if gameBoard.checkWin() and currentPlayer != self.name: #If the player wins, return a large positive value
                    return (100000,None)
                else:
                    return (0,None)
            else: #Depth must have reached 0
                key = self.generateZorbistKey(gameBoard.gameBoard) #Generates a zorbist key based on the game state
                if key in self.transpositionTable: #Checks if it exists in the transposition table
                    return(self.transpositionTable[key],None) #Does not evaluate the board as it has already been done
                else:
                    bVal = self.board_evaluate(gameBoard,True)
                    self.transpositionTable[key] = bVal
                return (bVal,None) #Evaluates the board state

            
        elif maximisingPlayer:
            
            value = -math.inf #Sets value to negative infinity
            column = 0 #Choses the first column incase the search fails
            for col in validPos: #Iterates through all valid positions
                
                self.numExpanded +=1 #Increments nodes expanded
                b = gameBoard.copy() #Makes a copy of the board to avoid memory issues
                b.addPiece(col,self.name) #Adds a piece based on col
                newScore = self.minimax(b,depth-1,False)[0] #Recursivley calls the function untill depth reaches 0
                
                if newScore > value:#Checks to see if the new gamestate is better than the previous states
                    #Assings variables accordingly
                    value = newScore 
                    column = col
                    
            return (value,column) #returns the value and column as a tuple
        
        else:
            #Similar code for maximising player however slightly changed in order to minimise
            value = math.inf
            column = 0
            for col in validPos:
                self.numExpanded += 1
                b = gameBoard.copy()
                b.addPiece(col,"O")
                newScore = self.minimax(b,depth-1,True)[0]
                if newScore < value:
                    value = newScore 
                    column = col
            return (value,column)
        
    
    
    #MinMax algorithm with Alpha Beta pruning, following pseudocode from wikipedia
    #Code almost identical however checks if 
    def AlphaBeta(self,gameBoard, depth, alpha, beta, maximisingPlayer):
        validPos = self.possibleMoves(gameBoard)
        
        currentPlayer = gameBoard.lastPlay[2]
        
        if currentPlayer == " ":
            currentPlayer = self.name
        elif currentPlayer == "O":
            currentPlayer = self.name
        else:
            currentPlayer = "O"
        
        if depth == 0 or self.isFinished(gameBoard):
            if self.isFinished(gameBoard):
                if gameBoard.checkWin() and currentPlayer == self.name:
                    return (-100000,None)
                if gameBoard.checkWin() and currentPlayer != self.name:
                    return (100000,None)
                else:
                    return (0,None)
            else:
                key = self.generateZorbistKey(gameBoard.gameBoard)
                if key in self.transpositionTable:
                    return(self.transpositionTable[key],None)
                else:
                    bVal = self.board_evaluate(gameBoard,True)
                    self.transpositionTable[key] = bVal
                    return (bVal,None)
    
            
        elif maximisingPlayer:
            
            value = -math.inf
            column = 0
            for col in validPos:
                self.numExpanded +=1
                b = gameBoard.copy()
                b.addPiece(col,self.name)
                newScore = self.AlphaBeta(b,depth-1,alpha,beta,False)[0]
                
                if newScore > value:
                    value = newScore 
                    column = col
                #changes the value of alpha to the max of the value or previous alpha
                alpha = max(alpha,value)
               
                if alpha >= beta: #Prunes if alpha >= beta
                   
                    self.numPruned +=1
                    break
                    
            return (value,column)
        
        else:
            
            value = math.inf
            column = 0
            for col in validPos:
                self.numExpanded += 1
                b = gameBoard.copy()
                b.addPiece(col,"O")
                newScore = self.AlphaBeta(b,depth-1,alpha, beta,True)[0]
                if newScore < value:
                    value = newScore 
                    column = col
                #changes the value of beta to the min of the value or previous beta
                beta = min(beta,value)
                if alpha >= beta: #Prunes if alpha >= beta
                    self.numPruned +=1
                   
                    break
            return (value,column)
        
        
	