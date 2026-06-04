from helper import slice_words, create_id
import re 
from styles import print_styles

email_pattern = re.compile(r'[\w\-=+\[{;:\'\"}\],\./?`~\$]+@[a-z0-9]+\.[a-z]{2,}')
password_pattern = re.compile(r"^[\w=+-]{8,20}$")
    
FILE_USERS = 'txt/users.txt'
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
def show_users():
    """
    Imprime todos los usuarios
    """    
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    print(f'{"Usuarios":^50}')
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    
    try:
        with open('txt/users.txt', mode='r', encoding='UTF-8') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            
            count_matrix = len(lines)
            
            print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
            print("="*print_styles.MAX_SPACES_CATEGORIES)
            print(f"{print_styles.BOLD}{'Número':<15}{'Nombre':<15}{print_styles.RESET}")
            
            for line in lines:
                id, permission, username, password, email = line.split(';')
                
                username_sliced = slice_words(14, username)
                print(f"{id:<15}{username_sliced:<15}")
                
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
    """
    Busca y autentica a un usuario en el archivo de registros del sistema.

    email: dirección de correo electrónico del usuario a buscar
    password: contraseña de la cuenta del usuario
    Retorna: Un diccionario con los datos del usuario si coincide, None en caso contrario o si ocurre un error
    """
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

def read_users(file=FILE_USERS):
    """
    Devuelve una lista de usuarios
    file: ruta del archivo donde se almacenan los usuarios 
    """
    users = []
    try:
        with open(file, mode='r', encoding='UTF-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                id_str, permission, username, password, email = line.split(';')
                users.append({
                    "id": int(id_str),
                    "permission": permission,
                    "username": username,
                    "password": password,
                    "email": email
                })
        return users
    except FileNotFoundError:
        print(f"{print_styles.RED}No se encontró el archivo de usuarios.{print_styles.RESET}")
        return []
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error al leer los usuarios.{print_styles.RESET}")
        return []

def write_users(users, file=FILE_USERS):
    """
    users: lista de todos los usuarios
    file: ruta del archivo donde se almacenan los usuarios 
    Escribe en el txt toda la informacion
    """
    try:
        with open(file, mode='w', encoding='UTF-8') as f:
            for user in users:
                f.write(f"{user['id']};{user['permission']};{user['username']};{user['password']};{user['email']}\n")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error al guardar los usuarios.{print_styles.RESET}")

def add_user(username, email, password, file=FILE_USERS):
    """
    Registra un nuevo usuario en el sistema y guarda los cambios en el archivo.

    username: nombre de usuario de la nueva cuenta
    email: dirección de correo electrónico del usuario
    password: contraseña para la cuenta del usuario
    file: ruta del archivo donde se almacenan los usuarios 
    Retorna None
    """
    try:
        users = read_users(file)
        next_id = create_id(users) if users else 1
        users.append({
            "id": next_id,
            "permission": "user",
            "username": username,
            "password": password,
            "email": email
        })
        write_users(users, file)
        print(f"{print_styles.GREEN}Usuario agregado correctamente.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error al agregar el usuario.{print_styles.RESET}")

def delete_user(user_id, file=FILE_USERS):
    """
    Elimina un usuario del sistema buscando por su identificador único.

    user_id: identificador único del usuario que se desea eliminar
    file: ruta del archivo donde se almacenan los usuarios 
    Retorna None
    """
    try:
        users = read_users(file)      
        updated_users = [user for user in users if user["id"] != user_id]
        if len(updated_users) == len(users):
            print(f"{print_styles.YELLOW}No se encontró el usuario con id {user_id}.{print_styles.RESET}")
            return
        write_users(updated_users, file)
        print(f"{print_styles.GREEN}Usuario eliminado correctamente.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error al eliminar el usuario.{print_styles.RESET}")

def update_user_password(user_id, new_password, file=FILE_USERS):
    """
    Modifica la contraseña de un usuario específico en el sistema.

    user_id: identificador único del usuario al que se le cambiará la contraseña
    new_password: nueva contraseña que se asignará a la cuenta
    file: ruta del archivo donde se almacenan los usuarios
    Retorna None
    """
    try:
        users = read_users(file)
        found = False
        for user in users:
            if user["id"] == user_id:
                user["password"] = new_password
                found = True
                break
        if not found:
            print(f"{print_styles.YELLOW}No se encontró el usuario con id {user_id}.{print_styles.RESET}")
            return
        write_users(users, file)
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error al actualizar la contraseña.{print_styles.RESET}")

def update_user_username(user_id, new_username, file=FILE_USERS):
    """
    Modifica el nombre de usuario de un usuario específico en el sistema.

    user_id: identificador único del usuario al que se le cambiará el nombre de usuario
    new_username: nuevo nombre de usuario que se asignará a la cuenta
    file: ruta del archivo donde se almacenan los usuarios
    Retorna None
    """
    try:
        users = read_users(file)
        found = False
        for user in users:
            if user["id"] == user_id:
                user["username"] = new_username
                found = True
                break
        if not found:
            print(f"{print_styles.YELLOW}No se encontró el usuario con id {user_id}.{print_styles.RESET}")
            return
        write_users(users, file)
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error al actualizar el username.{print_styles.RESET}")