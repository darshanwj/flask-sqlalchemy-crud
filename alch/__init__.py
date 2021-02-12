""" application """
from flask import Flask


def create_app(test_conf=None):
    """ application factory """
    app = Flask(__name__)

    app.config.from_mapping(
        MYSQL='mysql+mysqldb://root:root@mysql/myalch'
    )

    if test_conf is not None:
        app.config.update(test_conf)

    with app.app_context():
        from alch import views  # pylint: disable=unused-import,import-outside-toplevel

    from alch.db import close  # pylint: disable=import-outside-toplevel
    app.teardown_appcontext(close)

    return app
