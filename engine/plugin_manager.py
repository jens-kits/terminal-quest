# TerminalQuest/engine/plugin_manager.py

import importlib
import os

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self, plugin_dir):
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                module = importlib.import_module(f'plugins.{module_name}')
                if hasattr(module, 'register_plugin'):
                    plugin = module.register_plugin()
                    self.plugins[plugin.name] = plugin

    def get_plugin(self, name):
        return self.plugins.get(name)

    def execute_plugin(self, name, *args, **kwargs):
        plugin = self.get_plugin(name)
        if plugin:
            return plugin.execute(*args, **kwargs)
        else:
            raise ValueError(f"Plugin '{name}' not found")

# Example plugin structure:
# class ExamplePlugin:
#     name = "example_plugin"
#     
#     def execute(self, game, command):
#         # Plugin logic here
#         pass
# 
# def register_plugin():
#     return ExamplePlugin()