import firebase_admin
from firebase_admin import credentials,auth

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

id = "Sherlin"
emailid = "sherlinarulkumar@gmail.com"
password = "12345678910"

user = auth.create_user(uid = id, email = emailid, password = password)

print(user)