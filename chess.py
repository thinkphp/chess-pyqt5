import sys
import enum
from typing import List, Tuple, Optional
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                             QLabel, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QColor, QPainter, QFont, QBrush
from PyQt5.QtCore import Qt, QSize

class PieceType(enum.Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

class Color(enum.Enum):
    WHITE = 1
    BLACK = 2

class ChessPiece:
    def __init__(self, piece_type: PieceType, color: Color, initial_pos: Tuple[int, int]):
        self.type = piece_type
        self.color = color
        self.position = initial_pos
        self.has_moved = False

    def get_possible_moves(self, board):
        """Generate possible moves for the piece"""
        if self.type == PieceType.PAWN:
            return self._get_pawn_moves(board)
        elif self.type == PieceType.ROOK:
            return self._get_rook_moves(board)
        elif self.type == PieceType.KNIGHT:
            return self._get_knight_moves(board)
        elif self.type == PieceType.BISHOP:
            return self._get_bishop_moves(board)
        elif self.type == PieceType.QUEEN:
            return self._get_queen_moves(board)
        elif self.type == PieceType.KING:
            return self._get_king_moves(board)
        return []

    def _get_pawn_moves(self, board):
        moves = []
        x, y = self.position
        direction = -1 if self.color == Color.WHITE else 1

        # Forward move
        if 0 <= x + direction < 8 and board[x + direction][y] is None:
            moves.append((x + direction, y))

            # Initial two-square move
            if not self.has_moved and 0 <= x + 2*direction < 8 and board[x + 2*direction][y] is None:
                moves.append((x + 2*direction, y))

        # Diagonal captures
        capture_positions = [
            (x + direction, y - 1),
            (x + direction, y + 1)
        ]

        for nx, ny in capture_positions:
            if 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = board[nx][ny]
                if target_piece and target_piece.color != self.color:
                    moves.append((nx, ny))

        return moves

    def _get_rook_moves(self, board):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            x, y = self.position
            while True:
                x += dx
                y += dy

                if not (0 <= x < 8 and 0 <= y < 8):
                    break

                if board[x][y] is None:
                    moves.append((x, y))
                else:
                    if board[x][y].color != self.color:
                        moves.append((x, y))
                    break

        return moves

    def _get_knight_moves(self, board):
        moves = []
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        x, y = self.position

        for dx, dy in knight_moves:
            nx, ny = x + dx, y + dy

            if 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = board[nx][ny]
                if target_piece is None or target_piece.color != self.color:
                    moves.append((nx, ny))

        return moves

    def _get_bishop_moves(self, board):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            x, y = self.position
            while True:
                x += dx
                y += dy

                if not (0 <= x < 8 and 0 <= y < 8):
                    break

                if board[x][y] is None:
                    moves.append((x, y))
                else:
                    if board[x][y].color != self.color:
                        moves.append((x, y))
                    break

        return moves

    def _get_queen_moves(self, board):
        # Queen moves are combination of rook and bishop moves
        return (self._get_rook_moves(board) +
                self._get_bishop_moves(board))

    def _get_king_moves(self, board):
        moves = []
        king_moves = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        x, y = self.position

        for dx, dy in king_moves:
            nx, ny = x + dx, y + dy

            if 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = board[nx][ny]
                if target_piece is None or target_piece.color != self.color:
                    moves.append((nx, ny))

        return moves

class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()
        # Increased board size
        self.BOARD_SIZE = 600  # Increased from 400
        self.CELL_SIZE = self.BOARD_SIZE // 8
        self.setFixedSize(self.BOARD_SIZE, self.BOARD_SIZE)
        
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = Color.WHITE
        self.selected_piece = None
        self.initialize_board()

    def initialize_board(self):
        # Reuse the initialization from the previous implementation
        # White pieces
        piece_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP,
                       PieceType.QUEEN, PieceType.KING, PieceType.BISHOP,
                       PieceType.KNIGHT, PieceType.ROOK]

        # Pawns
        for y in range(8):
            self.board[1][y] = ChessPiece(PieceType.PAWN, Color.BLACK, (1, y))
            self.board[6][y] = ChessPiece(PieceType.PAWN, Color.WHITE, (6, y))

        # Other pieces
        for y, piece_type in enumerate(piece_order):
            self.board[0][y] = ChessPiece(piece_type, Color.BLACK, (0, y))
            self.board[7][y] = ChessPiece(piece_type, Color.WHITE, (7, y))

    def paintEvent(self, event):
        painter = QPainter(self)
        cell_size = self.CELL_SIZE

        # Draw board with slightly more pronounced colors
        light_square = QColor(240, 217, 181)  # Beige
        dark_square = QColor(181, 136, 99)    # Brown

        for row in range(8):
            for col in range(8):
                # Alternate square colors
                color = light_square if (row + col) % 2 == 0 else dark_square
                painter.fillRect(col * cell_size, row * cell_size,
                                 cell_size, cell_size, color)

        # Draw coordinate labels
        painter.setPen(QColor(100, 100, 100))
        painter.setFont(QFont('Arial', 10))
        
        # Column labels (a-h)
        for col in range(8):
            label = chr(ord('a') + col)
            painter.drawText(
                col * cell_size + cell_size // 2 - 5, 
                self.height() - 5, 
                label
            )

        # Row labels (1-8)
        for row in range(8):
            label = str(8 - row)
            painter.drawText(
                5, 
                row * cell_size + cell_size // 2 + 5, 
                label
            )

        # Draw pieces with larger, more readable symbols
        painter.setFont(QFont('Arial', 36))  # Larger font
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    # Different colors for white and black pieces
                    color = Qt.black if piece.color == Color.BLACK else Qt.white
                    painter.setPen(color)
                    
                    # Center the piece symbol in the cell
                    painter.drawText(
                        col * cell_size + cell_size // 4,
                        row * cell_size + cell_size * 3 // 4,
                        self.get_piece_symbol(piece)
                    )

    def get_piece_symbol(self, piece):
        symbols = {
            PieceType.PAWN: '♙' if piece.color == Color.WHITE else '♟',
            PieceType.ROOK: '♖' if piece.color == Color.WHITE else '♜',
            PieceType.KNIGHT: '♘' if piece.color == Color.WHITE else '♞',
            PieceType.BISHOP: '♗' if piece.color == Color.WHITE else '♝',
            PieceType.QUEEN: '♕' if piece.color == Color.WHITE else '♛',
            PieceType.KING: '♔' if piece.color == Color.WHITE else '♚'
        }
        return symbols[piece.type]

    def mousePressEvent(self, event):
        cell_size = self.CELL_SIZE
        col = event.x() // cell_size
        row = event.y() // cell_size

        clicked_piece = self.board[row][col]

        if self.selected_piece:
            # Try to move the selected piece
            if (row, col) in self.selected_piece.get_possible_moves(self.board):
                self.move_piece(self.selected_piece.position, (row, col))
                self.selected_piece = None
                self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
            else:
                self.selected_piece = None
        elif clicked_piece and clicked_piece.color == self.current_player:
            self.selected_piece = clicked_piece

        self.update()

    def move_piece(self, from_pos, to_pos):
        fx, fy = from_pos
        tx, ty = to_pos

        # Move the piece
        self.board[tx][ty] = self.board[fx][fy]
        self.board[fx][fy] = None

        # Update piece position
        self.board[tx][ty].position = (tx, ty)
        self.board[tx][ty].has_moved = True

class ChessGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess Game")
        self.setGeometry(100, 100, 700, 800)  # Increased window size

        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Player turn label
        self.turn_label = QLabel("White's Turn")
        self.turn_label.setAlignment(Qt.AlignCenter)
        self.turn_label.setFont(QFont('Arial', 18))
        main_layout.addWidget(self.turn_label)

        # Chess board
        self.chess_board = ChessBoard()
        main_layout.addWidget(self.chess_board)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

def main():
    app = QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
