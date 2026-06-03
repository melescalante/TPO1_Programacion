from styles import print_styles 

ROLE_LEVELS = {
    "user": 1,
    "admin": 2
}

def has_permission(user, required_level, file='txt/users.txt'):
    """
    user: diccionario con información del usuario logueado o None
    required_level: nivel de permiso requerido (1=user, 2=admin)
    Retorna: True si el usuario tiene el nivel de permiso requerido, False en caso contrario
    """
    if not user:
        print('Debes loguearte para usar el sistema')
        return
    
    try:
        with open(file, mode='r', encoding='UTF-8') as f:
            line = f.readline()
            while line:
                id, permission, username, password, email = line.strip().split(';')
                if user['id'] == id:
                    line = f.readline()
                    continue

                actual_level = ROLE_LEVELS.get(permission, 1)
                if actual_level >= required_level:
                    return True
                        
                # print('No tienes permiso')
            return False
    except FileNotFoundError:
        print(f"{print_styles.BOLD}Ocurrió un error al intentar abrir el archivo.{print_styles.RESET}")
        return False
    except:
        print("pepe")
        print(f"{print_styles.BOLD}Ocurrió un error inesperado.{print_styles.RESET}")
        return False