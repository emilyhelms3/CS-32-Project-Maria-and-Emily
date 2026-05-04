import json
import os
import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

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


def item_matches_keywords(item, keywords):
    item = item.lower()
    return any(keyword in item for keyword in keywords)


def choose_best_item(items, keywords):
    matching_items = [
        item for item in items
        if item_matches_keywords(item, keywords)
    ]

    if matching_items:
        return random.choice(matching_items)

    return random.choice(items) if items else None


def generate_outfit(wardrobe, occasion, weather):
    outfit = {}

    weather_keywords = {
        "hot": ["tank", "t-shirt", "tee", "short sleeve", "shorts", "skirt", "sandals"],
        "mild": ["t-shirt", "tee", "jeans", "sneakers", "cardigan"],
        "cold": ["sweater", "hoodie", "long sleeve", "jeans", "boots", "coat", "jacket"],
        "rainy": ["jacket", "raincoat", "boots", "sneakers", "hoodie"]
    }

    occasion_keywords = {
        "casual": ["t-shirt", "tee", "hoodie", "jeans", "leggings", "sneakers"],
        "work / class": ["blouse", "sweater", "cardigan", "jeans", "pants", "flats", "sneakers"],
        "going out": ["nice", "black", "skirt", "dress", "boots", "heels"],
        "formal / event": ["dress", "blouse", "skirt", "heels", "flats", "blazer"],
        "outdoor / active": ["t-shirt", "tee", "shorts", "leggings", "sneakers", "hoodie"],
        "date": ["dress", "skirt", "nice", "blouse", "boots", "heels"]
    }

    keywords = weather_keywords.get(weather, []) + occasion_keywords.get(occasion, [])

    if occasion in ["formal / event", "date"] and wardrobe["dresses"]:
        dress = choose_best_item(wardrobe["dresses"], keywords)
        outfit["Dress"] = dress
    else:
        top = choose_best_item(wardrobe["tops"], keywords)
        bottom = choose_best_item(wardrobe["bottoms"], keywords)

        if top:
            outfit["Top"] = top
        if bottom:
            outfit["Bottom"] = bottom

    shoes = choose_best_item(wardrobe["shoes"], keywords)
    if shoes:
        outfit["Shoes"] = shoes

    if weather in ["cold", "rainy"] and wardrobe["outerwear"]:
        outerwear = choose_best_item(wardrobe["outerwear"], keywords)
        outfit["Outerwear"] = outerwear

    accessory = choose_best_item(wardrobe["accessories"], keywords)
    if accessory:
        outfit["Accessory"] = accessory

    if weather == "hot":
        outfit["Weather Note"] = "Hot weather: lighter clothes are recommended."
    elif weather == "cold":
        outfit["Weather Note"] = "Cold weather: layering is recommended."
    elif weather == "rainy":
        outfit["Weather Note"] = "Rainy weather: waterproof shoes or a jacket are recommended."

    return outfit


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Personal Stylist</title>

    <style>
        body {
            font-family: Arial;
            background-color: #f7f0f5;
            padding: 30px;
        }

        .container {
            max-width: 750px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
        }

        h1, h2 {
            color: #8b3a62;
        }

        input, select, button {
            padding: 8px;
            margin: 5px;
        }

        button {
            background-color: #8b3a62;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }

        .remove-button {
            background-color: #cc5c5c;
            margin-left: 10px;
        }

        .box {
            background-color: #f2e6ee;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }

        li {
            margin-bottom: 8px;
        }
    </style>
</head>

<body>
<div class="container">
    <h1>Welcome to Your Personal Stylist!</h1>

    <form method="POST" action="/">
        <label>Username:</label>
        <input type="text" name="username" value="{{ username }}" required>
        <button type="submit" name="action" value="login">Log In / Create Profile</button>
    </form>

    {% if username %}
        <h2>Hello, {{ username }}!</h2>

        <div class="box">
            <h2>Add Clothes</h2>

            <form method="POST" action="/">
                <input type="hidden" name="username" value="{{ username }}">

                <select name="category">
                    {% for category in categories %}
                        <option value="{{ category }}">{{ category.title() }}</option>
                    {% endfor %}
                </select>

                <input type="text" name="item" placeholder="Item name" required>

                <button type="submit" name="action" value="add">Add Item</button>
            </form>
        </div>

        <div class="box">
            <h2>Your Wardrobe</h2>

            {% for category, items in wardrobe.items() %}
                <p><strong>{{ category.title() }}:</strong></p>

                {% if items %}
                    <ul>
                        {% for item in items %}
                            <li>
                                {{ item }}

                                <form method="POST" action="/" style="display:inline;">
                                    <input type="hidden" name="username" value="{{ username }}">
                                    <input type="hidden" name="category" value="{{ category }}">
                                    <input type="hidden" name="item" value="{{ item }}">

                                    <button class="remove-button" type="submit" name="action" value="remove">
                                        Remove
                                    </button>
                                </form>
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p>None</p>
                {% endif %}
            {% endfor %}
        </div>

        <div class="box">
            <h2>Generate Outfit</h2>

            <form method="POST" action="/">
                <input type="hidden" name="username" value="{{ username }}">

                <label>Occasion:</label>
                <select name="occasion">
                    {% for occasion in occasions %}
                        <option value="{{ occasion }}">{{ occasion }}</option>
                    {% endfor %}
                </select>

                <label>Weather:</label>
                <select name="weather">
                    {% for weather in weather_options %}
                        <option value="{{ weather }}">{{ weather }}</option>
                    {% endfor %}
                </select>

                <button type="submit" name="action" value="generate">Generate Outfit</button>
            </form>
        </div>

        {% if outfit %}
            <div class="box">
                <h2>Suggested Outfit</h2>

                {% for key, value in outfit.items() %}
                    <p><strong>{{ key }}:</strong> {{ value }}</p>
                {% endfor %}
            </div>
        {% endif %}
    {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    data = load_data()
    username = ""
    wardrobe = None
    outfit = None

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        action = request.form.get("action")

        if username:
            if username not in data:
                data[username] = empty_wardrobe()

            wardrobe = data[username]

            if action == "add":
                category = request.form.get("category")
                item = request.form.get("item", "").strip()

                # Avoid adding the same clothing item twice.
                if item and item not in wardrobe[category]:
                    wardrobe[category].append(item)

                data[username] = wardrobe
                save_data(data)

            elif action == "remove":
                category = request.form.get("category")
                item = request.form.get("item", "").strip()

                # Remove the selected item from the correct clothing category.
                if item in wardrobe.get(category, []):
                    wardrobe[category].remove(item)

                data[username] = wardrobe
                save_data(data)

            elif action == "generate":
                occasion = request.form.get("occasion")
                weather = request.form.get("weather")

                outfit = generate_outfit(wardrobe, occasion, weather)

            save_data(data)

    return render_template_string(
        HTML,
        username=username,
        wardrobe=wardrobe,
        categories=CATEGORIES,
        occasions=OCCASIONS,
        weather_options=WEATHER_OPTIONS,
        outfit=outfit
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
