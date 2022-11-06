from flask import render_template, current_app


def internal_server_error(error):
    """Internal server error handler"""
    return render_template(
        'error.html',
        title='Error 500',
        error=error,
        menu=current_app.config['MENU'],
        top_drivers=current_app.config['TOP_DRIVERS']
    ), 500


def page_not_found(error):
    """Page not found error handler"""
    return render_template(
        'error.html',
        title='Error 404',
        error=error,
        menu=current_app.config['MENU'],
        top_drivers=current_app.config['TOP_DRIVERS']
    ), 404

