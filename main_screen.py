from asyncore import write
from distutils.command.upload import upload
import requests
import json
import main_screen,login_screen,switch_screen
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
from kivymd.uix.textfield import *
from kivymd.uix.button import *
from kivymd.utils import asynckivy
from kivymd.uix.refreshlayout import *
from kivymd.uix.list import *
from kivymd.toast import toast

def main_screen(self,sm,user_id):
        screen = Screen(name = "main_screen")
        
        boxlayout = MDBoxLayout(orientation = "vertical")
        
        def logout():
            login_screen.Login(self,sm)
            f = open('remember_login.txt',"w+")
            f.close()

        toolbar = MDToolbar(title = 'Balance Amount')
        toolbar.right_action_items = [["logout", lambda x: logout()]]
        boxlayout.add_widget(toolbar)
     
        amount_card = MDCard (
            size_hint_y= .4,
            pos_hint= {"center_x": .5, "center_y": .7},
            elevation= 20,
            radius= 70,
            ripple_behavior= True
            
        )
        boxlayout.add_widget(amount_card)
        firebase_url = "https://home-network-52f96-default-rtdb.firebaseio.com/"
        balance = requests.get(url=firebase_url+ ".json").json()

        json_file = open('json_file.json', 'w')
        json.dump(balance, json_file)

        json_file = open('json_file.json', 'r')
        #json.dump(balance, json_file)
        json_dict = json.load(json_file)

        '''balance = requests.get(url=firebase_url+ "/Amount/.json").text
        balance_json = json.loads(balance)'''
        balance_amount = json_dict['Amount']['amount']

        l = MDLabel(text = str(balance_amount),halign= "center",font_style="H3")
        amount_card.add_widget(l)

        bottom_navigation = MDBottomNavigation()
        bottom_navigation1 = MDBottomNavigationItem(
            name= 'screen 1',
            text= 'Transactions',
            icon= 'bank-transfer'
        )
        scroll_view = ScrollView()
        mdl = MDList()
        bottom_navigation1.add_widget(scroll_view)

        
        '''p = requests.get(url=firebase_url+ "count_transaction/.json").text
        o = json.loads(p)'''
        count = json_dict['count_transaction']['count']

        int_count = int(count)
        while int_count >= 0:
            '''get_data = requests.get(url=firebase_url+ f'Transactions/{int_count-1}/.json').text
            get_data_json = json.loads(get_data)'''
            name = json_dict['Transactions'][int_count-1]['name']
            mode = json_dict['Transactions'][int_count-1]['mode']
            amount = json_dict['Transactions'][int_count-1]['Amount']

            if mode == 'deposit':
                lst =  OneLineAvatarIconListItem(
                    size_hint_x= .9,
                    bg_color = "22DD22",  
                    text= f"{name} returned {amount}"
                )
                lst.add_widget(
                    IconLeftWidget(
                        icon= "arrow-down",
                )
                )
            elif mode == 'withdraw':
                lst =  OneLineAvatarIconListItem(
                    size_hint_x= .9,
                    bg_color = "B30000",  
                    text= f"{name} took {amount}"
                )
                lst.add_widget(
                    IconLeftWidget(
                        icon= "arrow-up",
                )
            
                )
            elif mode == 'add':
                lst =  OneLineAvatarIconListItem(
                    size_hint_x= .9,
                    bg_color = "FF4D6A",  
                    text= f"{name} Added {amount}"
                )
                lst.add_widget(
                    IconLeftWidget(
                        icon= "arrow-up",
                )
            
                )
            mdl.add_widget(lst)
            if int_count != 1:
                int_count = int_count - 1
            elif int_count == 1 :
                break
        
        scroll_view.add_widget(mdl)
        bottom_navigation.add_widget(bottom_navigation1)

        bottom_navigation2 = MDBottomNavigationItem(
            name= 'screen 2',
            text= 'Deposit',
            icon= 'cash-plus'
        )

        textfield1 = MDTextField(
            hint_text= "Deposit",
            size_hint_x= .9,
            mode = "rectangle",
            pos_hint= {"center_x": .5, "center_y": .55}
        )
        
        def call_back(amount,mode,name):
            if mode == "deposit":
                firebase_url = "https://home-network-52f96-default-rtdb.firebaseio.com/"
                

                p = requests.get(url=firebase_url+ "count_transaction/.json").text
                o = json.loads(p)
                count = o['count']

                try:
                    data = '{"' + str(count) +'":{"name" : "' + name + '", "Amount" : "' + str(amount) + '", "mode" : "' + mode + '"} }'
                    requests.patch(firebase_url + "Transactions/.json",json=json.loads(data))
                    incr_count = int(count)
                    count_data = '{"count" : "'+ str(incr_count+1) +'"}'
                    requests.put(firebase_url + "count_transaction/.json",json=json.loads(count_data))

                    balance = requests.get(url=firebase_url+ "/Amount/.json").text
                    balance_json = json.loads(balance)
                
                    balance_amount = int(balance_json['amount']) + int(amount)
                    upload_amount = '{"amount" : '+ str(balance_amount) +'}'
                    requests.patch(firebase_url + "/Amount/.json",json=json.loads(upload_amount))
                    l.text = str(balance_amount)
                except:
                    toast("Enter Number")
                
                
            elif mode == "withdraw":
                firebase_url = "https://home-network-52f96-default-rtdb.firebaseio.com/"
                

                p = requests.get(url=firebase_url+ "count_transaction/.json").text
                o = json.loads(p)
                count = o['count']

                try:
                    data = '{"' + str(count) +'":{"name" : "' + name + '", "Amount" : "' + str(amount) + '", "mode" : "' + mode + '"} }'
                    requests.patch(firebase_url + "Transactions/.json",json=json.loads(data))
                    incr_count = int(count)
                    count_data = '{"count" : "'+ str(incr_count+1) +'"}'
                    requests.put(firebase_url + "count_transaction/.json",json=json.loads(count_data))

                    balance = requests.get(url=firebase_url+ "/Amount/.json").text
                    balance_json = json.loads(balance)
                
                    balance_amount = int(balance_json['amount']) - int(amount)
                    upload_amount = '{"amount" : '+ str(balance_amount) +'}'
                    requests.patch(firebase_url + "/Amount/.json",json=json.loads(upload_amount))
                    l.text = str(balance_amount)
                except:
                    toast("Enter Number")


        btn1 = MDRaisedButton(
            text = "Put Money",
            pos_hint= {"center_x": .5, "center_y": .35},
            elevation= 10,
            on_release = lambda x: call_back(textfield1.text,"deposit",user_id)
        )
        
        bottom_navigation2.add_widget(textfield1)
        bottom_navigation2.add_widget(btn1)
        bottom_navigation.add_widget(bottom_navigation2)

        bottom_navigation3 = MDBottomNavigationItem(
            name= 'screen 3',
            text= 'Withdraw',
            icon= 'cash-minus'
        )
        textfield2 = MDTextField(
            hint_text= "Withdraw",
            mode = "rectangle",
            size_hint_x= .9,
            pos_hint= {"center_x": .5, "center_y": .55}
        )
        btn2 = MDRaisedButton(
            text = "Take Money",
            pos_hint= {"center_x": .5, "center_y": .35},
            elevation= 10,
            on_release = lambda x: call_back(textfield2.text,"withdraw",user_id)
        )

        bottom_navigation3.add_widget(textfield2)
        bottom_navigation3.add_widget(btn2)

        bottom_navigation.add_widget(bottom_navigation3)
        boxlayout.add_widget(bottom_navigation)
        screen.add_widget(boxlayout)
        self.sm.add_widget(screen)

def main_screen_amma(self,sm,user_id):
        screen2 = Screen(name = "main_screen_amma")
        boxlayout2 = MDBoxLayout(orientation = "vertical")
        toolbar2 = MDToolbar(title = 'Balance Amount')
        def toolbar_call():
            
            add_money_screen = Screen(name = "add_money_screen")
            lay = MDFloatLayout()
            
            enter_money = MDTextField(
                hint_text= "Enter Money to Add",
                size_hint_x= .9,
                mode = "rectangle",
                pos_hint= {"center_x": .5, "center_y": .65},
                helper_text_mode= "on_error",
                helper_text= "Enter text"
                )

            lay.add_widget(enter_money)
            def call_back(money,user_id,mode):
                s = str(money)
                if not money.isnumeric():
                    toast("Enter number")
                elif(money == ""):
                    toast("Enter Number")
                else:
                    firebase_url = "https://home-network-52f96-default-rtdb.firebaseio.com/"

                    amt_data = '{"amount" : "'+ money +'"}'
                    requests.put(url=firebase_url+ "/Amount/.json",json = json.loads(amt_data))
                    balance = requests.get(url=firebase_url+ "/Amount/.json").text
                    balance_json = json.loads(balance)
                    balance_amount = balance_json['amount']
                    l2.text = str(balance_amount)

                    p = requests.get(url=firebase_url+ "count_transaction/.json").text
                    o = json.loads(p)
                    count = o['count']


                    data = '{"' + str(count) +'":{"name" : "' + name + '", "Amount" : "' + str(money) + '", "mode" : "' + mode + '"} }'
                    requests.patch(firebase_url + "Transactions/.json",json=json.loads(data))
                    incr_count = int(count)
                    count_data = '{"count" : "'+ str(incr_count+1) +'"}'
                    requests.put(firebase_url + "count_transaction/.json",json=json.loads(count_data))

                    self.sm.current = "main_screen_amma"

            b = MDRaisedButton(
                text="ADD",
                pos_hint= {"center_x": .5, "center_y": .4},
                on_release = lambda x: call_back(enter_money.text,user_id,"add")
                )
        
            lay.add_widget(b)
            add_money_screen.add_widget(lay)
            self.sm.add_widget(add_money_screen)
            self.sm.current = "add_money_screen"
        
        def logout():
            login_screen.Login(self,sm)
            f = open('remember_login.txt',"w+")
            f.close()
            
                

        toolbar2.right_action_items = [["plus",lambda x: toolbar_call()],["logout", lambda x: logout()]]
        boxlayout2.add_widget(toolbar2)
        amount_card2 = MDCard(
            size_hint_y= .4,
            pos_hint= {"center_x": .5, "center_y": .7},
            elevation= 20,
            radius= 70,
            ripple_behavior= True
            
        )
        boxlayout2.add_widget(amount_card2)
        firebase_url = "https://home-network-52f96-default-rtdb.firebaseio.com/"

        balance = requests.get(url=firebase_url+ ".json").json()

        json_file = open('json_file.json', 'w')
        json.dump(balance, json_file)

        json_file = open('json_file.json', 'r')
        #json.dump(balance, json_file)
        json_dict = json.load(json_file)

        '''balance = requests.get(url=firebase_url+ "/Amount/.json").text
        balance_json = json.loads(balance)'''
        balance_amount = json_dict['Amount']['amount']

        l2 = MDLabel(text = str(balance_amount),halign= "center",font_style="H3")
        amount_card2.add_widget(l2)

        bottom_navigation2 = MDBottomNavigation()
        btn1 = MDBottomNavigationItem(
            name= 'screen 1',
            text= 'Transactions',
            icon= 'bank-transfer'
        )
        scroll_view2 = ScrollView()
        mdl2 = MDList()
        btn1.add_widget(scroll_view2)

        p = requests.get(url=firebase_url+ "count_transaction/.json").text
        o = json.loads(p)
        count = json_dict['count_transaction']['count']

        int_count = int(count)
        while int_count >= 0:
                
            '''get_data = requests.get(url=firebase_url+ f'Transactions/{int_count-1}/.json').text
            get_data_json = json.loads(get_data)'''
            name = json_dict['Transactions'][int_count-1]['name']
            mode = json_dict['Transactions'][int_count-1]['mode']
            amount = json_dict['Transactions'][int_count-1]['Amount']
            if mode == 'deposit':
                lst =  OneLineAvatarIconListItem(
                    size_hint_x= .9,
                    bg_color = "22DD22",  
                    text= f"{name} returned {amount}"
                )
                lst.add_widget(
                    IconLeftWidget(
                        icon= "arrow-down",
                )
                )
            elif mode == 'withdraw':
                lst =  OneLineAvatarIconListItem(
                    size_hint_x= .9,
                    bg_color = "B30000",  
                    text= f"{name} took {amount}"
                )
                lst.add_widget(
                    IconLeftWidget(
                        icon= "arrow-up",
                )
                )
            elif mode == "add":
                lst =  OneLineAvatarIconListItem(
                    size_hint_x= .9,
                    bg_color = "FF4D6A",  
                    text= f"{name} Added {amount}"
                )
                lst.add_widget(
                    IconLeftWidget(
                        icon= "arrow-up",
                )
                )
            
            mdl2.add_widget(lst)
            if int_count != 1:
                int_count = int_count - 1
            elif int_count == 1 :
                break
        
        scroll_view2.add_widget(mdl2)
        bottom_navigation2.add_widget(btn1)

        btn2 = MDBottomNavigationItem(
            name= 'screen 2',
            text= 'Deposit',
            icon= 'cash-plus'
        )

        tfield1 = MDTextField(
            hint_text= "Deposit",
            size_hint_x= .9,
            mode = "rectangle",
            pos_hint= {"center_x": .5, "center_y": .55}
        )

        def call_back(amount,mode,name):
            if mode == "deposit":
                firebase_url = "https://home-network-52f96-default-rtdb.firebaseio.com/"
                

                p = requests.get(url=firebase_url+ "count_transaction/.json").text
                o = json.loads(p)
                count = o['count']

                try:
                    data = '{"' + str(count) +'":{"name" : "' + name + '", "Amount" : "' + str(amount) + '", "mode" : "' + mode + '"} }'
                    requests.patch(firebase_url + "Transactions/.json",json=json.loads(data))
                    incr_count = int(count)
                    count_data = '{"count" : "'+ str(incr_count+1) +'"}'
                    requests.put(firebase_url + "count_transaction/.json",json=json.loads(count_data))

                    balance = requests.get(url=firebase_url+ "/Amount/.json").text
                    balance_json = json.loads(balance)
                
                    balance_amount = int(balance_json['amount']) + int(amount)
                    upload_amount = '{"amount" : '+ str(balance_amount) +'}'
                    requests.patch(firebase_url + "/Amount/.json",json=json.loads(upload_amount))
                    l2.text = str(balance_amount)
                except:
                    toast("Enter Number")
            elif mode == "withdraw":
                firebase_url = "https://home-network-52f96-default-rtdb.firebaseio.com/"
                

                p = requests.get(url=firebase_url+ "count_transaction/.json").text
                o = json.loads(p)
                count = o['count']

                try:
                    data = '{"' + str(count) +'":{"name" : "' + name + '", "Amount" : "' + str(amount) + '", "mode" : "' + mode + '"} }'
                    requests.patch(firebase_url + "Transactions/.json",json=json.loads(data))
                    incr_count = int(count)
                    count_data = '{"count" : "'+ str(incr_count+1) +'"}'
                    requests.put(firebase_url + "count_transaction/.json",json=json.loads(count_data))

                    balance = requests.get(url=firebase_url+ "/Amount/.json").text
                    balance_json = json.loads(balance)
                
                    balance_amount = int(balance_json['amount']) - int(amount)
                    upload_amount = '{"amount" : '+ str(balance_amount) +'}'
                    requests.patch(firebase_url + "/Amount/.json",json=json.loads(upload_amount))
                    l2.text = str(balance_amount)
                except:
                    toast("Enter Number")


        butn1 = MDRaisedButton(
            text = "Put Money",
            pos_hint= {"center_x": .5, "center_y": .35},
            elevation= 10,
            on_release = lambda x: call_back(tfield1.text,"deposit",user_id)
        )
        
        btn2.add_widget(tfield1)
        btn2.add_widget(butn1)
        bottom_navigation2.add_widget(btn2)

        btn3 = MDBottomNavigationItem(
            name= 'screen 3',
            text= 'Withdraw',
            icon= 'cash-minus'
        )
        tfield2 = MDTextField(
            hint_text= "Withdraw",
            size_hint_x= .9,
            mode = "rectangle",
            pos_hint= {"center_x": .5, "center_y": .55}
        )
        butn2 = MDRaisedButton(
            text = "Take Money",
            pos_hint= {"center_x": .5, "center_y": .35},
            elevation= 10,
            on_release = lambda x: call_back(tfield2.text,"withdraw",user_id)
        )

        btn3.add_widget(tfield2)
        btn3.add_widget(butn2)

        bottom_navigation2.add_widget(btn3)
        boxlayout2.add_widget(bottom_navigation2)
        screen2.add_widget(boxlayout2)
        self.sm.add_widget(screen2)

