import importlib, os
import env

def load(mod):
    return importlib.import_module(mod)

def refresh(mod):
    importlib.reload(mod)

def rescan():
    env.handlers = {}

    for handle in os.listdir("./handlers/"):
        if handle.endswith(".py"):
            handle_name = handle[:-3]
            env.handlers[handle_name] = env.loader.load("handlers.{0}".format(handle_name))
