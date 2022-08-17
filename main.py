import random

import spritesheet
from entities import player, golem, wolf, witch, bat
import scenario
import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(.1)

FONT = pygame.font.SysFont('Times New Roman', 26)
TEXT_FONT = pygame.font.SysFont('Times New Roman', 18)
BLACK = (0, 0, 0)

FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
MAX_HEIGHT = 500
BACKGROUND = (50, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Proyecto Final by Enrique García 8-864-1269')

keys_size = 4
keys_image = pygame.image.load('assets/Hud/keys.png')
keys_width = keys_image.get_width()
keys_image = pygame.transform.scale(keys_image, (keys_width * 2, keys_image.get_height() * 2))
keys_sprites = spritesheet.SpriteSheet(keys_image)
keys_list = []

for keys_index in range(keys_size):
    keys_list.append(keys_sprites.get_image(keys_index, keys_width * 2 / keys_size, keys_image.get_height(), 1))

damage_texts = pygame.sprite.Group()
monsters = []
player = player.Player(screen, damage_texts, 0, 485)

game_over_sound_playing = False


def load_battle_music():
    global game_over_sound_playing

    pygame.mixer.music.unload()
    pygame.mixer.music.load('assets/Sounds/background.mp3')
    pygame.mixer.music.play(-1)
    game_over_sound_playing = False


def load_game_over_music():
    global game_over_sound_playing

    pygame.mixer.music.unload()
    pygame.mixer.music.load('assets/Sounds/game_over.mp3')
    pygame.mixer.music.play(-1)
    game_over_sound_playing = True


def render_text(text, pos, color, surface):
    draw_text(text, pos, color, surface, FONT)


def draw_text(text, pos, color, surface, font):
    render = font.render(text, True, color)
    surface.blit(render, pos)


def game_over():
    if game_over_sound_playing is False:
        load_game_over_music()

    screen.fill(BLACK)
    render_text('Fin...', (100, 300), (255, 255, 255), screen)
    render_text('Presione Enter para continuar', (100, 340), (255, 255, 255), screen)


def draw_instructions():
    panel_image = pygame.image.load(f"assets/Hud/panel.png")
    panel_image = pygame.transform.scale(panel_image, (300, 150))

    draw_text('Para jugar presione las teclas', (40, 40), BLACK, panel_image, TEXT_FONT)

    rect = keys_image.get_rect(center=panel_image.get_rect().center)
    panel_image.blit(keys_image, (rect.x, 65))

    draw_text('para atacar al enemigo', (80, 90), BLACK, panel_image, TEXT_FONT)

    screen.blit(panel_image, (300, 50))


def draw_frame(panel, x, y, text_x, text_y, entity, key_image=None):

    if key_image is not None:
        panel.blit(key_image, (x, y))

    frame = pygame.surface.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.rect(frame, (143, 86, 59), (2, 2, 33, 33), 0)

    rect = entity.head_image.get_rect(center=frame.get_rect().center)
    frame.blit(entity.head_image, rect)

    panel.blit(frame, (x + 40, y))
    text = f'{entity.entity_name}: {entity.current_health} / {entity.max_health}'

    if entity.current_health == 0:
        color = (255, 0, 0)
    elif entity.current_health / entity.max_health <= 0.5:
        color = (240, 255, 0)
    else:
        color = BLACK

    render_text(text, (text_x + 40, text_y), color, panel)


def draw_panel():
    panel_image = pygame.image.load(f"assets/Hud/panel.png")
    draw_frame(panel_image, 50, 50, 100, 50, player)

    for monster_index in range(len(monsters)):
        y = 30 + (35 * monster_index)
        draw_frame(panel_image, 400, y, 450, y, monsters[monster_index], keys_list[monster_index])

    screen.blit(panel_image, (0, MAX_HEIGHT))


def handle_fight(is_menu_state, bg, user, monsters_list):
    bg.draw()
    draw_panel()

    if is_menu_state:
        draw_instructions()

    user.animate(is_menu_state)

    for i in range(len(monsters_list)):
        monsters_list[i].animate(is_menu_state)


def attack_monster(index):
    if index > len(monsters):
        return False

    if monsters[index - 1].is_dead is False:
        player.attack(monsters[index - 1])
        return True
    else:
        return False


def generate_monsters():
    monsters.clear()
    max_monsters = random.randrange(3, 5)

    for i in range(max_monsters):
        monster_type = random.randrange(0, 4)
        monster_x = 350 + (100 * i)

        if monster_type == 0:
            monsters.append(wolf.Wolf(screen, damage_texts, monster_x, 485))
        elif monster_type == 1:
            monsters.append(golem.Golem(screen, damage_texts, monster_x, 485))
        elif monster_type == 2:
            monsters.append(witch.Witch(screen, damage_texts, monster_x, 485))
        elif monster_type == 3:
            monsters.append(bat.Bat(screen, damage_texts, monster_x, 450, 485))


def monsters_left():
    for index in range(len(monsters)):
        if monsters[index].is_dead is False:
            return True

    return False


def handle_player_input():
    if key_pressed[pygame.K_1]:
        return attack_monster(1)
    elif key_pressed[pygame.K_2]:
        return attack_monster(2)
    elif key_pressed[pygame.K_3]:
        return attack_monster(3)
    elif key_pressed[pygame.K_4]:
        return attack_monster(4)

    if key_pressed[pygame.K_RETURN]:
        if player.is_dead or monsters_left() is False:
            load_battle_music()
            player.reset()
            generate_monsters()

    if advance_turn:
        return True

    return False


if __name__ == '__main__':

    turn = 0
    clock = pygame.time.Clock()

    run = True

    generate_monsters()
    background = scenario.Scenario(screen, SCREEN_WIDTH, MAX_HEIGHT)
    on_menu = True
    advance_turn = False
    current_attacker = player
    load_battle_music()

    while run:
        # update background
        screen.fill(BACKGROUND)

        clock.tick(FPS)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()

        if turn == 0:
            advance_turn = handle_player_input()

            if on_menu and advance_turn:
                on_menu = False
        else:
            if (monsters[turn - 1]).is_dead is False and current_attacker != monsters[turn - 1]:
                monsters[turn - 1].attack(player)
                current_attacker = monsters[turn - 1]
            advance_turn = True

        if advance_turn and current_attacker.locked is False:
            turn += 1
            advance_turn = False

        if turn > len(monsters):
            turn = 0
            current_attacker = player

        if player.is_dead or monsters_left() is False:
            game_over()
        else:
            handle_fight(on_menu, background, player, monsters)

        damage_texts.update()
        damage_texts.draw(screen)
        pygame.display.update()

    pygame.quit()
