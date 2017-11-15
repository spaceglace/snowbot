import asyncio, aiohttp, json
import env, constants

class Discord:
    def __init__(self, token, os, browser, platform, status=constants.STATUS_ONLINE, afk=False):
        self.token = token
        self.os = os
        self.browser = browser
        self.platform = platform
        self.compress = False
        self.large_threshold = 250
        self.shard = [0, 1]
        self.in_game = False
        self.game = None
        self.status = status
        self.afk = afk
        self.last_seq = None

    def SetGame(self, name, state):
        self.game = {
            'name': name,
            'type':state
        }

    def SetStatus(self, status):
        self.status = status

    def SetAFK(self, afk):
        self.afk = afk

    async def _SendIdentifyString(self):
        await self.queue.put({
            "op": constants.OPCODE_IDENTIFY,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": self.os,
                    "$browser": self.browser,
                    "$platform": self.platform
                },
                "compress": self.compress,
                "large_threshold": self.large_threshold,
                "shard": [0, 1],
                "presence": {
                    "since": None,
                    "game": self.game
                },
                "status": self.status,
                "afk": self.afk
            }
        })

    async def _Request(self, path, method):
        print("Enter Discord.Request({0})".format(path))

        headers = {'Authorization': 'Bot {0}'.format(self.token)}

        async with method('https://discordapp.com/api/v6' + path, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                print("Bad response: {0}".format(response))

    async def _Heartbeat(self):
        #print("Sending heartbeat, seq={0}".format(self.last_seq))

        await self.queue.put({
            "op": constants.OPCODE_HEARTBEAT,
            "d": self.last_seq
        })

    async def _Keepalive(self):
        print("Entering Discord.Keepalive...")

        while True:
            await asyncio.sleep(self.heartbeat_interval / 1000)
            await self._Heartbeat()

    async def _Speak(self):
        print("Entering Discord.Speak...")

        while True:
            data = await self.queue.get()
            #print("Sending message...")
            await self.socket.send_json(data)

    async def _Listen(self):
        print("Entering Discord.Listen...")

        while True:
            message = await self.socket.receive()

            if message.tp == aiohttp.WSMsgType.TEXT:
                #print("Got a message: {0}".format(message.data))

                data = json.loads(message.data)

                if 'op' not in data:
                    print("Unknown message: {0}".format(data))

                elif data['op'] == constants.OPCODE_DISPATCH:
                    self.last_seq = data['s']

                    if data['t'] in env.handlers:
                        asyncio.ensure_future(env.handlers[data['t']].run(data['d']))
                    else:
                        print("Unknown event: {0}".format(data['t']))

                elif data['op'] == constants.OPCODE_HEARTBEAT:
                    print('heartbeat')
                    await self._Heartbeat()

                elif data['op'] == constants.OPCODE_RECONNECT:
                    print('reconnect')

                elif data['op'] == constants.OPCODE_INVALID_SESSION:
                    print('invalid session')

                elif data['op'] == constants.OPCODE_HELLO:
                    self.heartbeat_interval = data['d']['heartbeat_interval']
                    env.logger.debug("Received HELLO. heartbeat_interval is {0}".format(self.heartbeat_interval))

                    # Start the keepalive
                    self.task_keepalive = asyncio.ensure_future(self._Keepalive())

                    # Send our identify
                    await self._SendIdentifyString()

                elif data['op'] == constants.OPCODE_HEARTBEAT_ACK:
                    continue
                #    print('heartbeat ack')

                else:
                    print("Unknown opcode: {0}".format(data))

            elif message.tp == aiohttp.WSMsgType.CLOSE:
                print('Socket being closed')

            elif message.tp == aiohttp.WSMsgType.CLOSED:
                print('Socket closed')
                break

            else:
                print("UNKNOWN WSMsgType: {0}".format(message.tp))
                print("Full: {0}".format(message))

    async def _Wrapper(self):
        gateway = await self._Request("/gateway/bot", self.session.get)
        print("Got gateway: {0}".format(gateway['url']))

        self.socket = await self.session.ws_connect("{0}/?v=6&encoding=json".format(gateway['url']))

        self.task_listen = asyncio.ensure_future(self._Listen())
        self.task_speak = asyncio.ensure_future(self._Speak())

        await asyncio.wait([self.task_listen, self.task_speak], return_when=asyncio.FIRST_COMPLETED)

        print("Broke out of _Wrapper.asyncio.wait")
        print("Listen: {0}".format(self.task_listen))
        print("Speak: {0}".format(self.task_speak))

    def Connect(self):
        print("Entering Discord.Connect...")

        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.queue = asyncio.Queue()

        self.loop.set_debug(True)
        self.loop.run_until_complete(self._Wrapper())

        self.session.close()
        self.loop.close()

        print("Exiting Discord.Connect...")
