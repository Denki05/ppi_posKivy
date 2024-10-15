from kivy.uix.screenmanager import Screen
from models.auth import AuthManager

class LoginScreen(Screen):
    def authenticate_user(self, username, password):
        if AuthManager.authenticate(username, password):
            self.manager.current = 'dashboard'
            self.ids.login_message.text = ''
        else:
            self.ids.login_message.text = 'Invalid Username or Password'