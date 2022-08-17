from entities import entity


class Player(entity.Entity):
    entity_name = 'Knight'
    frames = [15, 8, 22, 15]
    flip = False

    max_health = 50
    min_hit = 5
    max_hit = 20

    def __init__(self, screen, damage_texts, x, y):
        super().__init__(screen, damage_texts, x, y)

    def move(self):
        self.x += 5

    def calc_final_position(self, npc):
        return npc.x - 150

    def should_attack(self):
        return self.x >= self.final_position
