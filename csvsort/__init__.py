import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['UPLOAD_DEFAULT_NAME'] = 'upload.csv'
    app.config['ALLOWED_EXTENSIONS'] = {'csv'}
    app.config['SECRET_KEY'] = 'fb391a8c6c30d2e4da24efc7'

    from csvsort.main.routes import main
    app.register_blueprint(main)

    return app
