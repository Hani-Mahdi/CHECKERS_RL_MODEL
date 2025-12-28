from game.piece import Piece


class Board:
    
    def __init__(self, size=8, game_mode='classic'):
        self.size = size
        self.game_mode = game_mode
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.pieces = {}
        
        if game_mode == 'classic':
            self._setup_classic()
        else:
            self._setup_four_player()
    
    def _setup_classic(self):
        self.pieces = {'red': [], 'black': []}
        
        for row in range(3):
            for col in range(self.size):
                if (row + col) % 2 == 1:
                    piece = Piece('black', row, col)
                    self.grid[row][col] = piece
                    self.pieces['black'].append(piece)
        
        for row in range(5, 8):
            for col in range(self.size):
                if (row + col) % 2 == 1:
                    piece = Piece('red', row, col)
                    self.grid[row][col] = piece
                    self.pieces['red'].append(piece)
    
    def _setup_four_player(self):
        self.pieces = {'red': [], 'blue': [], 'green': [], 'yellow': []}
        
        for row in range(9, 12):
            for col in range(3, 9):
                if (row + col) % 2 == 1:
                    piece = Piece('red', row, col)
                    self.grid[row][col] = piece
                    self.pieces['red'].append(piece)
        
        for row in range(0, 3):
            for col in range(3, 9):
                if (row + col) % 2 == 1:
                    piece = Piece('blue', row, col)
                    self.grid[row][col] = piece
                    self.pieces['blue'].append(piece)
        
        for row in range(3, 9):
            for col in range(0, 3):
                if (row + col) % 2 == 1:
                    piece = Piece('green', row, col)
                    self.grid[row][col] = piece
                    self.pieces['green'].append(piece)
        
        for row in range(3, 9):
            for col in range(9, 12):
                if (row + col) % 2 == 1:
                    piece = Piece('yellow', row, col)
                    self.grid[row][col] = piece
                    self.pieces['yellow'].append(piece)
    
    def is_valid_square(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        
        if self.game_mode == 'four_player':
            if row < 3 and col < 3:
                return False
            if row < 3 and col >= 9:
                return False
            if row >= 9 and col < 3:
                return False
            if row >= 9 and col >= 9:
                return False
        
        return True
    
    def get_piece(self, row, col):
        if not self.is_valid_square(row, col):
            return None
        return self.grid[row][col]
    
    def move_piece(self, piece, new_row, new_col):
        self.grid[piece.row][piece.col] = None
        piece.move(new_row, new_col)
        self.grid[new_row][new_col] = piece
        self._check_promotion(piece)
    
    def _check_promotion(self, piece):
        if piece.is_king:
            return
        
        if self.game_mode == 'classic':
            if piece.color == 'red' and piece.row == 0:
                piece.make_king()
            elif piece.color == 'black' and piece.row == 7:
                piece.make_king()
        else:
            if piece.color == 'red' and piece.row <= 2:
                piece.make_king()
            elif piece.color == 'blue' and piece.row >= 9:
                piece.make_king()
            elif piece.color == 'green' and piece.col >= 9:
                piece.make_king()
            elif piece.color == 'yellow' and piece.col <= 2:
                piece.make_king()
    
    def remove_piece(self, piece):
        self.grid[piece.row][piece.col] = None
        if piece.color in self.pieces:
            if piece in self.pieces[piece.color]:
                self.pieces[piece.color].remove(piece)
    
    def get_all_pieces(self, color):
        return self.pieces.get(color, [])
    
    def copy(self):
        new_board = Board(self.size, self.game_mode)
        new_board.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        new_board.pieces = {color: [] for color in self.pieces.keys()}
        
        for color, pieces in self.pieces.items():
            for piece in pieces:
                new_piece = piece.copy()
                new_board.grid[new_piece.row][new_piece.col] = new_piece
                new_board.pieces[color].append(new_piece)
        
        return new_board
    
    def get_state_key(self):
        state = []
        for row in range(self.size):
            for col in range(self.size):
                piece = self.grid[row][col]
                if piece is None:
                    state.append(0)
                else:
                    colors = ['red', 'black', 'blue', 'green', 'yellow']
                    color_idx = colors.index(piece.color) + 1
                    value = color_idx * 2 + (1 if piece.is_king else 0)
                    state.append(value)
        return tuple(state)
