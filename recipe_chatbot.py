import gradio as gr
from transformers import pipeline, Conversation
import re

# Initialize the conversational model
chatbot = pipeline(model="facebook/blenderbot-400M-distill", task="conversational")

# Vegetarian recipe database (10 recipes)
recipe_db = {
    "tofu": {
        "name": "Tofu Stir-Fry",
        "ingredients": ["tofu", "soy sauce", "bell peppers", "broccoli", "garlic", "ginger", "sesame oil"],
        "instructions": "1. Press and cube tofu. 2. Heat sesame oil, sauté garlic and ginger. 3. Add tofu and stir-fry until golden. 4. Add bell peppers, broccoli, and soy sauce; cook until tender."
    },
    "lentil": {
        "name": "Lentil Curry",
        "ingredients": ["lentils", "coconut milk", "tomatoes", "onion", "curry powder", "garlic", "ginger"],
        "instructions": "1. Sauté onion, garlic, and ginger. 2. Add curry powder, tomatoes, and coconut milk. 3. Stir in lentils and simmer for 30 minutes. 4. Serve with rice."
    },
    "pasta": {
        "name": "Creamy Mushroom Pasta",
        "ingredients": ["pasta", "mushrooms", "cream", "parmesan", "garlic", "olive oil", "parsley"],
        "instructions": "1. Boil pasta until al dente. 2. Sauté garlic and mushrooms in olive oil. 3. Add cream and simmer. 4. Toss pasta in sauce, top with parmesan and parsley."
    },
    "quinoa": {
        "name": "Quinoa Veggie Bowl",
        "ingredients": ["quinoa", "black beans", "avocado", "corn", "tomato", "lime", "cilantro"],
        "instructions": "1. Cook quinoa according to package. 2. Mix with black beans, corn, and diced tomato. 3. Top with avocado slices and cilantro. 4. Squeeze lime juice over the bowl."
    },
    "soup": {
        "name": "Vegetable Minestrone Soup",
        "ingredients": ["zucchini", "carrots", "celery", "tomato", "vegetable broth", "pasta", "beans"],
        "instructions": "1. Sauté carrots, celery, and zucchini. 2. Add tomatoes and vegetable broth. 3. Simmer with pasta and beans for 20 minutes. 4. Season with salt and pepper."
    },
    "chickpea": {
        "name": "Chickpea Salad",
        "ingredients": ["chickpeas", "cucumber", "tomato", "red onion", "feta cheese", "olive oil", "lemon juice"],
        "instructions": "1. Rinse and drain chickpeas. 2. Chop cucumber, tomato, and red onion. 3. Toss with olive oil, lemon juice, and crumbled feta. 4. Chill before serving."
    },
    "eggplant": {
        "name": "Eggplant Parmesan",
        "ingredients": ["eggplant", "marinara sauce", "mozzarella", "parmesan", "breadcrumbs", "olive oil"],
        "instructions": "1. Slice and bread eggplant, then bake until golden. 2. Layer with marinara sauce and cheeses. 3. Bake at 375°F for 20 minutes. 4. Garnish with basil."
    },
    "sweet potato": {
        "name": "Stuffed Sweet Potatoes",
        "ingredients": ["sweet potatoes", "black beans", "salsa", "avocado", "cilantro", "lime"],
        "instructions": "1. Bake sweet potatoes at 400°F for 45 minutes. 2. Scoop out flesh, mix with black beans and salsa. 3. Refill potatoes, top with avocado and cilantro. 4. Drizzle with lime juice."
    },
    "spinach": {
        "name": "Spinach and Ricotta Stuffed Shells",
        "ingredients": ["pasta shells", "spinach", "ricotta cheese", "marinara sauce", "mozzarella", "garlic"],
        "instructions": "1. Cook pasta shells. 2. Mix spinach, ricotta, and garlic. 3. Stuff shells with mixture, place in a baking dish with marinara. 4. Top with mozzarella, bake at 375°F for 25 minutes."
    },
    "dessert": {
        "name": "Vegan Chocolate Mousse",
        "ingredients": ["avocado", "cocoa powder", "maple syrup", "almond milk", "vanilla extract"],
        "instructions": "1. Blend avocado, cocoa powder, maple syrup, almond milk, and vanilla until smooth. 2. Chill for 1 hour. 3. Serve with fresh berries."
    }
}

# Intent recognition (rule-based)
def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["suggest", "recipe", "make", "cook", "prepare"]):
        return "recipe_suggestion"
    elif any(word in text for word in ["hi", "hello", "hey"]):
        return "greeting"
    else:
        return "general"

# Entity extraction (keyword matching)
def extract_entities(text):
    text = text.lower()
    entities = []
    for key in recipe_db.keys():
        if key in text:
            entities.append(key)
    return entities

# Generate recipe response
def get_recipe_response(entities):
    if not entities:
        return "Could you specify a vegetarian ingredient or dish type (e.g., tofu, lentil, pasta, quinoa, soup, chickpea, eggplant, sweet potato, spinach, dessert)?"
    entity = entities[0]
    if entity in recipe_db:
        recipe = recipe_db[entity]
        return f"Here's a vegetarian recipe for {recipe['name']}:\n**Ingredients**: {', '.join(recipe['ingredients'])}\n**Instructions**: {recipe['instructions']}"
    return "Sorry, I only have vegetarian recipes for tofu, lentil, pasta, quinoa, soup, chickpea, eggplant, sweet potato, spinach, or dessert. Try one of those!"

# Main chatbot logic
def chatbot_response(user_input, state):
    # Initialize state if None
    if state is None:
        state = {"history": [], "conversation": Conversation()}
    
    # Extract history and conversation
    history = state["history"]
    conversation = state["conversation"]
    
    # Preprocess input
    cleaned_input = user_input.strip()
    
    # Detect intent and entities
    intent = detect_intent(cleaned_input)
    entities = extract_entities(cleaned_input)
    
    # Handle intents
    if intent == "greeting":
        response = "Hello! I'm your vegetarian recipe assistant. Ask me for a vegetarian recipe or cooking ideas!"
        conversation.add_user_input(cleaned_input)
        conversation = chatbot(conversation)
    elif intent == "recipe_suggestion" and entities:
        response = get_recipe_response(entities)
        conversation.add_user_input(cleaned_input)
        conversation = chatbot(conversation)
    else:
        # Use BlenderBot for general conversation
        conversation.add_user_input(cleaned_input)
        conversation = chatbot(conversation)
        response = conversation.generated_responses[-1]
        if entities:
            response += "\n\n" + get_recipe_response(entities)
        else:
            response += "\n\nI'm here to help with vegetarian recipes! Try asking for a recipe with tofu, lentil, pasta, quinoa, soup, chickpea, eggplant, sweet potato, spinach, or dessert."
    
    # Update history with openai-style format
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})
    
    # Update state
    state = {"history": history, "conversation": conversation}
    
    return history, state

# Gradio interface
def main():
    iface = gr.Interface(
        fn=chatbot_response,
        inputs=[
            gr.Textbox(label="Your Message", placeholder="Type your message here (e.g., 'Suggest a vegetarian pasta recipe')"),
            gr.State()  # Single state for both history and conversation
        ],
        outputs=[
            gr.Chatbot(label="Conversation", type="messages"),
            gr.State()  # Return updated state
        ],
        title="Vegetarian Recipe Chatbot",
        description="Ask for vegetarian recipe suggestions or chat about cooking! Try: 'Suggest a pasta recipe' or 'What can I make with tofu?'"
    )
    iface.launch()

if __name__ == "__main__":
    main()