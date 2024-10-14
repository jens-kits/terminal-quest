# TerminalQuest/ui/gui.py

import tkinter as tk
from tkinter import scrolledtext

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

    def start(self):
        self.display_intro()
        self.root.mainloop()

    def display(self, text, tag=None):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text + "\n", tag)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def display_intro(self):
        intro_text = "Welcome to TerminalQuest!\nEmbark on a text-based adventure...\n"
        self.display(intro_text, "intro")

    def display_location(self, location):
        self.display(f"\n{location.name}", "location_name")
        self.display("-" * len(location.name), "location_name")
        self.display(location.description, "description")

        if location.items:
            self.display("\nItems here:", "items_header")
            for item in location.items:
                self.display(f"- {item.name}", "item")

        if location.exits:
            self.display("\nExits:", "exits_header")
            for direction in location.exits:
                self.display(f"- {direction}", "exit")

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

    # Add more methods as needed for inventory, health, score, etc.

# Note: This GUI implementation is basic and would need to be integrated with the game logic.
# You might need to modify the Game class to work with this GUI instead of CLI.