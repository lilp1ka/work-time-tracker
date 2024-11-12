from auth_service.app.auth import Register, Login
from auth_service.app.email_logic import Email
from auth_service.app.user_data import UserData, ChangeUserData
register_instance = Register()
login_instance = Login()
email_instance = Email()
user_instance = UserData()
change_user_instance = ChangeUserData()
