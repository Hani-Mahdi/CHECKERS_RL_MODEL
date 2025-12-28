class Piece:
    
    def __init__(self, color, row, col):
        self.color = color
        self.is_king = False
        self.row = row
        self.col = col
    
    def make_king(self):
        self.is_king = True
    
    def move(self, row, col):
        self.row = row
        self.col = col
    
    def get_direction(self):
        if self.is_king:
            return [-1, 1]
        
        if self.color == 'red':
            return [-1]
        elif self.color == 'black':
            return [1]
        elif self.color == 'blue':
            return [1]
        elif self.color == 'green':
            return [-1]
        elif self.color == 'yellow':
            return [-1]
        
        return [1]
    
    def copy(self):
        new_piece = Piece(self.color, self.row, self.col)
        new_piece.is_king = self.is_king
        return new_piece
    
    def __repr__(self):
        king_str = "K" if self.is_king else ""
        return f"{self.color[0].upper()}{king_str}({self.row},{self.col})"
