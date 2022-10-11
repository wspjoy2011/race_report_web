from pathlib import Path

import racing_data
from report_framework.report import main as main_report, sort_race_logs
from report_framework.cli_report import prepare_race_table


def get_patch_to_race_data():
    """Return patch to race data"""
    path_to_race_data = str(Path(racing_data.__file__).parent.absolute())
    return path_to_race_data


def get_top_drivers():
    """Return top drivers"""
    race_results, abbrs = main_report(PATH_TO_RACE_DATA)
    race_results_sorted = sort_race_logs(race_results, 'asc')
    race_table = prepare_race_table(race_results_sorted, abbrs, '')
    top_drivers = race_table[:3]
    return top_drivers


PATH_TO_RACE_DATA = get_patch_to_race_data()
TOP_DRIVERS = get_top_drivers()
MENU = {
    'Home': '/',
    'Report': '/report',
    "Drivers": '/report/drivers/',
    "Login": '/login'
}
