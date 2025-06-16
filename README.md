# Chess Analyzer

A simple Python-based chess analyzer using the [`python-chess`](https://python-chess.readthedocs.io/) library and the Stockfish engine.  
This tool lets you interactively view and evaluate board positions using a custom interface in the terminal.

## Features

- Stockfish integration for position evaluation
- FEN-based input and board state management
- Terminal-based board rendering
- Modular function design via `functions.py`

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/chess-analyzer.git
   cd chess-analyzer

2.	Install dependencies:
   ```bash
	pip install python-chess stockfish
```
4.	Download and configure Stockfish:
- Download from https://stockfishchess.org/download/
- Place the binary (e.g. stockfish-macos-m1-apple-silicon) in a known location
- Edit the path in chess_analyzer.py to point to your Stockfish path:

Run the script:
```
python chess_analyzer.py
```
- You will be asked whether to run Stockfish
- The board is initialized using initialize_board()
- Evaluations are printed after each move if Stockfish is enabled

Example Output
```
Do you want to run Stockfish Y/N?
> Y

Evaluation: +0.24 (white slightly better)

  a b c d e f g h
8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 8
7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 7
6 · · · · · · · · 6
...
1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 1
  a b c d e f g h
```
Notes
- Requires Python 3.6 or higher
- Ensure the Stockfish binary is executable (use chmod +x if needed)
- You can modify board setup and printing in functions.py
