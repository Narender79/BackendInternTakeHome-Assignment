# AI Safety Incident Log API

A simple Flask API to log and manage hypothetical AI safety incidents.  
Built as part of a backend take-home assignment for HumanChain AI Safety.

---

## 🚀 Technology Stack
- **Language:** Python 3.x
- **Framework:** Flask
- **Database:** PostgreSQL
- **Libraries:**
  - psycopg2 (PostgreSQL driver for Python)
  - Flask (Web framework)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-link>
cd <your-project-folder>
2. Install Dependencies
Make sure you have Python and pip installed.
pip install flask psycopg2

3. Set Up PostgreSQL Database
Install PostgreSQL if not already installed.

Create a new database:

CREATE DATABASE myapi;
Connect to the database and create the incidents table:
sql
\c myapi

CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    severity VARCHAR(10) NOT NULL CHECK (severity IN ('Low', 'Medium', 'High')),
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
4. Configure Database Connection
Update your database credentials inside the Python file if needed:

DB_NAME = 'myapi'
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'
Make sure PostgreSQL is running and listening on the correct port (default: 5432 or as per your setup).

🏃 Running the Project
python app.py
Flask will start running locally at http://127.0.0.1:5000/

🛠 API Endpoints and Usage
1. GET /
Path: /
Description: Welcome message.

2. GET /incidents
Path: /incidents
Description: Retrieve all incidents.
Example using curl:
curl http://127.0.0.1:5000/incidents

3. POST /incidents
Path: /incidents
Description: Create a new incident.
Example using curl:
curl -X POST http://127.0.0.1:5000/incidents \
-H "Content-Type: application/json" \
-d '{"title": "AI Model Failure", "description": "Model generated biased outputs.", "severity": "High"}'

4. GET /incidents/{id}
Path: /incidents/<incident_id>
Description: Retrieve an incident by ID.
Example using curl:
curl http://127.0.0.1:5000/incidents/1

5. PUT /incidents/{id}
Path: /incidents/<incident_id>
Description: Update an existing incident.
Example using curl:
curl -X PUT http://127.0.0.1:5000/incidents/1 \
-H "Content-Type: application/json" \
-d '{"title": "Updated Title", "description": "Updated description.", "severity": "Medium"}'

6. DELETE /incidents/{id}
Path: /incidents/<incident_id>

Description: Delete an incident.

Example using curl:
curl -X DELETE http://127.0.0.1:5000/incidents/1
📌 Design Decisions & Challenges
Kept the project lightweight using psycopg2 directly for SQL handling to have full control over queries.

Implemented basic validation on API level, such as checking required fields and verifying that severity is one of "Low", "Medium", "High".
