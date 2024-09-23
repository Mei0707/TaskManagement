from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), nullable=False, default='Medium')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class TaskLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Helper function to log task actions
def log_task_action(task_id, action, user_id):
    log_entry = TaskLog(task_id=task_id, action=action, user_id=user_id)
    db.session.add(log_entry)
    db.session.commit()

# Task endpoints
@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'Medium'),
        user_id=current_user_id
    )
    db.session.add(new_task)
    db.session.commit()

    log_task_action(new_task.id, "create", current_user_id)

    return jsonify({"msg": "Task created", "id": new_task.id}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if task:
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        task.priority = data.get('priority', task.priority)

        db.session.commit()

        log_task_action(task.id, "update", get_jwt_identity())

        return jsonify({"msg": "Task updated"}), 200
    return jsonify({"msg": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()

        log_task_action(task.id, "delete", get_jwt_identity())

        return jsonify({"msg": "Task deleted"}), 200
    return jsonify({"msg": "Task not found"}), 404

# Task log retrieval endpoint
@app.route('/task_logs', methods=['GET'])
@jwt_required()
def get_task_logs():
    current_user_id = get_jwt_identity()
    logs = TaskLog.query.filter_by(user_id=current_user_id).all()
    return jsonify([{
        "id": log.id,
        "task_id": log.task_id,
        "action": log.action,
        "timestamp": log.timestamp
    } for log in logs]), 200

if __name__ == '__main__':
    app.run(debug=True)
