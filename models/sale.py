import csv
import os

class SaleManager:
    @staticmethod
    def record_sale(product_name, quantity, price):
        total = price * quantity
        try:
            with open('assets/sales.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([product_name, quantity, price, total])
        except Exception as e:
            print(f"Error saving sale: {e}")
