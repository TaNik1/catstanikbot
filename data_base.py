from peewee import SqliteDatabase, Model, IntegerField
import datetime as dt

db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db


class Chat(BaseModel):
    tg_id = IntegerField(default=0)
    settings = IntegerField(default=1)


db.connect()
db.create_tables([Chat])
