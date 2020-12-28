from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from config import BaseConfig


def create_database():
    database_uri_without_db_name = BaseConfig.SQLALCHEMY_DATABASE_URI[
        :BaseConfig.SQLALCHEMY_DATABASE_URI.rfind('/')
    ]
    with db.create_engine(
        database_uri_without_db_name,
            isolation_level='AUTOCOMMIT').connect() as conn:
        conn.execute('create database gravuty owner postgres')


try:
    db.create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI).connect()
except Exception as e:
    print(e)
    create_database()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()