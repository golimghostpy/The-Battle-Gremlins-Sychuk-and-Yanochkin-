import pygame
import os
import sys
from mechanics import *

#  conditions
A, B, C = 1, 2, 3
class Display:
    def __init__(self):
        self.condition = A
        self.width = 754
        self.height = 432
        self.screen = None
        self.running = False
        self.field = None
        self.clock = None  # pygame.time.Clock()

    def build(self):
        pygame.init()
        pygame.display.set_caption('The Battle Gremlins')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))
        self.main_cycle()

    #  pygame.display.flip()

    def draw_A(self):
        self.screen.blit(self.load_image('menu_background.png', None), (0, 0))
        self.screen.blit(self.load_image('title.png'), (self.width // 2 - 247, self.height // 5))
        self.screen.blit(self.load_image('start_button.png'), (self.width // 2 - 118, self.height // 5 * 2))
        self.screen.blit(self.load_image('gremlins_menu.png'), (self.width // 2 - 86, self.height // 5 * 3))
        self.screen.blit(self.load_image('quit.png'), (self.width // 2 - 45, self.height // 5 * 4))

    def move_from_A_to_B(self, event):
        x, y = event.pos
        if (self.width // 2 - 118 <= x <= self.width // 2 + 118 and
                self.height // 5 * 2 <= y <= self.height // 5 * 2 + 56):
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 2 - 120, self.height // 5 * 2, 236, 56), 2)
            self.condition = B
            return True
        return False

    def move_from_A_to_C(self, event):
        x, y = event.pos
        if (self.width // 2 - 86 <= x <= self.width // 2 + 86 and
                self.height // 5 * 3 <= y <= self.height // 5 * 3 + 53):
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 2 - 88, self.height // 5 * 3, 172, 53), 2)
            self.condition = C
            return True
        return False

    def leave_game_from_A(self, event):
        x, y = event.pos
        if (self.width // 2 - 45 <= x <= self.width // 2 + 45 and
                self.height // 5 * 4 <= y <= self.height // 5 * 4 + 53):
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 2 - 47, self.height // 5 * 4, 90, 53), 2)
            self.running = False
            return True
        return False

    def position_A(self, event):
        self.draw_A()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.move_from_A_to_B(event):
                return
            elif self.move_from_A_to_C(event):
                return
            elif self.leave_game_from_A(event):
                return


    def draw_B(self):
        self.screen.blit(self.load_image('menu_background.png', None), (0, 0))
        self.screen.blit(self.load_image('levels_txt.png'), (self.width // 2 - 100, 20))
        self.screen.blit(self.load_image('level_1.png'), (self.width // 5 - 110, self.height // 4))
        self.screen.blit(self.load_image('level_2.png'), (self.width // 5 * 2 - 110, self.height // 4))
        self.screen.blit(self.load_image('level_3.png'), (self.width // 5 * 3 - 110, self.height // 4))
        self.screen.blit(self.load_image('level_4.png'), (self.width // 5 * 4 - 110, self.height // 4))
        self.screen.blit(self.load_image('level_5.png'), (self.width - 110, self.height // 4))
        self.screen.blit(self.load_image('back_btn.png'), (self.width // 2 - 83, 330))

    def position_B(self, event):
        self.draw_B()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if (self.width // 2 - 83 <= x <= self.width // 2 + 83 and
                    330 <= y <= 410):
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (self.width // 2 - 83, 330, 166, 80), 2)
                self.condition = A

    def draw_C(self):
        self.screen.blit(self.load_image('menu_background.png', None), (0, 0))
        self.screen.blit(self.load_image('back_btn.png'), (self.width // 2 - 83, 330))

    def position_C(self, event):
        self.draw_C()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if (self.width // 2 - 83 <= x <= self.width // 2 + 83 and
                    330 <= y <= 410):
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (self.width // 2 - 83, 330, 166, 80), 2)
                self.condition = A

    def main_cycle(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue
                if self.condition == A:
                    self.position_A(event)
                elif self.condition == B:
                    self.position_B(event)
                elif self.condition == C:
                    self.position_C(event)
            pygame.display.flip()
        pygame.quit()

    def load_image(self, name, colorkey=-1):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image


def main():
    display = Display()
    display.build()


if __name__ == '__main__':
    main()