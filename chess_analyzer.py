import chess
from stockfish import Stockfish
from functions import print_board
from functions import initialize_board
from time import sleep
from os import system

system('clear')

path = 'your/path/to/stockfish'

running = True
stockfish_bool = True
board = None

no_board = True
while no_board:
    try:
        board = initialize_board()
        no_board = False
    except:
        pass

while True:
    stock = input('Do you want to run Stockfish Y/N?\n')
    if stock.upper() not in ['Y', 'N']:
        print('Not a valid answer. Try again')
    elif stock.upper() == 'Y':
        stockfish = Stockfish(path)
        break
    else:
        stockfish_bool = False
        break

while running:
    if stockfish_bool:
        stockfish.set_fen_position(board.fen())
        eval = stockfish.get_evaluation()
        running = print_board(board, eval)
    else:
        running = print_board(board)
    