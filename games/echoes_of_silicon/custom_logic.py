# TerminalQuest/games/echoes_of_silicon/custom_logic.py

class EchoesOfSiliconLogic:
    def __init__(self, game):
        self.game = game
        self.keycard_used = False

    def check_win_condition(self):
        if self.keycard_used and self.game.player.current_location == "Dome":
            return True
        return False

    def use_keycard(self):
        if self.game.player.current_location == "Dome" and self.game.player.has_item("keycard"):
            self.keycard_used = True
            return "You insert the keycard into the control panel. The system comes to life, granting you access to the city's core functions. You've done it!"
        elif self.game.player.has_item("keycard"):
            return "You need to be at the Dome's control panel to use the keycard."
        else:
            return "You don't have a keycard to use."

    def custom_command_handler(self, command):
        if command == "use keycard":
            return self.use_keycard()
        return None  # Not a custom command

# This class would be instantiated and used by the main game loop to handle
# game-specific logic and win conditions.