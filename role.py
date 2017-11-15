class Role:
    def __init__(self, role):
        self.position = role['position']
        self.permissions = role['permissions']
        self.name = role['name']
        self.mentionable = role['mentionable']
        self.managed = role['managed']
        self.id = role['id']
        self.hoist = role['hoist']
        self.color = role['color']
