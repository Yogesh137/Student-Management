# Student Management API (Flask + SQLite)

Minimal REST API for student CRUD built with Flask and SQLite.

## Files
- `app.py`           - Flask application (routes + app factory)
- `models.py`        - SQLAlchemy models (Student)
- `schemas.py`       - Marshmallow schema for validation
- `db_init.py`       - Script to initialize the SQLite DB
- `requirements.txt` - Python dependencies
- `.env` (optional)  - Environment variables

## Prerequisites
- Python 3.10+ installed
- (Recommended) `virtualenv` / `venv`
- `curl` or Postman for testing

## Setup (Windows / macOS / Linux)
1. Create & activate virtual environment
   ```bash
   python -m venv venv
   # macOS / Linux
   source venv/bin/activate
   # Windows PowerShell
   venv\Scripts\Activate.ps1
   # Windows cmd
   venv\Scripts\activate.bat

Install dependencies


pip install -r requirements.txt
Create .env (optional) — example:

FLASK_DEBUG=1
DATABASE_URL=sqlite:///students.db
SECRET_KEY=supersecretdevkey
Note: replace FLASK_ENV with FLASK_DEBUG=1 if you previously had FLASK_ENV.

Initialize the DB (creates students.db)

python db_init.py
Run the app

python app.py
The server will run at http://127.0.0.1:5000.

Test API (curl examples)
Create student (POST)
macOS / Linux:

curl -X POST http://127.0.0.1:5000/students \
  -H "Content-Type: application/json" \
  -d '{"roll":"CS101","name":"Alice","email":"alice@example.com"}'
Windows PowerShell:

curl -Method POST http://127.0.0.1:5000/students -Headers @{ "Content-Type" = "application/json"} -Body '{"roll":"CS101","name":"Alice","email":"alice@example.com"}'
List students (GET)

curl http://127.0.0.1:5000/students
Get student (GET)

curl http://127.0.0.1:5000/students/1
Update student (PUT)

curl -X PUT http://127.0.0.1:5000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice B"}'
Delete student (DELETE)

curl -X DELETE http://127.0.0.1:5000/students/1
Inspect DB
With sqlite3 CLI:

sqlite3 students.db ".tables"
sqlite3 students.db "SELECT * FROM student;"
(The SQLAlchemy default table name for the Student model is likely student.)

Or use DB Browser for SQLite (GUI) to open students.db.

Tips & Next Steps
Use Git: git init, commit and push to GitHub.

Add Postman collection or Swagger for docs.

Add logging, tests, and input sanitization.

Deploy: Render / Railway / Heroku are good starter hosts.

Consider Dockerizing for consistent deployments.

Troubleshooting
ModuleNotFoundError: No module named 'schemas' → ensure schemas.py is in the same folder as app.py and run from that folder.

If you see warnings about FLASK_ENV, remove it from .env and use FLASK_DEBUG=1.

---

# Quick checklist (do this now)
1. Overwrite your current `app.py` with the updated version above.  
2. Create or update `.env` to use `FLASK_DEBUG=1` instead of `FLASK_ENV`.  
3. Run:

python db_init.py    # if DB not created yet
python app.py
Open http://127.0.0.1:5000/ to verify JSON message.

Run the curl commands in the README to test endpoints.