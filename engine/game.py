# TerminalQuest/engine/game.py

import logging
from engine.world import World
from engine.player import Player
from plugins import load_plugins
from utils.config_loader import load_config
from utils.text_processor import process_text
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Game:
    def __init__(self, config_file):
        logger.info(f"Initializing game with config file: {config_file}")
        self.config = load_config(config_file)
        if self.config is None:
            logger.error(f"Failed to load configuration from {config_file}")
            raise ValueError(f"Failed to load configuration from {config_file}")
        
        self.game_name = self.config.get('game_name', 'ECHOES OF SILICON')
        
        self.world = World(self.config)
        self.player = Player(self.config.get('start_location', 'start'))
        self.plugins = load_plugins()
        
        self.ui = None
        self.running = False
        self.variables = {}  # Game state variables
        self.custom_commands = self.config.get('custom_commands', {})
        if not isinstance(self.custom_commands, dict):
            self.custom_commands = {}

    def set_ui(self, ui):
        self.ui = ui

    def start(self):
        if not self.ui:
            raise ValueError("UI has not been set. Call set_ui() before starting the game.")
        self.ui.display_intro(self.config)
        self.running = True
        self.game_loop()

    def game_loop(self):
        self.display_current_location()  # Display initial location
        while self.running:
            command = self.ui.get_command()
            
            if command is None or command.strip() == "":
                continue
            
            result = self.process_command(command)
            if result:
                self.ui.display_result(result)

    def process_command(self, command):
        try:
            command = command.lower()
            
            if command in self.custom_commands:
                return self.execute_custom_command(command)
            
            for plugin in self.plugins:
                result = plugin.execute(self, command)
                if result is not None:
                    return result
            
            if command in ["n", "s", "e", "w", "north", "south", "east", "west"]:
                return self.move_player(command)
            
            elif command in ["look", "l"]:
                return self.look()
            
            elif command in ["inventory", "i"]:
                return self.display_inventory()
            
            elif command.startswith("take "):
                item_name = command[5:].strip()
                return self.take_item(item_name)
            
            elif command.startswith("drop "):
                item_name = command[5:].strip()
                return self.drop_item(item_name)
            
            elif command.startswith("examine "):
                obj_name = command[8:].strip()
                return self.examine_object(obj_name)
            
            elif command.startswith("use "):
                item_name = command[4:].strip()
                return self.use_item(item_name)
            
            elif command == "help":
                return self.show_help()
            
            elif command == "hint":
                return self.get_hint()
            
            elif command == "license":
                return self.show_license()
            
            elif command in ["quit", "exit"]:
                self.end_game()
                return "Thanks for playing!"
            
            return "I don't understand that command."
        except Exception as e:
            logger.exception(f"Error processing command '{command}': {str(e)}")
            return f"An error occurred while processing your command. Please try again."

    def move_player(self, direction):
        direction = direction[0].lower()
        current_location = self.world.get_location(self.player.current_location)
        if current_location is None:
            return "You are in an invalid location."
        new_location_name = current_location.get_exit(direction)
        if new_location_name:
            self.player.current_location = new_location_name
            return self.display_current_location()
        return "You can't go that way."

    def look(self):
        return self.display_current_location()

    def display_current_location(self):
        location = self.world.get_location(self.player.current_location)
        if location:
            self.ui.display_location(location)
            return ""  # Return empty string as we've already displayed the location
        else:
            return "You are in an invalid location."

    def take_item(self, item_name):
        location = self.world.get_location(self.player.current_location)
        if location is None:
            return "You are in an invalid location."
        item = location.get_item(item_name)
        if item:
            self.player.add_to_inventory(item)
            location.remove_item(item)
            return f"Taken."
        return f"I don't see that here."

    def drop_item(self, item_name):
        item = self.player.get_item(item_name)
        if item:
            self.player.remove_from_inventory(item)
            location = self.world.get_location(self.player.current_location)
            if location:
                location.add_item(item)
                return f"Dropped."
            else:
                return "You are in an invalid location."
        return f"You don't have that."

    def examine_object(self, obj_name):
        location = self.world.get_location(self.player.current_location)
        if location is None:
            return "You are in an invalid location."
        
        # Check player's inventory
        for item in self.player.inventory:
            if obj_name.lower() in item.name.lower():
                return item.examine()
        
        # Check location items
        for item in location.items:
            if obj_name.lower() in item.name.lower():
                return item.examine()
        
        # Check location objects
        obj_description = location.get_object(obj_name)
        if obj_description:
            return obj_description
        
        return f"You don't see any {obj_name} here."

    def use_item(self, item_name):
        item = self.player.get_item(item_name)
        if item:
            if hasattr(item, 'use'):
                return item.use(self.player)
            return f"You can't use that."
        return f"You don't have that."

    def show_help(self):
        help_text = """
Available commands:
N, S, E, W - Move in a direction
LOOK - Examine your surroundings
INVENTORY - Check your inventory
TAKE [item] - Pick up an item
DROP [item] - Drop an item
EXAMINE [object] - Look closely at an object
USE [item] - Use an item
HINT - Get a hint for the current location
HELP - Show this help message
LICENSE - Show the game's license information
QUIT - End the game
        """
        return help_text.strip()

    def get_hint(self):
        return self.world.get_hint(self.player.current_location)

    def show_license(self):
        license_text = """
MIT License

Copyright (c) 2024 KITS AB

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
        """
        return license_text.strip()

    def display_inventory(self):
        if not self.player.inventory:
            return "You are empty-handed."
        return "You are carrying:\n" + "\n".join(f"- {item.name}" for item in self.player.inventory)

    def execute_custom_command(self, command):
        command_data = self.custom_commands.get(command)