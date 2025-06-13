import pygame
from settings import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe Game")

        self.font = pygame.font.Font(None, 70)  # For X/O symbols
        self.font2 = pygame.font.Font(None, 36)  # For status messages
        
        self.initialize_game()
        
    def initialize_game(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'  # X goes first
        self.game_over = False
        self.winner = None
        
    def handle_click(self, pos):
        if self.game_over:
            return
            
        x, y = pos
        col = (x - OFFSET_X // 2) // CELL_SIZE
        row = (y - OFFSET_Y // 2) // CELL_SIZE
        
        # Check if click is within board and cell is empty
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] is None:
            self.board[row][col] = self.current_player
            
            # Check for win or draw
            if self.check_win(self.current_player):
                self.game_over = True
                self.winner = self.current_player
            elif self.is_draw():
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def check_win(self, player):
        # rows
        for row in range(BOARD_SIZE):
            if all(self.board[row][col] == player for col in range(BOARD_SIZE)):
                return True
        
        # columns
        for col in range(BOARD_SIZE):
            if all(self.board[row][col] == player for row in range(BOARD_SIZE)):
                return True
        
        # diagonals
        if all(self.board[i][i] == player for i in range(BOARD_SIZE)):
            return True
        if all(self.board[i][BOARD_SIZE-1-i] == player for i in range(BOARD_SIZE)):
            return True
            
        return False
    
    def is_draw(self):
        return all(self.board[row][col] is not None 
                   for row in range(BOARD_SIZE) 
                   for col in range(BOARD_SIZE))
    
    def draw_board(self):
        # Draw grid lines
        for i in range(1, BOARD_SIZE):
            # Vertical lines
            pygame.draw.line(
                self.display, BLACK,
                (OFFSET_X // 2 + i * CELL_SIZE, OFFSET_Y // 2),
                (OFFSET_X // 2 + i * CELL_SIZE, HEIGHT - OFFSET_Y // 2),
                LINE_WIDTH
            )
            # Horizontal lines
            pygame.draw.line(
                self.display, BLACK,
                (OFFSET_X // 2, OFFSET_Y // 2 + i * CELL_SIZE),
                (WIDTH - OFFSET_X // 2, OFFSET_Y // 2 + i * CELL_SIZE),
                LINE_WIDTH
            )
        
        # Draw X's and O's
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is not None:
                    x = col * CELL_SIZE + OFFSET_X // 2 + CELL_SIZE // 2
                    y = row * CELL_SIZE + OFFSET_Y // 2 + CELL_SIZE // 2
                    
                    text = self.font.render(self.board[row][col], True, BLACK)
                    text_rect = text.get_rect(center=(x, y))
                    self.display.blit(text, text_rect)
    
    def draw_status(self):
        if self.game_over:
            if self.winner:
                message = f"Player {self.winner} wins! Click to play again."
            else:
                message = "Game ended in a draw! Click to play again."
        else:
            message = f"Player {self.current_player}'s turn"
            
        text = self.font2.render(message, True, BLACK)
        self.display.blit(text, (WIDTH // 2 - text.get_width() // 2, OFFSET_Y // 4))
    
    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.game_over:
                            self.initialize_game()  # Restart game
                        else:
                            self.handle_click(event.pos)
            
            # Drawing
            self.display.fill(WHITE)
            self.draw_board()
            self.draw_status()
            pygame.display.update()


def main():
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()