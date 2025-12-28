import pygame
from ui.colors import (
    BACKGROUND, WHITE, PANEL_NORMAL, PANEL_HOVER,
    PANEL_BORDER, PANEL_BORDER_HOVER, TEXT_TITLE,
    TEXT_DESCRIPTION, TEXT_ACCENT
)


class HomeScreen:
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.panel_width = int(screen_width * 0.8)
        self.panel_height = int(screen_height * 0.25)
        self.panel_spacing = 40
        
        panel_x = (screen_width - self.panel_width) // 2
        total_height = 2 * self.panel_height + self.panel_spacing
        start_y = (screen_height - total_height) // 2 + 60
        
        self.classic_panel = pygame.Rect(
            panel_x, start_y,
            self.panel_width, self.panel_height
        )
        self.four_player_panel = pygame.Rect(
            panel_x, start_y + self.panel_height + self.panel_spacing,
            self.panel_width, self.panel_height
        )
        
        self.hovered_panel = None
        
        self.title_font = None
        self.label_font = None
        self.desc_font = None
    
    def _init_fonts(self):
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 72)
            self.label_font = pygame.font.Font(None, 48)
            self.desc_font = pygame.font.Font(None, 32)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            if self.classic_panel.collidepoint(mouse_pos):
                self.hovered_panel = 'classic'
            elif self.four_player_panel.collidepoint(mouse_pos):
                self.hovered_panel = 'four_player'
            else:
                self.hovered_panel = None
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.classic_panel.collidepoint(mouse_pos):
                    return 'classic'
                elif self.four_player_panel.collidepoint(mouse_pos):
                    return 'four_player'
        
        return None
    
    def draw(self, screen):
        self._init_fonts()
        
        screen.fill(BACKGROUND)
        
        title_text = self.title_font.render("CHECKERS", True, TEXT_TITLE)
        title_rect = title_text.get_rect(centerx=self.screen_width // 2, y=40)
        screen.blit(title_text, title_rect)
        
        subtitle_text = self.desc_font.render("Select a game mode to play", True, TEXT_DESCRIPTION)
        subtitle_rect = subtitle_text.get_rect(centerx=self.screen_width // 2, y=110)
        screen.blit(subtitle_text, subtitle_rect)
        
        self._draw_panel(
            screen,
            self.classic_panel,
            "Classic Checkers — 1 vs AI",
            "Standard checkers against a computer opponent",
            self.hovered_panel == 'classic'
        )
        
        self._draw_panel(
            screen,
            self.four_player_panel,
            "Four Player Checkers — 1 vs 3 CPUs",
            "Expanded board with three AI opponents",
            self.hovered_panel == 'four_player'
        )
    
    def _draw_panel(self, screen, rect, title, description, is_hovered):
        if is_hovered:
            bg_color = PANEL_HOVER
            border_color = PANEL_BORDER_HOVER
            border_width = 4
        else:
            bg_color = PANEL_NORMAL
            border_color = PANEL_BORDER
            border_width = 2
        
        pygame.draw.rect(screen, bg_color, rect, border_radius=12)
        pygame.draw.rect(screen, border_color, rect, border_width, border_radius=12)
        
        title_surface = self.label_font.render(title, True, TEXT_ACCENT if is_hovered else TEXT_TITLE)
        title_rect = title_surface.get_rect(centerx=rect.centerx, centery=rect.centery - 20)
        screen.blit(title_surface, title_rect)
        
        desc_surface = self.desc_font.render(description, True, TEXT_DESCRIPTION)
        desc_rect = desc_surface.get_rect(centerx=rect.centerx, centery=rect.centery + 30)
        screen.blit(desc_surface, desc_rect)
        
        if is_hovered:
            hint_font = pygame.font.Font(None, 24)
            hint_surface = hint_font.render("Click to play", True, TEXT_ACCENT)
            hint_rect = hint_surface.get_rect(centerx=rect.centerx, bottom=rect.bottom - 15)
            screen.blit(hint_surface, hint_rect)
