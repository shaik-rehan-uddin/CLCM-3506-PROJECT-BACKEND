from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from admin import admin
from models import db
from routes import store_contact, get_health
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@"
    f"{environ.get('DB_HOST')}:{environ.get('DB_PORT')}/{environ.get('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = (
    "4AC372EE8EB4DF2FB3D4EDAA68C166728C7C6C5A8925DAE396C2F31E239CF473"
)

CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

admin.init_app(app)

app.route("/", methods=["GET"])(get_health)
app.route("/api/contact", methods=["POST", "OPTIONS"])(store_contact)

if __name__ == "__main__":
    app.run(debug=True)
