# TerminalQuest/plugins/basic_commands.py

class BasicCommandsPlugin:
    name = "basic_commands"

    @staticmethod
    def execute(game, command):
        if command.startswith("go ") or command in ["n", "s", "e", "w", "north", "south", "east", "west"]:
            return BasicCommandsPlugin.move(game, command)
        elif command == "look" or command == "l":
            return BasicCommandsPlugin.look(game)
        elif command == "inventory" or command == "i":
            return BasicCommandsPlugin.inventory(game)
        elif command.startswith("take "):
            return BasicCommandsPlugin.take(game, command[5:])
        elif command.startswith("drop "):
            return BasicCommandsPlugin.drop(game, command[5:])
        elif command.startswith("examine ") or command.startswith("x "):
            return BasicCommandsPlugin.examine(game, command.split(maxsplit=1)[1])
        elif command.startswith("use ") or command.startswith("interact "):
            return BasicCommandsPlugin.interact(game, command.split(maxsplit=1)[1])
        elif command == "hint":
            return BasicCommandsPlugin.hint(game)
        elif command == "help":
            return BasicCommandsPlugin.help(game)
        elif command == "credits":
            return game.game_logic.show_credits()
        elif command in ["quit", "exit", "logout"]:
            return BasicCommandsPlugin.logout(game)
        return None  # Command not recognized by this plugin

    @staticmethod
    def move(game, command):
        return game.move_player(command)

    @staticmethod
    def look(game):
        return game.look()

    @staticmethod
    def inventory(game):
        return game.display_inventory()

    @staticmethod
    def take(game, item_name):
        return game.take_item(item_name)

    @staticmethod
    def drop(game, item_name):
        return game.drop_item(item_name)

    @staticmethod
    def examine(game, obj_name):
        return game.examine_object(obj_name)

    @staticmethod
    def interact(game, obj_name):
        return game.interact_with_object(obj_name)

    @staticmethod
    def hint(game):
        return game.get_hint()

    @staticmethod
    def help(game):
        return game.show_help()

    @staticmethod
    def logout(game):
        game.end_game()
        return "Thank you for playing. Goodbye!"

def register_plugin():
    return BasicCommandsPlugin()