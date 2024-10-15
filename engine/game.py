# TerminalQuest/engine/game.py

import logging
from engine.world import World
from engine.player import Player
from plugins import load_plugins
from utils.config_loader import load_config
from utils.text_processor import process_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Game:
    def __init__(self, config_file):
        logger.info(f"Initializing game with config file: {config_file}")
        self.config = load_config(config_file)
        if self.config is None:
            logger.error(f"Failed to load configuration from {config_file}")
            raise ValueError(f"Failed to load configuration from {config_file}")
        
        self.game_name = self.config.get('game_name', 'TerminalQuest Game')
        
        logger.info("Creating world")
        self.world = World(self.config)
        
        logger.info("Creating player")
        self.player = Player(self.config.get('start_location', 'start'))
        
        logger.info("Loading plugins")
        self.plugins = load_plugins()
        
        self.ui = None
        self.running = False
        self.variables = {}  # Game state variables
        self.custom_commands = self.config.get('custom_commands', {})
        logger.info("Game initialization complete")

    def set_ui(self, ui):
        logger.info(f"Setting UI: {type(ui).__name__}")
        self.ui = ui

    def start(self):
        if not self.ui:
            logger.error("UI has not been set before starting the game")
            raise ValueError("UI has not been set. Call set_ui() before starting the game.")
        logger.info("Starting game")
        self.ui.display_intro(self.config)
        self.running = True
        self.game_loop()

    def game_loop(self):
        logger.info("Entering game loop")
        while self.running:
            current_location = self.world.get_location(self.player.current_location)
            if current_location is None:
                logger.error(f"Invalid location: {self.player.current_location}")
                self.ui.display_error(f"Error: You are in an invalid location. Returning to starting location.")
                self.player.current_location = self.config.get('start_location', 'start')
                continue
            
            self.ui.display_location(current_location)
            command = self.ui.get_command()
            result = self.process_command(command)
            self.ui.display_result(result)

    def process_command(self, command):
        logger.debug(f"Processing command: {command}")
        
        if command in self.custom_commands:
            return self.execute_custom_command(command)
        
        for plugin in self.plugins:
            result = plugin.execute(self, command)
            if result is not None:
                return result
        
        if command.startswith("go ") or command in ["n", "s", "e", "w", "north", "south", "east", "west"]:
            new_location = self.move_player(command)
            if new_location:
                self.ui.display_location(new_location)
                return "You have moved to a new location."
            return "You can't go that way."
        
        elif command == "look" or command == "l":
            return self.world.get_location(self.player.current_location).describe()
        
        elif command == "inventory" or command == "i":
            self.ui.display_inventory(self.player.inventory)
            return "Displayed inventory."
        
        elif command.startswith("take "):
            item_name = command[5:]
            return self.take_item(item_name)
        
        elif command.startswith("drop "):
            item_name = command[5:]
            return self.drop_item(item_name)
        
        elif command.startswith("examine ") or command.startswith("x "):
            obj_name = command.split(maxsplit=1)[1]
            return self.examine_object(obj_name)
        
        elif command.startswith("use "):
            item_name = command[4:]
            return self.use_item(item_name)
        
        elif command == "help":
            return self.show_help()
        
        elif command == "quit" or command == "exit":
            self.end_game()
            return "Thanks for playing!"
        
        return "I don't understand that command."

    def move_player(self, direction):
        if direction.startswith("go "):
            direction = direction[3:]
        direction = direction[0].lower()  # Get first letter of direction
        current_location = self.world.get_location(self.player.current_location)
        new_location_name = current_location.get_exit(direction)
        if new_location_name:
            self.player.current_location = new_location_name
            return self.world.get_location(new_location_name)
        return None

    def take_item(self, item_name):
        location = self.world.get_location(self.player.current_location)
        item = location.get_item(item_name)
        if item:
            self.player.add_to_inventory(item)
            location.remove_item(item)
            return f"You take the {item.name}."
        return f"There is no {item_name} here to take."

    def drop_item(self, item_name):
        item = self.player.get_item(item_name)
        if item:
            self.player.remove_from_inventory(item)
            location = self.world.get_location(self.player.current_location)
            location.add_item(item)
            return f"You drop the {item.name}."
        return f"You don't have a {item_name} to drop."

    def examine_object(self, obj_name):
        location = self.world.get_location(self.player.current_location)
        
        # Check inventory
        item = self.player.get_item(obj_name)
        if item:
            return item.examine()
        
        # Check location items
        item = location.get_item(obj_name)
        if item:
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
            return f"You can't use the {item.name}."
        return f"You don't have a {item_name} to use."

    def show_help(self):
        help_text = """
Available commands:
- look (l): Examine your surroundings
- go [direction] or n/s/e/w: Move in a direction
- inventory (i): Check your inventory
- take [item]: Pick up an item
- drop [item]: Drop an item from your inventory
- examine (x) [object]: Look closely at an object
- use [item]: Use an item from your inventory
- help: Show this help message
- quit/exit: End the game
        """
        return help_text.strip()

    def execute_custom_command(self, command):
        command_data = self.custom_commands[command]
        if 'text' in command_data:
            return process_text(command_data['text'], self.variables)
        elif 'action' in command_data:
            # Execute a predefined action
            return self.execute_action(command_data['action'])
        else:
            return f"Invalid custom command: {command}"

    def execute_action(self, action):
        # Implement custom action execution logic here
        return f"Executing action: {action}"

    def end_game(self):
        logger.info("Ending game")
        self.running = False
        self.ui.display_outro(self.game_name)

    def display_text(self, text):
        processed_text = process_text(text, self.variables)
        self.ui.display(processed_text)