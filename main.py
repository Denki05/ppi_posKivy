import os
import csv
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from models.auth import AuthManager

class LoginScreen(Screen):
    def authenticate_user(self, username, password):
        if AuthManager.authenticate(username, password):
            self.manager.current = 'dashboard'
            self.ids.login_message.text = ''
        else:
            self.ids.login_message.text = 'Invalid Username or Password'

class DashboardScreen(Screen):
    def logout(self):
        # Clear session data or any relevant information
        # Example: App.get_running_app().current_user = None
        self.manager.current = 'login'

class ProductScreen(Screen):
    products = ListProperty([])  # List to store loaded products

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

class SalesScreen(Screen):
    selected_product = ListProperty([])
    product_list = ListProperty([])  # List of product names for the spinner
    selected_brand = ListProperty([])
    products = []  # List of products to store product info

    def __init__(self, **kwargs):
        super(SalesScreen, self).__init__(**kwargs)
        self.all_products = []  # Store all products for searching

    def on_enter(self):
        product_screen = self.manager.get_screen('product')
        self.products = product_screen.products
        self.all_products = self.products.copy()  # Copy original products

    def update_products(self, brand_name):
        self.product_list.clear()
        if brand_name:
            self.product_list = [product for product in self.products if brand_name.lower() in product[1].lower()]

        if not self.product_list:
            self.ids.product_spinner.values = []
            self.ids.product_spinner.text = 'No products available'
        else:
            self.ids.product_spinner.values = [product[2] for product in self.product_list]

    def save_sale(self, customer, address, quantity):
        product_name = self.ids.product_spinner.text
        if not all([product_name, quantity, customer, address]):
            self.ids.sale_message.text = 'Please fill in all fields!'
            return

        try:
            quantity = int(quantity)
        except ValueError:
            self.ids.sale_message.text = 'Quantity must be an integer.'
            return

        self.show_confirmation_popup(customer, address, product_name, quantity)

    def show_confirmation_popup(self, customer, address, product_name, quantity):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text='Confirm Sale?', size_hint_y=None, height=40))

        btn_yes = Button(text='Yes', size_hint_y=None, height=40)
        btn_no = Button(text='No', size_hint_y=None, height=40)

        content.add_widget(btn_yes)
        content.add_widget(btn_no)

        popup = Popup(title='Confirm Save', content=content, size_hint=(0.6, 0.4))

        btn_yes.bind(on_release=lambda x: self.confirm_save(popup, customer, address, product_name, quantity))
        btn_no.bind(on_release=popup.dismiss)

        popup.open()

    def confirm_save(self, popup, customer, address, product_name, quantity):
        popup.dismiss()
        sale_code = f"sale_{len(os.listdir('assets/sales')) + 1}"
        filename = f'assets/sales/{sale_code}.csv'

        sale_entry = [sale_code, customer, address, product_name, quantity]
        with open(filename, mode='w', newline='') as csvfile:
            csv.writer(csvfile).writerow(['Sale Code', 'Customer', 'Address', 'Product Name', 'Quantity'])
            csv.writer(csvfile).writerow(sale_entry)

        self.ids.sale_message.text = 'Sale saved successfully!'
        self.reset_form()

    def reset_form(self):
        self.ids.customer.text = ''
        self.ids.address.text = ''
        self.ids.brand_name.text = 'Select Brand'
        self.ids.quantity.text = ''
        self.ids.product_spinner.text = 'Select Product'

class POSApp(App):
    def build(self):
        Builder.load_file('kv/main.kv')
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(ProductScreen(name='product'))
        sm.add_widget(SalesScreen(name='sales'))
        return sm

if __name__ == '__main__':
    POSApp().run()