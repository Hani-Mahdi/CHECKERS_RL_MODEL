import pygame
import sys

from ui.home_screen import HomeScreen
from ui.game_screen import GameScreen
from ui.colors import BACKGROUND
from game.board import Board
from game.rules import Rules
from ai.q_learning import QLearningAI


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60


class CheckersGame:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Checkers")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.state = 'HOME'
        self.game_mode = None
        
        self.home_screen = HomeScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.game_screen = None
        
        self.board = None
        self.rules = None
        self.players = []
        self.current_player_index = 0
        self.ai_players = {}
        
        self.selected_piece = None
        self.valid_moves = {}
        
        self.winner = None
        self.restart_button = None
        self.menu_button = None
        
        self.ai_delay = 500
        self.ai_move_time = 0
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self._handle_event(event)
            
            self._update()
            self._draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def _handle_event(self, event):
        if self.state == 'HOME':
            self._handle_home_event(event)
        elif self.state == 'PLAYING':
            self._handle_game_event(event)
        elif self.state == 'GAME_OVER':
            self._handle_game_over_event(event)
    
    def _handle_home_event(self, event):
        result = self.home_screen.handle_event(event)
        
        if result == 'classic':
            self._start_game('classic')
        elif result == 'four_player':
            self._start_game('four_player')
    
    def _handle_game_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = 'HOME'
                return
        
        current_player = self.players[self.current_player_index]
        if current_player != 'red':
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_player_click(event.pos)
    
    def _handle_player_click(self, mouse_pos):
        square = self.game_screen.get_square_from_mouse(mouse_pos)
        
        if square is None:
            return
        
        row, col = square
        clicked_piece = self.board.get_piece(row, col)
        
        if self.selected_piece and (row, col) in self.valid_moves:
            captured = self.valid_moves[(row, col)]
            was_king = self.selected_piece.is_king
            
            self.rules.execute_move(self.selected_piece, (row, col), captured)
            
            became_king = not was_king and self.selected_piece.is_king
            
            self._process_move_result(captured, became_king)
            
            self.selected_piece = None
            self.valid_moves = {}
            self._next_turn()
        
        elif clicked_piece and clicked_piece.color == 'red':
            self.selected_piece = clicked_piece
            self.valid_moves = self.rules.get_valid_moves(clicked_piece)
            
            if self.rules.has_captures('red'):
                if not any(self.valid_moves.values()):
                    self.valid_moves = {}
        
        else:
            self.selected_piece = None
            self.valid_moves = {}
    
    def _handle_game_over_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            if self.restart_button and self.restart_button.collidepoint(mouse_pos):
                self._start_game(self.game_mode)
            elif self.menu_button and self.menu_button.collidepoint(mouse_pos):
                self.state = 'HOME'
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = 'HOME'
    
    def _start_game(self, mode):
        self.game_mode = mode
        self.state = 'PLAYING'
        
        if mode == 'classic':
            self.board = Board(8, 'classic')
            self.players = ['red', 'black']
            self.game_screen = GameScreen(SCREEN_WIDTH, SCREEN_HEIGHT, 8)
            
            self.ai_players = {
                'black': QLearningAI('black')
            }
        else:
            self.board = Board(12, 'four_player')
            self.players = ['red', 'blue', 'green', 'yellow']
            self.game_screen = GameScreen(SCREEN_WIDTH, SCREEN_HEIGHT, 12)
            self.game_screen.update_board_size(12)
            
            self.ai_players = {
                'blue': QLearningAI('blue'),
                'green': QLearningAI('green'),
                'yellow': QLearningAI('yellow')
            }
        
        self.rules = Rules(self.board)
        self.current_player_index = 0
        self.selected_piece = None
        self.valid_moves = {}
        self.winner = None
        self.ai_move_time = 0
        
        for ai in self.ai_players.values():
            ai.reset()
    
    def _update(self):
        if self.state != 'PLAYING':
            return
        
        game_over, winner = self.rules.is_game_over(self.players)
        if game_over:
            self.winner = winner
            self.state = 'GAME_OVER'
            return
        
        current_player = self.players[self.current_player_index]
        if current_player in self.ai_players:
            current_time = pygame.time.get_ticks()
            
            if self.ai_move_time == 0:
                self.ai_move_time = current_time + self.ai_delay
            elif current_time >= self.ai_move_time:
                self._execute_ai_turn(current_player)
                self.ai_move_time = 0
    
    def _execute_ai_turn(self, color):
        ai = self.ai_players[color]
        move = ai.choose_move(self.board, self.rules)
        
        if move is None:
            self._next_turn()
            return
        
        piece, destination, captured = move
        was_king = piece.is_king
        
        self.rules.execute_move(piece, destination, captured)
        
        became_king = not was_king and piece.is_king
        
        game_over, winner = self.rules.is_game_over(self.players)
        won = winner == color
        reward = ai.calculate_reward(captured, became_king, game_over, won)
        ai.learn(self.board, reward)
        
        self._next_turn()
    
    def _process_move_result(self, captured, became_king):
        pass
    
    def _next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        attempts = 0
        while attempts < len(self.players):
            current_player = self.players[self.current_player_index]
            pieces = self.board.get_all_pieces(current_player)
            
            if pieces:
                moves = self.rules.get_all_valid_moves(current_player)
                if moves:
                    break
            
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            attempts += 1
    
    def _draw(self):
        if self.state == 'HOME':
            self.home_screen.draw(self.screen)
        
        elif self.state == 'PLAYING':
            current_player = self.players[self.current_player_index]
            is_four_player = self.game_mode == 'four_player'
            
            self.game_screen.draw(
                self.screen,
                self.board,
                current_player,
                self.selected_piece,
                self.valid_moves,
                self.game_mode,
                is_four_player
            )
        
        elif self.state == 'GAME_OVER':
            current_player = self.players[self.current_player_index]
            is_four_player = self.game_mode == 'four_player'
            
            self.game_screen.draw(
                self.screen,
                self.board,
                current_player,
                None,
                {},
                self.game_mode,
                is_four_player
            )
            
            is_player_win = self.winner == 'red'
            self.restart_button, self.menu_button = self.game_screen.draw_game_over(
                self.screen, self.winner, is_player_win
            )


def main():
    game = CheckersGame()
    game.run()


if __name__ == '__main__':
    main()
