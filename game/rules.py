class Rules:
    
    def __init__(self, board):
        self.board = board
    
    def get_valid_moves(self, piece):
        moves = {}
        captures = self._get_captures(piece, piece.row, piece.col, [])
        
        if captures:
            for capture_path in captures:
                if capture_path:
                    final_row, final_col, captured = capture_path[-1]
                    all_captured = [c for _, _, c in capture_path]
                    moves[(final_row, final_col)] = all_captured
        else:
            moves = self._get_regular_moves(piece)
        
        return moves
    
    def _get_regular_moves(self, piece):
        moves = {}
        directions = piece.get_direction()
        
        for d_row in directions:
            for d_col in [-1, 1]:
                new_row = piece.row + d_row
                new_col = piece.col + d_col
                
                if self.board.is_valid_square(new_row, new_col):
                    if self.board.get_piece(new_row, new_col) is None:
                        moves[(new_row, new_col)] = []
        
        return moves
    
    def _get_captures(self, piece, current_row, current_col, already_captured):
        captures = []
        
        if piece.is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            row_dirs = piece.get_direction()
            directions = [(d, -1) for d in row_dirs] + [(d, 1) for d in row_dirs]
        
        for d_row, d_col in directions:
            capture_row = current_row + d_row
            capture_col = current_col + d_col
            land_row = current_row + 2 * d_row
            land_col = current_col + 2 * d_col
            
            if not self.board.is_valid_square(land_row, land_col):
                continue
            
            target = self.board.get_piece(capture_row, capture_col)
            landing = self.board.get_piece(land_row, land_col)
            
            if target is not None and target.color != piece.color:
                if target not in already_captured:
                    if landing is None or (land_row == piece.row and land_col == piece.col):
                        new_captured = already_captured + [target]
                        
                        further_captures = self._get_captures(
                            piece, land_row, land_col, new_captured
                        )
                        
                        if further_captures:
                            for path in further_captures:
                                captures.append([(land_row, land_col, target)] + path)
                        else:
                            captures.append([(land_row, land_col, target)])
        
        return captures
    
    def has_captures(self, color):
        for piece in self.board.get_all_pieces(color):
            captures = self._get_captures(piece, piece.row, piece.col, [])
            if captures:
                return True
        return False
    
    def get_all_valid_moves(self, color):
        all_moves = {}
        has_capture = self.has_captures(color)
        
        for piece in self.board.get_all_pieces(color):
            moves = self.get_valid_moves(piece)
            
            if has_capture:
                capture_moves = {k: v for k, v in moves.items() if v}
                if capture_moves:
                    all_moves[piece] = capture_moves
            else:
                if moves:
                    all_moves[piece] = moves
        
        return all_moves
    
    def is_game_over(self, colors):
        players_with_pieces = []
        players_with_moves = []
        
        for color in colors:
            pieces = self.board.get_all_pieces(color)
            if pieces:
                players_with_pieces.append(color)
                moves = self.get_all_valid_moves(color)
                if moves:
                    players_with_moves.append(color)
        
        if len(players_with_pieces) == 1:
            return True, players_with_pieces[0]
        elif len(players_with_pieces) == 0:
            return True, None
        
        if len(players_with_moves) == 1:
            return True, players_with_moves[0]
        elif len(players_with_moves) == 0:
            return True, None
        
        return False, None
    
    def execute_move(self, piece, destination, captured_pieces):
        new_row, new_col = destination
        
        for captured in captured_pieces:
            self.board.remove_piece(captured)
        
        self.board.move_piece(piece, new_row, new_col)
        
        return True
