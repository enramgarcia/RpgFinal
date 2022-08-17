from entities import entity


class Wolf(entity.Entity):
    entity_name = 'Wolf'
    frames = [12, 8, 16, 18]
    max_health = 8

    def __init__(self, screen, damage_texts, x, y):
        super().__init__(screen, damage_texts, x, y)

