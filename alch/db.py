""" setup db connection """
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app as app

engine = create_engine(app.config.get('MYSQL'), echo=True)

Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


def close(err=None):
    """ close db session on teardown """
    if err is not None:
        app.logger.error(err)

    Session.remove()
