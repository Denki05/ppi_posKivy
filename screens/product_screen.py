import os
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.uix.label import Label

class ProductScreen(Screen):
    products = ListProperty([])

    def on_enter(self):
        self.load_product_data()

    def load_product_data(self):
        self.ids.product_grid.clear_widgets()
        self.products.clear()

        product_file = 'assets/product.txt'
        if not os.path.exists(product_file):
            self.ids.product_grid.add_widget(Label(text="No product data found.", size_hint=(1, None), height=40))
            return

        with open(product_file, 'r') as file:
            lines = file.readlines()

        headers = ['ID', 'Brand', 'Code', 'Name']
        for header in headers:
            self.ids.product_grid.add_widget(Label(text=header, bold=True, size_hint=(1, None), height=40))

        for line in lines:
            product_data = line.strip().split(',')
            if len(product_data) == 4:
                self.products.append(product_data)
                for item in product_data:
                    self.ids.product_grid.add_widget(Label(text=item, size_hint=(1, None), height=40))
