from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Application factory function"""
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object('app.config.settings.Config')
    
    # Initialize extensions
    db.init_app(app)
    
    return app
