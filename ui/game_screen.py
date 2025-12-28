import pygame
from ui.colors import (
    BACKGROUND, BOARD_LIGHT, BOARD_DARK, WHITE, GRAY, DARK_GRAY,
    RED, RED_KING, BLACK, BLACK_KING,
    BLUE, BLUE_KING, GREEN, GREEN_KING, YELLOW, YELLOW_KING,
    HIGHLIGHT_SELECTED, HIGHLIGHT_VALID, HIGHLIGHT_CAPTURE,
    TEXT_TITLE, TEXT_DESCRIPTION, TEXT_ACCENT
)


class GameScreen:
    
    def __init__(self, screen_width, screen_height, board_size=8):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_size = board_size
        
        self.margin = 60
        self.info_height = 80
        available_size = min(
            screen_width - 2 * self.margin,
            screen_height - self.info_height - 2 * self.margin
        )
        self.square_size = available_size // board_size
        self.board_pixel_size = self.square_size * board_size
        
        self.board_x = (screen_width - self.board_pixel_size) // 2
        self.board_y = self.info_height + (screen_height - self.info_height - self.board_pixel_size) // 2
        
        self.title_font = None
        self.info_font = None
        self.button_font = None
        
        self.piece_colors = {
            'red': (RED, RED_KING),
            'black': (BLACK, BLACK_KING),
            'blue': (BLUE, BLUE_KING),
            'green': (GREEN, GREEN_KING),
            'yellow': (YELLOW, YELLOW_KING)
        }
    
    def _init_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 48)
            self.info_font = pygame.font.Font(None, 36)
            self.button_font = pygame.font.Font(None, 32)
    
    def get_square_from_mouse(self, mouse_pos):
        x, y = mouse_pos
        
        if x < self.board_x or x >= self.board_x + self.board_pixel_size:
            return None
        if y < self.board_y or y >= self.board_y + self.board_pixel_size:
            return None
        
        col = (x - self.board_x) // self.square_size
        row = (y - self.board_y) // self.square_size
        
        return (row, col)
    
    def draw(self, screen, board, current_player, selected_piece=None, 
             valid_moves=None, game_mode='classic', is_four_player=False):
        self._init_fonts()
        
        screen.fill(BACKGROUND)
        self._draw_info_bar(screen, current_player, is_four_player)
        self._draw_board(screen, board, is_four_player)
        
        if valid_moves:
            self._draw_valid_moves(screen, valid_moves)
        
        self._draw_pieces(screen, board)
        
        if selected_piece:
            self._draw_selected_highlight(screen, selected_piece)
        
        hint_font = pygame.font.Font(None, 24)
        hint_text = hint_font.render("Press ESC for menu", True, GRAY)
        screen.blit(hint_text, (10, self.screen_height - 30))
    
    def _draw_info_bar(self, screen, current_player, is_four_player):
        player_text = f"Current Turn: {current_player.upper()}"
        if current_player == 'red':
            player_text += " (You)"
        else:
            player_text += " (CPU)"
        
        text_surface = self.info_font.render(player_text, True, TEXT_TITLE)
        text_rect = text_surface.get_rect(centerx=self.screen_width // 2, y=20)
        screen.blit(text_surface, text_rect)
        
        color = self.piece_colors.get(current_player, (GRAY, GRAY))[0]
        indicator_rect = pygame.Rect(text_rect.right + 15, 22, 25, 25)
        pygame.draw.circle(screen, color, indicator_rect.center, 12)
        pygame.draw.circle(screen, WHITE, indicator_rect.center, 12, 2)
    
    def _draw_board(self, screen, board, is_four_player):
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.board_x + col * self.square_size
                y = self.board_y + row * self.square_size
                
                if is_four_player and not board.is_valid_square(row, col):
                    pygame.draw.rect(screen, BACKGROUND, 
                                   (x, y, self.square_size, self.square_size))
                    continue
                
                if (row + col) % 2 == 0:
                    color = BOARD_LIGHT
                else:
                    color = BOARD_DARK
                
                pygame.draw.rect(screen, color, 
                               (x, y, self.square_size, self.square_size))
        
        pygame.draw.rect(screen, DARK_GRAY,
                        (self.board_x - 3, self.board_y - 3,
                         self.board_pixel_size + 6, self.board_pixel_size + 6), 3)
    
    def _draw_pieces(self, screen, board):
        for color, pieces in board.pieces.items():
            for piece in pieces:
                self._draw_piece(screen, piece)
    
    def _draw_piece(self, screen, piece):
        x = self.board_x + piece.col * self.square_size + self.square_size // 2
        y = self.board_y + piece.row * self.square_size + self.square_size // 2
        radius = self.square_size // 2 - 8
        
        normal_color, king_color = self.piece_colors.get(piece.color, (GRAY, GRAY))
        color = king_color if piece.is_king else normal_color
        
        pygame.draw.circle(screen, (20, 20, 20), (x + 3, y + 3), radius)
        pygame.draw.circle(screen, color, (x, y), radius)
        pygame.draw.circle(screen, WHITE, (x, y), radius, 2)
        
        if piece.is_king:
            crown_font = pygame.font.Font(None, int(radius * 1.2))
            crown_text = crown_font.render("♔", True, WHITE)
            crown_rect = crown_text.get_rect(center=(x, y))
            screen.blit(crown_text, crown_rect)
    
    def _draw_selected_highlight(self, screen, piece):
        x = self.board_x + piece.col * self.square_size
        y = self.board_y + piece.row * self.square_size
        
        highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        highlight.fill(HIGHLIGHT_SELECTED)
        screen.blit(highlight, (x, y))
        
        pygame.draw.rect(screen, (100, 200, 100), 
                        (x, y, self.square_size, self.square_size), 3)
    
    def _draw_valid_moves(self, screen, valid_moves):
        for (row, col), captured in valid_moves.items():
            x = self.board_x + col * self.square_size
            y = self.board_y + row * self.square_size
            
            if captured:
                color = HIGHLIGHT_CAPTURE
            else:
                color = HIGHLIGHT_VALID
            
            highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            highlight.fill(color)
            screen.blit(highlight, (x, y))
            
            center_x = x + self.square_size // 2
            center_y = y + self.square_size // 2
            dot_color = (255, 100, 100) if captured else (100, 150, 255)
            pygame.draw.circle(screen, dot_color, (center_x, center_y), 10)
    
    def draw_game_over(self, screen, winner, is_player_win):
        self._init_fonts()
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        if winner is None:
            title = "DRAW!"
            subtitle = "No moves remaining"
        elif is_player_win:
            title = "YOU WIN!"
            subtitle = f"Congratulations!"
        else:
            title = "GAME OVER"
            subtitle = f"{winner.upper()} wins!"
        
        title_surface = self.title_font.render(title, True, TEXT_ACCENT)
        title_rect = title_surface.get_rect(centerx=self.screen_width // 2, 
                                           centery=self.screen_height // 2 - 50)
        screen.blit(title_surface, title_rect)
        
        subtitle_surface = self.info_font.render(subtitle, True, TEXT_DESCRIPTION)
        subtitle_rect = subtitle_surface.get_rect(centerx=self.screen_width // 2,
                                                  centery=self.screen_height // 2 + 10)
        screen.blit(subtitle_surface, subtitle_rect)
        
        button_y = self.screen_height // 2 + 80
        
        restart_rect = pygame.Rect(self.screen_width // 2 - 180, button_y, 150, 45)
        pygame.draw.rect(screen, DARK_GRAY, restart_rect, border_radius=8)
        pygame.draw.rect(screen, TEXT_ACCENT, restart_rect, 2, border_radius=8)
        restart_text = self.button_font.render("Play Again", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)
        screen.blit(restart_text, restart_text_rect)
        
        menu_rect = pygame.Rect(self.screen_width // 2 + 30, button_y, 150, 45)
        pygame.draw.rect(screen, DARK_GRAY, menu_rect, border_radius=8)
        pygame.draw.rect(screen, GRAY, menu_rect, 2, border_radius=8)
        menu_text = self.button_font.render("Main Menu", True, WHITE)
        menu_text_rect = menu_text.get_rect(center=menu_rect.center)
        screen.blit(menu_text, menu_text_rect)
        
        return restart_rect, menu_rect
    
    def update_board_size(self, new_size):
        self.board_size = new_size
        
        available_size = min(
            self.screen_width - 2 * self.margin,
            self.screen_height - self.info_height - 2 * self.margin
        )
        self.square_size = available_size // new_size
        self.board_pixel_size = self.square_size * new_size
        
        self.board_x = (self.screen_width - self.board_pixel_size) // 2
        self.board_y = self.info_height + (self.screen_height - self.info_height - self.board_pixel_size) // 2
