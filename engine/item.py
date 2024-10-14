# TerminalQuest/engine/item.py

class Item:
    def __init__(self, name, description, properties=None):
        self.name = name
        self.description = description
        self.properties = properties or {}

    def __str__(self):
        return self.name

    def examine(self):
        return self.description

    def use(self, player, target=None):
        use_message = self.properties.get('use_message', f"You use the {self.name}.")
        if 'consumable' in self.properties and self.properties['consumable']:
            player.remove_from_inventory(self)
        return use_message

class Weapon(Item):
    def __init__(self, name, description, damage, properties=None):
        super().__init__(name, description, properties)
        self.damage = damage

    def use(self, player, target=None):
        if target:
            damage_dealt = target.take_damage(self.damage)
            return f"You attack {target} with {self.name} for {damage_dealt} damage!"
        return f"You swing the {self.name}, but hit nothing."

class Consumable(Item):
    def __init__(self, name, description, effect, properties=None):
        super().__init__(name, description, properties)
        self.effect = effect

    def use(self, player, target=None):
        effect_result = self.effect(player)
        player.remove_from_inventory(self)
        return f"You use the {self.name}. {effect_result}"