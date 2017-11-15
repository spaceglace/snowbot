import role, member, channel

class Guild:
    def __init__(self, guild):
        self.verification_level = guild['verification_level']
        self.region = guild['region']
        self.owner_id = guild['owner_id']
        self.name = guild['name']
        self.mfa_level = guild['mfa_level']
        self.member_count = guild['member_count']
        self.large = guild['large']
        self.joined_at = guild['joined_at']
        self.id = guild['id']
        self.icon = guild['icon']
        self.afk_timeout = guild['afk_timeout']
        self.afk_channel_id = guild['afk_channel_id']

        self.roles = []
        self.presences = []
        self.members = []
        self.emojis = []
        self.channels = []

        for r in guild['roles']:
            self.roles.append(role.Role(r))

        for m in guild['members']:
            self.members.append(member.Member(m))

        for c in guild['channels']:
            self.channels.append(channel.Channel(c))
