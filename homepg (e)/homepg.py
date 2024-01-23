from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Sample data for meetings, tasks, and sales events
meetings = [
    {"title": "Team Meeting", "date": "2024-01-23", "time": "10:00 AM"},
    {"title": "Client Presentation", "date": "2024-01-25", "time": "2:30 PM"},
]

tasks = [
    {"description": "Prepare report for the meeting", "deadline": "2024-01-23", "completed": False},
    {"description": "Follow up with clients", "deadline": "2024-01-27", "completed": True},
]

sales_events = [
    {"title": "Product Launch", "date": "2024-02-01", "time": "3:00 PM"},
    {"title": "Sales Training", "date": "2024-02-05", "time": "11:00 AM"},
]

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@app.route('/')
def home():
    return render_template('home.html', meetings=meetings, tasks=tasks, sales_events=sales_events)

@app.route('/schedule')
def schedule():
    # Combine all events for a complete schedule
    all_events = meetings + tasks + sales_events
    return render_template('schedule.html', all_events=all_events)

@app.route('/update_tasks', methods=['POST'])
def update_tasks():
    for index, task in enumerate(tasks, start=1):
        task_id = f'task_{index}_id'
        task_completed = f'task_{index}'
        if task_id in request.form and task_completed in request.form:
            task_index = int(request.form[task_id]) - 1
            tasks[task_index]['completed'] = True if request.form[task_completed] == 'on' else False

    return redirect(url_for('home'))

@app.route('/add_task_form')
def add_task_form():
    return render_template('add_task.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    description = request.form.get('new_task_description')
    deadline = request.form.get('new_task_deadline')

    # Validate date format (you can add more validation if needed)
    if not validate_date(deadline):
        return "Invalid date format. Please use YYYY-MM-DD."

    new_task = {"description": description, "deadline": deadline, "completed": False}
    tasks.append(new_task)

    return redirect(url_for('home'))

# New routes for login and create_user
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/create_user')
def create_user():
    return render_template('create_user.html')

if __name__ == '__main__':
    app.run(debug=True)
