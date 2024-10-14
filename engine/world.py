# TerminalQuest/engine/world.py

from .item import Item
from .npc import NPC
import logging

logger = logging.getLogger(__name__)

class World:
    def __init__(self, config):
        self.locations = {}
        self.items = {}
        self.npcs = {}
        if config is None:
            logger.error("Received None config in World initialization")
            raise ValueError("Config cannot be None")
        self.load_world(config)

    def load_world(self, config):
        logger.info("Starting to load world")
        if not isinstance(config, dict):
            logger.error(f"Expected config to be a dict, but got {type(config)}")
            raise ValueError("Invalid config format")

        logger.info("Loading locations")
        locations = config.get('locations')
        if locations is None:
            logger.error("No 'locations' key found in config")
            raise ValueError("Config must contain 'locations' key")
        for loc_data in locations:
            self.locations[loc_data['name']] = Location(loc_data)
        
        logger.info("Loading items")
        items = config.get('items')
        if items is None:
            logger.warning("No 'items' key found in config")
        else:
            for item_data in items:
                self.items[item_data['name']] = Item(item_data['name'], item_data['description'])

        logger.info("Loading NPCs")
        npcs = config.get('npcs')
        if npcs is None:
            logger.warning("No 'npcs' key found in config")
        else:
            for npc_data in npcs:
                self.npcs[npc_data['name']] = NPC(npc_data['name'], npc_data['description'], npc_data.get('dialogue', {}))

        logger.info("Setting up location connections and placing items and NPCs")
        for loc_data in locations:
            location = self.locations[loc_data['name']]
            for exit_dir, exit_loc in loc_data.get('exits', {}).items():
                location.exits[exit_dir] = self.locations[exit_loc]
            for item_name in loc_data.get('items', []):
                if item_name in self.items:
                    location.add_item(self.items[item_name])
                else:
                    logger.warning(f"Item '{item_name}' referenced in location '{location.name}' but not defined in items list")
            for npc_name in loc_data.get('npcs', []):
                if npc_name in self.npcs:
                    location.add_npc(self.npcs[npc_name])
                else:
                    logger.warning(f"NPC '{npc_name}' referenced in location '{location.name}' but not defined in npcs list")

        logger.info("World loading complete")

    def get_location(self, location_name):
        return self.locations.get(location_name)

    def get_item(self, item_name):
        return self.items.get(item_name)

    def get_npc(self, npc_name):
        return self.npcs.get(npc_name)

class Location:
    def __init__(self, data):
        self.name = data['name']
        self.description = data['description']
        self.exits = {}
        self.items = []
        self.npcs = []
        self.objects = data.get('objects', {})

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def add_npc(self, npc):
        self.npcs.append(npc)

    def remove_npc(self, npc):
        self.npcs.remove(npc)

    def get_exit(self, direction):
        return self.exits.get(direction)

    def get_item(self, item_name):
        return next((item for item in self.items if item.name.lower() == item_name.lower()), None)

    def get_npc(self, npc_name):
        return next((npc for npc in self.npcs if npc.name.lower() == npc_name.lower()), None)

    def get_object(self, object_name):
        return self.objects.get(object_name.lower())

    def describe(self):
        description = f"{self.name}\n{'-' * len(self.name)}\n{self.description}\n"
        
        if self.items:
            description += "\nItems here:\n" + "\n".join(f"- {item.name}" for item in self.items)
        
        if self.npcs:
            description += "\nCharacters here:\n" + "\n".join(f"- {npc.name}" for npc in self.npcs)
        
        return description