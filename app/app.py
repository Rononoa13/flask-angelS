from flask import Flask, Blueprint
from routes.users import user_bp
from routes.auth import auth_bp
from routes.contents import content_bp

app = Flask(__name__)

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v1.register_blueprint(user_bp)
api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(content_bp)

app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=True)