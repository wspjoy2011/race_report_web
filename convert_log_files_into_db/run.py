import argparse
from argparse import Namespace

from convert_log_files_into_db.utils import create_db, write_drivers, write_companies, write_race_table
from report_framework.cli_report import prepare_race_table
from report_framework.report import main as main_report, sort_race_logs

from database.exceptions.create import DatabaseAlreadyExist, DatabaseTableAlreadyExist


def parse_args() -> Namespace:
    """
    Parse cli arguments with argparse
    :return instance of argparse:
    """
    parser = argparse.ArgumentParser(prog='Data mapper',
                                     usage='%(prog)s run.py --data <log_files_path> --db <path_to_database>]"',
                                     description='Map data from race log files into database')
    parser.add_argument('-d',
                        '--data',
                        type=str,
                        help='path to race log files',
                        required=True)
    parser.add_argument('-db',
                        '--database',
                        help='path to database',
                        required=True)
    args = parser.parse_args()
    return args


def main(data: str, db_name: str):
    """Main controller of cli_report module"""
    try:
        create_db(db_name)
        print(f'Database {db_name} created')
    except DatabaseAlreadyExist as error:
        print(error)
        exit()

    race_results, abbrs = main_report(data)
    race_results_sorted = sort_race_logs(race_results, 'asc')
    race_table = prepare_race_table(race_results_sorted, abbrs, '')

    drivers = [{'abbr': abbr, 'name': driver[0]} for abbr, driver in abbrs.items()]
    companies = [{'name': company[1]} for company in abbrs.values()]

    try:
        write_drivers(drivers)
        write_companies(companies)
        write_race_table(race_table)
        print('Table "Driver", "Company", "Race" complete')
    except DatabaseTableAlreadyExist as error:
        print(error)


if __name__ == '__main__':
    args = parse_args()
    race_data = args.data
    order_db_name = args.database
    main(race_data, order_db_name)
