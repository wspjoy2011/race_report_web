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

from models.race_model import Race, Driver, Company


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
    race_table_rows = (Race.select(Race.place, Driver.name.alias('driver'), Company.name.alias('company'), Race.time)
                       .join(Driver, on=(Race.driver == Driver.id))
                       .join(Company, on=(Race.company == Company.id))
                       .dicts())
    race_table = sorted(race_table_rows, key=lambda race: race['place'],
                        reverse=True if order == 'desc' else False)

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

    if order not in ['asc', 'desc']:
        abort(404)

    order = True if order == 'desc' else False
    drivers_rows = Driver.select(Driver.abbr, Driver.name).dicts()
    drivers = sorted(drivers_rows, key=lambda driver: driver['abbr'], reverse=order)

    if driver_id:
        drivers = [driver for driver in drivers if driver['abbr'] == driver_id]
        if not drivers:
            abort(404)
        drivers = drivers.pop()
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
