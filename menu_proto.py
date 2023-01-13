import pygame
import os
import sys
from math import sin
from mechanics import *

#  conditions
LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, MAIN, LEVELS, UNITS, END_SCREEN = 1, 2, 3, 4, 5, 6, 7, 8, 9
BOSS_DIALOG = 10
#  ----------
SCHEDULES = {
    LEVEL_1: [],
    LEVEL_2: [],
    LEVEL_3: [],
    LEVEL_4: [],
    LEVEL_5: []
}
HEIGHT = 325


class Display:
    def __init__(self):
        self.condition = MAIN
        self.width = 754
        self.height = 432
        self.screen = None
        self.running = False
        self.field = None
        self.clock = pygame.time.Clock()
        self.paused = False
        self.sprites = pygame.sprite.Group()
        self.active_level = None
        self.winner_team = None

    def build(self):
        pygame.init()
        pygame.display.set_caption('The Battle Gremlins')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))
        self.main_cycle()

    def draw_MAIN(self):
        self.screen.blit(load_image('menu_background.png', None), (0, 0))
        self.screen.blit(load_image('MAIN\\title.png'), (self.width // 2 - 247, self.height // 5))
        self.screen.blit(load_image('MAIN\\start_button.png'), (self.width // 2 - 118, self.height // 5 * 2))
        self.screen.blit(load_image('MAIN\\gremlins_menu.png'), (self.width // 2 - 86, self.height // 5 * 3))
        self.screen.blit(load_image('MAIN\\quit.png'), (self.width // 2 - 45, self.height // 5 * 4))

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

    def draw_LEVELS(self):
        self.screen.blit(load_image('menu_background.png', None), (0, 0))
        self.screen.blit(load_image('LEVELS\\levels_txt.png'), (self.width // 2 - 100, 20))
        self.screen.blit(load_image('LEVELS\\level_1.png'), (self.width // 5 - 110, self.height // 4))
        self.screen.blit(load_image('LEVELS\\level_2.png'), (self.width // 5 * 2 - 110, self.height // 4))
        self.screen.blit(load_image('LEVELS\\level_3.png'), (self.width // 5 * 3 - 110, self.height // 4))
        self.screen.blit(load_image('LEVELS\\level_4.png'), (self.width // 5 * 4 - 110, self.height // 4))
        self.screen.blit(load_image('LEVELS\\level_5.png'), (self.width - 110, self.height // 4))
        self.screen.blit(load_image('back_btn.png'), (self.width // 2 - 83, 330))

    def starting_LEVEL(self):
        self.winner_team = None
        self.clock.tick()
        self.field = Field(SCHEDULES[self.condition], self.sprites)
        Gremlin_Tower_unit = Tower(1, 1500, 'Gremlin_Tower', self.field)
        Gremlin_Tower_unit.put(150)
        Human_Tower_unit = Tower(-1, 1500, 'Human_Tower', self.field)
        Human_Tower_unit.put(640)
        Unit(1, 0.1, 10, 500, 100, 'Basic_Gremlin', 1000, self.field, False).put(150)
        Unit(-1, 0.1, 10, 500, 100, 'Basic_Gremlin', 1500, self.field, False).put(550)

    def finish_LEVEL(self):
        self.field = None

    def draw_UNITS(self):
        self.screen.blit(load_image('menu_background.png', None), (0, 0))
        self.screen.blit(load_image('back_btn.png'), (self.width // 2 - 83, 330))

    def move_from_LEVELS_to_START(self, event):
        x, y = event.pos
        if self.width // 5 - 110 <= x <= self.width // 5 - 30 and self.height // 4 <= y <= self.height // 4 + 80:
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 5 - 110, self.height // 4, 84, 84), 2)
            self.condition = LEVEL_1
            return True
        elif self.width // 5 * 2 - 110 <= x <= self.width // 5 * 2 - 30 and \
                self.height // 4 <= y <= self.height // 4 + 80:
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 5 * 2 - 110, self.height // 4, 84, 84), 2)
            self.condition = LEVEL_2
            return True
        elif self.width // 5 * 3 - 110 <= x <= self.width // 5 * 3 - 30 and \
                self.height // 4 <= y <= self.height // 4 + 80:
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 5 * 3 - 110, self.height // 4, 84, 84), 2)
            self.condition = LEVEL_3
            return True
        elif self.width // 5 * 4 - 110 <= x <= self.width // 5 * 4 - 30 and \
                self.height // 4 <= y <= self.height // 4 + 80:
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width // 5 * 4 - 110, self.height // 4, 84, 84), 2)
            self.condition = LEVEL_4
            return True
        elif self.width - 110 <= x <= self.width - 30 and self.height // 4 <= y <= self.height // 4 + 80:
            pygame.draw.rect(self.screen, pygame.Color('green'),
                             (self.width - 110, self.height // 4, 84, 84), 2)
            self.condition = LEVEL_5
            return True
        return False

    def draw_LEVEL(self):
        self.screen.blit(load_image(f'LEVEL_{self.active_level}\\background.png', None), (0, 0))

    def draw_END_SCREEN(self):
        pygame.draw.rect(self.screen, pygame.Color('Grey'),
                         (self.width // 4, self.height // 4, self.width // 2, self.height // 2))
        font = pygame.font.Font(None, 50)
        if self.winner_team == 1:
            result = 'Victory'
        else:
            result = 'Defeat'
        headline = font.render(result, True, 'black')
        self.screen.blit(headline, (self.width // 2 - headline.get_width() // 2, self.height // 2 - 100))
        font = pygame.font.Font(None, 36)
        self.next = font.render('Next level', True, 'black')
        self.screen.blit(self.next, (self.width // 2 - self.next.get_width() // 2, self.height // 2 - 40))
        self.lvl_menu = font.render('Level menu', True, 'black')
        self.screen.blit(self.lvl_menu, (self.width // 2 - self.lvl_menu.get_width() // 2, self.height // 2 + 80))

    def draw_pause(self):
        pygame.draw.rect(self.screen, pygame.Color('Grey'),
                         (self.width // 4, self.height // 4, self.width // 2, self.height // 2))
        font = pygame.font.Font(None, 50)
        pause = font.render('Pause', True, 'black')
        self.screen.blit(pause, (self.width // 2 - pause.get_width() // 2, self.height // 2 - 100))
        font = pygame.font.Font(None, 36)
        self.cont = font.render('Continue', True, 'black')
        self.screen.blit(self.cont, (self.width // 2 - self.cont.get_width() // 2, self.height // 2 - 40))
        self.esc = font.render('Escape', True, 'black')
        self.screen.blit(self.esc, (self.width // 2 - self.esc.get_width() // 2, self.height // 2 + 80))

    def passive_MAIN(self):
        self.draw_MAIN()

    def active_MAIN(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.move_from_MAIN_to_LEVELS(event):
                return
            elif self.move_from_MAIN_to_UNITS(event):
                return
            elif self.leave_game_from_MAIN(event):
                return

    def passive_LEVELS(self):
        self.draw_LEVELS()

    def active_LEVELS(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.width // 2 - 83 <= x <= self.width // 2 + 83 and 330 <= y <= 410:
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (self.width // 2 - 83, 330, 166, 80), 2)
                self.condition = MAIN
            elif self.move_from_LEVELS_to_START(event):
                self.starting_LEVEL()
                return

    def passive_UNITS(self):
        self.draw_UNITS()

    def active_UNITS(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.width // 2 - 83 <= x <= self.width // 2 + 83 and \
                    330 <= y <= 410:
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (self.width // 2 - 83, 330, 166, 80), 2)
                self.condition = MAIN

    def passive_LEVEL(self):
        self.draw_LEVEL()
        if self.paused:
            self.draw_pause()
            self.clock.tick()
        else:
            for display_level in self.field.display_levels:
                for team in [-1, 0, 1]:
                    if display_level[team]:
                        unit = display_level[team]
                        unit.sprite.image = load_image(unit.picture())
                        unit.sprite.rect = unit.sprite.image.get_rect()
                        unit.sprite.rect.x = unit.position - (1 + unit.team) // 2 * unit.sprite.image.get_width()
                        unit.sprite.rect.y = HEIGHT - unit.sprite.image.get_height()
                        if team == 0:
                            unit.sprite.rect.y -= unit.height
                            unit.sprite.rect.x += 10 * sin(0.01 * unit.phase_timer)
            self.sprites.draw(self.screen)
            self.field.main_cycle(self.clock.tick())
            if self.field.winner():
                self.winner_team = self.field.winner()
                self.condition = END_SCREEN

    def active_LEVEL(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
        if self.paused:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if self.width // 2 - self.cont.get_width() // 2 <= x <= self.width // 2 + self.cont.get_width() // 2 \
                        and self.height // 2 - 40 <= y <= self.height // 2 - 40 + self.cont.get_height():
                    self.paused = False
                elif self.width // 2 - self.esc.get_width() // 2 <= x <= self.width // 2 + self.esc.get_width() // 2 \
                        and self.height // 2 + 80 <= y <= self.height // 2 + 80 + self.esc.get_height():
                    self.paused = False
                    self.condition = LEVELS
        else:
            pass
            #
            # freaking ton of player actions
            #

    def passive_END_SCREEN(self):
        self.passive_LEVEL()
        self.draw_END_SCREEN()

    def active_END_SCREEN(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.width // 2 - self.next.get_width() // 2 <= x <= self.width // 2 + self.next.get_width() // 2 \
                    and self.height // 2 - 40 <= y <= self.height // 2 - 40 + self.next.get_height():
                if 1 <= self.active_level <= 4:
                    self.condition = self.active_level + 1
                else:
                    self.condition = BOSS_DIALOG
            elif self.width // 2 - self.lvl_menu.get_width() // 2 <= x <= self.width // 2 + self.lvl_menu.get_width() \
                    // 2 and self.height // 2 + 80 <= y <= self.height // 2 + 80 + self.lvl_menu.get_height():
                self.condition = LEVELS

    def passive_BOSS_DIALOG(self):
        pass

    def active_BOSS_DIALOG(self, event):
        pass

    def main_cycle(self):
        self.running = True
        while self.running:
            if self.condition == MAIN:
                self.passive_MAIN()
            elif self.condition == LEVELS:
                self.passive_LEVELS()
            elif self.condition == UNITS:
                self.passive_UNITS()
            elif self.condition in [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5]:
                self.active_level = self.condition
                self.passive_LEVEL()
            elif self.condition == END_SCREEN:
                self.passive_END_SCREEN()
            elif self.condition == BOSS_DIALOG:
                self.passive_BOSS_DIALOG()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue
                if self.condition == MAIN:
                    self.active_MAIN(event)
                elif self.condition == LEVELS:
                    self.active_LEVELS(event)
                elif self.condition == UNITS:
                    self.active_UNITS(event)
                elif self.condition in [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5]:
                    self.active_level = self.condition
                    self.active_LEVEL(event)
                elif self.condition == END_SCREEN:
                    self.active_END_SCREEN(event)
                elif self.condition == BOSS_DIALOG:
                    self.active_BOSS_DIALOG(event)
            pygame.display.flip()
        pygame.quit()


def load_image(name, colorkey=-1):
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
