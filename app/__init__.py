from flask import Flask
from flasgger import Swagger
from peewee import SqliteDatabase

from app.api.reports_race import init_api as reports_race_init_api
from app.api.drivers import init_api as drivers_init_api
from app.api.driver_info import init_api as driver_info_init_api
from app.config_main import config
from models.race_model import database_proxy


def create_app(config_name='default'):
    app = Flask(__name__)
    app.static_folder = 'static'

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if config_name == 'testing':
        db = SqliteDatabase(':memory:')
        database_proxy.initialize(db)
    else:
        db = SqliteDatabase(app.config['DB_NAME'])
        database_proxy.initialize(db)

    app.config['db'] = db
    swagger = Swagger(app)
    swagger.config['title'] = 'Monaco race report Open API'
    swagger.config['version'] = '1.0.0'
    swagger.config['favicon'] = '/static/img/favicon.png'

    from app import main
    app.register_blueprint(main.main)
    reports_race_init_api(app)
    drivers_init_api(app)
    driver_info_init_api(app)
    return app
