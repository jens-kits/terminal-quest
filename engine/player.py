# TerminalQuest/engine/player.py

class Player:
    def __init__(self, starting_location):
        self.current_location = starting_location
        self.inventory = []
        self.health = 100
        self.score = 0

    def move_to(self, new_location):
        self.current_location = new_location

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def has_item(self, item_name):
        return any(item.name.lower() == item_name.lower() for item in self.inventory)

    def get_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def change_health(self, amount):
        self.health += amount
        if self.health < 0:
            self.health = 0
        elif self.health > 100:
            self.health = 100

    def change_score(self, amount):
        self.score += amount