import os

from peewee import *

db = SqliteDatabase(os.path.expanduser('~/food-choose.db'))

class Restaurant(Model):
    restaurant_id = IntegerField(primary_key=True)
    last_suggest = DateField()

    class Meta:
        database = db

class Review(Model):
    review_id = IntegerField(primary_key=True)
    restaurant_id = ForeignKeyField(Restaurant, null=True)
    rating = IntegerField()
    rating_date = DateField()

    class Meta:
        database = db

if __name__ == "__main__":
    db.create_tables([Restaurant, Review])
