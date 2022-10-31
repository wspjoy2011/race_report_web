from peewee import *

database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Driver(BaseModel):
    abbr = CharField(max_length=3)
    name = CharField(max_length=100)


class Company(BaseModel):
    name = CharField(max_length=3)


class Race(BaseModel):
    place = IntegerField()
    driver = ForeignKeyField(Driver)
    company = ForeignKeyField(Company)
    time = DateTimeField()
