from entities import entity


class Witch(entity.Entity):
    entity_name = 'Witch'
    frames = [7, 8, 18, 11]
    animation_cooldown = 60

    def __init__(self, screen, damage_texts, x, y):
        super().__init__(screen, damage_texts, x, y)
