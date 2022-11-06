import os
from app import create_app
from dotenv import load_dotenv

from database import PATH_TO_DATABASE
from database.exceptions.create import DatabaseAlreadyExist


if __name__ == '__main__':
    load_dotenv('.flaskenv')

    db_name = os.path.join(str(PATH_TO_DATABASE), str(os.getenv('DATABASE')))
    if not os.path.isfile(os.path.join(PATH_TO_DATABASE, db_name)):
        raise DatabaseAlreadyExist(f'Database {db_name} not exist\n')

    app = create_app()

    app.run(load_dotenv=True, host='0.0.0.0')
