from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.popup import Popup

class LoginScreen(MDScreen):
    def __init__(self, on_login_callback, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.on_login_callback = on_login_callback
        self.app_ref = app_ref
        self.build_ui()
    
    def build_ui(self):
        """بناء واجهة تسجيل الدخول"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )
        
        # عنوان التطبيق
        title = MDLabel(
            text="نظام إدارة المزرعة",
            font_style="H3",
            halign="center",
            size_hint_y=0.2
        )
        main_layout.add_widget(title)
        
        # بطاقة تسجيل الدخول
        card = MDCard(
            orientation="vertical",
            padding="25dp",
            spacing="15dp",
            size_hint_y=0.7,
            elevation=3,
            radius=[15],
            md_bg_color=(1, 1, 1, 1)
        )
        
        # حقل اسم المستخدم
        self.username_field = MDTextField(
            hint_text="اسم المستخدم",
            mode="rectangle",
            size_hint_x=1,
            multiline=False
        )
        card.add_widget(self.username_field)
        
        # حقل كلمة المرور
        self.password_field = MDTextField(
            hint_text="كلمة المرور",
            password=True,
            mode="rectangle",
            size_hint_x=1,
            multiline=False
        )
        card.add_widget(self.password_field)
        
        # زر تسجيل الدخول
        login_btn = MDRaisedButton(
            text="دخول",
            size_hint_x=1,
            size_hint_y=None,
            height="50dp"
        )
        login_btn.bind(on_press=self.handle_login)
        card.add_widget(login_btn)
        
        main_layout.add_widget(card)
        self.add_widget(main_layout)
    
    def handle_login(self, instance):
        """معالجة تسجيل الدخول"""
        username = self.username_field.text.strip()
        password = self.password_field.text.strip()
        
        if not username or not password:
            self.show_error("الرجاء ملء جميع الحقول")
            return
        
        # التحقق من بيانات المستخدم
        user_data = self.app_ref.db.authenticate_user(username, password)
        
        if user_data:
            self.on_login_callback(user_data)
        else:
            self.show_error("اسم المستخدم أو كلمة المرور غير صحيحة")
    
    def show_error(self, message):
        """عرض رسالة خطأ"""
        content = MDBoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="15dp"
        )
        
        label = MDLabel(text=message)
        content.add_widget(label)
        
        close_btn = MDRaisedButton(
            text="حسناً",
            size_hint_x=1
        )
        
        popup = Popup(
            title="تنبيه",
            content=content,
            size_hint=(0.8, 0.3)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()