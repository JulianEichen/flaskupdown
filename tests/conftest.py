import os
import pytest
from csvsort import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app()

    upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'],
                               'upload.csv')
    if os.path.exists(upload_path):
        os.remove(upload_path)

    yield app


@pytest.fixture(scope='module')
def test_client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client