from flask import Blueprint, request, jsonify
from utils.auth import hash_password
from db import get_conn

user_bp = Blueprint("users", __name__)

@user_bp.route("/users/signup", methods=["POST"])
def signup():
    data = request.json

    # Extract fields
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")
    hashed_password = hash_password(data["password"])
    country = data.get("country")

    # Basic validation
    if not all([first_name, last_name, email, hashed_password]):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_conn()
    cur = conn.cursor()

    try:
        # Insert into DB
        cur.execute("""
            INSERT INTO users (first_name, last_name, email, password, country)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, email, first_name, last_name, country, created_at, updated_at
                    """, (first_name, last_name, email, hashed_password, country))
        user = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

    return jsonify({
        "data": {
            "id": user[0],
            "type": "users",
            "attributes": {
                "token": "dummy-token (we'll upgrade later)",
                "email": user[1],
                "name": f"{user[2]} {user[3]}",
                "country": user[4],
                "createdAt": str(user[5]),
                "updatedAt": str(user[6])
            }
        }
    }), 201