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


class Field:  # класс поля, контролирующего взаимодействие юнитов
    def __init__(self, schedule, sprites):
        self.units = {1: set(), 0: set(), -1: set()}  # хранилище всех живых юнитов на поле
        self.schedule = schedule  # расписание выхода противников на уровне
        self.dead_set = set()  # множество убитых за итерацию юнитов
        self.towers = {1: None, -1: None}  # указатели на башни игрока и противника
        self.sprites = sprites
        self.display_levels = [{1: None, 0: None, -1: None} for _ in range(50)]  # уровни отрисовки

    def winner(self):  # выводит победителя (игрок / противник / никто)
        if self.towers[1].alive and self.towers[-1].alive:
            return None
        if self.towers[1].alive:
            return 1
        return -1

    def main_cycle(self, dt):
        for team in [1, 0, -1]:
            for unit in self.units[team]:
                unit.tick(dt)
        for unit in self.dead_set:
            unit.disappear()
        self.dead_set.clear()

    def attack_check(self, unit):  # проверка на то, может ли атаковать юнит
        for enemy in self.units[-unit.team]:
            if 0 <= unit.team * (enemy.position - unit.position) <= unit.range:
                return True
        return False

    def commit_attack(self, unit):  # выполнение атаки юнитов
        if unit.area:
            for enemy in self.units[-unit.team]:
                if 0 <= unit.team * (enemy.position - unit.position) <= unit.range:
                    enemy.take_damage(unit.damage)
        else:
            target, distance = None, unit.range
            for enemy in self.units[-unit.team]:
                if 0 <= unit.team * (enemy.position - unit.position) <= distance:
                    target, distance = enemy, unit.team * (enemy.position - unit.position)
            if target:
                target.take_damage(unit.damage)


class Unit:  # класс боевого юнита
    def __init__(self, team, speed, range, damage, health, images, haste, field, area):
        self.sprite = pygame.sprite.Sprite()  # используется для отрисовки
        self.images = images  # изображение юнита
        self.team = team  # команда юнита (враг или союзник)
        self.speed = speed  # скорость перемещения юнита
        self.damage = damage  # урон юнита
        self.range = range  # дальность атаки юнита
        self.health = health  # здоровье юнита
        self.haste = haste  # скорость атаки юнита
        self.field = field  # поле, на котором сражается юнит
        self.attacking = False  # находится ли юнит в процессе атаки
        self.position = None  # расположение юнита
        self.area = area  # бьёт юнит по зоне или по одиночной цели
        self.attack_timer = 0  # для отслеживания задержки атаки
        self.display_level = None  # для отрисовки юнитов поверх друг друга
        self.phase = 0  # фаза (для анимаций)
        self.phase_timer = 0  # таймеры смены фаз
        self.animation_periods = {False: {0: 1000, 1: 1000}, True: {0: 0.75 * self.haste, 1: 0.25 * self.haste}}

    def put(self, position):  # постановка юнита на поле боя
        self.field.units[self.team].add(self)
        self.position = position
        self.field.sprites.add(self.sprite)
        for i in range(len(self.field.display_levels)):
            if not self.field.display_levels[i][self.team]:
                self.display_level = i
                self.field.display_levels[i][self.team] = self
                return
        self.field.display_levels.append({1: None, 0: None, -1: None})
        self.field.display_levels[-1][self.team] = self

    def disappear(self):  # "уборка трупа"
        self.field.units[self.team].remove(self)
        self.field.display_levels[self.display_level][self.team] = None
        self.sprite.kill()
        Ghost(self).summon()

    def take_damage(self, damage):  # получение урона юнитом
        self.health -= damage
        if self.health <= 0:
            self.field.dead_set.add(self)

    def tick(self, dt):  # действия юнита за время dt
        if not self.attacking:
            self.attacking = self.field.attack_check(self)
            if self.attacking:
                self.phase = 0
                self.phase_timer = 0
        self.phase_timer += dt
        if self.phase_timer >= self.animation_periods[self.attacking][self.phase]:
            self.phase_timer = 0
            self.phase = 1 - self.phase
        self.act(dt)

    def picture(self):  # юнит возвращает изображение для отрисовки себя
        return f'Sprites\\{self.images}\\animation{int(self.attacking)}{self.phase}.png'

    def act(self, dt):
        if self.attacking:
            self.attack_timer += dt
            if self.attack_timer >= self.haste:
                self.attack_timer = 0
                self.field.commit_attack(self)
                self.attacking = False
                self.phase = 0
                self.phase_timer = 0
        else:
            self.position += self.team * self.speed * dt

    def __str__(self):
        return f'Team: {self.team}, HP: {self.health}, pos: {str(self.position)[:4]}, attacking: {self.attacking}'

    def __repr__(self):
        return f'Unit({self.team}, {self.health})'


class Tower(Unit):  # класс башни (подкласс юнита)
    def __init__(self, team, health, images, field):
        super().__init__(team, 0, 0, 0, health, images, 0, field, False)
        self.alive = False

    def put(self, position):
        super().put(position)
        self.field.towers[self.team] = self
        self.alive = True

    def disappear(self):
        self.alive = False

    def tick(self, dt):
        pass

    def picture(self):
        return f'Sprites\\{self.images}\\animation{int(self.alive)}.png'


class Ghost(Unit):  # класс призрака (используется для анимации смерти юнитов, невидим для живых юнитов)
    def __init__(self, unit):
        super().__init__(0, 0.1, 0, 0, 0, 'Ghost', 0, unit.field, False)
        self.height = 0
        self.body = unit
        self.existence_limit = 2000

    def summon(self):
        super().put(self.body.position)
        self.team = self.body.team

    def tick(self, dt):
        self.phase_timer += dt
        self.height += dt * self.speed
        if self.phase_timer >= self.existence_limit:
            self.field.dead_set.add(self)

    def disappear(self):
        self.field.units[0].remove(self)
        self.field.display_levels[self.display_level][0] = None
        self.sprite.kill()

    def picture(self):
        return 'Sprites\\Ghost\\animation.png'


if __name__ == '__main__':
    pass
