import random

import pygame

import damage_sprite
import spritesheet


class Entity:
    entity_name = ''

    damage_color = (255, 0, 0)

    _idle = 0
    _run = 1
    _attack = 2
    _death = 3

    frames = []
    flip = True

    actions = ['idle', 'run', 'attack', 'death']
    current_action = _idle

    max_health = 10
    max_hit = 5
    min_hit = 1

    animation_cooldown = 50

    attack_sound_route = 'assets/Sounds/attack.wav'
    target = None

    def __init__(self, screen, damage_texts, x, y, death_y=-1):
        pygame.font.get_init()
        self.font = pygame.font.SysFont('Times New Roman', 18)
        self.animations = []
        self.sheets = []
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.damage_texts = damage_texts

        self.locked = False
        self.is_dead = False
        self.init_position = 0
        self.final_position = 0
        self.current_health = self.max_health
        self.attack_sound = pygame.mixer.Sound(self.attack_sound_route)
        self.attack_sound.set_volume(.3)

        head = pygame.image.load(f"assets/{self.entity_name}/head.png")
        self.head_image = pygame.transform.scale(head, (25, 25))

        for i in range(len(self.actions)):
            temp_animations = []
            action = self.actions[i]
            max_frames = self.frames[i]
            route = f"assets/{self.entity_name}/{action}.png"
            sheet = pygame.image.load(route).convert_alpha()
            sprites = spritesheet.SpriteSheet(sheet)

            width = sheet.get_width() / max_frames

            for j in range(max_frames):
                temp_animations.append(sprites.get_image(j, width, 64, 2, self.flip))

            self.animations.append(temp_animations)

        self.x = self.init_position = x
        self.y = y

        if death_y == -1:
            self.death_y = y
        else:
            self.death_y = death_y

        self.image = self.animations[self.current_action][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.screen = screen

    def animate(self, on_menu):
        self.image = self.animations[self.current_action][self.current_frame]

        if self.current_action == 1 and on_menu is False:
            self.move()

        self.draw()

        if on_menu and self.current_action != self._idle:
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.last_update >= self.animation_cooldown:
            self.update_frames(current_time)

    def move(self):
        self.x -= 5

    def update_frames(self, current_time):
        if self.current_action != self._death:
            self.current_frame += 1

        self.last_update = current_time

        if self.current_action == self._idle:
            self.reset_animation()
        elif self.current_action == self._run:
            self.handle_run()
        elif self.current_action == self._attack:
            self.handle_attack()
        elif self.current_action == self._death:
            self.handle_death()

    def reset_animation(self):
        if self.current_frame >= self.frames[self.current_action]:
            self.current_frame = 0

    def attack(self, target):
        self.locked = True
        self.target = target
        self.current_frame = 0
        self.current_action = self._run
        self.final_position = self.calc_final_position(target)

    def calc_final_position(self, entity):
        return 64

    def handle_run(self):
        self.reset_animation()

        if self.should_attack():
            self.current_action = self._attack

    def should_attack(self):
        return self.x <= self.final_position

    def handle_attack(self):
        if self.current_frame >= self.frames[self.current_action]:
            self.current_frame = 0
            self.final_position = 0
            self.x = self.init_position
            self.current_action = 0
            self.locked = False

            damage = random.randrange(self.min_hit, self.max_hit)
            self.attack_sound.play()
            self.target.get_hit(damage)

            self.target = None

    def get_hit(self, damage):
        dmg_sprite = damage_sprite.DamageSprite(self.rect.x + 150, self.rect.y - 20, str(damage), self.damage_color)
        self.damage_texts.add(dmg_sprite)

        if self.current_health - damage <= 0:
            self.current_health = 0
            self.is_dead = True
            self.y = self.death_y
            self.current_action = self._death
        else:
            self.current_health -= damage

    def handle_death(self):
        if self.current_frame >= (self.frames[self.current_action] - 1):
            self.is_dead = True
        else:
            self.current_frame += 1

    def reset(self):
        self.x = self.final_position
        self.current_health = self.max_health
        self.is_dead = False
        self.locked = False
        self.current_frame = 0
        self.current_action = self._idle

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y - self.image.get_height()))


