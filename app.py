from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), 'todos.json')

VALID_PRIORITIES = {'high', 'medium', 'low'}
VALID_CATEGORIES = {'work', 'personal', 'health'}

def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_todos(todos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(todos, f, indent=2)

def normalize_priority(p):
    if not p:
        return 'medium'
    p = str(p).strip().lower()
    return p if p in VALID_PRIORITIES else 'medium'

def normalize_category(c):
    if not c:
        return 'personal'
    c = str(c).strip().lower()
    return c if c in VALID_CATEGORIES else 'personal'

def normalize_due_date(d):
    if not d:
        return ''
    try:
        # Accept YYYY-MM-DD or ISO formats; store as YYYY-MM-DD
        dt = datetime.fromisoformat(d)
        return dt.date().isoformat()
    except Exception:
        try:
            # fallback: accept just YYYY-MM-DD
            datetime.strptime(d, '%Y-%m-%d')
            return d
        except Exception:
            return ''

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    todos = load_todos()
    return render_template('index.html', todos=todos)

@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    return jsonify(load_todos())

@app.route('/add', methods=['POST'])
def add_todo():
    data = request.get_json(silent=True) or request.form
    title = (data.get('title').strip() if data and data.get('title') else None)
    if not title:
        return ('', 400)

    priority = normalize_priority(data.get('priority') if data else None)
    category = normalize_category(data.get('category') if data else None)
    due_date = normalize_due_date(data.get('due_date') if data else None)

    todos = load_todos()
    new_id = max([t.get('id', 0) for t in todos], default=0) + 1
    todo = {
        'id': new_id,
        'title': title,
        'done': False,
        'priority': priority,
        'category': category,
        'due_date': due_date
    }
    todos.append(todo)
    save_todos(todos)
    return jsonify(todo)

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    todos = load_todos()
    for t in todos:
        if t.get('id') == todo_id:
            t['done'] = not t.get('done', False)
            save_todos(todos)
            return jsonify(t)
    return ('', 404)

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todos = load_todos()
    new = [t for t in todos if t.get('id') != todo_id]
    if len(new) == len(todos):
        return ('', 404)
    save_todos(new)
    return ('', 204)

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    data = request.get_json(silent=True) or request.form
    if not data:
        return ('', 400)

    todos = load_todos()
    for t in todos:
        if t.get('id') == todo_id:
            # allow updating title, priority, category, due_date
            if 'title' in data and data.get('title') is not None:
                t['title'] = data.get('title').strip()
            if 'priority' in data:
                t['priority'] = normalize_priority(data.get('priority'))
            if 'category' in data:
                t['category'] = normalize_category(data.get('category'))
            if 'due_date' in data:
                t['due_date'] = normalize_due_date(data.get('due_date'))
            save_todos(todos)
            return jsonify(t)
    return ('', 404)

if __name__ == '__main__':
    # Ensure data file exists
    if not os.path.exists(DATA_FILE):
        save_todos([])
    app.run(debug=True, host='127.0.0.1', port=5000)
