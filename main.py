from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from app.auth import LoginScreen
from app.dashboard import DashboardScreen
from app.database import Database

# إعدادات النافذة
Window.size = (400, 800)

class FarmManagementApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.current_user = None
        
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "500"
        
        self.screen_manager = MDScreenManager()
        
        # شاشة تسجيل الدخول
        login_screen = LoginScreen(
            name="login",
            on_login_callback=self.on_login_success,
            app_ref=self
        )
        self.screen_manager.add_widget(login_screen)
        
        return self.screen_manager
    
    def on_login_success(self, user_data):
        """عند نجاح تسجيل الدخول"""
        self.current_user = user_data
        
        # شاشة لوحة التحكم
        dashboard = DashboardScreen(
            name="dashboard",
            user_data=user_data,
            app=self
        )
        self.screen_manager.add_widget(dashboard)
        self.screen_manager.current = "dashboard"
    
    def go_back_to_login(self):
        """العودة إلى شاشة تسجيل الدخول"""
        self.current_user = None
        self.screen_manager.current = "login"

if __name__ == "__main__":
    FarmManagementApp().run()