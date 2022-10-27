from flask import Flask
from flasgger import Swagger
from app.api.reports_race import init_api as reports_race_init_api
from app.api.drivers import init_api as drivers_init_api
from app.api.driver_info import init_api as driver_info_init_api


def create_app(config_name=None):
    app = Flask(__name__)
    app.static_folder = 'static'

    if config_name is None:
        app.config.from_pyfile('config_main.py', silent=True)
    else:
        app.config.from_mapping(config_name)

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
