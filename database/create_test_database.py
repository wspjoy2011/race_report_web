from pathlib import Path

import racing_data
from convert_log_files_into_db.utils import write_drivers, write_companies, write_race_table
from models.race_model import Driver, Company, Race
from report_framework.cli_report import prepare_race_table
from report_framework.report import main as main_report, sort_race_logs


def create_db(db):
    db.create_tables([Driver, Company, Race])

    data = str(Path(racing_data.__file__).parent.absolute())
    race_results, abbrs = main_report(data)
    race_results_sorted = sort_race_logs(race_results, 'asc')
    race_table = prepare_race_table(race_results_sorted, abbrs, '')

    drivers = [{'abbr': abbr, 'name': driver[0]} for abbr, driver in abbrs.items()]
    companies = [{'name': company[1]} for company in abbrs.values()]

    write_drivers(drivers)
    write_companies(companies)
    write_race_table(race_table)
