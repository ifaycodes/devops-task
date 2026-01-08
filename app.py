from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    return jsonify({
        'message': 'Task API -Devops project',
        'version': '1.0.0',
        'endpoint': {
            'GET /health': 'Health check',
            'GET /tasks': 'Get all tasks',
            'POST /tasks': 'Create a task',
            'GET /tasks/<task_id>': 'Get a specific task',
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
    })

@app.route('/tasks', method=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks, 'count': len(tasks)})

@app.route('/tasks', method=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'completed': False,
        'created_at': datetime.now().isoformat(),
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', method=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)