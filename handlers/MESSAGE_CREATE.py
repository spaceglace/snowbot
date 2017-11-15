import asyncio
import env, channel, guild, member

async def run(discord, data):
    print("<{0}> {1}".format(data['author']['username'], data['content']))

    if data['content'] == "whoami":
        target_id = data['author']['id']
        channel_id = data['channel_id']
        found = False
        output = ""

        for g in env.guilds:
            for c in env.guilds[g].channels:
                if c.id == channel_id:
                    for m in env.guilds[g].members:
                        if m.id == target_id:
                            found = True
                            output = "You are {0}#{1}, otherwise known as {2}".format(
                                m.username,
                                m.discriminator,
                                m.nick
                            )
                            break
                    break

        if not found:
            output = "Couldn't find you. Do you exist?"

        await discord.Say(channel_id, output)
