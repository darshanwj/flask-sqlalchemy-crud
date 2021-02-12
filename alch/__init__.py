""" application """
from flask import Flask


def create_app():
    """ application factory """
    app = Flask(__name__)

    app.config.from_mapping(
        MYSQL='mysql://root:root@mysql/myalch'
    )

    with app.app_context():
        from alch import views  # pylint: disable=unused-import,import-outside-toplevel

    from alch.db import close  # pylint: disable=import-outside-toplevel
    app.teardown_appcontext(close)

    return app
