import os
import logging
from flask import Flask, request, jsonify, abort
from models import db, Student
from schema import StudentSchema
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///students.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devkey')
    # Respect FLASK_DEBUG env var if set
    app.debug = bool(int(os.getenv('FLASK_DEBUG', '0')))

    # Initialize extensions
    db.init_app(app)
    CORS(app)  # allows cross-origin requests (useful when adding frontend)

    # Logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

    student_schema = StudentSchema()
    students_schema = StudentSchema(many=True)

    @app.route('/')
    def index():
        return jsonify({
            "message": "Student Management API is running",
            "endpoints": ["/students", "/health"]
        })

    @app.route('/health')
    def health():
        return jsonify({"status": "ok", "db": "sqlite (students.db)"}), 200

    @app.route('/students', methods=['POST'])
    def create_student():
        data = request.get_json() or {}
        errors = student_schema.validate(data)
        if errors:
            app.logger.info("Validation errors on create: %s", errors)
            return jsonify(errors), 400
        roll = data.get('roll')
        name = data.get('name')
        email = data.get('email')
        # check uniqueness
        existing = None
        if roll and email:
            existing = Student.query.filter((Student.roll == roll) | (Student.email == email)).first()
        elif roll:
            existing = Student.query.filter_by(roll=roll).first()
        elif email:
            existing = Student.query.filter_by(email=email).first()

        if existing:
            return jsonify({"error": "Student with given roll/email exists"}), 400

        s = Student(roll=roll, name=name, email=email)
        db.session.add(s)
        db.session.commit()
        app.logger.info("Created student id=%s roll=%s", s.id, s.roll)
        return jsonify(student_schema.dump(s)), 201

    @app.route('/students', methods=['GET'])
    def list_students():
        students = Student.query.order_by(Student.id.desc()).all()
        return jsonify(students_schema.dump(students)), 200

    @app.route('/students/<int:id>', methods=['GET'])
    def get_student(id):
        s = Student.query.get_or_404(id)
        return jsonify(student_schema.dump(s)), 200

    @app.route('/students/<int:id>', methods=['PUT'])
    def update_student(id):
        s = Student.query.get_or_404(id)
        data = request.get_json() or {}
        errors = student_schema.validate(data, partial=True)
        if errors:
            return jsonify(errors), 400
        if 'roll' in data: s.roll = data['roll']
        if 'name' in data: s.name = data['name']
        if 'email' in data: s.email = data['email']
        db.session.commit()
        app.logger.info("Updated student id=%s", s.id)
        return jsonify(student_schema.dump(s)), 200

    @app.route('/students/<int:id>', methods=['DELETE'])
    def delete_student(id):
        s = Student.query.get_or_404(id)
        db.session.delete(s)
        db.session.commit()
        app.logger.info("Deleted student id=%s", id)
        return jsonify({"message": "deleted"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    # if you want to use FLASK_DEBUG from .env, ensure it's set to '1' or '0'
    app.run(host='127.0.0.1', port=5000)
