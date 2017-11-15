import os
import env, config, constants

# Boot strap the module loader into the environment
import utils.loader
env.loader = utils.loader.load('utils.loader')
del utils.loader

# Load standard utilities
env.discord = env.loader.load('utils.discord')
env.logger = env.loader.load('utils.logger')

for handle in os.listdir("./handlers/"):
    if handle.endswith(".py"):
        handle_name = handle[:-3]
        env.handlers[handle_name] = env.loader.load("handlers.{0}".format(handle_name))

discord = env.discord.Discord(config.BOT_TOKEN, "GLaciOS", "GlaciBrowser", "Glaciplatform")
discord.SetGame("to the chickens roar", constants.GAME_TYPE_LISTENING)
discord.Connect()
