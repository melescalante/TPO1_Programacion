from data import users
from helper import slice_words
import re 
from styles import print_styles

email_pattern = re.compile(r'[\w\-=+\[{;:\'\"}\],\./?`~\$]+@[a-z0-9]+\.[a-z]{2,}')
password_pattern = re.compile(r"^[\w=+-]{8,20}$")

def login():
    """
    Retorna: diccionario con datos del usuario autenticado o None si la autenticación falla
    """
    email = input("Ingrese su email: ")
    email_lower =email.lower()
    password = input("Ingrese su contraseña: ")
    valid_email = validate_email(email)
    valid_password = validate_password(password)
    if not valid_email:
        print(f"{print_styles.RED}Debe ingresar un email valido.{print_styles.RESET}")
        return
    
    if not valid_password:
        print(f"{print_styles.RED}Debe ingresar una contraseña valida.{print_styles.RESET}")
        return

    user_found = get_user(email, password)
    
    # user_found = list(filter(lambda x:x["email"].lower()==email_lower and x["password"] == password, users))
    if user_found:
        print(f"\nBienvenido {print_styles.BOLD}{user_found["username"].title()}!{print_styles.RESET}")
        # return user_found[0]
        return user_found
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
    
    return False

def get_users():
    """
    Imprime todos los usuarios
    """    
    print("="*30)
    print(f"{print_styles.BOLD}{"Número":<15}{"Nombre":<15}{print_styles.RESET}")

    try:
        with open('txt/users.txt', mode='r', encoding='UTF-8') as file:
            line = file.readline()
            while line:
                id, _, username, _, _ = line.strip().split(';')
                if id == str(id_user):
                    username_sliced = slice_words(14, username)
                    print(f"{id:<15}{username_sliced:<15}")
                line = file.readline()
    except FileNotFoundError:
        print(f"{print_styles.RED}No se encontró la ruta del archivo.{print_styles.RESET}")
    except:
        print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
    
def get_user_by_id(id_user):
    """
    id_user: id del usuario que se busca
    Retorna: devuelva una lista del usuario que se busca
    """   
    try:
        with open('txt/users.txt', mode='r', encoding='UTF-8') as file:
            line = file.readline()
            user_found = None
            while line:
                id, permission, username, password, email = line.strip().split(';')
                if id == str(id_user):
                    user_found = { 'id': id, 'permission': permission, 'username': username, 'password': password, 'email': email }
                    break
                line = file.readline()
            return user_found
    except FileNotFoundError:
        print(f"{print_styles.RED}No se encontró la ruta del archivo.{print_styles.RESET}")
        return None
    except:
        print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
        return None

def get_user(email, password):
    try:
        with open('txt/users.txt', mode='r', encoding='UTF-8') as file:
            line = file.readline()
            user_found = None
            while line:
                id, permission, username, password, email = line.strip().split(';')
                if email.lower() == email and password == password:
                    user_found = { 'id': id, 'permission': permission, 'username': username, 'password': password, 'email': email }
                    break
                line = file.readline()
            return user_found
    except FileNotFoundError:
        print(f"{print_styles.RED}No se encontró la ruta del archivo.{print_styles.RESET}")
        return None
    except:
        print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
        return None