import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(os.path.dirname(basedir), 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.students import bp as students_bp
    app.register_blueprint(students_bp)

    from app.courses import bp as courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')

    return app
