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
        loading_screen = game_config.get('custom_loading_screen', [])
        for item in loading_screen:
            if item['type'] == 'text':
                self.slow_print(item['content'], color=item.get('color', 'white'), speed=item.get('speed', 0.03))
            elif item['type'] == 'line':
                print(self.colorize(item['content'] * item.get('repeat', 1), item.get('color', 'white')))
            elif item['type'] == 'pause':
                time.sleep(item.get('duration', 1))
            elif item['type'] == 'input':
                input(self.colorize(item['content'], item.get('color', 'white')))

    def show_progress_bar(self):
        for i in range(21):
            sys.stdout.write('\r')
            sys.stdout.write(self.colorize(f"[{'#'*i:20}] {5*i}%", 'green'))
            sys.stdout.flush()
            time.sleep(0.1)
        print()

    def display_intro(self, game_config):
        self.show_loading_screen(game_config)

    def slow_print(self, text, speed=0.03, color='white'):
        for char in text:
            sys.stdout.write(self.colorize(char, color))
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def display_game_over(self, is_win, message, epilogue=None):
        self.clear_screen()
        print(self.colorize("GAME OVER", 'red'))
        print()
        print(self.colorize("=" * 60, 'white'))
        print()
        self.slow_print(message, color='yellow', speed=0.02)
        print()
        print(self.colorize("=" * 60, 'white'))
        print()
        if epilogue:
            print(self.colorize("Epilogue:", 'cyan'))
            self.slow_print(epilogue, color='green', speed=0.02)
            print()
            print(self.colorize("=" * 60, 'white'))
        print()
        print(self.colorize("Thank you for playing!", 'magenta'))
        print()
        input(self.colorize("Press Enter to exit...", 'yellow'))

    def display_location(self, location):
        print(self.colorize(f"\n{location.name}", 'cyan'))
        print(self.colorize("-" * len(location.name), 'cyan'))
        print(self.colorize(location.description, 'green'))

    def get_command(self):
        try:
            return input(self.colorize("\n> ", 'yellow')).strip()
        except EOFError:
            print("\nExiting game...")
            return "quit"
        except KeyboardInterrupt:
            print("\nExiting game...")
            return "quit"

    def display_result(self, result):
        if result:
            print(self.colorize(result, 'white'))

    def display_error(self, error):
        print(self.colorize(f"Error: {error}", 'red'))

    def display_inventory(self, inventory):
        if not inventory:
            print(self.colorize("You are empty-handed.", 'yellow'))
        else:
            print(self.colorize("You are carrying:", 'yellow'))
            for item in inventory:
                print(self.colorize(f"- {item.name}", 'white'))

    def display_health(self, health):
        color = 'green' if health > 50 else 'yellow' if health > 25 else 'red'
        print(self.colorize(f"Health: {health}", color))

    def display_score(self, score):
        print(self.colorize(f"Score: {score}", 'cyan'))

    def display_outro(self, game_config):
        self.clear_screen()
        outro_text = game_config.get('outro_text', [])
        for line in outro_text:
            self.slow_print(line.get('content', ''), color=line.get('color', 'white'), speed=line.get('speed', 0.03))
        print()
        input(self.colorize("Press Enter to exit...", 'green'))