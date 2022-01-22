import pyautogui as pag
import time
import copy

boxes = [[(267,362), (317,364), (364,364), (430,362), (480,363), (529,364), (590,363), (642,362), (693,362)], 
        [(266,417), (317,417), (367,416), (429,416), (478,416), (531,415), (593,416), (642,416), (691,416)], 
        [(269,465), (315,467), (367,468), (427,469), (478,470), (529,469), (589,468), (643,469), (689,469)], 
        [(267,530), (317,528), (365,528), (430,528), (478,528), (531,528), (594,528), (642,532), (691,531)], 
        [(267,583), (314,583), (365,580), (429,582), (481,584), (531,580), (594,579), (642,583), (683,581)], 
        [(268,636), (317,635), (366,634), (428,634), (481,633), (531,635), (594,636), (642,638), (689,635)], 
        [(266,691), (316,690), (367,693), (428,691), (481,691), (531,691), (594,691), (642,698), (689,691)], 
        [(269,745), (316,746), (368,744), (431,748), (481,748), (531,747), (594,743), (642,741), (692,745)], 
        [(269,798), (315,798), (366,797), (429,796), (481,795), (531,797), (594,797), (642,796), (692,796)]]

numbers = [0,(292,895),(387,898),(476,894),(574,895),(665,895),(289,981),(384,985),(480,982),(575,982)]

time.sleep(2)

topleftx = 251
toplefty = 336
bottomrightx = 708
bottomrighty = 822

boxwidth = (bottomrightx - topleftx)/8
boxheight = (bottomrighty - toplefty)/8


def findNextCellToFill(sudoku):
    for x in range(9):
        for y in range(9):
            if sudoku[x][y] == 0:
                return x, y
    return -1, -1


def isValid(sudoku, i, j, e):
    rowOk = all([e != sudoku[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != sudoku[x][j] for x in range(9)])
        if columnOk:
            secTopX, secTopY = 3*(i//3), 3*(j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if sudoku[x][y] == e:
                        return False
            return True
    return False


def solveSudoku(sudoku, i=0, j=0):
    global backtracks
    i, j = findNextCellToFill(sudoku)
    if i == -1:
        return True

    for e in range(1, 10):
        if isValid(sudoku, i, j, e):
            sudoku[i][j] = e
            if solveSudoku(sudoku, i, j):
                return True
            sudoku[i][j] = 0
    return False


def printsudoku():
    print("\n---------------------\n")
    for i in range(len(sudoku)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(sudoku[i][j])+" "
        print(line)


def fillsudoku(nr, pos):
    global sudoku
    indexlocx = int((pos[0] - topleftx + boxwidth/2)//boxwidth)
    indexlocy = int((pos[1] - toplefty + boxheight/2)//boxwidth)
    sudoku[indexlocy][indexlocx] = nr


def fillcell(nr, x, y):
    xcoord = topleftx + boxwidth * x
    ycoord = toplefty + boxheight * y
    pag.click(boxes[x][y][0], boxes[x][y][1])
    pag.click(boxes[x][y][0], boxes[x][y][1])
    pag.click(numbers[nr][0],numbers[nr][1])
    pag.click(numbers[nr][0],numbers[nr][1])


while True:
    sudoku =    [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
            
    for i in range(1, 10):
        for pos in pag.locateAllOnScreen('Images/'+str(i)+'.png',confidence=0.95):
            fillsudoku(i, pos)

    printsudoku()
    sudokucopy = copy.deepcopy(sudoku)
    solveSudoku(sudoku)
    printsudoku()

    for x in range(9):
        for y in range(9):
            if sudokucopy[x][y] == 0:
                fillcell(sudoku[x][y], x, y)
    
    print("waiting for 5 seconds")
    time.sleep(5)

    pag.click(483,711)
    
    print("Waiting for 5 seconds")
    time.sleep(5)

    pag.click(471,976)
    
    print("Waiting for 5 seconds")
    time.sleep(5)

    pag.click(479,709)
    
    print("Waiting for 20 seconds")
    time.sleep(40)

    pag.click(550,899)
    
    print("Waiting for 5 seconds")
    time.sleep(5)

    pag.click(550,899)

    print("Waiting for 5 seconds")
    time.sleep(5)


