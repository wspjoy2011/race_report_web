from app import app
from flask import render_template, request, abort
from pathlib import Path

from report_framework.report import main as main_report, sort_race_logs
from report_framework.cli_report import prepare_race_table
import racing_data


path_to_race_data = str(Path(racing_data.__file__).parent.absolute())

race_results, abbrs = main_report(path_to_race_data)
race_results_sorted = sort_race_logs(race_results, 'asc')
race_table = prepare_race_table(race_results_sorted, abbrs, '')
top_drivers = race_table[:3]


menu = {
    'Home': '/',
    'Report': '/report',
    "Drivers": '/report/drivers/',
    "Login": '/login'
}


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        '404.html',
        title='Error 404',
        error=error,
        menu=menu,
        top_drivers=top_drivers
    ), 404


@app.route('/')
@app.route('/home')
def index():
    title = 'F1 Monaco Race 2018'
    template = 'home.html'
    return render_template(
        template,
        title=title,
        menu=menu,
        top_drivers=top_drivers
    )


@app.route('/report/')
def show_report():
    order = request.args.get('order')
    if not order:
        order = 'asc'
    if order not in ['asc', 'desc']:
        abort(404)
    race_results, abbrs = main_report(path_to_race_data)
    race_results_sorted = sort_race_logs(race_results, order)
    race_table = prepare_race_table(race_results_sorted, abbrs, '')
    title = 'Race Report'
    template = 'report/report.html'

    return render_template(
        template,
        title=title,
        race_table=race_table,
        top_drivers=top_drivers,
        menu=menu,
        order=order
    )


@app.route('/report/drivers/')
def show_drivers():
    order = request.args.get('order')
    driver_id = request.args.get('driver_id')
    if not order:
        order = 'asc'
    order = False if order == 'asc' else True
    _, drivers = main_report(path_to_race_data)
    drivers = dict(sorted(drivers.items(), reverse=order))
    if driver_id:
        if driver_id in drivers:
            drivers = {driver_id: drivers[driver_id]}
        else:
            abort(404)
    title = 'Race Drivers'
    template = 'report/drivers.html'

    return render_template(
        template,
        title=title,
        drivers=drivers,
        menu=menu,
        top_drivers=top_drivers
    )
