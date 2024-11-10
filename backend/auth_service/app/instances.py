from auth_service.app.auth import Register, Login
from auth_service.app.email_logic import Email

register_instance = Register()
login_instance = Login()
email_instance = Email()