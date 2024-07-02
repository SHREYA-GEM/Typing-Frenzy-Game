import pygame
import random
import string
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (215, 191, 0)
FONT_SIZE = 36
WORM_SPEED = 1
FIRELFY_INTERVAL = 3000
MAX_LIVES = 3
GAME_DURATION = 60000  # 60 seconds

# Load assets and apply blur to background images
bg_forest = pygame.image.load("forest_background.jpg")
bg_forest_blurred = pygame.transform.smoothscale(bg_forest, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_garden = pygame.image.load("forest_background.jpg")
bg_garden_blurred = pygame.transform.smoothscale(bg_garden, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_night_sky = pygame.image.load("forest_background.jpg")
bg_night_sky_blurred = pygame.transform.smoothscale(bg_night_sky, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load worm image and resize
worm_image = pygame.image.load("worm.png")
worm_image = pygame.transform.scale(worm_image, (100, 90))  # Resizing worm image

music_forest = "forest_music.mp3"
music_garden = "garden_music.mp3"
music_night_sky = "night_sky_music.mp3"

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Speed Test Game")

# Load fonts
font = pygame.font.Font(None, FONT_SIZE)

# Firefly class
class Firefly:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter
        self.rect = pygame.Rect(x, y, 40, 40)

    def draw(self, surface):
        text = font.render(self.letter, True, BLACK)
        surface.blit(text, (self.x, self.y))

    def move(self):
        pass  # Fireflies don't move

# Worm class
class Worm:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def move_towards(self, target_x, target_y):
        # Calculate direction vector
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            # Normalize direction vector
            dx /= distance
            dy /= distance

        # Adjust speed based on direction towards the target
        self.x += dx * WORM_SPEED
        self.y += dy * WORM_SPEED

# Function to choose theme
def choose_theme(theme):
    if theme == "forest":
        bg_image = bg_forest_blurred
        bg_music = music_forest
    elif theme == "garden":
        bg_image = bg_garden_blurred
        bg_music = music_garden
    else:
        bg_image = bg_night_sky_blurred
        bg_music = music_night_sky
    return bg_image, bg_music

# Function to display game over message with play again option
def show_game_over(message):
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
        pygame.time.delay(10)  # Small delay to avoid high CPU usage

# Game loop
def main():
    # Choose theme
    theme = "forest"  # Change theme here
    bg_image, bg_music = choose_theme(theme)

    # Load and play background music
    pygame.mixer.music.load(bg_music)
    pygame.mixer.music.play(-1)  # Loop music

    clock = pygame.time.Clock()
    score = 0
    lives = MAX_LIVES
    fireflies = []
    worms = []
    running = True
    last_firefly_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()

    while running:
        screen.blit(bg_image, (0, 0))

        # Display lives and score
        lives_text = font.render(f"LIVES: {lives}", True, BLACK)
        score_text = font.render(f"SCORE: {score}", True, BLACK)
        screen.blit(lives_text, (SCREEN_WIDTH - 150, 50))
        screen.blit(score_text, (SCREEN_WIDTH - 150, 100))

        # Check game time
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= GAME_DURATION:
            running = False
            if show_game_over("Time's up! Press Enter to play again."):
                return  # Restart the game

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for firefly in fireflies:
                    if event.unicode == firefly.letter:
                        fireflies.remove(firefly)
                        score += 1
                        break

        # Add new firefly
        if current_time - last_firefly_time > FIRELFY_INTERVAL:
            x = random.randint(0, SCREEN_WIDTH - 40)
            y = random.randint(0, SCREEN_HEIGHT - 40)
            letter = random.choice(string.ascii_lowercase)
            fireflies.append(Firefly(x, y, letter))
            worms.append(Worm(0, y, worm_image))
            last_firefly_time = current_time

        # Update and draw fireflies and worms
        for worm, firefly in zip(worms, fireflies):
            worm.move_towards(firefly.x, firefly.y)
            worm.draw(screen)

        for firefly in fireflies:
            firefly.draw(screen)

        # Check if any worm has reached a firefly
        for worm in worms[:]:
            for firefly in fireflies[:]:
                if math.sqrt((worm.x - firefly.x)**2 + (worm.y - firefly.y)**2) < 10:
                    fireflies.remove(firefly)
                    worms.remove(worm)
                    lives -= 1
                    if lives <= 0:
                        running = False
                        if show_game_over("No lives left! Press Enter to play again."):
                            return  # Restart the game

        # Update display and tick clock
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
