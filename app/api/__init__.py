from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import reports_race, drivers, driver_info
