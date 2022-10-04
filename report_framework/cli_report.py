"""
Cli report module works with CLI
For example:

python cli_report.py --files <folder_path> [--asc | --desc]  shows list of drivers and optional order (default order is asc)
python cli_report.py --files <folder_path> --driver “Sebastian Vettel”  shows statistic about driver
"""
import argparse
from argparse import Namespace

from prettytable import PrettyTable

from report_framework.report import sort_race_logs, main as main_report


def parse_args() -> Namespace:
    """
    Parse cli arguments with argparse
    :return instance of argparse:
    """
    parser = argparse.ArgumentParser(prog='CLI Interface to report framework',
                                     usage='%(prog)s cli_report.py \"[--files "<folder_path>" [--asc | --desc] '
                                           '--driver]"',
                                     description='Show report about racing logs')
    parser.add_argument('--files',
                        type=str,
                        help='path to folder with txt files',
                        required=True)
    parser.add_argument('--asc',
                        action='store_true',
                        help='order by ascending',
                        default=False,
                        required=False)
    parser.add_argument('--desc',
                        action='store_true',
                        help='order by descending',
                        default=False,
                        required=False)
    parser.add_argument('--driver',
                        type=str,
                        help='shows statistic about driver',
                        default='',
                        required=False)
    args = parser.parse_args()
    return args


def prepare_race_table(race_results: dict[str: str], abbrs: dict[str: tuple[str]], current_driver: str):
    """Prepare race data to print"""
    race_table = []
    for counter, code in enumerate(race_results, 1):
        driver = abbrs[code][0]
        company = abbrs[code][1]
        race_time = race_results[code]
        if current_driver:
            if driver == current_driver:
                race_table.append((counter, driver, company, race_time))
                break
            continue
        race_table.append((counter, driver, company, race_time))

    if current_driver and not race_table:
        return False
    return race_table


def print_race_result_table(race_results: list[tuple[int, str, str, str]]):
    """Print console table with race results"""
    race_limit = 15
    cli_table = PrettyTable()
    cli_table.field_names = ["№", "Driver", "Company", "Race time"]
    len_number = max([len(str(number[0])) for number in race_results])
    len_race_time = len(race_results[0][3])
    len_driver = max([len(driver[1]) for driver in race_results])
    len_company = max([len(company[2]) for company in race_results])
    print(len_driver)
    for counter, driver, company, race_time in race_results:
        cli_table.add_row([counter, driver, company, race_time])
        if counter == race_limit:
            cli_table.add_row(['#' * len_number, '#' * len_driver, '#' * len_company, '#' * len_race_time])
    print(cli_table)


def main(folder: str | None, order_asc: bool = True, order_desc: bool = False, driver: str = ''):
    """Main controller of cli_report module"""
    if order_asc and order_desc:
        print('Cannot use two options together: --asc --desc')
        return False
    try:
        race_results, abbrs = main_report(folder)
    except FileNotFoundError as e:
        print(e)
        return False
    order = 'desc' if order_desc else 'asc'
    race_results_sorted = sort_race_logs(race_results, order)
    race_table = prepare_race_table(race_results_sorted, abbrs, driver)
    if not race_table:
        print('Driver not found')
    else:
        print_race_result_table(race_table)


if __name__ == '__main__':
    args = parse_args()
    folder = args.files
    order_asc = args.asc
    order_desc = args.desc
    driver = args.driver
    main(folder, order_asc, order_desc, driver)
