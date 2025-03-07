import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session
from typing import Generator
import tempfile
import os

@pytest.fixture(scope="module")
def app() -> Generator[Flask, None, None]:
    """Create and configure a new app instance for tests."""
    db_fd, db_path = tempfile.mkstemp()
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope="module")
def db(app: Flask) -> Generator[SQLAlchemy, None, None]:
    """Create a fresh database for each test module."""
    from app.models.url_model import db  # Import from application's models
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

@pytest.fixture(scope="function")
def client(app: Flask) -> Flask.test_client:
    """Create a test client for making requests."""
    return app.test_client()

@pytest.fixture(scope="function")
def session(db: SQLAlchemy) -> Generator[scoped_session, None, None]:
    """Create a new database session for each test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()

pytest_plugins = ["pytest_mock"]