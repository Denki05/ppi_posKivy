import os

class ProductManager:
    @staticmethod
    def get_all_products():
        products = []
        try:
            with open('assets/product.txt', 'r') as file:
                products = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print("Product file not found.")
        return products
