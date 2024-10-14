# TerminalQuest/plugins/advanced_interactions.py

class AdvancedInteractionsPlugin:
    name = "advanced_interactions"

    @staticmethod
    def execute(game, command):
        if command.startswith("use "):
            return AdvancedInteractionsPlugin.use(game, command[4:])
        elif command.startswith("talk "):
            return AdvancedInteractionsPlugin.talk(game, command[5:])
        elif command.startswith("examine "):
            return AdvancedInteractionsPlugin.examine(game, command[8:])
        return None  # Command not recognized by this plugin

    @staticmethod
    def use(game, item_name):
        item = game.player.get_item(item_name)
        if not item:
            return f"You don't have a {item_name}."
        
        # Check if the item has a custom use method
        if hasattr(item, 'use'):
            return item.use(game.player)
        
        # Default use behavior
        return f"You use the {item.name}, but nothing happens."

    @staticmethod
    def talk(game, npc_name):
        location = game.world.get_location(game.player.current_location)
        npc = next((npc for npc in location.npcs if npc.name.lower() == npc_name.lower()), None)
        if npc:
            return npc.talk()
        return f"There is no {npc_name} here to talk to."

    @staticmethod
    def examine(game, obj_name):
        # First, check player's inventory
        item = game.player.get_item(obj_name)
        if item:
            return item.examine()
        
        # Then, check location items
        location = game.world.get_location(game.player.current_location)
        location_item = next((item for item in location.items if item.name.lower() == obj_name.lower()), None)
        if location_item:
            return location_item.examine()
        
        # Finally, check location objects
        if obj_name in location.objects:
            return location.objects[obj_name]
        
        return f"You don't see any {obj_name} here."

def register_plugin():
    return AdvancedInteractionsPlugin()