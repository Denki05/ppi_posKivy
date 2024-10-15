import json
import os

class AuthManager:
    @staticmethod
    def authenticate(username, password):
        try:
            with open('assets/data_login.json', 'r') as file:
                login_data = json.load(file)
            for user in login_data.get('users', []):
                if user['username'] == username and user['password'] == password:
                    return True
        except FileNotFoundError:
            print("Login data file not found.")
        return False