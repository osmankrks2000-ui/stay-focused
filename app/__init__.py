from flask import Flask
from flask_cors import CORS
from .database import init_db
from .routes import api, pages


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'stay-focused-change-this'
    CORS(app)
    init_db(app)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(pages)
    return app
