# TerminalQuest/engine/event_system.py

class Event:
    def __init__(self, event_type, data=None):
        self.type = event_type
        self.data = data or {}

class EventSystem:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_type, callback):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def remove_listener(self, event_type, callback):
        if event_type in self.listeners and callback in self.listeners[event_type]:
            self.listeners[event_type].remove(callback)

    def dispatch(self, event):
        if event.type in self.listeners:
            for callback in self.listeners[event.type]:
                callback(event)

# Example usage:
# event_system = EventSystem()
# event_system.add_listener("item_picked_up", lambda e: print(f"Player picked up {e.data['item']}"))
# event_system.dispatch(Event("item_picked_up", {"item": "Magic Sword"}))