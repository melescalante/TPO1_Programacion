from datetime import datetime, time

from data import accounts, transactions, categories, budgets
from transactions import *
from budgets import *
from categories import *
from accounts import *
from user import *
from analytics import *
from helper import *
from permissions import has_permission

# Permissions
READ=1
READ_WRITE=2


print("¡Bienvenido/a al sistema de Gestor de Gastos!\n")
user = users[0]
while user==None:
    user=login()

is_logged(user)

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():

    #-------------------------------------------------
    # Bloque de menú
    #----------------------------------------------------------------------------------------------
    while True:
        can_read = has_permission(user, READ)
        can_write = has_permission(user, READ_WRITE)
        valid_options = ["0"]
        if can_read: valid_options.extend(["1"])
        if can_write: valid_options.extend(["2", "3", "4"])
        while True:
            options = 5
            print()
            print("---------------------------")
            print("MENÚ PRINCIPAL")
            print("---------------------------")
            print(f"{print_styles.BOLD}[1]{print_styles.RESET} Gestión de Transacciones")
            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Gestión de Categorías")
            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Gestión de Presupuestos")
            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Gestión de Cuentas")
            print(f"{print_styles.BOLD}[5]{print_styles.RESET} Resumen")

            print("---------------------------")
            print(f"{print_styles.BOLD}[0]{print_styles.RESET} Salir del programa")
            print("---------------------------")
            print()
            
            option = input("Seleccione una opción: ")
            if option in [str(i) for i in range(0, options + 1)]: # Sólo continua si se elije una opcion de menú válida
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if option == "0": # Opción salir del programa
            exit() # También puede ser sys.exit() para lo cual hay que importar el módulo sys

        elif option == "1":   # Opción 1 --> Gestión de transacciones
            while True:
                while True:
                    options = 5
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Transacciones")
                    print("---------------------------")
                    if can_read:
                        print(f"{print_styles.BOLD}[1]{print_styles.RESET} Mostrar Transacciones")
            
                        if can_write:
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Añadir Transacciones")
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Actualizar Transacciones")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Eliminar Transacciones")
                        print(f"{print_styles.BOLD}[5]{print_styles.RESET} Ver Transacciones por Categoria")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    
                    if can_read: valid_options.extend(["5"])
                    if option in valid_options: 
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":   # Opción 1
                    permission= has_permission(user,READ)
                    if permission:
                        get_transactions(transactions, accounts, categories)
                        # get_transactions(transactions, accounts, categories, lambda x: x[5] >= 10000)
                elif option == "2":   # Opción 2
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        while True:
                            while True:
                                sub_options = 2
                                print()
                                print("---------------------------")
                                print("MENÚ PRINCIPAL > Gestión de Transacciones > Añadir")
                                print("---------------------------")
                                print(f"{print_styles.BOLD}[1]{print_styles.RESET} Opción 1 (Ingreso)")
                                print(f"{print_styles.BOLD}[2]{print_styles.RESET} Opción 2 (Egreso)")
                                print("---------------------------")
                                print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                                print("---------------------------")
                                print()
                                
                                sub_option = input("Seleccione una opción: ")
                                if sub_option in [str(i) for i in range(0, sub_options + 1)]: 
                                    break
                                else:
                                    input("Opción inválida. Presione ENTER para volver a seleccionar.")
                            print()

                            if sub_option == "0":
                                break # Vuelve al menú de Gestión de Transacciones
                            
                            actual_date = datetime.now().date()
                            print(f"Su fecha actual es: {print_styles.YELLOW}{actual_date}{print_styles.RESET}, presione Enter si desea dejar la fecha actual")
                            date = input("Ingrese la fecha (formato: YYYY-MM-DD): ")
                            if len(date) == 0:
                                date = str(actual_date)
                            else:
                                message, is_valid = validate_date(date)
                                if not is_valid:
                                    print(f"{print_styles.RED}{message}{print_styles.RESET}")
                                    break
                            
                            parse_time = time(datetime.now().hour, datetime.now().minute)
                            print(f"Su hora actual es: {print_styles.YELLOW}{str(parse_time)[0:-3]}{print_styles.RESET}, presione Enter si desea dejar la hora actual")
                            actual_time = input("Ingrese la hora (formato: HH:MM): ")
                            if len(actual_time) == 0:
                                actual_time = str(parse_time)[0:-3]
                            else:
                                message, is_valid = validate_hour(actual_time)
                                if not is_valid:
                                    print(f"{print_styles.RED}{message}{print_styles.RESET}")
                                    break

                            get_accounts(accounts)
                            id_account = int(input("Ingrese el número de la cuenta: "))
                            get_categories(categories)
                            id_category = int(input("Ingrese el número de la categoria: "))
                            amount = int(input("Ingrese el importe: "))
                            descripcion = input("Ingrese la descripcion: ")
                            month = "Marzo"

                            if sub_option == "1":
                                add_transaction(transactions, accounts, categories, budgets, id_account, id_category, date, actual_time, amount, descripcion, month)
                            elif sub_option == "2":
                                add_transaction(transactions, accounts, categories, budgets,id_account, id_category, date, actual_time, amount, descripcion, month, "Expense")
                elif option == "3":   # Opción 3
                    permission = has_permission(user,READ_WRITE)
                    if permission: 
                        get_transactions(transactions, accounts, categories)
                        transaction = get_transaction_by_user_input(transactions)

                        while transaction is not None:
                            print(f"\033[1;34m¿Qué campo de la transacción deseas actualizar?{print_styles.RESET}")
                            print(f"{print_styles.BOLD}[1]{print_styles.RESET} Cuenta")
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Categoría")
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Fecha")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Hora")
                            print(f"{print_styles.BOLD}[5]{print_styles.RESET} Importe")
                            print(f"{print_styles.BOLD}[6]{print_styles.RESET} Descripción")
                            print(f"{print_styles.BOLD}[7]{print_styles.RESET} Mes")
                            print(f"{print_styles.BOLD}[0]{print_styles.RESET} Guardar y salir")
                            
                            option = input("Seleccione una opción: ")
                            
                            if option == "1":
                                update_account_transaction(transaction, accounts)
                            elif option == "2":
                                update_category_transaction(transaction, categories)
                            elif option == "3":
                                update_date_transaction(transaction)
                            elif option == "4":
                                update_time_transaction(transaction)
                            elif option == "5":
                                update_amount_transaction(transaction, accounts, budgets)
                            elif option == "6":
                                update_description_transaction(transaction)
                            elif option == "7":
                                update_month_transaction(transaction)
                            elif option == "0":
                                print(f"{print_styles.GREEN}La transacción se actualizó con éxito.{print_styles.RESET}")
                                break
                            else:
                                print(f"{print_styles.RED}Opción no válida. Intente nuevamente.{print_styles.RESET}")
                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        get_transactions(transactions, accounts, categories)
                        id = int(input("Que transaccion deseas eliminar? Indique el número o escriba 0 para salir: "))
                        while id < 0 or id > len(transactions):
                            id = int(input("Que transaccion deseas eliminar? Indique el número o escriba 0 para salir: "))
                            
                        if id != 0:
                            delete_transaction(transactions, accounts, categories, budgets)
                        else:
                            print(f"{print_styles.GREEN}No se elimino ninguna transacción.{print_styles.RESET}")
                elif option=='5':
                     permission = has_permission(user,READ)
                     if permission:
                        get_transactions_by_category(transactions, accounts, categories)
                                                                                
                input("Presione ENTER para volver a seleccionar.")
        
        elif option == "2":   # Opción 2 --> Gestión de categorías

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Categorías")
                    print("---------------------------")
                    if can_read:
                        print(f"{print_styles.BOLD}[1]{print_styles.RESET} Mostrar Categorías")
                        if can_write:
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Añadir Categoría")
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Actualizar Categoría")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Eliminar Categoría")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    if option in valid_options: 
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":   # Opción 1
                    permission= has_permission(user,READ)
                    if permission:
                        get_categories(categories)
                elif option == "2":   # Opción 2
                    permission= has_permission(user,READ_WRITE)
                    if permission:
                        category = input("Ingrese el nombre de la categoria: ")
                        add_category(categories, category)

                elif option == "3":   # Opción 3
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        update_category(categories)

                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission: 
                        delete_category(categories, transactions, budgets)
                                                        
                input("Presione ENTER para volver a seleccionar.")

        elif option == "3":   # Opción 3 --> Gestión de Presupuestos

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Presupuestos")
                    print("---------------------------")
                    if can_read:
                        print(f"{print_styles.BOLD}[1]{print_styles.RESET} Mostrar Presupuestos")
                        if can_write:
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Añadir Presupuesto")
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Actualizar Presupuestos")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Eliminar Presupuesto")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    if option in valid_options: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":   # Opción 1
                    permission = has_permission(user, READ)
                    if permission:
                        get_budgets(budgets, categories)
                elif option == "2":   # Opción 2
                    permission = has_permission(user, READ_WRITE)
                    if permission:
                        get_categories(categories)
                        category_id = int(input("Ingrese el ID de la categoría: "))
                        limit_amount = int(input("Ingrese el monto limite para la categoría: "))
                        create_budget(budgets, category_id, limit_amount, categories)

                elif option == "3":   # Opción 3
                    permission = has_permission(user, READ_WRITE)
                    if permission:                             
                        get_budgets(budgets, categories)
                        budget = get_budget_by_user_input(budgets)

                        while budget is not None:
                            print("\033[1;34m¿Qué campo del presupuesto deseas actualizar?\033[0m")
                            print(f"{print_styles.BOLD}[1]{print_styles.RESET} Categoría")
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Monto")
                            print(f"{print_styles.BOLD}[0]{print_styles.RESET} Guardar y salir")
                            
                            option = input("Seleccione una opción: ")
                            
                            if option == "1":
                                update_category_for_budget(budget, categories)
                            elif option == "2":
                                update_budget_amount(budget)
                            elif option == "0":
                                print("\033[32mEl presupuesto se actualizó con éxito.\033[0m")
                                break
                            else:
                                print("\033[31mOpción no válida. Intente nuevamente.\033[0m")

                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        delete_budget(budgets, categories)
                                                        
                input("Presione ENTER para volver a seleccionar.")

        elif option == "4":   # Opción 4 --> Gestión de cuentas

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Cuentas")
                    print("---------------------------")
                    if can_read:
                        print(f"{print_styles.BOLD}[1]{print_styles.RESET} Mostrar Cuentas")
                        if can_write:
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Añadir Cuentas")
                            print(f"{print_styles.BOLD}[3]{print_styles.RESET} Actualizar Cuentas")
                            print(f"{print_styles.BOLD}[4]{print_styles.RESET} Eliminar Cuentas")
                    print("---------------------------")
                    print(f"{print_styles.BOLD}[0]{print_styles.RESET} Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    if option in valid_options: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":   # Opción 1
                    permission = has_permission(user,READ)
                    if permission:
                        get_accounts(accounts)
                elif option == "2":   # Opción 2
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        account_name = input("Ingrese el nombre de la cuenta: ")
                        total_money = input("Ingrese el monto de la cuenta: ")
                        add_account(accounts, account_name, total_money)

                elif option == "3":   # Opción 3
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        get_accounts(accounts)

                        account = get_account_by_user_input(accounts)

                        while account is not None:
                            print(f"{print_styles.BOLD_BLUE}¿Qué campo de la cuenta deseas actualizar?{print_styles.RESET}")
                            print(f"{print_styles.BOLD}[1]{print_styles.RESET} Nombre")
                            print(f"{print_styles.BOLD}[2]{print_styles.RESET} Monto")
                            print(f"{print_styles.BOLD}[0]{print_styles.RESET} Guardar y salir")
                            
                            option = input("Selecciona una opción: ")
                            
                            if option == "1":
                                update_name_account(account)
                            elif option == "2":
                                update_money_account(account)
                            elif option == "0":
                                print(f"{print_styles.GREEN}La cuenta se actualizó con éxito.{print_styles.RESET}")
                                break
                            else:
                                print(f"{print_styles.RED}Opción no válida. Intente nuevamente.{print_styles.RESET}")

                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:                        
                        allow_delete = input(f"{print_styles.YELLOW}Se borraran todas las transacciones relacionadas a esta cuenta{print_styles.RESET}, ¿desea proseguir? y/n: ")

                        while allow_delete != 'y' and allow_delete != 'n':
                            print(f"\n{print_styles.RED}No se reconoce el carácter{print_styles.RESET}")
                            allow_delete = input("¿Desea proseguir? y/n: ")

                        if (allow_delete == 'n'):
                            print(f"\n{print_styles.GREEN}No se borrará ninguna cuenta.{print_styles.RESET}")
                            break                        
                        
                        get_accounts(accounts)
                        id_account = int(input("Que cuenta deseas eliminar? Indique el numero o escriba 0 para salir: "))
                        while id_account < 0 or id_account > len(accounts):
                            if id_account == 0:
                                print(f"{print_styles.GREEN}No se elimino ninguna cuenta.{print_styles.RESET}")
                                break
                            id_account = int(input("Que cuenta deseas eliminar? Indique el numero o escriba 0 para salir: "))

                        if id_account != 0:
                            related_accounts_transaction = list(filter(lambda x: x[1] == id_account, transactions))
                            for actual_transaction in related_accounts_transaction:
                                delete_transaction(transactions, accounts, categories, budgets, actual_transaction[0])
                            delete_account(accounts, id_account)
                        else:
                            print(f"{print_styles.GREEN}No se elimino ninguna cuenta.{print_styles.RESET}")

                input("Presione ENTER para volver a seleccionar.")

        elif option == "5":   # Opción 5 --> Resumen

            while True:
                while True:
                    options = 2
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Resumen")
                    print("---------------------------")
                    print("[1] Ver resumen de gastos totales")
                    print("[2] Ver resumen de gastos por categoría")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()
                    
                    option = input("Seleccione una opción: ")
                    if option in [str(i) for i in range(0, options + 1)]: # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if option == "0": # Opción salir del submenú
                    break # No salimos del programa, volvemos al menú anterior
                elif option == "1":
                    total, month = total_last_month(transactions)
                    print(f"Total Gastado en el mes de {month}: {total}")
                    print(f"Promedio de total gastado por mes: {average_month(transactions)}")
                    print("Categoria con mas gastos: ")
                    print("Cuenta con mas gastos:")
                elif option == "2":
                    filter_transactions, total = calculate_percentage_of_category(transactions)
                    get_percentage_of_category(filter_transactions, total, categories)                
                
                input("Presione ENTER para volver a seleccionar.")
              
        print("\n\n")


# Punto de entrada al programa
main()