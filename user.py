from data import users
import re 
from Styles import print_styles

email_pattern = re.compile(r'[\w\-=+\[{;:\'\"}\],\./?`~\$]+@[a-z0-9]+\.[a-z]{2,}')
password_pattern = re.compile(r"^[\w=+-]{8,20}$")

def login():
    """
    Retorna: diccionario con datos del usuario autenticado o None si la autenticación falla
    """
    email= input("Ingrese su email: ")
    email_lower=email.lower()
    password= input("Ingrese su contraseña: ")
    password_lower= password.lower()
    result=validate_email(email)
    valid_password = validate_password(password_lower)
    if not result:
        print(f"{print_styles.RED}Debe ingresar un email valido.{print_styles.RESET}")
        return
    
    if not valid_password:
        print(f"{print_styles.RED}Debe ingresar una contraseña valida.{print_styles.RESET}")
        return
    
    user_found=list(filter(lambda x:x["email"].lower()==email_lower and x["password"].lower()==password_lower, users))
    if user_found:
        print(f"\nBienvenido {print_styles.BOLD}{user_found[0]["username"].title()}!{print_styles.RESET}")
        return user_found[0]
    if not user_found:
        print(f"{print_styles.RED}No existe el usuario ingresado.{print_styles.RESET}")
    return

def validate_email(email):
    """
    email: dirección de correo electrónico a validar
    Retorna: True si el email es válido según el patrón, False en caso contrario
    """
    result = email_pattern.findall(email)
    return True if result else False

def validate_password(password):
    """
    password: contraseña a validar
    Retorna: True si la contraseña es válida según el patrón, False en caso contrario
    """
    result = password_pattern.search(password)
    return result is not None

def is_logged(loggedUser):
    """
    loggedUser: información del usuario logueado
    Retorna: True si el usuario está logueado, False en caso contrario
    """
    if (loggedUser): return True