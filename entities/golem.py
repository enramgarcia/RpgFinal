from entities import entity


class Golem(entity.Entity):
    entity_name = 'Golem'
    frames = [12, 7, 16, 28]
    max_health = 20

    def __init__(self, screen, damage_texts, x, y):
        super().__init__(screen, damage_texts, x, y)
