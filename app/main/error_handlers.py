from flask import render_template
from app.config_main import MENU, TOP_DRIVERS


def internal_server_error(error):
    """Internal server error handler"""
    return render_template(
        'error.html',
        title='Error 500',
        error=error,
        menu=MENU,
        top_drivers=TOP_DRIVERS
    ), 500


def page_not_found(error):
    """Page not found error handler"""
    return render_template(
        'error.html',
        title='Error 404',
        error=error,
        menu=MENU,
        top_drivers=TOP_DRIVERS
    ), 404

