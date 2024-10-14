# TerminalQuest/engine/game.py

import logging
from engine.world import World
from engine.player import Player
from plugins import load_plugins
from utils.config_loader import load_config

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
        for plugin in self.plugins:
            result = plugin.execute(self, command)
            if result is not None:
                return result
        return "I don't understand that command."

    def end_game(self):
        logger.info("Ending game")
        self.running = False
        self.ui.display_outro(self.game_name)