import os
from flask import Flask
from flasgger import Swagger


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.static_folder = 'static'
app.config.from_object('config_main')

swagger = Swagger(app)
swagger.config['title'] = 'Monaco race report Open API'
swagger.config['version'] = '1.0.0'
swagger.config['favicon'] = '/static/img/favicon.png'

from app import routes
from app.api import reports_race, drivers, driver_info
from app.error_handlers import page_not_found, internal_server_error

app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)
