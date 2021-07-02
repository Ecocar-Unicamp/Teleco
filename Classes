
# Classe das checkboxes
# Escrito por Nuno em 02/07/2021

class Check_box:
    def __init__(self, main_color, secondary_color, x, y, size=20, state=False):
        self.main_color = main_color
        self.secondary_color = secondary_color
        self.color = main_color
        self.x = x
        self.y = y
        self.size = size
        self.state = state

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.size + 4, self.size + 4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 0)
        font = pygame.font.SysFont('freesansbold.ttf', int(1.5 * self.size))
        if self.state:
            text = font.render("X", True, (0, 0, 0))
            win.blit(text, (self.x + (self.size / 2 - text.get_width() / 2), self.y + (self.size / 2 - text.get_height() / 2)))
        else:
            text = font.render("", True, (0, 0, 0))
            win.blit(text, (self.x + (self.size / 2 - text.get_width() / 2), self.y + (self.size / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.size:
            if self.y < pos[1] < self.y + self.size:
                self.color = self.secondary_color
                return True
        self.color = self.main_color
        return False
