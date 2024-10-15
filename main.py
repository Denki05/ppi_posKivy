from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from screens.login_screen import LoginScreen
from screens.dashboard_screen import DashboardScreen
from screens.product_screen import ProductScreen
from screens.sales_screen import SalesScreen
from kivy.core.window import Window

# Set the window size
Window.size = (800, 600)

class POSApp(App):
    def build(self):
        # Load the main KV file and other individual KV files for screens
        Builder.load_file('kv/main.kv')  # Load the main KV file
        Builder.load_file('kv/login_screen.kv')  # Load the login screen KV file
        Builder.load_file('kv/dashboard_screen.kv')  # Load the dashboard screen KV file
        Builder.load_file('kv/product_screen.kv')  # Load the product screen KV file
        Builder.load_file('kv/sales_screen.kv')  # Load the sales screen KV file

        # Initialize the ScreenManager and add screens
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(ProductScreen(name='product'))
        sm.add_widget(SalesScreen(name='sales'))

        sm.current = 'login'  # Set the initial screen to login
        return sm

if __name__ == '__main__':
    POSApp().run()