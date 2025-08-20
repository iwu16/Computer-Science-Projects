'''
Name: Isabella Wu

Date: 10/31/21

Description: 

This Minesweeper code takes dimensions of the gameboard from console. Bombs are represented by * signs, the displayboard icons are + signs, and flags are represented by - signs. Throughout the code, try except as well as if statements are used to catch potential index errors if the user enters in a coordinate that is outside the range of the gameboard, as well as if they enter in nonintegers. In order to handle the user's first input (that is used to generate the board) vs the rest of user's inputs (simply revealing the coordinate), a boolean is used for "first". If first is true, this signals to the code that it is user's first input, and the makegameboard() function is run with user's first input as arguments. This is to make sure the user can't lose on their first try. If first is false, the reveal() function is run to reveal that coordinate. Two boards are created - solution board and displayboard. The displayboard is what the user sees, while the solutionboard remains hidden and contains the location of bombs, as well as the surrounding numbers that will be revealed when the user chooses a spot on the displayboard to reveal. The purpose of making the solutionboard and displayboard with w+2 and h+2 dimensions is create gutters for running the code more smoothly.  
'''

#take width and height of gameboard, as well as number of bombs, from console
import sys
import random
w = int(sys.argv[1])
h = int(sys.argv[2])
b = int(sys.argv[3])

#makes sure # of bombs doesn't exceed total number of spaces on board
if b>w*h:
    print("That's too many bombs! Please run the code again.")
    sys.exit()

#creates solution and display board
solutionboard = [[0 for a in range(w+2)]for b in range(h+2)] 
displayboard = [['+' for a in range(w+2)]for b in range(h+2)] 

#userInput function prompts user to input coordinates to reveal. 'first' is used as a variable to differentiate between user's first input and the rest of them. 
def userInput(first):
    userchoice = input(">>> ")
    userchoices = userchoice.split(" ")
    try:
        #divides user's input into two coordinates, x and y
        x = int(userchoices[0])
        y = int(userchoices[1])
    #makes sure userinput is an integer coordinate
    except (IndexError, ValueError): 
        print("Please enter in integer coordinates that fit within the gameboard.")
        userInput(first)
    #makes sure (x,y) is within the range of the gameboard
    if (not(1 <= x <= w) or not(1 <= y <= h)):
        print("Please enter in integer coordinates that fit within the range of the gameboard.")
        userInput(first)
    else:
        if first: #makes gameboard with user's first input as arguments
            makegameboard(x,y)
            decide(userchoices, x, y) 
        else: 
            decide(userchoices,x,y)
#after each reveal, the code checks to see if the user has fullfilled winning conditions. the user will win when the number of flagged spaces and number of unrevealed spaces add up to the total number of bombs in the solutionboard. 
def checkforwin(): 
    counter1 = sum(row[1:-1].count('-') for row in displayboard[1:-1])
    counter2 = sum(row[1:-1].count('+') for row in displayboard[1:-1])
    bombs = sum(row.count('*') for row in solutionboard)
    if counter1 + counter2 == bombs:
        win()
    else:
        userInput(False)

#endgame() occurs when user trys to reveal a bomb. they are given the option to restart. 
def endgame(): 
    print("\n\nYou hit a bomb - game over!\n\n")
    restart()

#takes user's inputted coordinates as arguments, and reveals that spot by setting the displayboard icon at that coordinate equal to the number on the solutionboard that corresponds with that spot. checks for a win after each reveal. if the spot the user chooses is a bomb, endgame() will run and the user loses. if the spot user chooses to reveal is a 0, clearingzeros() runs in order to handle the special clearing of zeros. 
def reveal(x,y):
    if solutionboard[y][x] == "*":
        endgame()
    elif solutionboard[y][x] == 0:
        #print(x,y)
        clearingzeros(x,y)
    else:
        pass
    displayboard[y][x] = solutionboard[y][x]
    for row in displayboard[1:-1]:
        print(*row[1:-1])
    checkforwin()

#flag() gives the user the option to flag a coordinate if they deduce that a bomb is located there. if that spot has already been flagged, flagging that spot again will unflag it. 
def flag(x,y): 
    if displayboard[y][x] == '-':
    	displayboard[y][x] = '+'
    else: 
    	displayboard[y][x] = '-'
    for row in displayboard[1:-1]:
    	print(*row[1:-1])
    userInput(False)

#decide() looks at the userinput and decides whether the user has chosen to flag a coordinate or simply reveal it. if the userinput enters a 'f' after the coordinate, flag() will run. else, reveal() will run.
def decide(userIn, x, y):
    if len(userIn) >= 3: 
        if userIn[2] == "f":
            flag(x,y) 
        else:
            print("To flag, please input in the letter f after your coordinates.")
            userInput(False)
    else:
        reveal(x,y)

#makegameboard() creates the gameboard with the dimensions user inputted in console. a random location is generated for each bomb. however, if there is already a bomb in that location or that location is the same location as the user's first input, a new random spot is chosen. this is to make sure the user can't lose on their first move. after a location is chosen for the bomb, the surrounding spaces will all +1, to indicate that there is a bomb in one of the surrounding locations.makegameboard also makes sure that all the gutters have a value of one, to ensure that there won't be an error later on in the clearingzeros() function.  
def makegameboard(x,y):
    global solutionboard,displayboard
    solutionboard = [[0 for a in range(w+2)]for b in range(h+2)] 
    for a in range(b):
        randomRow = random.randint(1,h)
        randomColumn = random.randint(1,w)
        #print(randomRow, randomColumn)
        while solutionboard[randomRow][randomColumn] == "*" or (randomRow==x and randomColumn==y):
            randomRow = random.randint(1,h)
            randomColumn = random.randint(1,w)
        solutionboard[randomRow][randomColumn] = "*"
        for i in range(randomRow - 1, randomRow +2):
            for j in range(randomColumn - 1, randomColumn + 2):
                if solutionboard[i][j] != "*":
                    solutionboard[i][j] += 1
    displayboard = [['+' for a in range(w+2)]for b in range(h+2)] 
    solutionboard[0] = [1]*(w+2)
    solutionboard[-1] = [1]*(w+2)
    for q in range(len(solutionboard)):
        solutionboard[q][0] = 1
        solutionboard[q][-1] = 1

#clearingzeros() runs when user chooses a spot with a zero located there. that zero will be revealed, and then the spaces surrounding that zero will be checked to see if there are any zeros. if the code finds a zero in a surrounding space, it will reveal that zero, and then check the spaces around that zero for another zero, and so on.      
def clearingzeros(x,y):
    zeros = []
    zeros.append((y,x))
    while len(zeros)>0:
        y,x = zeros.pop(0)
        for r in range(y-1, y+2):
            for c in range(x-1,x+2):
                if ((1 <= r <= h) and (1 <= c <= w)):
                    #print(c,r)
                    if ((solutionboard[r][c] == 0) and (displayboard[r][c] == '+')):
                        zeros.append((r,c))
                    displayboard[r][c] = solutionboard[r][c]
    for row in displayboard[1:-1]:
        print(*row[1:-1])
    checkforwin()

#when checkforwin() finds that the winning conditions are satisifed, win() ends the game and gives user the option to restart. 
def win(): 
    print("\n\nYou win!\n\n")
    restart()

#restart() lets user try another game with the same board dimensions. try except is used to make sure user enters in 1 or 2. 
def restart():
    try: 
        userchoiceg = int(input("Try again? Yes = 1, No = 2\n\n"))
        if(userchoiceg == 1):
            start()
        elif(userchoiceg == 2):
            print("\n\nThank you for playing, see you next time!!\n\n")
            sys.exit()
        else:
            print("\nPlease enter in either 1 or 2.\n\n")
            restart()
    except ValueError: 
        print("\nThat is not a number, try again.\n\n")
        restart()

#starts the game, gives user instructions. 
def start(): 
    print("\n\nWelcome to Minesweeper! The instructions for this game are very similar to the minesweeper you may have played as a child. The + signs represent the icons of the board. The goal of the game is to reveal all spaces on the board - without hitting a bomb! When a space is revealed, you'll see a number, this number represents the number of bombs that surround that coordinate. The number of bombs you inputted in console will be the number of bombs on the board - make sure to be aware of the numbers you revealto deduce where the bombs are located. Once you've revealed all spaces on the board aside from the bombs, you win! If you accidentally reveal a bomb however, the game will end and you lose. :(.\n\nAlright! Let's get into some more detailed instructions, shall we? When the game starts, you'll see some symbols that look like this: >>> . When this symbol appears, enter in a coordinate (x,y) into the terminal and press enter. This coordinate should be in the form x space y. This will be the coordinate that you want to reveal on the gameboard, and the + icon will be replaced with a number that represents the number of bombs in its surroundings.\n\nIf you have figured out where a bomb is located, you can flag that location by entering in a coordinate followed by a space and an f at the end. The flag will be depicted by a - sign. To unflag a coordinate, enter in the coordinate again followed by a space and an f, and the flag will be replaced by a regular board icon.\n\nNow that the instructions are over with, let's get minesweeping! As a reminder, when the symbol >>> appears, enter in a coordinate and watch the magic happen! The gameboard will be generated around your first coordinate, so don't worry about hitting a bomb your first time. Good luck, and have fun!\n\n")
    userInput(True)
start()

