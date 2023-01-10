import pygame

UNITS = {
    # команда, скорость, дальность, урон, здоровье, анимации, скорость атаки, поле, аое, цена, кд
    1: (1, 0.01, 20, 5, 20, '', 2, None, False, 50, 3),
    2: (1),
    3: (1),
    4: (1),
    5: (1),
    6: (1),
    7: (-1),
    8: (-1),
    9: (-1),
    10: (-1),
    11: (-1),
    12: (-1)
}
FIELD_LENGTH = 700
START = 20


class Display:
    def __init__(self):
        self.condition = None
        self.width = 1000
        self.height = 600
        self.screen = None
        self.running = False
        self.field = None
        self.clock = None  # pygame.time.Clock()

    def build(self):
        pygame.init()
        pygame.display.set_caption('The Battle Goblins')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))

    #  pygame.display.flip()

    def position_A(self, event):
        pass

    def position_B(self, event):
        pass

    def position_C(self, event):
        pass

    def main_cycle(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue
                if self.condition == 'A':
                    self.position_A(event)
                if self.condition == 'B':
                    self.position_B(event)
                if self.condition == 'C':
                    self.position_C(event)
            pygame.display.flip()
        pygame.quit()


class Field:
    def __init__(self, schedule):
        self.units = {1: set(), -1: set()}
        self.schedule = schedule
        self.dead_set = set()
        self.towers = {1: None, -1: None}

    def main_cycle(self, dt):
        for team in [1, -1]:
            for unit in self.units[team]:
                unit.tick(dt)
        for unit in self.dead_set:
            unit.disappear()
        self.dead_set.clear()

    def attack_check(self, unit):
        for enemy in self.units[-unit.team]:
            if 0 <= unit.team * (enemy.pos - unit.pos) <= unit.range:
                return True
        return False

    def commit_attack(self, unit):
        if unit.area:
            for enemy in self.units[-unit.team]:
                if 0 <= unit.team * (enemy.pos - unit.pos) <= unit.range:
                    enemy.take_damage(unit.damage)
        else:
            target, distance = None, unit.range
            for enemy in self.units[-unit.team]:
                if 0 <= unit.team * (enemy.pos - unit.pos) <= distance:
                    target, distance = enemy, unit.team * (enemy.pos - unit.pos)
            if target:
                target.take_damage(unit.damage)


class Unit(pygame.sprite.Sprite):
    def __init__(self, team, speed, range, damage, health, images, haste, field, area):
        super().__init__()
        self.images = images  # изображение юнита
        self.team = team  # команда юнита (враг или союзник)
        self.speed = speed  # скорость перемещения юнита
        self.damage = damage  # урон юнита
        self.range = range  # дальность атаки юнита
        self.health = health  # здоровье юнита
        self.haste = haste  # скорость атаки юнита
        self.field = field  # поле, на котором сражается юнит
        self.attacking = False  # находится ли юнит в процессе атаки
        self.pos = None
        self.area = area
        self.timer = 0

    def put(self, position):
        self.field.units[self.team].add(self)
        self.pos = position

    def disappear(self):
        self.field.units[self.team].remove(self)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.field.dead_set.add(self)

    def tick(self, dt):
        if not self.attacking:
            self.attacking = self.field.attack_check(self)
        self.act(dt)

    def act(self, dt):
        if self.attacking:
            self.timer += dt
            #  animations
            if self.timer >= self.haste:
                self.timer = 0
                self.field.commit_attack(self)
                self.attacking = False
        else:
            #  animations
            self.pos += self.team * self.speed * dt

    def __str__(self):
        return f'Team: {self.team}, HP: {self.health}, position: {str(self.pos)[:4]}, attacking: {self.attacking}, moving: {not self.attacking}'


class Tower(Unit):
    def __init__(self, team, health, images, field):
        super().__init__(team, 0, 0, 0, health, images, 0, field, False)

    def put(self, position):
        super().put(position)
        self.field[self.team] = self

    def tick(self, dt):
        pass


if __name__ == '__main__':
    pass