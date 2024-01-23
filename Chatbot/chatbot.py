from flask import Flask, render_template, request, redirect, url_for, Markup, flash
from fuzzywuzzy import fuzz

app = Flask(__name__)

chat_history = []

def get_category_link(category):
    return f"#{category.lower().replace(' ', '_')}"

def fuzzy_match(query, options, threshold=80):
    # Find the best match among options using fuzzy matching
    best_match, score = max([(option, fuzz.partial_ratio(query.lower(), option.lower())) for option in options], key=lambda x: x[1])

    # If the score is above the threshold, return the best match
    if score >= threshold:
        return best_match
    else:
        return None

def is_greeting(query):
    greetings = ['hi', 'hello', 'hey', 'hola', 'bonjour', 'greetings', 'yo', 'hi there']
    return any(greeting in query.lower().split() for greeting in greetings)

def is_farewell(query):
    farewells = ['bye', 'goodbye', 'farewell', 'see you', 'see ya', 'adios', 'au revoir']
    return any(farewell in query.lower().split() for farewell in farewells)

def is_question(query):
    return query.strip().endswith('?')

def fashion_chatbot(query):
    # Check if the query is a greeting
    if is_greeting(query):
        return Markup(f"Helloooo! Welcome, I'm ecochicBOT! How can I assist you today?")

    # Check if the query is a farewell
    if is_farewell(query):
        return "Goodbye! If you have more questions in the future, feel free to ask. Have a great day!"

    # Check if the query is a question
    if is_question(query):
        return "That's a great question!"

    # Explicitly check for 'clothing' in the query (as a separate word) before fuzzy matching
    if 'clothing' in query.lower().split():
        return "I see you're interested in clothing. How can I help you with specific categories like Women Clothing, Men Clothing, or Kids Clothing?"

    categories = ['Women Clothing', 'Men Clothing', 'Kids Clothing', 'Shoes', 'Accessories', 'Beauty and Health']

    # Explicitly check for variations of 'women' in the query before fuzzy matching
    if any(keyword in query.lower() for keyword in ['wmen', 'wman', 'woman', 'women']):
        return Markup("Here is more information about <a href='#women_clothing' style='text-decoration: none; color: blue;'>Women Clothing</a>. Any other questions?")
    elif any(keyword in query.lower() for keyword in ['men', 'man']):
        return Markup("Here is more information about <a href='#men_clothing' style='text-decoration: none; color: blue;'>Men Clothing</a>. Any other questions?")

    category_match = fuzzy_match(query, categories)
    if category_match:
        link = get_category_link(category_match)
        return Markup(f"Here is more information about <a href='{link}' style='text-decoration: none; color: blue;'>{category_match}</a>. Any other questions?")

    if fuzzy_match(query, ['yes']):
        return "What other questions do you have?"
    elif fuzzy_match(query, ['no']):
        return "Okay, have a nice day! Goodbye!"

    chat_history.append({'user': 'User', 'message': query})
    return "I'm sorry, I couldn't find information on that. Please try asking about Women Clothing, Men Clothing, Kids Clothing, Shoes, Accessories, or Beauty and Health."


@app.route('/')
def index():
    return render_template('chatbot.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']

    # Validate user input
    if not user_message:
        flash('Please enter a message.', 'error')
        return redirect(url_for('index'))

    bot_response = fashion_chatbot(user_message)
    chat_history.append({'user': 'User', 'message': user_message})
    chat_history.append({'user': 'Bot', 'message': bot_response})
    return render_template('chatbot.html', user_message=user_message, bot_response=bot_response, chat_history=chat_history)

@app.route('/view_chat')
def view_chat():
    return render_template('view_chat.html', chat_history=chat_history)

@app.route('/delete_chat_history', methods=['POST'])
def delete_chat_history():
    selected_messages = request.form.getlist('selected_messages[]')
    select_all = 'select_all' in request.form

    if select_all:
        chat_history.clear()
    elif selected_messages:
        selected_indices = [int(index) - 1 for index in selected_messages]
        selected_indices.sort(reverse=True)

        for index in selected_indices:
            if 0 <= index < len(chat_history):
                del chat_history[index]

    return redirect(url_for('view_chat'))

if __name__ == '__main__':
    app.run(debug=True)
