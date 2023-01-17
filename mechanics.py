import pygame


bases = {-1: 650, 1: 140}
walking, standing, attacking = 0, 1, 2
rewards = {
    'Basic_Gremlin': 0, 'Wall_Gremlin': 0, 'Axe_Gremlin': 0,
    'Sausage_Gremlin': 0, 'Spear_Gremlin': 0, 'Shaman_Gremlin': 0,
    'Fat_Human': 250, 'Torch_Human': 500, 'Archer_Human': 750,
    'Bazuka_Human': 1000, 'Mace_Human': 1250, 'Mage_Human': 10000,
    'Ghost': 0, 'Gremlin_Tower': 0, 'Human_Tower': 0,
}


class Field:  # класс поля, контролирующего взаимодействие юнитов
    def __init__(self, schedule, sprites):
        self.units = {1: set(), 0: set(), -1: set()}  # хранилище всех живых юнитов на поле
        with open(schedule, 'r') as text:
            self.schedule = text.readlines()  # расписание выхода противников на уровне
        self.dead_set = set()  # множество убитых за итерацию юнитов
        self.towers = {1: None, -1: None}  # указатели на башни игрока и противника
        self.sprites = sprites
        self.display_levels = [{1: None, 0: None, -1: None} for _ in range(50)]  # уровни отрисовки
        self.time = 0
        self.schedule_row = 0
        self.boss = None

    def winner(self):  # выводит победителя (игрок / противник / никто)
        if self.towers[1].alive and self.towers[-1].alive:
            return None
        if self.towers[1].alive:
            return 1
        return -1

    def put_unit_from_schedule(self):  # читает статы врагов из .txt и присваивает их
        stats = self.schedule[self.schedule_row].split()
        team, damage, health = int(stats[1]), int(stats[2]), int(stats[3])
        images, haste, area = stats[4], int(stats[5]), bool(int(stats[6]))
        Unit(team, damage, health, images, haste, self, area).put(bases[team])

    def main_cycle(self, dt):
        reward = 0
        self.time += dt
        # спавн юнитов противника в соответствии с расписанием
        if self.schedule_row < len(self.schedule) and self.towers[-1].alive:
            if self.time >= int(self.schedule[self.schedule_row].split()[0]):
                self.put_unit_from_schedule()
                self.schedule_row += 1
        # проверка живых юнитов
        for team in [-1, 1]:
            if not self.towers[team].alive:
                for unit in self.units[team]:
                    self.dead_set.add(unit)
        # начало следующей итерации для живых юнитов
        for team in [1, 0, -1]:
            for unit in self.units[team]:
                unit.tick(dt)
        # уничтожение мертвых юнитов
        for unit in self.dead_set:
            unit.disappear()
            reward += rewards[unit.images]
        self.dead_set.clear()
        # переключение состояний живых юнитов
        for team in [-1, 1]:
            for unit in self.units[team]:
                if unit.condition == standing:
                    if self.attack_check(unit):
                        unit.condition = attacking
                        if unit.haste:
                            unit.condition = standing
                    else:
                        unit.condition = walking
        return reward

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
    def __init__(self, team, damage, health, images, haste, field, area):
        self.sprite = pygame.sprite.Sprite()  # используется для отрисовки
        self.images = images  # изображение юнита
        self.team, self.damage = team, damage  # команда юнита (враг или союзник), урон атак юнита
        self.health, self.haste = health, haste  # здоровье юнита, скорость атаки юнита
        self.field, self.condition = field, walking  # поле, на котором сражается юнит, состояние юнита
        self.position, self.area = None, area  # расположение юнита, бьёт юнит по зоне или по одиночной цели
        self.display_level = None  # для отрисовки юнитов поверх друг друга
        with open(f'data\\Sprites\\{images}\\stats.txt', 'r') as stats:
            text = stats.readline().split()
            self.distance, self.speed, self.range = int(text[0]), float(text[1]), int(text[2])
            self.attack_animations = [int(text[3]), int(text[4])]
            self.moving_animation = int(text[5])  # скорость движения и дальность атаки юнита
        self.timer = self.haste
        self.phase = 0
        self.phase_timer = 0

    def put(self, position):  # постановка юнита на поле боя
        self.field.units[self.team].add(self)
        self.position = position
        self.field.sprites.add(self.sprite)
        if self.images == 'Mage_Human':
            self.field.boss = self
        for i in range(len(self.field.display_levels)):
            if not self.field.display_levels[i][self.team]:
                self.display_level = i
                self.field.display_levels[i][self.team] = self
                return
        self.display_level = len(self.field.display_levels)
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
        self.get_purpose(dt)
        self.act(dt)

    def picture(self):  # юнит возвращает изображение для отрисовки себя
        return f'Sprites\\{self.images}\\animation{self.condition}{self.phase}.png'

    def get_purpose(self, dt):  # юнит получает информацию о том, что ему делать (идти/стоять/атаковать)
        self.timer += dt
        if self.field.attack_check(self):
            if self.condition == attacking:
                self.phase_timer += dt
                if self.phase_timer >= self.attack_animations[self.phase]:
                    self.phase = 1 - self.phase
                    self.phase_timer = 0
            else:
                self.phase = 0
                self.phase_timer = 0
                if self.timer >= self.haste:
                    self.condition = attacking
                    self.timer = 0
                else:
                    self.condition = standing
        else:
            if self.condition == walking:
                self.phase_timer += dt
                if self.phase_timer >= self.moving_animation:
                    self.phase = 1 - self.phase
                    self.phase_timer = 0
            elif self.condition == standing:
                self.condition = walking
                self.phase = 0
                self.phase_timer = 0
            else:
                self.phase_timer += dt
                if self.phase_timer >= self.attack_animations[self.phase]:
                    self.phase = 1 - self.phase
                    self.phase_timer = 0

    def act(self, dt):  # произведение всех действий юнита
        if self.condition == walking:
            self.position += self.team * self.speed * dt
        elif self.condition == attacking:
            if self.timer >= sum(self.attack_animations):
                self.field.commit_attack(self)
                self.timer = 0
                self.phase = 0
                self.phase_timer = 0
                self.condition = standing


class Tower(Unit):  # класс башни (подкласс юнита)
    def __init__(self, team, health, images, field):
        super().__init__(team, 0, health, images, 0, field, False)
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
        super().__init__(0, 0, 0, 'Ghost', 0, unit.field, False)
        self.height = 0
        self.body = unit
        self.existence_limit = 2000
        self.timer = 0

    def summon(self):
        super().put(self.body.position)
        self.team = self.body.team

    def tick(self, dt):
        self.timer += dt
        self.height += dt * self.speed
        if self.timer >= self.existence_limit:
            self.field.dead_set.add(self)

    def disappear(self):
        self.field.units[0].remove(self)
        self.field.display_levels[self.display_level][0] = None
        self.sprite.kill()

    def picture(self):
        return 'Sprites\\Ghost\\animation.png'


if __name__ == '__main__':
    pass
