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
        elif command == "help":
            return BasicCommandsPlugin.help()
        return None  # Command not recognized by this plugin

    @staticmethod
    def move(game, command):
        direction = command.split()[-1][0].lower()  # Get first letter of last word
        current_location = game.world.get_location(game.player.current_location)
        if current_location is None:
            return "Error: You are in an invalid location."
        
        new_location_name = current_location.get_exit(direction)
        if new_location_name:
            game.player.current_location = new_location_name
            new_location = game.world.get_location(new_location_name)
            if new_location is None:
                return f"Error: Invalid destination '{new_location_name}'. Staying in current location."
            return f"You move {direction}.\n\n" + new_location.describe()
        else:
            return "You can't go that way."

    @staticmethod
    def look(game):
        location = game.world.get_location(game.player.current_location)
        if location is None:
            return "Error: You are in an invalid location."
        return location.describe()

    @staticmethod
    def inventory(game):
        if not game.player.inventory:
            return "Your inventory is empty."
        return "Inventory:\n" + "\n".join(f"- {item.name}" for item in game.player.inventory)

    @staticmethod
    def take(game, item_name):
        location = game.world.get_location(game.player.current_location)
        if location is None:
            return "Error: You are in an invalid location."
        item = next((item for item in location.items if item_name.lower() in item.name.lower()), None)
        if item:
            game.player.add_to_inventory(item)
            location.remove_item(item)
            return f"You take the {item.name}."
        return f"There is no {item_name} here."

    @staticmethod
    def drop(game, item_name):
        item = next((item for item in game.player.inventory if item_name.lower() in item.name.lower()), None)
        if item:
            game.player.remove_from_inventory(item)
            location = game.world.get_location(game.player.current_location)
            if location:
                location.add_item(item)
                return f"You drop the {item.name}."
            else:
                return "Error: You are in an invalid location. Item not dropped."
        return f"You don't have a {item_name}."

    @staticmethod
    def help():
        return """Available commands:
- look (l): Examine your surroundings
- go [direction] or n/s/e/w: Move in a direction
- inventory (i): Check your inventory
- take [item]: Pick up an item
- drop [item]: Drop an item from your inventory
- help: Show this help message"""