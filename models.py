from peewee import *

DATABASE = 'worklog.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):

    class Meta():

        database = database

class Entry(BaseModel):

    name = TextField()
    date = DateTimeField()
    title = TextField()
    time_spent = IntegerField()
    notes = TextField()


