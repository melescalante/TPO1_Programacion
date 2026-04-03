from Styles import print_styles
from matrix import accounts
from helper import create_id, get_by_id

def add_account(account_name, total_money):
    id=create_id(accounts)
    for account in accounts:
        if account[1] == account_name:
            return
    accounts.append([id, account_name, total_money])
 
def get_accounts(matrix_account):
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f'{"Cuentas":^60}')
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD}{'Numero':<20}{'Nombre Cuenta':<30}{'Dinero':<30}{print_styles.RESET}")
    for i in range(len(matrix_account)):
        id=matrix_account[i][0]
        name = matrix_account[i][1]
        amount = "$"+str(matrix_account[i][2])
        print(f"{print_styles.BOLD}{id:<20}{print_styles.RESET}{name:<30}{amount:<30}")
    return

def update_account(matrix_accounts):
    get_accounts(matrix_accounts)
    id_account = int(input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: "))
    if id_account == 0:
        print("\033[32mNo se actualizo ninguna cuenta.\033[0m")
        return

    account = get_by_id(matrix_accounts, id_account)
    while account is None:
        print("\033[31mLa cuenta no existe.\033[0m")

        id_account = int(input("¿Que cuenta desea actualizar? Indique el numero o escriba 0 para salir: "))            
        if id_account == 0:
            print("\033[32mNo se actualizo ninguna cuenta.\033[0m")
            return
                
        account = get_by_id(matrix_accounts, id_account)

    while True:
        print("\033[1;34m¿Qué campo de la cuenta deseas actualizar?\033[0m")
        print("1. Nombre")
        print("2. Monto")
        print("0. Guardar y salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            change_name_account(account)
        elif opcion == "2":
            change_money_account(account)
        elif opcion == "0":
            print("\033[32mLa cuenta se actualizó con éxito.\033[0m")
            return
        else:
            print("\033[31mOpción no válida. Intente nuevamente.\033[0m")

def change_name_account(account):
    name_account = input("Ingrese un nuevo nombre de cuenta: ")
    while len(name_account) == 0 or not name_account.isalpha():
        print("\033[33mEl nombre que ingreso no tiene valor o no es una palabra.\033[0m")
        name_account = input("Ingrese un nuevo nombre de cuenta: ")
    account[1] = name_account

def change_money_account(account):            
    total_money = input("Ingrese un nuevo monto de dinero: ")
    while not total_money.isnumeric():
        print("\033[33mEl valor que ingreso no es número o es menor a 0.\033[0m")
        total_money = input("Ingrese un nuevo monto de dinero: ")
    account[2] = int(total_money)

def delete_account():
    get_accounts(accounts)
    id = int(input("Que cuenta deseas eliminar? Indique el numero o escriba 0 para salir: "))
    delete=[]
    index=0
    if id == 0:
        print("\033[32mNo se elimino ninguna cuenta.\033[0m")
        return
    for acc in accounts:
        if acc[0]==id:
            index=accounts.index(acc)
            delete=accounts.pop(index)
            print("\033[32mOperación realizada con éxito. Cuenta eliminada correctamente.\033[0m")
            return
    print()
    
def revert_money_account(matrix_accounts, id_account, amount):
    for account in matrix_accounts:
        if account[0] == id_account:
            amount *= -1 # Invierte el monto para devolver al resultado anterior a la cuenta.
            account[2] += amount
            print(amount)
            return
        

