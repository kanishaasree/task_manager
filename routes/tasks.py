from flask import Blueprint, request, jsonify
from models.task import Task
from extension import db
from flask_jwt_extended import jwt_required 

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required() 
def list_task():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])

@tasks_bp.route('/task/<int:taskid>', methods=["GET"])
@jwt_required()  
def get_task(taskid):
    tas = Task.query.get(taskid)
    if tas:
        return jsonify([tas.to_dict()])
    else:
        return jsonify({"error": "Task not found"}), 404

@tasks_bp.route('/add_task', methods=['POST'])
@jwt_required()
def create_task():
    data = request.json

    
    if 'task_name' not in data or not isinstance(data['task_name'], str):
        return jsonify({'error': 'task_name is required and must be a string'}), 400
    if 'task_status' not in data or data['task_status'] not in ['pending', 'completed']:
        return jsonify({'error': 'task_status must be either pending or completed'}), 400

    DATA1 = Task(**data)
    db.session.add(DATA1)
    db.session.commit()
    return jsonify({"message": "Task added successfully"})

@tasks_bp.route('/delete/<int:taskid>', methods=['DELETE'])
@jwt_required()  
def remove_task(taskid):
    tas = Task.query.get(taskid)
    if tas:
        db.session.delete(tas)
        db.session.commit()
        return jsonify({"message": "Deleted successfully"})
    else:
        return jsonify({"error": "Task not found"}), 404
