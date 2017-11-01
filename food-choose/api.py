from random import randint
import datetime

from bottle import (
    post,
    get,
    delete,
    run,
    hook
)

from models import (
    db,
    Restaurant,
    Review
)

@hook('before_request')
def connect_to_db():
    db.connect()

@hook('after_request')
def connect_to_db():
    db.close()

@get('/restaurant')
def restaurant_collection():
    """ Gives you a list of all possible restaurants. """

    restaurants = []

    for restaurant in Restaurant.select():
        restaurants.append(
                {
                    "restaurant_id": restaurant.restaurant_id,
                    "name": restaurant.name,
                    "last_suggested": restaurant.last_suggest
                }
            )
    return {"data": restaurants}

@get('/restaurant/random')
def restaurant_random():
    """ Passes back a random restaurant for easy choosing. """
    restaurants = Restaurant.select()
    number_of_restaurants = len(restaurants)

    random_number = randint(0, number_of_restaurants)

    restaurant = restaurants[random_number]

    if restaurant.last_suggest:
        last_suggest = restaurant.last_suggest.strftime('%m-%d-%Y')
    else:
        last_suggest = None

    return_data = {
            "data": {
                "restaurant_id": restaurant.restaurant_id,
                "name": restaurant.name,
                "last_suggested": last_suggest
            }
        }

    # Because we've suggested this place, now we need to update it to reflect that.
    restaurant.last_suggest = datetime.datetime.now()
    restaurant.save()

    return return_data

@get('/restaurant/<id:int>')
def restaurant(id):
    restaurant = Restaurant.select().where(Restaurant.restaurant_id == id).get()

    if restaurant.last_suggest:
        last_suggest = restaurant.last_suggest.strftime('%m-%d-%Y')
    else:
        last_suggest = None

    return {
            "data": {
                "restaurant_id": restaurant.restaurant_id,
                "name": restaurant.name,
                "last_suggested": last_suggest
            }
        }

if __name__ == "__main__":
    run(host='localhost', port=9000, debug=True, reloader=True)
