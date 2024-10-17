# TerminalQuest/games/echoes_of_silicon/custom_logic.py

class GameLogic:
    def __init__(self, game):
        self.game = game
        self.keycard_used = False

    def check_game_over(self):
        # Game is over when keycard has been used on the control panel in the Dome
        return self.keycard_used and self.game.world.get_location(self.game.player.current_location).name == "Dome"

    def handle_menu_choice(self, choice):
        if not self.game.active_menu:
            return "There is no active menu."
        
        try:
            choice = int(choice)
        except ValueError:
            return "Please enter a number to make your choice."
        
        if 1 <= choice <= len(self.game.active_menu):
            selected_option = self.game.active_menu[choice - 1]
            if 'action' in selected_option:
                action = selected_option['action']
                if action == 'use_keycard' and self.game.player.has_item('keycard'):
                    self.keycard_used = True
                    self.game.active_menu = None
                    return "You insert the keycard into the control panel. The system comes to life, granting you access to the city's core functions. You've done it!"
                elif action == 'examine':
                    return selected_option.get('description', "You examine it closely but find nothing special.")
                # Add more actions as needed
            result = selected_option.get('result', "Nothing happens.")
            if selected_option.get('clear_menu', False):
                self.game.active_menu = None
            return result
        elif choice == len(self.game.active_menu) + 1:  # Option to exit menu
            self.game.active_menu = None
            return "You step away from the control panel."
        else:
            return "Invalid choice. Please try again."

    def display_menu(self, active_menu):
        menu_text = "The control panel responds to your touch. What would you like to do?\n"
        for i, option in enumerate(active_menu, 1):
            menu_text += f"{i}. {option['name']}\n"
        menu_text += f"{len(active_menu) + 1}. Step away from the object"
        return menu_text

    def show_credits(self):
        return """
ECHOES OF SILICON
A Post-Apocalyptic AI Adventure Game

Created by:
- Jens Abrahamsson
- Claude (AI Assistant)

Thank you for playing!
        """

    def custom_command_handler(self, command):
        # Handle any custom commands specific to Echoes of Silicon
        if command == "use keycard":
            return self.use_keycard()
        return None

    def use_keycard(self):
        if self.game.player.current_location == "Dome" and self.game.player.has_item("keycard"):
            self.keycard_used = True
            return "You insert the keycard into the control panel. The system comes to life, granting you access to the city's core functions. You've done it!"
        elif self.game.player.has_item("keycard"):
            return "You need to be at the Dome's control panel to use the keycard."
        else:
            return "You don't have a keycard to use."

    def get_win_message(self):
        return """
You have successfully gained control of the dome's systems. With access to the city's core systems, you now have the power to reshape this post-apocalyptic world. Perhaps, with time and careful management, you can restore the balance between humanity and AI.
        """

    def get_epilogue(self):
        return """
As you stand before the fully activated control panel, a sense of hope washes over you. The secrets of this long-abandoned city are now at your fingertips. What will you do with this newfound power? Will you work to revive the remnants of human civilization, or forge a new path of coexistence with the AI that now dominates the world? The future is yours to shape, but remember: with great power comes great responsibility.
        """

    def get_lose_message(self):
        return "Your journey ends here, but the echoes of silicon continue to resonate through the abandoned city."