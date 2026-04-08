from data import users
import re 
from Styles import print_styles
def login():
    print("Bienvenido/a al sistema de Gestor de Gastos.")
    email= input("Ingrese su email: ")
    email_lower=email.lower()
    password= input("Ingrese su contraseña: ")
    password_lower= password.lower()
    result=validate_email(email)
    if not result:
        print(f"{print_styles.RED}Debe ingresar un email valido.{print_styles.RESET}")
        return
    user_found=list(filter(lambda x:x["email"].lower()==email_lower and x["password"].lower()==password_lower, users))
    if user_found:
        print(f"Bienvenido {print_styles.BOLD}{user_found[0]["username"].title()}!{print_styles.RESET}")
        return user_found[0]
    if not user_found:
        print(f"{print_styles.RED}No existe el usuario ingresado.{print_styles.RESET}")
    return

def validate_email(email):
    patter=re.compile(r'[\w\-=+\[{;:\'\"}\],\./?`~\$]+@[a-z0-9]+\.[a-z]{2,}')
    result= re.findall(patter, email)
    if result: return True

def is_logged(loggedUser):
    if (loggedUser): return True