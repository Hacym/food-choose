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
    pass

@get('/restaurant/<name:path>')
def restaurant(id):
    pass


if __name__ == "__main__":
    run(host='localhost', port=9000, debug=True, reloader=True)
