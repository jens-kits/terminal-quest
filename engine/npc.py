# TerminalQuest/engine/npc.py

class NPC:
    def __init__(self, name, description, dialogue):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.inventory = []

    def __str__(self):
        return self.name

    def examine(self):
        return self.description

    def talk(self):
        return self.dialogue['greeting']

    def respond(self, keyword):
        return self.dialogue.get(keyword, "I don't know anything about that.")

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

class Enemy(NPC):
    def __init__(self, name, description, dialogue, health, damage):
        super().__init__(name, description, dialogue)
        self.health = health
        self.damage = damage

    def attack(self, target):
        damage_dealt = target.change_health(-self.damage)
        return f"{self.name} attacks {target} for {damage_dealt} damage!"

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        return amount