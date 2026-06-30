from flask import Blueprint, request, jsonify
import bcrypt
from db import get_connection

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Name, email aur password sab chahiye"}), 400

    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users (name, email, phone, password_hash)
            VALUES (%s, %s, %s, %s) RETURNING id, name, email
        """, (data['name'], data['email'], data.get('phone', ''), hashed.decode()))
        user = cur.fetchone()
        conn.commit()
        return jsonify({
            "message": "Registration successful!",
            "user": {"id": user[0], "name": user[1], "email": user[2]}
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Email already registered"}), 400
    finally:
        cur.close()
        conn.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, email, password_hash FROM users WHERE email = %s",
        (data['email'],)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if bcrypt.checkpw(data['password'].encode(), user[3].encode()):
        return jsonify({
            "message": "Login successful",
            "user": {"id": user[0], "name": user[1], "email": user[2]}
        })
    return jsonify({"error": "Wrong password"}), 401
