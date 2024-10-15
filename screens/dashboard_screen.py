from kivy.uix.screenmanager import Screen

class DashboardScreen(Screen):
    def logout(self):
        self.manager.current = 'login'
