import json
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "wardrobes.json"

CATEGORIES = ["tops", "bottoms", "outerwear", "shoes", "accessories", "dresses"]

OCCASIONS = [
    "casual",
    "work / class",
    "going out",
    "formal / event",
    "outdoor / active",
    "date"
]

WEATHER_OPTIONS = ["hot", "mild", "cold", "rainy"]


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def empty_wardrobe():
    return {
        "tops": [],
        "bottoms": [],
        "outerwear": [],
        "shoes": [],
        "accessories": [],
        "dresses": []
    }


def generate_outfit(wardrobe, occasion, weather):
    outfit = {}

    if wardrobe["dresses"] and occasion in ["formal / event", "date"]:
        outfit["Dress"] = random.choice(wardrobe["dresses"])
    else:
        if wardrobe["tops"]:
            outfit["Top"] = random.choice(wardrobe["tops"])
        if wardrobe["bottoms"]:
            outfit["Bottom"] = random.choice(wardrobe["bottoms"])

    if wardrobe["shoes"]:
        outfit["Shoes"] = random.choice(wardrobe["shoes"])

    if weather in ["cold", "rainy"] and wardrobe["outerwear"]:
        outfit["Outerwear"] = random.choice(wardrobe["outerwear"])

    if wardrobe["accessories"]:
        outfit["Accessory"] = random.choice(wardrobe["accessories"])

    return outfit


class OutfitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Stylist")
        self.root.geometry("600x550")

        self.data = load_data()
        self.username = ""
        self.wardrobe = None

        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()

        title = tk.Label(self.root, text="Welcome to Your Personal Stylist!", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        tk.Label(self.root, text="Enter your username:").pack()

        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=10)

        login_button = tk.Button(self.root, text="Continue", command=self.login)
        login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip().lower()

        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return

        self.username = username

        if username not in self.data:
            self.data[username] = empty_wardrobe()

        self.wardrobe = self.data[username]
        self.create_main_screen()

    def create_main_screen(self):
        self.clear_screen()

        title = tk.Label(self.root, text=f"Hello, {self.username}!", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Category:").grid(row=0, column=0, padx=5)

        self.category_box = ttk.Combobox(frame, values=CATEGORIES, state="readonly")
        self.category_box.grid(row=0, column=1, padx=5)
        self.category_box.current(0)

        tk.Label(frame, text="Item:").grid(row=1, column=0, padx=5, pady=10)

        self.item_entry = tk.Entry(frame, width=30)
        self.item_entry.grid(row=1, column=1, padx=5)

        add_button = tk.Button(frame, text="Add Item", command=self.add_item)
        add_button.grid(row=1, column=2, padx=5)

        self.wardrobe_text = tk.Text(self.root, height=12, width=60)
        self.wardrobe_text.pack(pady=10)

        self.update_wardrobe_display()

        options_frame = tk.Frame(self.root)
        options_frame.pack(pady=10)

        tk.Label(options_frame, text="Occasion:").grid(row=0, column=0, padx=5)

        self.occasion_box = ttk.Combobox(options_frame, values=OCCASIONS, state="readonly")
        self.occasion_box.grid(row=0, column=1, padx=5)
        self.occasion_box.current(0)

        tk.Label(options_frame, text="Weather:").grid(row=1, column=0, padx=5, pady=10)

        self.weather_box = ttk.Combobox(options_frame, values=WEATHER_OPTIONS, state="readonly")
        self.weather_box.grid(row=1, column=1, padx=5)
        self.weather_box.current(1)

        generate_button = tk.Button(self.root, text="Generate Outfit", command=self.show_outfit)
        generate_button.pack(pady=10)

        self.outfit_label = tk.Label(self.root, text="", font=("Arial", 12), justify="left")
        self.outfit_label.pack(pady=10)

        save_button = tk.Button(self.root, text="Save Wardrobe", command=self.save_wardrobe)
        save_button.pack(pady=5)

    def add_item(self):
        category = self.category_box.get()
        item = self.item_entry.get().strip()

        if not item:
            messagebox.showerror("Error", "Please enter an item.")
            return

        if item in self.wardrobe[category]:
            messagebox.showinfo("Duplicate", f"{item} is already in {category}.")
        else:
            self.wardrobe[category].append(item)
            self.item_entry.delete(0, tk.END)
            self.update_wardrobe_display()
            self.save_wardrobe()

    def update_wardrobe_display(self):
        self.wardrobe_text.delete("1.0", tk.END)

        for category, items in self.wardrobe.items():
            if items:
                self.wardrobe_text.insert(tk.END, f"{category.title()}: {', '.join(items)}\n")
            else:
                self.wardrobe_text.insert(tk.END, f"{category.title()}: None\n")

    def show_outfit(self):
        occasion = self.occasion_box.get()
        weather = self.weather_box.get()

        outfit = generate_outfit(self.wardrobe, occasion, weather)

        if not outfit:
            self.outfit_label.config(text="Not enough clothing items to generate an outfit.")
            return

        outfit_text = "Suggested Outfit:\n"
        for key, value in outfit.items():
            outfit_text += f"{key}: {value}\n"

        self.outfit_label.config(text=outfit_text)

    def save_wardrobe(self):
        self.data[self.username] = self.wardrobe
        save_data(self.data)
        messagebox.showinfo("Saved", "Your wardrobe has been saved!")


root = tk.Tk()
app = OutfitApp(root)
root.mainloop()
