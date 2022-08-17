from extensions import db 

# Context Manager for the db sessions
# To always ensure they open and close whatever the user accesses
# a database session. Closing will happen whether error is thrown 
# in the middle or not. 
class DbSessionContext(object):
    def __init__(self):
        self.db = db

    def __enter__(self):
        self.db.session().expire_on_commit = False
        return self.db.session()

    def __exit__(self, type, value, traceback): 
        self.db.session.close()


def insert_into_db(item):
    with DbSessionContext() as session:
        session.add(item)
        session.commit()

def delete_from_db(item):
    with DbSessionContext() as session:
        session.delete(item)
        session.commit()

def commit_changes():
    with DbSessionContext() as session:
        session.commit()
