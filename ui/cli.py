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
        print(self.colorize("ECHOES OF SILICON", 'cyan'))
        print(self.colorize("Copyright KITS AB 1982", 'yellow'))
        print()
        print(self.colorize("Connecting to ARPANET... please wait", 'green'))
        self.show_progress_bar()
        print(self.colorize("Connection established. Initiating game sequence...", 'green'))
        time.sleep(1)

    def show_progress_bar(self):
        for i in range(21):
            sys.stdout.write('\r')
            sys.stdout.write(self.colorize(f"[{'#'*i:20}] {5*i}%", 'green'))
            sys.stdout.flush()
            time.sleep(0.1)
        print()

    def display_intro(self, game_config):
        self.show_loading_screen(game_config)
        self.clear_screen()
        print(self.colorize("=" * 60, 'white'))
        print(self.colorize("ECHOES OF SILICON", 'cyan'))
        print(self.colorize("Copyright KITS AB 1982", 'yellow'))
        print(self.colorize("A Post-Apocalyptic AI Adventure Game", 'magenta'))
        print(self.colorize("=" * 60, 'white'))
        print()
        self.slow_print("Initializing system...", color='green')
        self.slow_print("Establishing connection to central AI...", color='green')
        self.slow_print("Connection established. Welcome, human.", color='green')
        print()
        self.slow_print("You have returned to Earth after centuries of absence.", color='magenta')
        self.slow_print("The world you once knew is no more. Artificial Intelligence now reigns supreme.", color='magenta')
        self.slow_print("Your mission: Uncover the fate of humanity and restore balance to a world", color='magenta')
        self.slow_print("controlled by machines.", color='magenta')
        print()
        input(self.colorize("Press Enter to begin your adventure...", 'yellow'))

    def slow_print(self, text, speed=0.03, color='white'):
        for char in text:
            sys.stdout.write(self.colorize(char, color))
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def display_game_over(self, is_win, message, epilogue=None):
        self.clear_screen()
        if is_win:
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
            print(self.colorize("Thank you for playing ECHOES OF SILICON!", 'magenta'))
            print()
            print(self.colorize("You were successful this time... but you will soon be made redundant by AI", 'red'))
            print()
        else:
            print(self.colorize("GAME OVER", 'red'))
            print()
            self.slow_print(message, color='yellow')
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

    def display_outro(self, game_name):
        self.clear_screen()
        print(self.colorize(f"Thank you for playing {game_name}!", 'cyan'))
        print(self.colorize("We hope you enjoyed your adventure.", 'yellow'))
        print()
        print(self.colorize("Farewell, human.", 'magenta'))
        print()
        input(self.colorize("Press Enter to exit...", 'green'))