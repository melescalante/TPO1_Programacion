from data import users
from Styles import print_styles
def login():
    print("Bienvenido/a al sistema de Gestor de Gastos.")
    username= input("Ingrese su nombre: ")
    username_lower=username.lower()
    password= input("Ingrese su contrase├▒a: ")
    password_lower= password.lower()
    user_found=list(filter(lambda x:x["username"].lower()==username_lower and x["password"].lower()==password_lower, users))
    if user_found:
        print(f"Bienvenido {print_styles.BOLD}{username.title()}!{print_styles.RESET}")
        return user_found[0]
    if not user_found:
        print(f"{print_styles.RED}No existe el usuario ingresado.{print_styles.RESET}")
    return

def is_logged(loggedUser):
    if (loggedUser): return True