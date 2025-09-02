import pygame
import random
import math
from collections import deque

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
REWIND_DURATION = 3  # seconds to rewind


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

class Player:
    """Player character with jumping and collision detection"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.vel_y = 0
        self.on_ground = False
        self.ground_y = SCREEN_HEIGHT - 100
        
    def update(self):
        """Update player physics and position"""
        # Apply gravity
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # Ground collision
        if self.y >= self.ground_y - self.radius * 2:
            self.y = self.ground_y - self.radius * 2
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
    
    def jump(self):
        """Make player jump if on ground"""
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
    
    def draw(self, screen):
        """Draw player as blue circle"""
        pygame.draw.circle(screen, BLUE, (int(self.x + self.radius), int(self.y + self.radius)), self.radius)

class Obstacle:
    """Obstacle that moves from right to left"""
    
    def __init__(self, x, y, width=30, height=60):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = PLAYER_SPEED
        
    def update(self):
        """Move obstacle left"""
        self.x -= self.speed
        
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        """Draw obstacle as red rectangle"""
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

class GameState:
    """Stores game state for time rewind functionality"""
    
    def __init__(self, player_x, player_y, player_vel_y, obstacles, score):
        self.player_x = player_x
        self.player_y = player_y
        self.player_vel_y = player_vel_y
        self.obstacles = [{'x': obs.x, 'y': obs.y, 'width': obs.width, 'height': obs.height} for obs in obstacles]
        self.score = score

class TimeLoopRunner:
    """Main game class handling all game logic"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Time Loop Runner")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.player = Player(100, SCREEN_HEIGHT - 140)
        self.obstacles = []
        
        # Game state
        self.score = 0
        self.running = True
        self.game_over = False
        
        # Time rewind system
        self.state_history = deque(maxlen=FPS * REWIND_DURATION)  # Store 3 seconds of states
        self.rewind_active = False
        self.rewind_states = []
        self.rewind_index = 0
        
        # Obstacle spawning
        self.obstacle_timer = 0
        self.obstacle_spawn_rate = 120  # frames between spawns
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        
    def save_state(self):
        """Save current game state for potential rewind"""
        state = GameState(
            self.player.x, self.player.y, self.player.vel_y,
            self.obstacles.copy(), self.score
        )
        self.state_history.append(state)
    
    def start_rewind(self):
        """Initialize rewind sequence"""
        if len(self.state_history) > 0:
            self.rewind_active = True
            self.rewind_states = list(self.state_history)
            self.rewind_index = len(self.rewind_states) - 1
    
    def update_rewind(self):
        """Update rewind animation"""
        if self.rewind_index >= 0:
            state = self.rewind_states[self.rewind_index]
            
            # Restore player state
            self.player.x = state.player_x
            self.player.y = state.player_y
            self.player.vel_y = state.player_vel_y
            
            # Restore obstacles (but keep them for learning)
            self.obstacles.clear()
            for obs_data in state.obstacles:
                obstacle = Obstacle(obs_data['x'], obs_data['y'], obs_data['width'], obs_data['height'])
                self.obstacles.append(obstacle)
            
            self.score = state.score
            self.rewind_index -= 2  # Rewind speed
        else:
            # Rewind complete
            self.rewind_active = False
            self.state_history.clear()
    
    def spawn_obstacle(self):
        """Spawn new obstacle at random height"""
        ground_y = SCREEN_HEIGHT - 100
        # Random obstacle type
        if random.random() < 0.7:  # Ground obstacle
            obstacle = Obstacle(SCREEN_WIDTH, ground_y - 60, 30, 60)
        else:  # Floating obstacle
            obstacle = Obstacle(SCREEN_WIDTH, ground_y - 150, 40, 30)
        
        self.obstacles.append(obstacle)
    
    def check_collisions(self):
        """Check if player collides with any obstacle"""
        player_rect = self.player.get_rect()
        
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.get_rect()):
                return True
        return False
    
    def update_game(self):
        """Update all game objects and logic"""
        if self.rewind_active:
            self.update_rewind()
            return
        
        # Save current state for potential rewind
        self.save_state()
        
        # Update player
        self.player.update()
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update()
            # Remove obstacles that are off screen
            if obstacle.x < -obstacle.width:
                self.obstacles.remove(obstacle)
        
        # Spawn new obstacles
        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_spawn_rate:
            self.spawn_obstacle()
            self.obstacle_timer = 0
            # Gradually increase difficulty
            if self.obstacle_spawn_rate > 60:
                self.obstacle_spawn_rate -= 1
        
        # Update score (distance traveled)
        self.score += 1
        
        # Check collisions
        if self.check_collisions():
            self.start_rewind()
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.rewind_active:
                        self.player.jump()
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
    
    def restart_game(self):
        """Reset game to initial state"""
        self.player = Player(100, SCREEN_HEIGHT - 140)
        self.obstacles.clear()
        self.score = 0
        self.game_over = False
        self.state_history.clear()
        self.rewind_active = False
        self.obstacle_timer = 0
        self.obstacle_spawn_rate = 120
    
    def draw_game(self):
        """Render all game objects"""
        # Clear screen
        self.screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Draw rewind indicator
        if self.rewind_active:
            rewind_text = self.font.render("REWINDING TIME...", True, YELLOW)
            text_rect = rewind_text.get_rect(center=(SCREEN_WIDTH//2, 50))
            self.screen.blit(rewind_text, text_rect)
        
        # Draw instructions
        if self.score < 100:  # Show instructions for new players
            instruction_text = self.font.render("SPACE to Jump - Collisions rewind time!", True, BLACK)
            text_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
            self.screen.blit(instruction_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update_game()
            self.draw_game()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    """Entry point for the game"""
    try:
        game = TimeLoopRunner()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Game error: {e}")
        raise

# Run the game
if __name__ == "__main__":
    main()
