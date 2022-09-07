import requests
import json
import firebase_admin
from firebase_admin import credentials,auth
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import *
from kivymd.uix.floatlayout import *
from kivy.uix.scrollview import *
from kivymd.uix.toolbar import *
from kivymd.uix.card import *
from kivymd.uix.label import *
from kivymd.uix.bottomnavigation import *
from kivymd.uix.textfield import *
from kivymd.uix.button import *
from kivymd.uix.list import *
from kivymd.toast import toast
import login_screen
import switch_screen


class main(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        self.sm = ScreenManager()
        file = open("remember_login.txt","r")
        remember_check = file.read()
        
        if remember_check != "":
            switch_screen.switch_screen(self,remember_check,self.sm)
            file.close()
        elif remember_check == "":
            file.close()
            login_screen.Login(self,self.sm) 
  
        return self.sm
if __name__ == "__main__":  
    main().run()
