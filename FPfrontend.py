import json
import os
import random
from flask import Flask, render_template_string, request, redirect, url_for

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

        .box {
            background-color: #f2e6ee;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
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
                <p><strong>{{ category.title() }}:</strong>
                {% if items %}
                    {{ items | join(", ") }}
                {% else %}
                    None
                {% endif %}
                </p>
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

                if item and item not in wardrobe[category]:
                    wardrobe[category].append(item)

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
