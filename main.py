from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import requests
from requests.auth import HTTPBasicAuth

def restart(event):
    global final_url
    final_url = 'http://www.healthyhunt.xyz/'
    sm.remove_widget(sm.current_screen) # removes results so they can be repopulated
    sm.current = 'restaurantscreen'
    print(final_url)

def restaurant_to_filter(event):
    restaurant = event.text.replace("'", "%27").replace(" ", "%20")
    global final_url
    final_url += restaurant
    print(final_url)
    sm.current = 'filterscreen'


def filter_to_result(event):
    global final_url
    if event.text == 'Low Calorie Options':
        filter = '/lowcal'
        final_url += filter
    if event.text == 'Low Carbohydrate Options':
        filter = '/lowcarb'
        final_url += filter
    if event.text == 'High Protein Options':
        filter = '/highprotein'
        final_url += filter
    print(final_url)
    sc3 = ResultScreen()
    sm.add_widget(sc3)
    sm.current = 'resultscreen'

class RestaurantScreen(Screen):

    def __init__(self, *args, **kwargs):
        self.name = 'restaurantscreen'
        super(RestaurantScreen, self).__init__(*args, **kwargs)
        self.restaurant_screen_layout()

    def restaurant_screen_layout(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        with requests.Session() as s:
            query_dict = s.get('http://www.healthyhunt.xyz/restaurantlist',
                               auth=HTTPBasicAuth('healthykivy', 'knockknock469')).json()
            s.close()
        # build the restaurant buttons based on alphabetic dict
        rank = 1
        for _ in query_dict:
            btn = Button(text=str(query_dict[str(rank)]), size_hint_y=None, height=40)
            btn.bind(on_release=restaurant_to_filter)
            layout.add_widget(btn)
            rank += 1
        # layer on the widgets to allow scrolling
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        self.add_widget(root)

class FilterScreen(Screen):
    def __init__(self, *args, **kwargs):
        self.name = 'filterscreen'
        super(FilterScreen, self).__init__(*args, **kwargs)
        self.filter_screen_layout()

    def filter_screen_layout(self):
        layout = GridLayout(cols=1, spacing=10)

        lowcal_btn = Button(text='Low Calorie Options', size_hint_y=None, height=40)
        lowcal_btn.bind(on_release=filter_to_result)
        layout.add_widget(lowcal_btn)

        lowcarb_btn = Button(text='Low Carbohydrate Options', size_hint_y=None, height=40)
        lowcarb_btn.bind(on_release=filter_to_result)
        layout.add_widget(lowcarb_btn)

        highprotein_btn = Button(text='High Protein Options', size_hint_y=None, height=40)
        highprotein_btn.bind(on_release=filter_to_result)
        layout.add_widget(highprotein_btn)

        self.add_widget(layout)

class ResultScreen(Screen):
    def __init__(self, *args, **kwargs):
        self.name = 'resultscreen'
        super(ResultScreen, self).__init__(*args, **kwargs)
        self.result_screen_layout()

    def result_screen_layout(self):
        global final_url
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        with requests.Session() as s:
            query_dict = s.get(final_url, auth=HTTPBasicAuth('healthykivy', 'knockknock469')).json()
            s.close()

        rank = 1
        for _ in query_dict:
            btn = Button(text=str(query_dict[str(rank)]['name']) + ' | calories = {},'.format(query_dict[str(rank)]['calories']), size_hint_y=None, height=40)
            btn.bind(on_release=restart)
            layout.add_widget(btn)
            rank += 1
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        self.add_widget(root)

class MyScreenManagement(ScreenManager):
    def __init__(self, *args, **kwargs):
        self.transition = FadeTransition()
        super(MyScreenManagement, self).__init__(*args, **kwargs)
        self.boot_up()

    def boot_up(self):
        sc1 = RestaurantScreen()
        sc2 = FilterScreen()
        #sc3 = ResultScreen()
        self.add_widget(sc1)
        self.add_widget(sc2)
        #self.add_widget(sc3)



# presentation = Builder.load_file("main.kv")
final_url = 'http://www.healthyhunt.xyz/'
sm = MyScreenManagement()
class TestClass(App):
    def build(self):
        return sm

if __name__ == "__main__":
    TestClass().run()