from flask import Blueprint, request, jsonify
from db import get_conn
from utils.auth import get_user_id_from_token, get_user_id_from_request

content_bp = Blueprint("content", __name__)

@content_bp.route("/contents", methods=["POST"])
def create_content():
    user_id = get_user_id_from_token(request)
    if not user_id:
        return {"error": "Unauthorized"}, 401
    
    data = request.json
    title = data.get("title")
    body = data.get("body")

    if not title or not body:
        return jsonify({"error": "title and body required"}), 401
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
            INSERT INTO contents (user_id, title, body)
                VALUES (%s, %s, %s)
                RETURNING id, title, body, created_at    
            """, (user_id, title, body))
    
    content = cur.fetchone()
    conn.commit()
    conn.close()

    return jsonify({
        "data": {
            "id": content[0],
            "title": content[1],
            "body": content[2],
            "createdAt": content[3]
        }
    }), 201

# GET ALL contents
@content_bp.route("/content", methods=["GET"])
def get_contents():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
                SELECT id, title, body, created_at
                FROM contents
                ORDER BY id DESC
            """)
    
    rows = cur.fetchall()
    conn.close()

    return jsonify({
        "data": [
            {
                "id": r[0],
                "title": r[1],
                "body": r[2],
                "createdAt": r[3]
            } for r in rows
        ]
    }), 200

# UPDATE content
@content_bp.route("/contents/<int:content_id>", methods=["PUT"])
def update_content(content_id):
    user_id = get_user_id_from_request()

    if not user_id:
        return {"error": "Unauthorized"}, 401

    data = request.json
    title = data.get("title")
    body = data.get("body")

    conn = get_conn()
    cur = conn.cursor()

    # ownership check + update in one step
    cur.execute("""
        UPDATE contents
        SET title = %s,
            body = %s,
            updated_at = NOW()
        WHERE id = %s AND user_id = %s
        RETURNING id, title, body, created_at, updated_at
    """, (title, body, content_id, user_id))

    updated = cur.fetchone()
    conn.commit()
    conn.close()

    if not updated:
        return {"error": "Not found or not allowed"}, 403

    return {
        "data": {
            "id": updated[0],
            "title": updated[1],
            "body": updated[2],
            "createdAt": updated[3],
            "updatedAt": updated[4],
        }
    }, 200

# 
@content_bp.route("/contents/<int:content_id>", methods=["DELETE"])
def delete_content(content_id):
    user_id = get_user_id_from_request()

    if not user_id:
        return {"error": "Unauthorized"}, 401

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM contents
        WHERE id = %s AND user_id = %s
        RETURNING id
    """, (content_id, user_id))

    deleted = cur.fetchone()
    conn.commit()
    conn.close()

    if not deleted:
        return {"error": "Not found or not allowed"}, 403

    return {"message": "Deleted"}, 200
