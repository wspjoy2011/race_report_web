from app.main import main
from app.main.forms import RegistrationForm
from flask import (
    render_template,
    request,
    current_app,
    abort,
    session,
    redirect,
    url_for,
    flash
)

from report_framework.report import main as main_report, sort_race_logs
from report_framework.cli_report import prepare_race_table


@main.route('/')
def index():
    """Home page about race"""
    return render_template(
        'home.html',
        title='F1 Monaco Race 2018',
        menu=current_app.config['MENU'],
        top_drivers=current_app.config['TOP_DRIVERS'],
        user=session.get('user')
    )


@main.route('/report/')
def show_report():
    """Show report from race"""
    order = request.args.get('order')
    if not order:
        order = 'asc'
    if order not in ['asc', 'desc']:
        abort(404)
    race_results, abbrs = main_report(current_app.config['PATH_TO_RACE_DATA'])
    race_results_sorted = sort_race_logs(race_results, order)
    race_table = prepare_race_table(race_results_sorted, abbrs, '')

    return render_template(
        'report/report.html',
        title='Race Report',
        race_table=race_table,
        top_drivers=current_app.config['TOP_DRIVERS'],
        menu=current_app.config['MENU'],
        order=order,
        user=session.get('user')
    )


@main.route('/report/drivers/')
def show_drivers():
    """Show drivers or driver profile"""
    order = request.args.get('order')
    driver_id = request.args.get('driver_id')
    title = 'Race Drivers'
    template_name = 'report/drivers.html'

    if not order:
        order = 'asc'

    order = False if order == 'asc' else True
    _, drivers = main_report(current_app.config['PATH_TO_RACE_DATA'])
    drivers = dict(sorted(drivers.items(), reverse=order))

    if driver_id:
        drivers = {driver_id: drivers.get(driver_id, False)}
        title = 'Driver profile'
        template_name = 'report/driver_profile.html'

    return render_template(
        template_name,
        title=title,
        drivers=drivers,
        menu=current_app.config['MENU'],
        top_drivers=current_app.config['TOP_DRIVERS'],
        user=session.get('user')
    )


@main.route('/registration/', methods=['GET', 'POST'])
def registration():
    """Registrate user on site"""
    form = RegistrationForm()

    if session.get('user'):
        return redirect(url_for('index'))

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm = form.confirm.data

        session['user'] = email
        flash(f'{email} registered')
        return redirect(url_for('registration'))

    return render_template(
        'auth/registration.html',
        title='Registrate new user',
        menu=current_app.config['MENU'],
        top_drivers=current_app.config['TOP_DRIVERS'],
        form=form,
        user=session.get('user')
    )


@main.route('/logout/')
def logout():
    """Logout user session"""
    del session['user']
    return redirect(url_for('index'))
