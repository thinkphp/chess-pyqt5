# PyQt Chess 

A fully functional chess game implemented in Python using PyQt5, featuring a graphical user interface and complete chess game mechanics.

![Chess Game Screenshot](screenshot.png)

## Features

- Full chess board with 8x8 grid
- Coordinate labels (a-h, 1-8)
- Unicode chess piece symbols
- Turn-based gameplay
- Implemented move rules for all chess pieces:
  - Pawn
  - Rook
  - Knight
  - Bishop
  - Queen
  - King
- Move validation
- Visual piece selection

## Prerequisites

- Python 3.7+
- PyQt5

## Installation

1. Clone the repository:
```bash
git https://github.com/thinkphp/chess-pyqt5.git
cd pyqt-chess
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required dependencies:
```bash
pip install PyQt5
```

## Running the Game

```bash
python chess_game.py
```

## How to Play

1. Click on a piece to select it
2. Click on a valid destination square to move the piece
3. Players alternate turns between white and black
4. Game follows standard chess movement rules

## Future Improvements

- Checkmate detection
- En passant move
- Castling
- Game state tracking
- Move history
- AI opponent

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open-source and available under the MIT License.

## Technologies

- Python
- PyQt5
- Object-Oriented Programming

## Author

Adrian Statescu
