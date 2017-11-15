class Member:
    def __init__(self, user):
        self.username = user['user']['username']
        self.id = user['user']['id']
        self.discriminator = user['user']['discriminator']
        self.nick = None if 'nick' not in user else user['nick']
