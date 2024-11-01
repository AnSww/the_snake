import pygame
import random

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10


class Snake:
    """Класс для управления змейкой."""

    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update(self):
        """Обновление позиции змейки."""
        if self.grow:
            self.positions.append(self.positions[-1])
            self.grow = False
        else:
            self.positions.pop()

        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.positions.insert(0, new_head)

    def handle_keys(self):
        """Обработка нажатий клавиш."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT

    def update_direction(self):
        """Обновление направления змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


class Apple:
    """Класс для управления яблоком."""

    def __init__(self):
        self.position = self.spawn()

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(screen, APPLE_COLOR, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def spawn(self):
        """Появление яблока в случайной позиции."""
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))


def main():
    """Основная функция игры."""
    # Инициализация Pygame
    pygame.init()
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.handle_keys()
        snake.update_direction()
        snake.update()

        # Проверка на столкновение со яблоком
        if snake.positions[0] == apple.position:
            snake.grow = True
            apple.position = apple.spawn()  # Исправлено на правильное назначение

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
