import firebase_admin
from firebase_admin import credentials,auth
import login_screen
import main_screen
from kivymd.toast import toast


cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

def switch_screen(self,verify_id,sm):
            
            try:
                emailid = auth.get_user_by_email(verify_id)

                user_id = emailid.uid
                screen_change = True
            except:
                toast("Invalid E-Mail id")
                screen_change = False
                
            if screen_change == True:
                if (emailid.email == "ajkirubajasmine@gmail.com"):
                    file = open("remember_login.txt","w+")
                    file.write(emailid.email)
                    file.close()
                    main_screen.main_screen_amma(self,sm,user_id)
                    self.sm.current = "main_screen_amma"
                else:
                    file = open("remember_login.txt","w+")
                    file.write(emailid.email)
                    file.close()
                    main_screen.main_screen(self,sm,user_id)
                    self.sm.current = "main_screen"
            else:
                login_screen.Login(self,sm)