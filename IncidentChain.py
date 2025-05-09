from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

DB_NAME = 'myapi'
DB_USER = 'postgres'
DB_PASSWORD = 'urekmazino'

conn = psycopg2.connect(
    host="localhost",
    port=8000,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

@app.route("/")
def home():
    return "Welcome to my AI Safety Incident Log API"

# Get all incidents
@app.route('/incidents', methods=['GET'])
def get_all_incidents():
    cur.execute(
        "SELECT id, title, description, severity, reported_at FROM incidents"
    )
    incidents = cur.fetchall()
    output = []
    for it in incidents:
        output.append({
            "id": it[0],
            "title": it[1],
            "description": it[2],
            "severity": it[3],
            "reported_at": it[4].isoformat()
        })
    return jsonify(output), 200

# Create a new incident
@app.route("/incidents", methods=["POST"])
def create_incident():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    severity = data.get("severity")

    if not title or not description or severity not in ["Low", "Medium", "High"]:
        return jsonify({"error": "Invalid input. Title, description, and valid severity (Low, Medium, High) are required."}), 400

    cur.execute(
        "INSERT INTO incidents (title, description, severity) VALUES (%s, %s, %s) RETURNING id, reported_at;",
        (title, description, severity)
    )
    incident = cur.fetchone()
    conn.commit()

    return jsonify({
        "id": incident[0],
        "title": title,
        "description": description,
        "severity": severity,
        "reported_at": incident[1].isoformat()
    }), 201

# Get an incident by ID
@app.route("/incidents/<int:incident_id>", methods=["GET"])
def get_incident_by_id(incident_id):
    cur.execute(
        "SELECT id, title, description, severity, reported_at FROM incidents WHERE id = %s;",
        (incident_id,)
    )
    incident = cur.fetchone()
    if incident:
        return jsonify({
            "id": incident[0],
            "title": incident[1],
            "description": incident[2],
            "severity": incident[3],
            "reported_at": incident[4].isoformat()
        }), 200
    else:
        return jsonify({'error': 'Incident not found'}), 404

# Update an existing incident
@app.route("/incidents/<int:incident_id>", methods=["PUT"])
def update_incident(incident_id):
    data = request.get_json()
    new_title = data.get("title")
    new_description = data.get("description")
    new_severity = data.get("severity")

    if not new_title or not new_description or new_severity not in ["Low", "Medium", "High"]:
        return jsonify({"error": "Invalid input. Title, description, and valid severity (Low, Medium, High) are required."}), 400

    cur.execute(
        "UPDATE incidents SET title = %s, description = %s, severity = %s WHERE id = %s;",
        (new_title, new_description, new_severity, incident_id)
    )
    conn.commit()
    if cur.rowcount > 0:
        return jsonify({"message": "Incident successfully updated"}), 200
    else:
        return jsonify({'error': 'Incident not found'}), 404

# Delete an incident
@app.route("/incidents/<int:incident_id>", methods=["DELETE"])
def delete_incident(incident_id):
    cur.execute(
        "DELETE FROM incidents WHERE id = %s;", (incident_id,)
    )
    conn.commit()
    if cur.rowcount > 0:
        return jsonify({"message": "Incident successfully deleted"}), 200
    else:
        return jsonify({"error": "Incident not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
