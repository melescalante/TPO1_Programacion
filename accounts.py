from styles import print_styles
from helper import json_loader,create_id, get_raw_by_id

def add_account(matrix_accounts, account_name, total_money):
    """
    matrix_accounts: lista de cuentas existentes
    account_name: nombre de la cuenta a agregar
    total_money: saldo inicial de la cuenta
    Retorna: None. Agrega una nueva cuenta si no existe con ese nombre
    """
    try:
        id=create_id(matrix_accounts)
        for account in matrix_accounts:
            if account["account"] == account_name:
                print(f"{print_styles.RED}La cuenta ya existe. Ingrese otro nombre por favor.{print_styles.RESET}")
                return
        dicc_account={
            "id":id,
            "account":account_name,
            "amount":total_money
        }
        matrix_accounts.append(dicc_account)
        json_loader('json/accounts.json',matrix_accounts)
        print(f"{print_styles.GREEN}Se ha creado la cuenta correctamente{print_styles.RESET}")
    except TypeError:
        print(f"{print_styles.RED}Error: Se recibió otro tipo de dato.{print_styles.RESET}")
    except ValueError:
        print(f"{print_styles.RED}Error: Debes ingresar un numero.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error inesperado{print_styles.RESET}")

 
def get_accounts(matrix_account):
    """
    matrix_account: lista de cuentas a mostrar
    Retorna: None. Imprime una tabla con todas las cuentas y sus saldos
    """
    count_matrix= len(matrix_account)
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f'{"Cuentas":^60}')
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD}{'Numero':<10}{'Nombre Cuenta':<25}{'Dinero':<25}{print_styles.RESET}")
    for i in range(len(matrix_account)):
        id=matrix_account[i]["id"]
        name = matrix_account[i]["account"]
        amount=matrix_account[i]["amount"]
        amount_str = "$"+str(matrix_account[i]["amount"])
        underline = print_styles.UNDERLINE_INCOME
        if int(amount)<0:
            underline= print_styles.UNDERLINE_EXPENSE
        print(f"{underline}{id:<10}{name:<25}{amount_str:<25}{print_styles.RESET}")
    return

def get_account_by_user_input(matrix_accounts):
    """
    matrix_accounts: lista de cuentas disponibles
    Retorna: cuenta seleccionada por el usuario o None si cancela
    """
    while True:
        try:
            id_account = int(input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: "))
            
            if id_account < 0 or id_account > len(matrix_accounts):
                print(f"{print_styles.RED}Entrada inválida. Debe ingresar una cuenta existente.{print_styles.RESET}")
                continue

            if id_account == 0:
                print(f"{print_styles.GREEN}No se actualizó ninguna cuenta.{print_styles.RESET}")
                return None

            account = get_raw_by_id(matrix_accounts, id_account)
            if account is None:
                print(f"{print_styles.RED}La cuenta no existe.{print_styles.RESET}")
                continue

            return account
        except Exception:
            print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")

def update_name_account(account):
    """
    account: registro de cuenta a modificar
    Retorna: None. Solicita y actualiza el nombre de la cuenta
    """
    try:
        name_account = input("Ingrese un nuevo nombre de cuenta: ")
        while len(name_account) == 0 or not name_account.isalpha(): # bug, no admite espacios
            print(f"{print_styles.YELLOW}El nombre que ingreso tiene espacios o no ingreso un valor. Por favor ingrese un nombre sin espacios.{print_styles.RESET}")
            name_account = input("Ingrese un nuevo nombre de cuenta: ")
        account[1] = name_account
        print(f"{print_styles.GREEN}Se ha actualizado el nombre correctamente.{print_styles.RESET}")
    except ValueError:
        print(f"{print_styles.YELLOW}Opción no válida. Intente nuevamente.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error inesperado{print_styles.RESET}")


def update_money_account(account):            
    """
    account: registro de cuenta a modificar
    Retorna: None. Solicita y actualiza el saldo de la cuenta
    """
    try:
        total_money = input("Ingrese un nuevo monto de dinero: ")
        while not total_money.isnumeric():
            print(f"{print_styles.YELLOW}El valor que ingreso no es número o es menor a 0.{print_styles.RESET}")
            total_money = input("Ingrese un nuevo monto de dinero: ")
        account[2] = int(total_money)
        print(f"{print_styles.GREEN}Se ha actualizado el monto correctamente.{print_styles.RESET}")
    except Exception:
       print(f"{print_styles.RED}Ocurrió un error inesperado{print_styles.RESET}")

def delete_account(matrix_accounts, id):
    """
    matrix_accounts: lista de cuentas disponibles
    id: identificador de la cuenta a eliminar
    Retorna: None. Elimina la cuenta con el id indicado
    """
    delete=[]
    index=0
    try:
        for acc in matrix_accounts:
            if acc[0]==id:
                index=matrix_accounts.index(acc)
                delete=matrix_accounts.pop(index)
                print(f"{print_styles.GREEN}Operación realizada con éxito. Cuenta eliminada correctamente.{print_styles.RESET}")
                return
    except IndexError:
        print(f"{print_styles.YELLOW}La cuenta no existe. Ingrese una cuenta valida{print_styles.RESET}")
    except Exception:
       print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
    print()
    
def update_account_balance(matrix_accounts, id_account, amount):
    """
    matrix_accounts: lista de cuentas a actualizar
    id_account: identificador de la cuenta a modificar
    amount: monto a sumar o restar del saldo
    Retorna: None. Ajusta el saldo de la cuenta indicada
    """
    for account in matrix_accounts:
        if account[0] == id_account:
            account[2] += amount
            return
        

