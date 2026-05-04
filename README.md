
# CS-32-Project-Maria-and-Emily


### Project Description
This project is a Python-based outfit generator that acts as a  personal stylist. The program allows users to create a digital wardrobe and generate outfit suggestions based on different constraints such as occasion and weather. Each user can create a profile using a username, and their wardrobe is saved so it can be reused in future sessions.


The purpose of this project is to design and implement the core logic of an outfit recommendation system. The program filters clothing items from a user’s wardrobe and selects pieces that fit the given conditions to create a complete outfit.


### Features
User profiles stored by username
Persistent wardrobe saved in a JSON file (wardrobes.json)
Multiple clothing categories:
  - Tops
  - Bottoms
  - Dresses
  - Outerwear
  - Shoes
  - Accessories
Outfit generation based on:
  - Occasion (casual, work/class, going out, formal/event, outdoor/active, date)
  - Weather (hot, mild, cold, rainy)
  - Randomized outfit suggestions from available clothing items


### How to Run the program
Make sure Python is installed on computer.
Open the project folder in IDE or terminal.


Run the program using:

- pip install Flask
- python3 FPfinal.py
- then open port 5000 on browser through popup


Follow the prompts:
  - Enter a username to create or access your profile
  - Add clothing items by category
  - Select an occasion
  - Enter the weather
  - The program will generate an outfit suggestion based on your inputs.


### Design Choices
A dictionary structure is used to organize wardrobes into categories.
JSON is used for storing user data so it persists between program runs.
Random selection (random.choice) is used to generate outfit combinations.
Dresses are prioritized for formal or date occasions when available.
Outerwear is included only when the weather is cold or rainy.


### Use of external tools
We used the following resources while developing this project:


Python documentation for:
  - json (saving and loading data)
  - os (file handling)
  - random (outfit generation)
Generative AI (ChatGPT) was used to:
  - Help debug parts of the code
  - Suggest improvements to program structure and logic
  - Create code for front end
All code was reviewed, tested, and implemented by us to ensure understanding of how it works.


### Authors
Emily Helms and Maria Gonzalez.
