from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


def connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="flask"
    )


@app.route("/students", methods=["GET"])
def get_students():
    con = connection()
    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return jsonify(students), 200
    finally:
        cursor.close()
        con.close()


@app.route("/students/<int:id>", methods=["GET"])
def get_student_by_id(id):
    con = connection()
    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        student = cursor.fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(student), 200
    finally:
        cursor.close()
        con.close()


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    con = connection()
    cursor = con.cursor()

    try:
        cursor.execute(
            "INSERT INTO students (name, email) VALUES (%s, %s)",
            (name, email)
        )
        con.commit()

        return jsonify({
            "message": "Student added successfully",
            "id": cursor.lastrowid,
            "name": name,
            "email": email
        }), 201
    except mysql.connector.IntegrityError:
        con.rollback()
        return jsonify({"error": "That email may already exist"}), 409
    finally:
        cursor.close()
        con.close()


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required for PUT"}), 400

    con = connection()
    cursor = con.cursor()

    try:
        cursor.execute(
            "UPDATE students SET name = %s, email = %s WHERE id = %s",
            (name, email, id)
        )
        con.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found or details unchanged"}), 404

        return jsonify({
            "message": "Student updated successfully",
            "id": id,
            "name": name,
            "email": email
        }), 200
    except mysql.connector.IntegrityError:
        con.rollback()
        return jsonify({"error": "That email may already exist"}), 409
    finally:
        cursor.close()
        con.close()


@app.route("/students/<int:id>", methods=["PATCH"])
def patch_student(id):
    data = request.get_json(silent=True) or {}
    name = data.get("name")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Provide a non-empty name"}), 400

    con = connection()
    cursor = con.cursor()

    try:
        cursor.execute(
            "UPDATE students SET name = %s WHERE id = %s",
            (name, id)
        )
        con.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found or name unchanged"}), 404

        return jsonify({
            "message": "Student name updated successfully",
            "id": id,
            "name": name
        }), 200
    finally:
        cursor.close()
        con.close()


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    con = connection()
    cursor = con.cursor()

    try:
        cursor.execute("DELETE FROM students WHERE id = %s", (id,))
        con.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({"message": "Student deleted successfully"}), 200
    finally:
        cursor.close()
        con.close()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
