# TerminalQuest/engine/world.py

from .item import Item
from .npc import NPC
import logging
import random

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
                location.exits[exit_dir] = exit_loc
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

    def get_hint(self, location_name):
        location = self.get_location(location_name)
        if location:
            return location.hint
        return "There are no specific hints for this location. Keep exploring!"

class Location:
    def __init__(self, data):
        self.name = data['name']
        self.description = data['description']
        self.exits = {}
        self.items = []
        self.npcs = []
        self.objects = data.get('objects', {})
        self.hint = data.get('hint', "There's nothing specific to hint at here. Keep exploring!")
        self.interactions = data.get('interactions', {})
        self.state = {}  # To keep track of location-specific states

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
        return next((item for item in self.items if item_name.lower() in item.name.lower()), None)

    def get_npc(self, npc_name):
        return next((npc for npc in self.npcs if npc_name.lower() in npc.name.lower()), None)

    def get_object(self, object_name):
        for name, description in self.objects.items():
            if object_name.lower() in name.lower():
                return description
        return None

    def interact_with_object(self, object_name, player):
        for name, interaction in self.interactions.items():
            if object_name.lower() in name.lower():
                if callable(interaction):
                    return interaction(self, player)
                elif isinstance(interaction, dict):
                    return self.handle_complex_interaction(interaction, player)
                else:
                    return interaction
        return f"You interact with the {object_name}, but nothing special happens."

    def handle_complex_interaction(self, interaction, player):
        if 'condition' in interaction:
            condition = interaction['condition']
            if condition == 'has_item' and 'item' in interaction:
                if player.has_item(interaction['item']):
                    return interaction.get('success', "You successfully use the item.")
                else:
                    return interaction.get('failure', f"You need the {interaction['item']} to do this.")
        elif 'menu' in interaction:
            return {'menu': interaction['menu']}
        return interaction.get('default', "Nothing happens.")

    def describe(self):
        description = f"{self.name}\n{'-' * len(self.name)}\n{self.description}"

        if self.items:
            item_descriptions = [f"You see {item.name} here." for item in self.items]
            description += f" {random.choice(item_descriptions)}"

        if self.exits:
            exit_descriptions = [
                "You can see paths leading in multiple directions.",
                "There are several ways to leave this area.",
                "You notice exits in various directions."
            ]
            description += f" {random.choice(exit_descriptions)}"

        return description

    def get_available_directions(self):
        return list(self.exits.keys())