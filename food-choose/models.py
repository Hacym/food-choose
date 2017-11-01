import os
import math

import requests
from peewee import *
from config import get_config

config = get_config()
db = SqliteDatabase(os.path.expanduser(config.get('db', 'location')))

class Establishment(Model):
    establishment_id = IntegerField()
    name = CharField()
 
    class Meta:
        database = db

class Restaurant(Model):
    restaurant_id = IntegerField()
    name = CharField()
    last_suggest = DateField(null=True)
    establishment_id = ForeignKeyField(Establishment, null=True)

    class Meta:
        database = db

class Review(Model):
    review_id = IntegerField(primary_key=True)
    restaurant_id = ForeignKeyField(Restaurant, null=True)
    rating = IntegerField()
    rating_date = DateField()

    class Meta:
        database = db

def populate_restaurant_list(
        location_id=config.get("zomato", "location_id"),
        location_type=config.get("zomato", "location_type")
    ):

    # These headers are required for any calls to the Zamoto API, so we'll
    # just go ahead and set these immediately.
    headers = {'user-key' : config.get("zomato", "api_key")}

    # First, let's get the type of establishments that we have to work with.
    establishments_url = (
            "https://developers.zomato.com/api/v2.1/establishments?city_id={}"
            .format(location_id)
        )

    r = requests.get(establishments_url, headers=headers)
    response = r.json()

    for establishment in response['establishments']:
        new_establishment = Establishment(
                establishment_id=establishment['establishment']['id'],
                name=establishment['establishment']['name']
            )

        new_establishment.save()

    establishments = [establishment.establishment_id for establishment in Establishment.select()]



    for establishment_id in establishments:
        zomato_url = (
            "https://developers.zomato.com/api/v2.1/search?entity_id={}&entity_type={}&establishment_type={}"
        ).format(
            location_id,
            location_type,
            establishment_id
        )

        r = requests.get(zomato_url, headers=headers)

        response = r.json()

        num_results = response['results_found']

        for restaurant in response['restaurants']:
            new_restaurant = Restaurant(
                    restaurant_id=restaurant['restaurant']['id'],
                    name=restaurant['restaurant']['name'],
                    establishment_id=establishment_id
                )

            new_restaurant.save()
        
        if (num_results - 20) > 0: 
            offset = 20
            for x in range(int((num_results - 20) / 20)):

                zomato_url = (
                    "https://developers.zomato.com/api/v2.1/search?entity_id={}&entity_type={}&start={}"
                ).format(
                    location_id,
                    location_type,
                    offset
                )

                zomato_url += "&establishment_type={}".format(establishment_id)

                r = requests.get(zomato_url, headers=headers)
                response = r.json()

                for restaurant in response['restaurants']:
                    new_restaurant = Restaurant(
                            restaurant_id=restaurant['restaurant']['id'],
                            name=restaurant['restaurant']['name']
                        )

                    new_restaurant.save()

                offset += 20

if __name__ == "__main__":
    db.create_tables([Restaurant, Review, Establishment])
    populate_restaurant_list()
