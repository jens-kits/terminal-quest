# TerminalQuest/ui/cli.py

import os
import time
import sys
import random

class CLI:
    def __init__(self):
        self.color_enabled = True

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def colorize(self, text, color):
        if not self.color_enabled:
            return text
        color_codes = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
        }
        return f"{color_codes.get(color, '')}{text}\033[0m"

    def show_loading_screen(self, game_config):
        self.clear_screen()
        if game_config.get('custom_loading_screen'):
            self.show_custom_loading_screen(game_config)
        else:
            self.show_default_loading_screen(game_config['game_name'])

    def show_default_loading_screen(self, game_name):
        print(self.colorize(f"Loading {game_name}...", 'cyan'))
        print()
        for i in range(21):
            sys.stdout.write('\r')
            sys.stdout.write(self.colorize("[%-20s] %d%%" % ('='*i, 5*i), 'green'))
            sys.stdout.flush()
            time.sleep(0.1)
        print("\n")
        time.sleep(0.5)

    def show_custom_loading_screen(self, game_config):
        loading_screen = game_config['custom_loading_screen']
        for element in loading_screen:
            if element['type'] == 'text':
                self.slow_print(element['content'], speed=element.get('speed', 0.02), color=element.get('color', 'white'))
            elif element['type'] == 'pause':
                time.sleep(element['duration'])
            elif element['type'] == 'input':
                input(self.colorize(element['content'], element.get('color', 'white')))
            elif element['type'] == 'clear':
                self.clear_screen()
            elif element['type'] == 'line':
                print(element['content'] * element.get('repeat', 1))

    def slow_print(self, text, speed=0.02, color='white'):
        for char in text:
            sys.stdout.write(self.colorize(char, color))
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def display_intro(self, game_config):
        self.show_loading_screen(game_config)
        if not game_config.get('custom_loading_screen'):
            self.clear_screen()
            print(self.colorize(f"Welcome to {game_config['game_name']}!", 'cyan'))
            print(self.colorize("Embark on a text-based adventure...", 'yellow'))
            print()
            input(self.colorize("Press Enter to start...", 'green'))

    def display_outro(self, game_name):
        self.clear_screen()
        print(self.colorize(f"Thank you for playing {game_name}!", 'cyan'))
        print(self.colorize("We hope you enjoyed your adventure.", 'yellow'))
        print()
        print(self.colorize("Farewell, adventurer!", 'magenta'))
        print()
        input(self.colorize("Press Enter to exit...", 'green'))

    def display_location(self, location):
        print(self.colorize(f"\n{location.name}", 'cyan'))
        print(self.colorize("-" * len(location.name), 'cyan'))
        print(location.description)
        
        if location.items:
            print(self.colorize("\nItems here:", 'yellow'))
            for item in location.items:
                print(f"- {item.name}")

    def get_command(self):
        return input(self.colorize("\n> ", 'green')).strip()

    def display_result(self, result):
        print(self.colorize(result, 'white'))

    def display_error(self, error):
        print(self.colorize(f"Error: {error}", 'red'))

    def display_inventory(self, inventory):
        if not inventory:
            print(self.colorize("Your inventory is empty.", 'yellow'))
        else:
            print(self.colorize("Inventory:", 'yellow'))
            for item in inventory:
                print(f"- {item.name}")

    def display_health(self, health):
        color = 'green' if health > 50 else 'yellow' if health > 25 else 'red'
        print(self.colorize(f"Health: {health}", color))

    def display_score(self, score):
        print(self.colorize(f"Score: {score}", 'cyan'))