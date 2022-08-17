from entities import entity


class Bat(entity.Entity):
    entity_name = 'Bat'
    frames = [8, 8, 10, 10]
    max_health = 4

    def __init__(self, screen, damage_texts, x, y, death_y):
        super().__init__(screen, damage_texts, x, y, death_y)
