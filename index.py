import json
from flask import Flask
from apps.users.routes import app as users_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from extensions import db, migrate
from models.user import User
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# migrate.init_app(app, db)
db.metadata.clear()

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer, unique=True)

with app.app_context():
    db.create_all()


# Sub Routes
app.register_blueprint(users_app)

# Main routes
@app.route('/', methods=['GET'])
def main():
    return {
        'success': True,
        'endpoints': []
    }
