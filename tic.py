import re
import random
import time


def ClearBoard():
    board = {'1,1': ' ', '1,2': ' ', '1,3': ' ',
             '2,1': ' ', '2,2': ' ', '2,3': ' ',
             '3,1': ' ', '3,2': ' ', '3,3': ' '}  # prepare empty board
    return board

def CreateBoard(board): #draw board
    for i in range(1,4):
        print(board[str(i)+',1'] + '|'+board[str(i)+',2'] +'|'+board[str(i)+',3'])
        print('-----')

def IfWon(board,que):
    columns = [[], [], []]
    rows = [[], [], []]
    for k in range(1,4): #check columns and rows
        for i in range(1,4):
            columns[i-1].append(board[str(i) + ',' + str(k)])
            rows[i-1].append(board[str(k) + ',' + str(i)])

    for i in range(3): #check if any column or row contains only x/o(que)
        if columns[i].count(que) == 3 or rows[i].count(que) == 3: #counts x/o in every column/row, if counted==3 -> win
            return True

    #check slant
    if board['2,2'] == que and ( (board['1,1']==que and board['3,3']==que) or (board['1,3']==que and board['3,1']==que) ):
        return True

    return False

def IfDraw(board):
    for k in range(1,4): #check columns and rows
        for i in range(1,4):
            if board[str(i) + ',' + str(k)] == ' ': #if any place is empty - game is still possible
                return False
    return True

def PlayAgainstHuman(wspRegex):
        board = ClearBoard()
        CreateBoard(board)  # draw starting-empty board
        que = 'X'

        while True:
            print('Kolej gracza ' + que + ', podaj współrzędne pola (y,x): ')
            wsp = input()

            wsp_m = wspRegex.search(wsp)
            if wsp_m == None:
                print("Nieprawidłowe wspołrzędne!\n")
                continue

            # check if certain place is empty
            if board[wsp] == ' ':
                board[wsp] = que
            else:
                print("Pole jest zajęte!")
                continue

            CreateBoard(board)  # board's actualization

            if IfWon(board, que):
                print("Gratulacje! wygrał gracz " + que)
                if AskForRound():
                    '''board = ClearBoard()
                    CreateBoard(board)
                    que = 'X'
                    continue'''
                    Main()
                break
            elif IfDraw(board):
                print("Remis!")
                if AskForRound():
                    '''board = ClearBoard()
                    CreateBoard(board)
                    que = 'X'
                    continue'''
                    Main()
                break

            if que == 'X':  # change que
                que = 'O'
            else:
                que = 'X'

def ComputerMove(board):
    possible_moves = [] #list of possible moves
    for k in range(1,4):
        for i in range(1,4):
            if board[str(k)+','+str(i)] == ' ':
                possible_moves.append(str(k)+','+str(i))

    wsp = '1,1'
    #check possibility to win or to block opponent to win
    for q in ['O', 'X']:
        for move in possible_moves:
            cp_board = board.copy()
            cp_board[move] = q
            if IfWon(cp_board, q):
                wsp = move
                return wsp

    #check possibility to take any of the corners
    empty_cornes = []
    for move in possible_moves:
        if move in ['1,1', '1,3', '3,1', '3,3']:#corners
            empty_cornes.append(move)
    if len(empty_cornes) > 0:
        wsp = SelectRandomWsp(empty_cornes)
        return wsp

    #check possibility to take the center
    if '2,2' in possible_moves:
        wsp = '2,2'
        return wsp

    #take any edge
    empty_edges = []
    for move in possible_moves:
        if move in ['1,2', '2,1', '2,3', '3,2']:
            empty_edges.append(move)
    if len(empty_edges)>0:
        wsp = SelectRandomWsp(empty_edges)
        return wsp

def PlayAgainstComputer(wspRegex):
    board = ClearBoard()
    CreateBoard(board)

    while True:
        que = "X"
        wsp = input("Podaj współrzędne pola (y,x): ")
        wsp_m = wspRegex.search(wsp)
        if wsp_m == None:
            print("Nieprawidłowe wspołrzędne!\n")
            continue

        # check if certain place is empty
        if board[wsp] == ' ':
            board[wsp] = que
        else:
            print("Pole jest zajęte!")
            continue

        CreateBoard(board)  # board's actualization

        #Check results
        if IfWon(board,que):
            print("Gratulacje! Wygrałeś!")
            if AskForRound():
                '''board = ClearBoard()
                CreateBoard(board)
                continue'''
                Main()
            break
        elif IfDraw(board):
            print("Remis!")
            if AskForRound():
                '''board = ClearBoard()
                CreateBoard(board)
                continue'''
                Main()
            break


        print("Ruch komputera:")
        time.sleep(1)
        #computer's move
        que = "O"
        cmp_wsp = ComputerMove(board)
        board[cmp_wsp] = que
        CreateBoard(board)

        # Check results
        if IfWon(board, que):
            print("Przegrana!")
            if AskForRound():
                '''board = ClearBoard()
                CreateBoard(board)
                continue'''
                Main()
            break
        elif IfDraw(board):
            print("Remis!")
            if AskForRound():
                '''board = ClearBoard()
                CreateBoard(board)
                continue'''
                Main()
            break

def SelectRandomWsp(possible_wsps):
    r = random.randrange(0,len(possible_wsps))
    return possible_wsps[r]

def AskForRound():
    answer = input("Czy chcesz zagrać jeszcze raz? (t/n): ")
    if answer == 't':
        return True
    else:
        return False

def Main():
    wspRegex = re.compile(r'[1-3],[1-3]')
    incorrect_input = True
    while incorrect_input:
        play_against = input("Chcesz grać przeciwko komputerowi czy człowiekowi? k/c: ")
        if play_against == 'c':
            PlayAgainstHuman(wspRegex)
            incorrect_input = False
        elif play_against == 'k':
            PlayAgainstComputer(wspRegex)
            incorrect_input = False
        else:
            print("Niepoprawne dane!")

Main()
