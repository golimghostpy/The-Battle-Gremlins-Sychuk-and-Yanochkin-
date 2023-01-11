import pygame
import os
import sys
from mechanics import *

#  conditions
MAIN, LEVELS, UNITS, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, END_SCREEN = 1, 2, 3, 4, 5, 6, 7, 8, 9
SCHEDULES = {
    LEVEL_1: [],
    LEVEL_2: [],
    LEVEL_3: [],
    LEVEL_4: [],
    LEVEL_5: []
}

class Display:
    def __init__(self):
        self.condition = MAIN
        self.width = 754
        self.height = 432
        self.screen = None
        self.running = False
        self.field = None
        self.clock = None  # pygame.time.Clock()
        self.paused = False

    def build(self):
        pygame.init()
        pygame.display.set_caption('The Battle Gremlins')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))
        self.main_cycle()

    #  pygame.display.flip()

    def draw_MAIN(self):
        self.screen.blit(self.load_image('menu_background.png', None), (0, 0))
        self.screen.blit(self.load_image('MAIN/title.png'), (self.width // 2 - 247, self.height // 5))
        self.screen.blit(self.load_image('MAIN/start_button.png'), (self.width // 2 - 118, self.height // 5 * 2))
        self.screen.blit(self.load_image('MAIN/gremlins_menu.png'), (self.width // 2 - 86, self.height // 5 * 3))
        self.screen.blit(self.load_image('MAIN/quit.png'), (self.width // 2 - 45, self.height // 5 * 4))

    def move_from_MAIN_to_LEVELS(self, event):
        x, y = event.pos
        if self.width // 2 - 118 <= x <= self.width // 2 + 118 and \
                self.height // 5 * 2 <= y <= self.height // 5 * 2 + 56:
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 2 - 120, self.height // 5 * 2, 236, 56), 2)
            self.condition = LEVELS
            return True
        return False

    def move_from_MAIN_to_UNITS(self, event):
        x, y = event.pos
        if self.width // 2 - 86 <= x <= self.width // 2 + 86 and \
                self.height // 5 * 3 <= y <= self.height // 5 * 3 + 53:
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 2 - 88, self.height // 5 * 3, 172, 53), 2)
            self.condition = UNITS
            return True
        return False

    def leave_game_from_MAIN(self, event):
        x, y = event.pos
        if self.width // 2 - 45 <= x <= self.width // 2 + 45 and \
                self.height // 5 * 4 <= y <= self.height // 5 * 4 + 53:
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 2 - 47, self.height // 5 * 4, 90, 53), 2)
            self.running = False
            return True
        return False

    def position_MAIN(self, event):
        self.draw_MAIN()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.move_from_MAIN_to_LEVELS(event):
                return
            elif self.move_from_MAIN_to_UNITS(event):
                return
            elif self.leave_game_from_MAIN(event):
                return


    def draw_LEVELS(self):
        self.screen.blit(self.load_image('menu_background.png', None), (0, 0))
        self.screen.blit(self.load_image('LEVELS/levels_txt.png'), (self.width // 2 - 100, 20))
        self.screen.blit(self.load_image('LEVELS/level_1.png'), (self.width // 5 - 110, self.height // 4))
        self.screen.blit(self.load_image('LEVELS/level_2.png'), (self.width // 5 * 2 - 110, self.height // 4))
        self.screen.blit(self.load_image('LEVELS/level_3.png'), (self.width // 5 * 3 - 110, self.height // 4))
        self.screen.blit(self.load_image('LEVELS/level_4.png'), (self.width // 5 * 4 - 110, self.height // 4))
        self.screen.blit(self.load_image('LEVELS/level_5.png'), (self.width - 110, self.height // 4))
        self.screen.blit(self.load_image('back_btn.png'), (self.width // 2 - 83, 330))

    def starting_LEVEL(self):
        self.clock = pygame.time.Clock()
        self.field = Field(SCHEDULES[self.condition])
        Tower(1, 1500, '', self.field).put(0)
        Tower(-1, 1500, '', self.field).put(0)

    def finish_LEVEL(self):
        self.clock = None
        self.field = None

    def position_LEVELS(self, event):
        self.draw_LEVELS()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.width // 2 - 83 <= x <= self.width // 2 + 83 and \
                    330 <= y <= 410:
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (self.width // 2 - 83, 330, 166, 80), 2)
                self.condition = MAIN
            elif self.move_from_LEVELS_to_START(event) == LEVEL_1:
                self.starting_LEVEL()
                return

    def draw_UNITS(self):
        self.screen.blit(self.load_image('menu_background.png', None), (0, 0))
        self.screen.blit(self.load_image('back_btn.png'), (self.width // 2 - 83, 330))

    def position_UNITS(self, event):
        self.draw_UNITS()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.width // 2 - 83 <= x <= self.width // 2 + 83 and \
                    330 <= y <= 410:
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (self.width // 2 - 83, 330, 166, 80), 2)
                self.condition = MAIN

    def move_from_LEVELS_to_START(self, event):
        x, y = event.pos
        if self.width // 5 - 110 <= x <= self.width // 5 - 30 and self.height // 4 <= y <= self.height // 4 + 80:
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 5 - 110, self.height // 4, 84, 84), 2)
            self.condition = LEVEL_1
            return LEVEL_1
        elif 1 <= x <= 1 and 1 <= y <= 1:

            self.condition = LEVEL_2
            return LEVEL_2
        elif 1 <= x <= 1 and 1 <= y <= 1:

            self.condition = LEVEL_3
            return LEVEL_3
        elif 1 <= x <= 1 and 1 <= y <= 1:

            self.condition = LEVEL_4
            return LEVEL_4
        elif 1 <= x <= 1 and 1 <= y <= 1:

            self.condition = LEVEL_5
            return LEVEL_5
        return False

    def draw_LEVEL_1(self):
        self.screen.blit(self.load_image('LEVEL_1/background_1.png', None), (0, 0))

    def position_LEVEL_1(self, event):
        self.draw_LEVEL_1()
        #  drawing units
        if self.paused:
            self.draw_pause()
            self.clock.tick()
        else:
            #
            #  freaking ton of player actions
            #
            self.field.main_cycle(self.clock.tick())
            if self.field.winner():
                self.condition = END_SCREEN

    def draw_pause(self):
        pass


    def main_cycle(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue
                if self.condition == MAIN:
                    self.position_MAIN(event)
                elif self.condition == LEVELS:
                    self.position_LEVELS(event)
                elif self.condition == UNITS:
                    self.position_UNITS(event)
                elif self.condition == LEVEL_1:
                    self.position_LEVEL_1(event)
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