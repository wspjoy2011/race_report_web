import os
from typing import NamedTuple
from datetime import datetime
from peewee import SqliteDatabase

from models.race_model import Driver, Company, Race, database_proxy
from database import PATH_TO_DATABASE
from database.exceptions.create import DatabaseAlreadyExist, DatabaseTableAlreadyExist


class RaceReport(NamedTuple):
    place: int
    driver: str
    company: str
    race_time: datetime


def create_db(db_name: str) -> bool:
    if os.path.isfile(os.path.join(PATH_TO_DATABASE, db_name)):
        raise DatabaseAlreadyExist(f'Database {db_name} exist')

    db = SqliteDatabase(os.path.join(PATH_TO_DATABASE, db_name))
    database_proxy.initialize(db)
    db.create_tables([Driver, Company, Race])
    return True


def write_drivers(drivers: list[dict[str, str]]) -> bool:
    if not Driver.select().count():
        for driver in drivers:
            driver = Driver(abbr=driver['abbr'], name=driver['name'])
            driver.save()
        return True
    raise DatabaseTableAlreadyExist('Table "Driver" is not empty. I don\'t do anything')


def write_companies(companies: list[dict[str, str]]) -> bool:
    if not Company.select().count():
        for company in companies:
            company = Company(name=company['name'])
            company.save()
        return True
    raise DatabaseTableAlreadyExist('Table "Company" is not empty. I don\'t do anything')


def write_race_table(race_table: list[RaceReport]) -> bool:
    if not Race.select().count():
        for race in race_table:
            driver_rows = Driver.select().where(Driver.name == race.driver)
            company_rows = Company.select().where(Company.name == race.company)
            if driver_rows and company_rows:
                place = race.place
                driver = list(driver_rows).pop()
                company = list(company_rows).pop()
                race_time = race.race_time
                race_complete = Race(
                    place=place,
                    driver=driver,
                    company=company,
                    time=race_time
                )
                race_complete.save()
        return True
    raise DatabaseTableAlreadyExist('Table "Company" is not empty. I don\'t do anything')
