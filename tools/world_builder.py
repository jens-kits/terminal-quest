# TerminalQuest/tools/world_builder.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yaml

class WorldBuilderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("TerminalQuest World Builder")
        self.master.geometry("800x600")

        self.world_data = {
            "game_name": "",
            "start_location": "",
            "locations": [],
            "items": [],
            "npcs": []
        }

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill='both')

        self.create_general_tab()
        self.create_locations_tab()
        self.create_items_tab()
        self.create_npcs_tab()

        # Add Save and Load buttons
        self.save_button = ttk.Button(self.master, text="Save World", command=self.save_world)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.load_button = ttk.Button(self.master, text="Load World", command=self.load_world)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_general_tab(self):
        general_frame = ttk.Frame(self.notebook)
        self.notebook.add(general_frame, text="General")

        ttk.Label(general_frame, text="Game Name:").grid(row=0, column=0, padx=5, pady=5)
        self.game_name_entry = ttk.Entry(general_frame)
        self.game_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(general_frame, text="Start Location:").grid(row=1, column=0, padx=5, pady=5)
        self.start_location_entry = ttk.Entry(general_frame)
        self.start_location_entry.grid(row=1, column=1, padx=5, pady=5)

    def create_locations_tab(self):
        locations_frame = ttk.Frame(self.notebook)
        self.notebook.add(locations_frame, text="Locations")

        self.locations_listbox = tk.Listbox(locations_frame)
        self.locations_listbox.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        locations_buttons_frame = ttk.Frame(locations_frame)
        locations_buttons_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(locations_buttons_frame, text="Add", command=self.add_location).pack(fill=tk.X)
        ttk.Button(locations_buttons_frame, text="Edit", command=self.edit_location).pack(fill=tk.X)
        ttk.Button(locations_buttons_frame, text="Remove", command=self.remove_location).pack(fill=tk.X)

    def create_items_tab(self):
        items_frame = ttk.Frame(self.notebook)
        self.notebook.add(items_frame, text="Items")

        self.items_listbox = tk.Listbox(items_frame)
        self.items_listbox.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        items_buttons_frame = ttk.Frame(items_frame)
        items_buttons_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(items_buttons_frame, text="Add", command=self.add_item).pack(fill=tk.X)
        ttk.Button(items_buttons_frame, text="Edit", command=self.edit_item).pack(fill=tk.X)
        ttk.Button(items_buttons_frame, text="Remove", command=self.remove_item).pack(fill=tk.X)

    def create_npcs_tab(self):
        npcs_frame = ttk.Frame(self.notebook)
        self.notebook.add(npcs_frame, text="NPCs")

        self.npcs_listbox = tk.Listbox(npcs_frame)
        self.npcs_listbox.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        npcs_buttons_frame = ttk.Frame(npcs_frame)
        npcs_buttons_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(npcs_buttons_frame, text="Add", command=self.add_npc).pack(fill=tk.X)
        ttk.Button(npcs_buttons_frame, text="Edit", command=self.edit_npc).pack(fill=tk.X)
        ttk.Button(npcs_buttons_frame, text="Remove", command=self.remove_npc).pack(fill=tk.X)

    # Implement methods for adding, editing, and removing locations, items, and NPCs
    def add_location(self):
        # Implement add location logic
        pass

    def edit_location(self):
        # Implement edit location logic
        pass

    def remove_location(self):
        # Implement remove location logic
        pass

    def add_item(self):
        # Implement add item logic
        pass

    def edit_item(self):
        # Implement edit item logic
        pass

    def remove_item(self):
        # Implement remove item logic
        pass

    def add_npc(self):
        # Implement add NPC logic
        pass

    def edit_npc(self):
        # Implement edit NPC logic
        pass

    def remove_npc(self):
        # Implement remove NPC logic
        pass

    def save_world(self):
        self.world_data["game_name"] = self.game_name_entry.get()
        self.world_data["start_location"] = self.start_location_entry.get()

        file_path = filedialog.asksaveasfilename(defaultextension=".yaml",
                                                 filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                yaml.dump(self.world_data, file)
            messagebox.showinfo("Save Successful", "World data saved successfully!")

    def load_world(self):
        file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.world_data = yaml.safe_load(file)
            self.update_gui_from_world_data()
            messagebox.showinfo("Load Successful", "World data loaded successfully!")

    def update_gui_from_world_data(self):
        # Update GUI elements based on loaded world data
        self.game_name_entry.delete(0, tk.END)
        self.game_name_entry.insert(0, self.world_data.get("game_name", ""))

        self.start_location_entry.delete(0, tk.END)
        self.start_location_entry.insert(0, self.world_data.get("start_location", ""))

        # Update locations, items, and NPCs listboxes
        # Implement this part

if __name__ == "__main__":
    root = tk.Tk()
    app = WorldBuilderGUI(root)
    root.mainloop()