import os
import csv
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from models.auth import AuthManager
from models.product import ProductManager
from models.sale import SaleManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class LoginScreen(Screen):
    def authenticate_user(self, username, password):
        if AuthManager.authenticate(username, password):
            self.manager.current = 'dashboard'
            self.ids.login_message.text = ''
        else:
            self.ids.login_message.text = 'Invalid Username or Password'

class DashboardScreen(Screen):
    pass

class ProductScreen(Screen):
    products = ListProperty([])  # List to store loaded products

    def on_enter(self):
        self.load_product_data()

    def load_product_data(self):
        # Clear existing data
        self.ids.product_table.clear_widgets()
        self.products.clear()  # Clear previous product list

        # Read the product data from the text file
        product_file = 'assets/product.txt'
        if not os.path.exists(product_file):
            self.ids.product_table.add_widget(Label(text="No product data found."))
            return

        with open(product_file, 'r') as file:
            lines = file.readlines()

        # Create header
        headers = ['ID', 'Brand', 'Code', 'Name']
        for header in headers:
            self.ids.product_table.add_widget(Label(text=header, bold=True))

        # Add product data to the table
        for line in lines:
            product_data = line.strip().split(',')
            if len(product_data) == 4:
                self.products.append(product_data)  # Store product data in the list
                for item in product_data:
                    self.ids.product_table.add_widget(Label(text=item))

class SalesScreen(Screen):
    selected_product = ObjectProperty(None)
    product_list = ListProperty([])  # List of product names for the spinner
    selected_brand = ObjectProperty(None)  # Selected brand from spinner
    products = []  # List of products to store product info loaded from the product screen

    def __init__(self, **kwargs):
        super(SalesScreen, self).__init__(**kwargs)

    def on_enter(self):
        # Get products from the ProductScreen
        product_screen = self.manager.get_screen('product')
        self.products = product_screen.products  # Assuming this is a list of products from the product screen

    def update_products(self, brand_name):
        # Filter products based on the brand name
        self.product_list.clear()  # Clear previous options

        if brand_name:
            for product_info in self.products:
                if brand_name.lower() in product_info[1].lower():  # Assuming brand name is at index 1
                    self.product_list.append(product_info)  # Append entire product info

        # Check if product_list is empty and update the spinner accordingly
        if not self.product_list:
            self.ids.product_spinner.values = []  # No products available
            self.ids.product_spinner.text = 'No products available'
        else:
            self.ids.product_spinner.values = [product[2] for product in self.product_list]  # Only product names

    def on_product_select(self, product_name):
        # Automatically fill in product code based on selected product
        for product_info in self.product_list:
            if product_info[2] == product_name:  # Assuming product name is at index 2
                self.ids.product_code.text = product_info[1]  # Assuming product code is at index 1
                break

    def save_sale(self, customer, address, quantity):
        product_name = self.ids.product_spinner.text
        if not product_name or not quantity or not customer or not address:
            self.ids.sale_message.text = 'Please fill in all fields!'
            return

        try:
            quantity = int(quantity)
        except ValueError:
            self.ids.sale_message.text = 'Invalid input! Quantity must be an integer.'
            return

        self.show_confirmation_popup(customer, address, product_name, quantity)

    def show_confirmation_popup(self, customer, address, product_name, quantity):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Are you sure you want to save this sale?'))

        btn_yes = Button(text='Yes')
        btn_no = Button(text='No')

        content.add_widget(btn_yes)
        content.add_widget(btn_no)

        popup = Popup(title='Confirm Save', content=content, size_hint=(0.6, 0.4))

        btn_yes.bind(on_release=lambda x: self.confirm_save(popup, customer, address, product_name, quantity))
        btn_no.bind(on_release=popup.dismiss)

        popup.open()

    def confirm_save(self, popup, customer, address, product_name, quantity):
        popup.dismiss()  # Close the popup
        self.sale_code = f"sale_{len(os.listdir('assets/sales')) + 1}"
        filename = f'assets/sales/{self.sale_code}.csv'

        sale_entry = [self.sale_code, customer, address, product_name, quantity]
        with open(filename, mode='w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Sale Code', 'Customer', 'Address', 'Product Name', 'Quantity'])
            csvwriter.writerow(sale_entry)

        self.ids.sale_message.text = 'Sale saved successfully!'
        self.reset_form()

    def reset_form(self):
        self.ids.customer.text = ''
        self.ids.address.text = ''
        self.ids.brand_name.text = ''
        self.ids.quantity.text = ''
        self.ids.product_spinner.text = 'Select Product'  # Reset the product selection
        self.ids.product_code.text = ''  # Reset product code

class POSApp(App):
    def build(self):
        # Load the KV file manually
        Builder.load_file('kv/main.kv')
        
        # Set up the ScreenManager
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(ProductScreen(name='product'))
        sm.add_widget(SalesScreen(name='sales'))
        return sm

if __name__ == '__main__':
    POSApp().run()