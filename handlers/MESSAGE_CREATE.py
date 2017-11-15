import asyncio

async def run(data):
    print("<{0}> {1}".format(data['author']['username'], data['content']))