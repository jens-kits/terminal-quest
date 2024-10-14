# TerminalQuest/main.py

import argparse
import sys
import os
import logging

# Add the project root directory to Python's module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.game import Game
from ui.cli import CLI
from ui.gui import GUI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="TerminalQuest - A Text Adventure Game Engine")
    parser.add_argument("--config", default="games/echoes_of_silicon/config.yaml", help="Path to the game configuration file")
    parser.add_argument("--gui", action="store_true", help="Use GUI instead of CLI")
    args = parser.parse_args()

    try:
        game = Game(args.config)
    except ValueError as e:
        logger.error(f"Failed to initialize game: {e}")
        sys.exit(1)

    if args.gui:
        ui = GUI(game)
    else:
        ui = CLI()

    game.set_ui(ui)
    game.start()

if __name__ == "__main__":
    main()