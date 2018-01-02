from bottle import default_app, route, hook
from peewee import *
import collections

db = MySQLDatabase(
    'nickcook530$healthydb',  # Required by Peewee.
    user='nickcook530',  # Will be passed directly to psycopg2.
    password='dbenter530',  # Ditto.
    host='nickcook530.mysql.pythonanywhere-services.com',  # Ditto.
)


class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db

class MenuStat2016(BaseModel):
    item_id = IntegerField(primary_key=True)
    item_restaurant = CharField()
    item_category = CharField()
    item_name = CharField()
    item_description = CharField(null=True)
    item_serving_size = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_serving_size_unit = CharField(null=True)
    item_serving_size_household = CharField(null=True)
    item_calories = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_total_fat = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_saturated_fat = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_trans_fat = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_cholesterol = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_sodium = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_potassium = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_carbohydrates = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_protein = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_sugar = DecimalField(max_digits=7, decimal_places=2, null=True)
    item_dietary_fiber = DecimalField(max_digits=7, decimal_places=2, null=True)



@hook('before_request')
def _connect_db():
    db.get_conn()
    print('Db is closed via before hook: {}'.format(db.is_closed()))

@hook('after_request')
def _close_db():
    db.close()
    print('Db is closed via after hook: {}'.format(db.is_closed()))

@route('/restaurantlist')
def restaurant_list():
    restaurant_dict = {}
    t = 1
    for entry in MenuStat2016.select(MenuStat2016.item_restaurant).distinct().order_by(MenuStat2016.item_restaurant.asc()):
        restaurant_dict[t] = entry.item_restaurant
        t += 1
    return restaurant_dict

@route('/<restaurant>/<foodfilter>')
def db_query(restaurant, foodfilter):
    if foodfilter == 'lowcal':
        lowcal_dict = {}
        t = 1
        for entry in MenuStat2016.select(MenuStat2016.item_name, MenuStat2016.item_category,
                        MenuStat2016.item_description, MenuStat2016.item_calories).where(
                        MenuStat2016.item_restaurant == restaurant).where(MenuStat2016.item_calories > 0).where((MenuStat2016.item_category != 'Beverages') &
                        (MenuStat2016.item_category != 'Toppings & Ingredients')).order_by(MenuStat2016.item_calories.asc()).limit(50):

            #lowcal_dict[entry.item_name] = {'calories':entry.item_calories, 'description':entry.item_description, 'category':entry.item_category}
            lowcal_dict[t] = {'name':entry.item_name, 'calories':entry.item_calories, 'description':entry.item_description, 'category':entry.item_category}
            t += 1
        return lowcal_dict

    if foodfilter == 'lowcarb':
        lowcarb_dict = {}
        t = 1
        for entry in MenuStat2016.select(MenuStat2016.item_name, MenuStat2016.item_category,
                        MenuStat2016.item_description, MenuStat2016.item_calories, MenuStat2016.item_carbohydrates).where(
                        MenuStat2016.item_restaurant == restaurant).where(MenuStat2016.item_calories > 0).where((MenuStat2016.item_category != 'Beverages') &
                        (MenuStat2016.item_category != 'Toppings & Ingredients')).order_by(MenuStat2016.item_carbohydrates.asc()).limit(50):

            #lowcarb_dict[entry.item_name] = {'carbs':entry.item_carbohydrates, 'calories':entry.item_calories, 'description':entry.item_description, 'category':entry.item_category}
            lowcarb_dict[t] = {'name':entry.item_name, 'carbs':entry.item_carbohydrates, 'calories':entry.item_calories, 'description':entry.item_description, 'category':entry.item_category}
            t += 1
        return lowcarb_dict

    if foodfilter == 'highprotein':
        highprotein_dict = {}
        t = 1
        for entry in MenuStat2016.select(MenuStat2016.item_name, MenuStat2016.item_category,
                        MenuStat2016.item_description, MenuStat2016.item_calories, MenuStat2016.item_protein).where(
                        MenuStat2016.item_restaurant == restaurant).where((MenuStat2016.item_calories > 0) &
                        (MenuStat2016.item_protein > 0)).order_by(MenuStat2016.item_protein.desc()).limit(50):

            #highprotein_dict[entry.item_name] = {'protein':entry.item_protein, 'calories':entry.item_calories, 'description':entry.item_description, 'category':entry.item_category}
            highprotein_dict[t] = {'name':entry.item_name, 'protein':entry.item_protein, 'calories':entry.item_calories, 'description':entry.item_description, 'category':entry.item_category}
            t += 1
        return highprotein_dict




application = default_app()