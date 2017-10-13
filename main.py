from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
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
        box = BoxLayout(orientation='vertical')
        header = Label(text='1) Select a Restaurant:', font_size='50', halign='left', padding=(100, 100), markup=True, bold=True)
        box.add_widget(header)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=[50, 0, 50, 0])  # size_hint_x=.8

        #box.add_widget(header)
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-header.height), bar_color=(0.051, 0.173, 1, 0.9),
                            bar_inactive_color=(0.051, 0.173, 1, 0.9), bar_width=10)

        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))

        with requests.Session() as s:
            query_dict = s.get('http://www.healthyhunt.xyz/restaurantlist',
                               auth=HTTPBasicAuth('healthykivy', 'knockknock469')).json()
            s.close()
        # build the restaurant buttons based on alphabetic dict
        rank = 1
        for _ in query_dict:
            btn = Button(text=str(query_dict[str(rank)]), size_hint_y=None, height=150, halign='center', valign='center')
            btn.bind(on_release=restaurant_to_filter)
            btn.bind(size=btn.setter('text_size'))
            layout.add_widget(btn)
            rank += 1
        # layer on the widgets to allow scrolling

        scroll.add_widget(layout)
        box.add_widget(scroll)
        self.add_widget(box)

class FilterScreen(Screen):
    def __init__(self, *args, **kwargs):
        self.name = 'filterscreen'
        super(FilterScreen, self).__init__(*args, **kwargs)
        self.filter_screen_layout()

    def filter_screen_layout(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[50, 0, 50, 50])
        header = Label(text='2) Select a Nutrition Filter:', font_size='50', halign='left',
                       padding=(100, 100), markup=True, bold=True)
        layout.add_widget(header)

        lowcal_btn = Button(text='Low Calorie Options')
        lowcal_btn.bind(on_release=filter_to_result)
        layout.add_widget(lowcal_btn)

        lowcarb_btn = Button(text='Low Carbohydrate Options')
        lowcarb_btn.bind(on_release=filter_to_result)
        layout.add_widget(lowcarb_btn)

        highprotein_btn = Button(text='High Protein Options')
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

        box = BoxLayout(orientation='vertical')
        header = Label(text='3) Tasty Results!', font_size='50', halign='left', padding=(100, 100), markup=True, bold=True)
        box.add_widget(header)
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-header.height), bar_color=(0.051, 0.173, 1, 0.9),
                          bar_inactive_color=(0.051, 0.173, 1, 0.9), bar_width=10)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=[50, 0, 50, 0])
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        with requests.Session() as s:
            query_dict = s.get(final_url, auth=HTTPBasicAuth('healthykivy', 'knockknock469')).json()
            s.close()

        rank = 1

        if 'lowcal' in final_url:
            for _ in query_dict:
                name = query_dict[str(rank)]['name']
                calories = query_dict[str(rank)]['calories']
                btn = Button(text='[b][u]' + str(name) + '[/u][/b]' + '\nCalories = {}'.format(calories),
                                    size_hint_y=None, height=150, halign='center', valign='center', markup=True)
                btn.bind(on_release=restart)
                btn.bind(size=btn.setter('text_size'))
                layout.add_widget(btn)
                rank += 1

        if 'lowcarb' in final_url:
            for _ in query_dict:
                name = query_dict[str(rank)]['name']
                carbs = query_dict[str(rank)]['carbs']
                calories = query_dict[str(rank)]['calories']
                btn = Button(text='[b][u]' + str(name) + '[/u][/b]' + '\nCarbs = {} grams'.format(carbs) +
                                ' | Calories = {}'.format(calories), size_hint_y=None, height=150, halign='center',
                                valign='center', markup=True)
                btn.bind(on_release=restart)
                btn.bind(size=btn.setter('text_size'))
                layout.add_widget(btn)
                rank += 1

        if 'highprotein' in final_url:
            for _ in query_dict:
                name = query_dict[str(rank)]['name']
                protein = query_dict[str(rank)]['protein']
                calories = query_dict[str(rank)]['calories']
                ratio = round(protein/calories, 2)
                btn = Button(text='[b][u]' + str(name) + '[/u][/b]' + '\nProtein = {} grams'.format(protein) +
                              ' | Calories = {}'.format(calories) + '\nRatio = {} grams of Protein per Calorie'.format(ratio),
                             size_hint_y=None, height=250, halign='center', valign='center', markup=True)
                btn.bind(size=btn.setter('text_size'))
                btn.bind(on_release=restart)
                layout.add_widget(btn)
                rank += 1

        scroll.add_widget(layout)
        box.add_widget(scroll)
        self.add_widget(box)

class MyScreenManagement(ScreenManager):
    def __init__(self, *args, **kwargs):
        self.transition = FadeTransition()
        super(MyScreenManagement, self).__init__(*args, **kwargs)
        self.boot_up()

    def boot_up(self):
        sc1 = RestaurantScreen()
        sc2 = FilterScreen()
        self.add_widget(sc1)
        self.add_widget(sc2)



# presentation = Builder.load_file("main.kv")
final_url = 'http://www.healthyhunt.xyz/'
sm = MyScreenManagement()
class TestClass(App):
    def build(self):
        return sm

if __name__ == "__main__":
    TestClass().run()