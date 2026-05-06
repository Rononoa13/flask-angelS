from flask import Blueprint, request, jsonify
from db import get_conn
from utils.auth import check_password, generate_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/signin", methods=["POST"])
def signin():
    data = request.json.get("auth", {})

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    conn = get_conn()
    cur = conn.cursor()

    #fetch user by email
    cur.execute("""    
                SELECT id, email, first_name, last_name, password, country
                FROM USERS
                WHERE email = %s
            """, (email,))
    user = cur.fetchone()
    conn.close()

    #  Check if user exists
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # 3. Verify password (bcrypt)
    is_valid = check_password(password, user[4])
    if not is_valid:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # 4. Generate JWT token
    token = generate_token(user[0])

    # 5. Response
    return jsonify({
        "data": {
            "id": user[0],
            "type": "users",
            "attributes": {
                "token": token,
                "email": user[1],
                "name": f"{user[2]} {user[3]}",
                "country": user[5]
            }
        }
    }), 200