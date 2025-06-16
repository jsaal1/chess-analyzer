import chess 
from stockfish import Stockfish
from os import system

def is_valid_fen(fen_str) -> bool:
    parts = fen_str.split()

    # Check if the FEN contains the right parts
    if len(parts) != 6 or fen_str.count(' ') != 5:
        return False
    
    # Convert the list of parts to seperate variables for further investigation
    pos, turn, castle, ep, hm, move = parts
    
    # Create a list of rows and check validity
    rows = pos.split('/')

    # Check board dimensions
    if len(rows) != 8:
        return False
    
    # Check for both kings and valid pieces as well as row length
    white_king = False
    black_king = False
    valid_pieces = 'pnbrqkPNBRQK'
    for row in rows:
        count = 0
        for char in row:
            if char not in valid_pieces and not char.isdigit():
                return False
            
            if char == 'k':
                black_king = True

            if char == 'K':
                white_king = True

            if char.isdigit():
                count+= int(char)
            else:
                count+= 1
        if count != 8:
            return False
        
    if not white_king or not black_king:
        return False
    
    # Check for valid turn
    if turn not in ['w', 'b']:
        return False
    
    # Check how many different castles available
    if len(castle) > 4:
        return False
    
    # Check if the castles available are valid castles
    valid_castle = set('kqKQ')
    if castle != '-':
        if any(c not in valid_castle for c in castle):
            return False
        if len(set(castle)) != len(castle):
            return False
        

    if ep != '-':
        if len(ep) != 2 or ep[0] not in 'abcdefgh' or ep[1] not in '36':
            return False
    
    if not hm.isdigit() or not move.isdigit():
        return False
    
    if not(0 <= int(hm) < 100):
        return False
    
    if int(move) < 1:
        return False
    
    return True

def initialize_board() -> chess.Board | None:
    check_fen = input('Do you want to start from a certain position Y/N?\n').strip()
    if check_fen.upper() not in ['Y', 'N']:
        print('Not a valid answer')
    else:
        if check_fen.upper() == 'Y':
            while True:
                fen = input('Enter the FEN:\n')
                if is_valid_fen(fen):
                    return chess.Board(fen)
                else:
                    print('That wasn\'t a valid FEN. Try again')
        else:
            return chess.Board()
        
def print_board(board: chess.Board, eval=dict()) -> bool:
    system('clear')

    result = board.result(claim_draw=True)
    
    rows = board.board_fen().split('/')
    board_matrix = [['| ' if (j != 0 and j != 7) else '[ ' if j == 0 else '| ]'for j in range(8)] for i in range(8)]

    for i, row in enumerate(board_matrix):
        for j, _ in enumerate(row):
            if (i+j)%2 == 0:
                board_matrix[i][j] = board_matrix[i][j][0] + '▓' + board_matrix[i][j][2:]

    # Mapping from FEN characters to Unicode chess symbols
    unicode_pieces = {
        'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
        'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙'
    }

    for i, row in enumerate(rows):
        col = 0
        for char in row:
            if char.isdigit():
                col += int(char)
            else:
                if col == 0:
                    board_matrix[i][col] = '[' + unicode_pieces[char]
                elif col == 7:
                    board_matrix[i][col] = '|' + unicode_pieces[char] + ']'
                else:
                    board_matrix[i][col] = '|' + unicode_pieces[char]
                col += 1

    if eval:
        bar_val = 8 - round(normalize_eval(eval)*8)

    print(' ', 19*'_')
    for i, row in enumerate(board_matrix):
        print( 8 - i, '|' + ''.join(row) + '|', end='')
        if eval:
            if bar_val > 0:
                print(' [ ]')
                bar_val -= 1
            else:
                print(' [█]')
        else:
            print()

    if eval:
        if eval.get('type') == 'cp':
            score_str = f'{eval.get('value')/100:.2f}'
        else:
            score_str = ' M' + str(abs(eval.get('value')))

    print(' ', 19*'‾', f'{'' if not eval else score_str}')
    print('    a b c d e f g h\n')

    if result == '*':
        if board.turn:
            print(f'Move: {board.fullmove_number}, White to move')
        else:
            print(f'Move: {board.fullmove_number}, Black to move')
        move = input('Enter your move in uci format (eg. Nf3 = g1f3): ')

        if move == '\x1b':
            system('clear')
            return False

        try:
            move_obj = chess.Move.from_uci(move)
            if move_obj in board.legal_moves:
                board.push(move_obj)
                return True
            else:
                print(f"{move} is not a legal move. Try again.")
                input()
                return True
        except ValueError:
            print(f"{move} is not a valid UCI format. Try again.")
            input()
            return True
    elif result == '1-0':
        print('White won!')
        input()
        return False
    elif result == '0-1':
        print('Black won!')
        input()
        return False
    else:
        print('Draw!')
        input()
        return False


def normalize_eval(eval: dict) -> float:
    if eval['type'] == 'mate':
        value = eval['value']
        return 1.0 if value > 0 else 0.0
    else:
        cp = eval['value']

        cp = max(-1000, min(1000, cp))
        return 0.5 + (cp/2000)
