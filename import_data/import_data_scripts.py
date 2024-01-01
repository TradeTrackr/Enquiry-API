from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from enquiry_api import config
from sqlalchemy.sql import text

class Sql(object):
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI,
                   pool_size= int(config.SET_POOL), max_overflow=0)
    Session = sessionmaker(bind=engine, autoflush=True)

    # create a Session
    session = Session()

    def try_commit():
        try:
            Sql.session.commit()
            output = True
        except Exception as e:
            print ("************************************")
            print(e)
            print ("************************************")
            print("commit failed rolling back")
            Sql.session.rollback()
            Sql.session.abort()
            output = False
        finally:
            Sql.session.bind.dispose()
            return output

    def import_role_types():
        f = open("/opt/import_data/insert_types.sql")
        script_str = f.read().strip()
        Sql.session.execute(text(script_str))
        Sql.try_commit()


def run_imports():
    Sql.import_role_types()
