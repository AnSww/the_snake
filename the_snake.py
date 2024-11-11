class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None):
        """Инициализирует базовые атрибуты объекта."""
        if position is None:
            position = (0, 0)  # или любое другое значение по умолчанию
        self.position = position
        self.body_color = (0, 0, 0)  # Цвет будет задан в дочерних классах

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self):
        """Инициализирует яблоко и задает его цвет."""
        super().__init__(self.randomize_position())  # передаем значение позиции в конструктор родителя
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        # Передаем начальную позицию змейки в конструктор GameObject
        super().__init__(self.positions[0])

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)
        self.last = self.positions[-1] if len(self.positions) > 1 else None
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
