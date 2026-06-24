from styles import print_styles
from helper import json_loader, create_id, get_raw_by_id

def add_account(data_accounts, account_name, total_money):
    """
    data_accounts: lista de cuentas existentes
    account_name: nombre de la cuenta a agregar
    total_money: saldo inicial de la cuenta
    Retorna: None. Agrega una nueva cuenta si no existe con ese nombre
    """
    try:
        id=create_id(data_accounts)
        if account_exists(data_accounts, account_name):
            print(f"{print_styles.RED}La cuenta ya existe. Ingrese otro nombre por favor.{print_styles.RESET}")
            return
        dicc_account={
            "id":id,
            "account":account_name,
            "amount":total_money
        }
        data_accounts.append(dicc_account)
        json_loader('json/accounts.json',data_accounts)
        print(f"{print_styles.GREEN}Se ha creado la cuenta correctamente{print_styles.RESET}")
    except TypeError:
        print(f"{print_styles.RED}Error: Se recibió otro tipo de dato.{print_styles.RESET}")
    except ValueError:
        print(f"{print_styles.RED}Error: Debes ingresar un numero.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error inesperado{print_styles.RESET}")

 
def get_accounts(data_accounts):
    """
    data_accounts: lista de cuentas a mostrar
    Retorna: None. Imprime una tabla con todas las cuentas y sus saldos
    """
    count_matrix= len(data_accounts)
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f'{"Cuentas":^60}')
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD_BLUE}Registros Totales: {count_matrix:<40}{print_styles.RESET}")
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD}{'Numero':<10}{'Nombre Cuenta':<25}{'Dinero':<25}{print_styles.RESET}")
    for i in range(len(data_accounts)):
        id=data_accounts[i]["id"]
        name = data_accounts[i]["account"]
        amount=data_accounts[i]["amount"]
        amount_str = "$"+str(data_accounts[i]["amount"])
        underline = print_styles.UNDERLINE_INCOME
        if int(amount)<0:
            underline= print_styles.UNDERLINE_EXPENSE
        print(f"{underline}{id:<10}{name:<25}{amount_str:<25}{print_styles.RESET}")
    return

def get_account_by_user_input(data_accounts):
    """
    data_accounts: lista de cuentas disponibles
    Retorna: cuenta seleccionada por el usuario o None si cancela
    """
    while True:
        try:
            id_account = int(input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: "))
            
            if id_account < 0 or id_account > len(data_accounts):
                print(f"{print_styles.RED}Entrada inválida. Debe ingresar una cuenta existente.{print_styles.RESET}")
                continue

            if id_account == 0:
                print(f"{print_styles.GREEN}No se actualizó ninguna cuenta.{print_styles.RESET}")
                return None

            account = get_raw_by_id(data_accounts, id_account)
            if account is None:
                print(f"{print_styles.RED}La cuenta no existe.{print_styles.RESET}")
                continue

            return account
        except Exception:
            print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")

def update_name_account(account,data_accounts):
    """
    account: registro de cuenta a modificar
    data_accounts: registro de cuenta totales
    Retorna: None. Solicita y actualiza el nombre de la cuenta
    """
    try:
        name_account = input("Ingrese un nuevo nombre de cuenta: ")

        while account_exists(data_accounts, name_account):
            if len(name_account) == 0:
                print(f"{print_styles.YELLOW}El nombre que ingreso tiene espacios o no ingreso un valor. Por favor ingrese un nombre sin espacios.{print_styles.RESET}")
                name_account = input("Ingrese un nuevo nombre de cuenta: ")
                continue
            print(f"{print_styles.RED}El nombre que ingreso ya existe en una cuenta. Por favor ingrese otra.{print_styles.RESET}")
            name_account = input("Ingrese un nuevo nombre de cuenta: ")
        account["account"] = name_account
        json_loader('json/accounts.json',data_accounts)
        print(f"{print_styles.GREEN}Se ha actualizado el nombre correctamente.{print_styles.RESET}")
    except ValueError:
        print(f"{print_styles.YELLOW}Opción no válida. Intente nuevamente.{print_styles.RESET}")
    except Exception:
        print(f"{print_styles.RED}Ocurrió un error inesperado{print_styles.RESET}")

def update_money_account(account,data_accounts):            
    """
    account: registro de cuenta a modificar
    data_accounts: registro de cuenta totales
    Retorna: None. Solicita y actualiza el saldo de la cuenta
    """
    try:
        total_money = input("Ingrese un nuevo monto de dinero: ")
        while not total_money.isnumeric():
            print(f"{print_styles.YELLOW}El valor que ingreso no es número o es menor a 0.{print_styles.RESET}")
            total_money = input("Ingrese un nuevo monto de dinero: ")
        account["amount"] = int(total_money)
        json_loader('json/accounts.json',data_accounts)
        print(f"{print_styles.GREEN}Se ha actualizado el monto correctamente.{print_styles.RESET}")
    except Exception:
       print(f"{print_styles.RED}Ocurrió un error inesperado{print_styles.RESET}")

def delete_account(data_accounts, id):
    """
    data_accounts: lista de cuentas disponibles
    id: identificador de la cuenta a eliminar
    Retorna: None. Elimina la cuenta con el id indicado
    """
    delete=[]
    index=0
    try:
        for acc in data_accounts:
            if acc["id"]==id:
                index=data_accounts.index(acc)
                delete=data_accounts.pop(index)
                json_loader('json/accounts.json',data_accounts)
                print(f"{print_styles.GREEN}Operación realizada con éxito. Cuenta eliminada correctamente.{print_styles.RESET}")
                return
    except IndexError:
        print(f"{print_styles.YELLOW}La cuenta no existe. Ingrese una cuenta valida{print_styles.RESET}")
    except Exception:
       print(f"{print_styles.RED}Ocurrió un error inesperado.{print_styles.RESET}")
    print()

def update_account_balance(data_accounts, id_account, amount):
    """
    data_accounts: lista de cuentas a actualizar
    data_accounts: lista de cuentas a actualizar
    id_account: identificador de la cuenta a modificar
    amount: monto a sumar o restar del saldo
    Retorna: None. Ajusta el saldo de la cuenta indicada
    """
    for account in data_accounts:
        if account['id'] == id_account:
            account['amount'] += amount
            json_loader('json/accounts.json', data_accounts)
            return
        
def account_exists(data_accounts, account_name, index=0):
    """
    Comprueba recursivamente si ya existe una cuenta con ese nombre.
    data_accounts: lista de cuentas (cada elemento es un dict con clave "account").
    account_name: nombre de cuenta a buscar.
    index: índice actual para la búsqueda recursiva (uso interno).
    Retorna: True si encuentra una cuenta con el mismo nombre, False si no.
    """
    if index >= len(data_accounts):
        return False

    if data_accounts[index]["account"].lower() == account_name.lower():
        return True

    return account_exists(data_accounts, account_name, index + 1)

# def update_account_balance(matrix_accounts, id_account, amount):
#     """
#     matrix_accounts: lista de cuentas a actualizar
#     id_account: identificador de la cuenta a modificar
#     amount: monto a sumar o restar del saldo
#     Retorna: None. Ajusta el saldo de la cuenta indicada
#     """
#     for account in matrix_accounts:
#         if account[0] == id_account:
#             account[2] += amount
#             return