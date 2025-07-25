# Vegetarian Recipe Chatbot

A conversational AI chatbot designed to suggest vegetarian recipes using natural language processing (NLP) techniques. Built with Hugging Face Transformers and deployed via Gradio, this project provides an interactive interface for users to explore 10 unique vegetarian recipes.

## Features
- Suggests vegetarian recipes based on user input (e.g., "Suggest a tofu recipe").
- Uses the BlenderBot-400M-distill model for general conversation.
- Includes 10 vegetarian recipes: Tofu Stir-Fry, Lentil Curry, Creamy Mushroom Pasta, Quinoa Veggie Bowl, Vegetable Minestrone Soup, Chickpea Salad, Eggplant Parmesan, Stuffed Sweet Potatoes, Spinach and Ricotta Stuffed Shells, and Vegan Chocolate Mousse.
- Rule-based intent recognition and entity extraction for recipe suggestions.
- Deployable locally with a web-based Gradio interface.

## Requirements
- Python 3.11 or later
- Libraries: `transformers`, `torch`, `gradio`
- Install dependencies:
  ```bash
  pip install transformers torch gradio


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Vegetarian-Recipe-Chatbot.git
   cd Vegetarian-Recipe-Chatbot
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the chatbot:
   ```bash
   python recipe_chatbot.py
   ```
   - Access the interface at `http://localhost:7860` in your browser.

## Usage
- Enter a message like "Suggest a vegetarian pasta recipe" to get a recipe.
- Use "Hello" or general questions to engage in conversation.
- The chatbot will only provide vegetarian recipes from its database.
