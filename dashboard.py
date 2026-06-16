from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.scrollview import ScrollView

class DashboardScreen(MDScreen):
    def __init__(self, user_data, app, **kwargs):
        super().__init__(**kwargs)
        self.user_data = user_data
        self.app = app
        self.current_module = None
        self.build_ui()
    
    def build_ui(self):
        """بناء لوحة التحكم"""
        main_layout = MDBoxLayout(orientation="vertical")
        
        # شريط العنوان
        toolbar = MDTopAppBar(
            title="لوحة التحكم",
            size_hint_y=0.08,
            left_action_items=[["arrow-left", lambda x: self.logout()]],
            right_action_items=[["account", lambda x: self.show_profile()]]
        )
        main_layout.add_widget(toolbar)
        
        # محتوى الصفحة
        self.content_frame = MDBoxLayout(
            orientation="vertical",
            size_hint_y=0.92
        )
        self.show_home_content()
        main_layout.add_widget(self.content_frame)
        
        self.add_widget(main_layout)
    
    def show_home_content(self):
        """عرض الصفحة الرئيسية"""
        self.content_frame.clear_widgets()
        
        # تحية للمستخدم
        greeting = MDLabel(
            text=f"أهلاً وسهلاً {self.user_data['username']}",
            font_style="H6",
            halign="right",
            size_hint_y=0.1,
            padding="10dp"
        )
        self.content_frame.add_widget(greeting)
        
        # قائمة الوحدات
        scroll = ScrollView(size_hint_y=0.9)
        grid = MDGridLayout(
            cols=2,
            spacing="15dp",
            padding="15dp",
            size_hint_y=None,
            height=1200
        )
        
        modules = [
            ("📊 الحسابات", "accounts", "إدارة الحسابات المالية"),
            ("📦 المخزون", "inventory", "إدارة المخزون والمواد"),
            ("👥 الموظفين", "employees", "إدارة الموظفين"),
            ("🌾 الأعلاف", "feed", "إدارة الأعلاف والمستلزمات"),
            ("🐄 الحيوانات", "animals", "إدارة الثروة الحيوانية"),
            ("📈 التقارير", "reports", "عرض التقارير والإحصائيات"),
        ]
        
        for icon_title, module_name, description in modules:
            card = MDCard(
                orientation="vertical",
                padding="15dp",
                spacing="10dp",
                size_hint_y=None,
                height=180,
                elevation=2,
                radius=[10],
                md_bg_color=(0.95, 0.95, 0.95, 1)
            )
            
            title_label = MDLabel(
                text=icon_title,
                font_style="H6",
                size_hint_y=0.3
            )
            card.add_widget(title_label)
            
            desc_label = MDLabel(
                text=description,
                font_style="Caption",
                size_hint_y=0.3,
                color=(0.5, 0.5, 0.5, 1)
            )
            card.add_widget(desc_label)
            
            btn = MDRaisedButton(
                text="فتح",
                size_hint_y=0.4,
                size_hint_x=1
            )
            btn.bind(on_press=lambda x, m=module_name: self.open_module(m))
            card.add_widget(btn)
            
            grid.add_widget(card)
        
        scroll.add_widget(grid)
        self.content_frame.add_widget(scroll)
    
    def open_module(self, module_name):
        """فتح الوحدة المطلوبة"""
        self.content_frame.clear_widgets()
        
        if module_name == "accounts":
            from app.modules.accounts import AccountsModule
            self.current_module = AccountsModule(self.content_frame, self.user_data, self)
        
        elif module_name == "inventory":
            from app.modules.inventory import InventoryModule
            self.current_module = InventoryModule(self.content_frame, self.user_data, self)
        
        elif module_name == "employees":
            from app.modules.employees import EmployeesModule
            self.current_module = EmployeesModule(self.content_frame, self.user_data, self)
        
        elif module_name == "feed":
            from app.modules.feed import FeedModule
            self.current_module = FeedModule(self.content_frame, self.user_data, self)
        
        elif module_name == "animals":
            self.show_placeholder("إدارة الحيوانات")
        
        elif module_name == "reports":
            self.show_placeholder("التقارير والفواتير")
    
    def show_placeholder(self, title):
        """عرض واجهة مؤقتة"""
        layout = MDBoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="20dp"
        )
        
        # زر العودة
        back_btn = MDFlatButton(text="← العودة", size_hint_y=0.1)
        back_btn.bind(on_press=lambda x: self.show_home_content())
        layout.add_widget(back_btn)
        
        label = MDLabel(
            text=f"{title}\n\nقيد التطوير",
            font_style="H5",
            halign="center",
            size_hint_y=0.9
        )
        layout.add_widget(label)
        
        self.content_frame.add_widget(layout)
    
    def logout(self):
        """تسجيل الخروج"""
        self.app.go_back_to_login()
    
    def show_profile(self):
        """عرض الملف الشخصي"""
        pass