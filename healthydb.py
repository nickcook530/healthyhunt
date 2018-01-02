from peewee import *
#(MySQLDatabase, Model, CharField, FloatField)

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




db.connect()
restaurant_dict = {}
t = 1
for entry in MenuStat2016.select(MenuStat2016.item_restaurant).distinct():
    restaurant_dict[t] = entry.item_restaurant
    t += 1
print(restaurant_dict)
db.close()