
# Boot strap the module loader into the environment
import utils.loader
env.loader = utils.loader.load('utils.loader')
del utils.loader

# Load the rest of the standard utilities
env.discord = env.loader.load('utils.discord')
env.logger = env.loader.load('utils.logger')