# TerminalQuest/ui/gui.py

import tkinter as tk
from tkinter import scrolledtext
import re

class GUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("TerminalQuest")
        self.setup_ui()

    def setup_ui(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=24)
        self.text_area.pack(padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED)

        self.input_field = tk.Entry(self.root, width=70)
        self.input_field.pack(side=tk.LEFT, padx=10, pady=10)
        self.input_field.bind("<Return>", self.process_command)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.process_command)
        self.submit_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.setup_text_tags()

    def setup_text_tags(self):
        self.text_area.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
        self.text_area.tag_configure("italic", font=("TkDefaultFont", 10, "italic"))
        self.text_area.tag_configure("underline", underline=1)
        self.text_area.tag_configure("location_name", foreground="cyan", font=("TkDefaultFont", 12, "bold"))
        self.text_area.tag_configure("description", foreground="white")
        self.text_area.tag_configure("items_header", foreground="yellow", font=("TkDefaultFont", 10, "bold"))
        self.text_area.tag_configure("objects_header", foreground="yellow", font=("TkDefaultFont", 10, "bold"))
        self.text_area.tag_configure("npcs_header", foreground="yellow", font=("TkDefaultFont", 10, "bold"))
        self.text_area.tag_configure("exits_header", foreground="yellow", font=("TkDefaultFont", 10, "bold"))
        self.text_area.tag_configure("item", foreground="light green")
        self.text_area.tag_configure("object", foreground="light blue")
        self.text_area.tag_configure("npc", foreground="light pink")
        self.text_area.tag_configure("exit", foreground="light yellow")
        self.text_area.tag_configure("error", foreground="red")
        self.text_area.tag_configure("command", foreground="green")

    def start(self):
        self.display_intro()
        self.root.mainloop()

    def display(self, text, tag=None):
        self.text_area.config(state=tk.NORMAL)
        if tag:
            self.text_area.insert(tk.END, text + "\n", tag)
        else:
            for segment in re.split(r'(\*\*.*?\*\*|\*.*?\*|_.*?_)', text):
                if segment.startswith('**') and segment.endswith('**'):
                    self.text_area.insert(tk.END, segment[2:-2], "bold")
                elif segment.startswith('*') and segment.endswith('*'):
                    self.text_area.insert(tk.END, segment[1:-1], "italic")
                elif segment.startswith('_') and segment.endswith('_'):
                    self.text_area.insert(tk.END, segment[1:-1], "underline")
                else:
                    self.text_area.insert(tk.END, segment)
            self.text_area.insert(tk.END, "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def display_intro(self):
        intro_text = "Welcome to TerminalQuest!\nEmbark on a text-based adventure...\n"
        self.display(intro_text, "description")

    def display_location(self, location):
        self.display(f"\n{location.name}", "location_name")
        self.display("-" * len(location.name), "location_name")
        self.display(location.description, "description")

        if location.items:
            self.display("\nYou can take the following items:", "items_header")
            for item in location.items:
                self.display(f"- {item.name}", "item")

        if location.objects:
            self.display("\nYou can examine the following:", "objects_header")
            for obj in location.objects.keys():
                self.display(f"- {obj}", "object")

        if location.npcs:
            self.display("\nCharacters here:", "npcs_header")
            for npc in location.npcs:
                self.display(f"- {npc.name}", "npc")

        if location.exits:
            self.display("\nExits:", "exits_header")
            for direction, loc in location.exits.items():
                self.display(f"- {direction.capitalize()}: {loc}", "exit")

    def get_command(self):
        # This method is not used in GUI mode, as commands are processed via the input field
        pass

    def process_command(self, event=None):
        command = self.input_field.get()
        self.input_field.delete(0, tk.END)
        self.display(f"> {command}", "command")
        result = self.game.process_command(command)
        self.display(result)

    def display_error(self, error):
        self.display(f"Error: {error}", "error")

    def display_inventory(self, inventory):
        if not inventory:
            self.display("Your inventory is empty.", "description")
        else:
            self.display("Inventory:", "items_header")
            for item in inventory:
                self.display(f"- {item.name}", "item")

    def display_health(self, health):
        color = "green" if health > 50 else "yellow" if health > 25 else "red"
        self.display(f"Health: {health}", color)

    def display_score(self, score):
        self.display(f"Score: {score}", "description")

    def display_outro(self, game_name):
        outro_text = f"""
Thank you for playing {game_name}!
We hope you enjoyed your adventure.

Farewell, adventurer!
        """
        self.display(outro_text, "description")