import pytest
from flask_login import FlaskLoginClient

from myapp import myapp_obj


@pytest.fixture()
def app():
    myapp = myapp_obj
    myapp.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # in-memory test db
        WTF_CSRF_ENABLED=False  # disable CSRF for easy posting
    )

    myapp.test_client_class = FlaskLoginClient

    # holds context of the app for testing
    with myapp.app_context():
        # get the database object and create the tables inside the memory test-database
        from myapp import db
        db.init_app(myapp)  # relink it to the app to get the updated uri
        db.create_all()
    yield myapp

    # Can add cleanup here



@pytest.fixture()
def client(myapp):
    return myapp.test_client()