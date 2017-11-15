import asyncio
import guild, env

async def run(discord, data):
    env.guilds[data['id']] = guild.Guild(data)
    print("Server {0} became available.".format(data['name']))
