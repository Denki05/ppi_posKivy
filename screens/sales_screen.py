import os
import csv
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class SalesScreen(Screen):
    selected_product = ListProperty([])
    product_list = ListProperty([])
    selected_brand = ListProperty([])
    products = []
    packaging = []  # To hold packaging data

    def __init__(self, **kwargs):
        super(SalesScreen, self).__init__(**kwargs)
        self.all_products = []

    def load_packaging_data(self):
        """Load packaging data from a file."""
        try:
            with open('assets/packaging.txt', 'r') as file:
                self.packaging = [line.strip().split(',') for line in file.readlines()]
            # Populate packaging spinner values
            self.ids.packaging_spinner.values = [f"{pkg[1]} ({pkg[0]})" for pkg in self.packaging]
            self.ids.packaging_spinner.text = 'Select Packaging'  # Set default text
        except FileNotFoundError:
            print("Packaging data file not found.")
            self.ids.packaging_spinner.values = []
            self.ids.packaging_spinner.text = 'No packaging available'

    def on_enter(self):
        product_screen = self.manager.get_screen('product')
        product_screen.load_product_data()  # Ensure products are reloaded
        self.products = product_screen.products
        self.all_products = self.products.copy()
        
        brand_name = self.ids.brand_name.text  # Get previously selected brand
        self.update_products(brand_name)  # Update products based on selected brand

        self.load_packaging_data()  # Move loading packaging data here

    def update_products(self, brand_name):
        self.product_list.clear()
        if brand_name:
            self.product_list = [product for product in self.all_products if brand_name.lower() in product[1].lower()]

        if not self.product_list:
            self.ids.product_spinner.values = []
            self.ids.product_spinner.text = 'No products available'
            self.ids.packaging_spinner.values = []
            self.ids.packaging_spinner.text = 'Select Packaging'
        else:
            # Combine product_code and product_name
            self.ids.product_spinner.values = [f"{product[2]} - {product[3]}" for product in self.product_list]
            self.ids.product_spinner.text = 'Select Product'

    def save_sale(self, customer, address, quantity):
        product_name = self.ids.product_spinner.text
        packaging_name = self.ids.packaging_spinner.text  # Get the selected packaging

        if not all([product_name, quantity, customer, address, packaging_name]):
            self.ids.sale_message.text = 'Please fill in all fields!'
            return

        try:
            quantity = int(quantity)
        except ValueError:
            self.ids.sale_message.text = 'Quantity must be an integer.'
            return

        self.show_confirmation_popup(customer, address, product_name, quantity, packaging_name)

    def show_confirmation_popup(self, customer, address, product_name, quantity, packaging_name):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text='Confirm Sale?', size_hint_y=None, height=40))

        btn_yes = Button(text='Yes', size_hint_y=None, height=40)
        btn_no = Button(text='No', size_hint_y=None, height=40)

        content.add_widget(btn_yes)
        content.add_widget(btn_no)

        popup = Popup(title='Confirm Save', content=content, size_hint=(0.6, 0.4))

        btn_yes.bind(on_release=lambda x: self.confirm_save(popup, customer, address, product_name, quantity, packaging_name))
        btn_no.bind(on_release=popup.dismiss)

        popup.open()

    def confirm_save(self, popup, customer, address, product_name, quantity, packaging_name):
        popup.dismiss()
        sale_code = f"sale_{len(os.listdir('assets/sales')) + 1}"
        filename = f'assets/sales/{sale_code}.csv'

        sale_entry = [sale_code, customer, address, product_name, packaging_name, quantity]
        with open(filename, mode='w', newline='') as csvfile:
            csv.writer(csvfile).writerow(['Sale Code', 'Customer', 'Address', 'Product Name', 'Packaging', 'Quantity'])
            csv.writer(csvfile).writerow(sale_entry)

        self.ids.sale_message.text = 'Sale saved successfully!'
        self.reset_form()

    def reset_form(self):
        self.ids.customer.text = ''
        self.ids.address.text = ''
        self.ids.brand_name.text = 'Select Brand'
        self.ids.quantity.text = ''
        self.ids.product_spinner.text = 'Select Product'
        self.ids.packaging_spinner.text = 'Select Packaging'  # Reset packaging spinner
