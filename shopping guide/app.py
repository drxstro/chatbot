from flask import Flask, render_template, request, redirect, url_for
import shelve

app = Flask(__name__)

# Initialize the Shelve database
db = shelve.open('size_color_db')

@app.route('/') #renders the index.html
def home():
    return render_template('index.html')

# CRUD Below

# CREATE (C)

# Description: Takes category and subcategory as parameters, retrieves size, color, and quantity information from the form,
# and stores it in the Shelve database under a specific key.

@app.route('/create/<category>/<subcategory>', methods=['GET', 'POST'])
def create(category, subcategory): # handles the creation of new entry in Shelve
    if request.method == 'POST':
        size = request.form.get('size')
        color = request.form.get('color')
        quantity = int(request.form.get('quantity'))

        key = f'{category}_{subcategory}'
        db[key] = {'size': size, 'color': color, 'quantity': quantity}

        return redirect(url_for('success', category=category, subcategory=subcategory, size=size, color=color, quantity=quantity))
    else:
        return render_template('create.html', category=category, subcategory=subcategory)


# READ (R)

# Description: Retrieves and displays all updates stored in the Shelve database. Passes the updates dictionary to the 'view_updates.html' template.

@app.route('/view_updates')
def view_updates(): # gets and shows all the updated data in Shelve
    updates = dict(db)
    return render_template('view_updates.html', updates=updates)



# UPDATE (U)

# Description: Handles the update of an existing entry in the Shelve database.
# Retrieves size, color, and quantity information from the form and updates the corresponding entry in the Shelve database.

@app.route('/update/<category>/<subcategory>', methods=['GET', 'POST'])
def update(category, subcategory):
    if request.method == 'POST':
        size = request.form.get('size')
        color = request.form.get('color')
        quantity = int(request.form.get('quantity'))

        key = f'{category}_{subcategory}'
        db[key] = {'size': size, 'color': color, 'quantity': quantity}

        return redirect(url_for('success', category=category, subcategory=subcategory, size=size, color=color, quantity=quantity))
    else:
        return render_template('update.html', category=category, subcategory=subcategory)

# DELETE (D)

# Description: Handles the deletion of an existing entry from the Shelve database.
# Checks if the specified key (combination of category and subcategory) exists and deletes it if found.
# Redirects to the 'view_updates' route after deletion.

@app.route('/delete/<category>/<subcategory>')
def delete(category, subcategory):
    key = f'{category}_{subcategory}'
    if key in db:
        del db[key]
        return redirect(url_for('view_updates'))
    else:
        return f'No entry found for {category}/{subcategory}'

@app.route('/success/<category>/<subcategory>/<size>/<color>/<int:quantity>')
def success(category, subcategory, size, color, quantity): # renders the success.html, showing the details
    return render_template('success.html', category=category, subcategory=subcategory, size=size, color=color, quantity=quantity)

if __name__ == '__main__':
    app.run(debug=True)
