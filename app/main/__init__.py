from flask import Blueprint

main = Blueprint('main', __name__)

from app.main import routes
from app.main.error_handlers import page_not_found, internal_server_error

main.register_error_handler(404, page_not_found)
main.register_error_handler(500, internal_server_error)
