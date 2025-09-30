import importlib
import os
from app import db
from app.models import Plugin

PLUGIN_DIR = os.path.join(os.path.dirname(__file__), 'plugins')

class PluginManager:
    def __init__(self):
        self.loaded_plugins = {}

    def load_plugin(self, name):
        if name in self.loaded_plugins:
            return False
        try:
            module = importlib.import_module(f'app.plugins.{name}')
            self.loaded_plugins[name] = module
            plugin = Plugin(name=name, description=module.__doc__, is_enabled=True)
            db.session.add(plugin)
            db.session.commit()
            return True
        except Exception as e:
            return False

    def unload_plugin(self, name):
        if name not in self.loaded_plugins:
            return False
        try:
            del self.loaded_plugins[name]
            plugin = Plugin.query.filter_by(name=name).first()
            if plugin:
                plugin.is_enabled = False
                db.session.commit()
            return True
        except Exception:
            return False

def load_plugins():
    plugins = {}
    plugin_folder = os.path.join(os.path.dirname(__file__), 'plugins')
    for filename in os.listdir(plugin_folder):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = f"app.plugins.{filename[:-3]}"
            module = importlib.import_module(module_name)
            for attr in dir(module):
                obj = getattr(module, attr)
                if hasattr(obj, 'run') and callable(getattr(obj, 'run')):
                    plugins[attr] = obj()
    return plugins
