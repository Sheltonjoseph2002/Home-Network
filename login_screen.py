
import switch_screen
from firebase_admin import credentials,auth
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivymd.app import MDApp
from kivymd.uix.boxlayout import *
from kivymd.uix.floatlayout import *
from kivy.uix.scrollview import *
from kivymd.uix.toolbar import *
from kivymd.uix.card import *
from kivymd.uix.label import *
from kivymd.uix.bottomnavigation import *
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import *
from kivymd.uix.list import *
from kivymd.toast import toast

def Login(self,sm):
        login_screen = Screen(name = "login_screen")
        lay = MDFloatLayout()
        
        email_id = MDTextField(
            hint_text= "E-Mail",
            size_hint_x= .9,
            mode = "rectangle",
            pos_hint= {"center_x": .5, "center_y": .65},
            helper_text_mode= "on_error",
            helper_text= "Enter text"
            )

        lay.add_widget(email_id)
        def call_back(verify_id,sm):
            switch_screen.switch_screen(self,verify_id,sm)
        b = MDRaisedButton(
            text="Login",
            pos_hint= {"center_x": .5, "center_y": .4},
            on_release = lambda x: call_back(email_id.text,sm)
            )
        
        lay.add_widget(b)
        login_screen.add_widget(lay)
        self.sm.add_widget(login_screen)
        self.sm.current = "login_screen"
        
