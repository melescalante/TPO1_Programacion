from data import accounts, transactions, categories, budgets
from transactions import *
from budgets import *
from categories import *
from accounts import *
from user import *
from analytics import * 
from permissions import has_permission

# Permissions
READ=1
READ_WRITE=2

user=users[0]
while user==None:
    user=login()

is_logged(user)

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    #-------------------------------------------------
    # Inicialización de variables
    #----------------------------------------------------------------------------------------------
    clientes = {...}
    

    #-------------------------------------------------
    # Bloque de menú
    #----------------------------------------------------------------------------------------------
    while True:
        while True:
            options = 5
            print()
            print("---------------------------")
            print("MENÚ PRINCIPAL")
            print("---------------------------")
            print("[1] Gestión de Transacciones")
            print("[2] Gestión de Categorías")
            print("[3] Gestión de Presupuestos")
            print("[4] Gestión de Cuentas")
            print("[5] Resumen")

            print("---------------------------")
            print("[0] Salir del programa")
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

        elif option == "1":   # Opción 1
            while True:
                while True:
                    options = 5
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Transacciones")
                    print("---------------------------")
                    print("[1] Mostrar Transacciones")
                    print("[2] Añadir Transacciones")
                    print("[3] Actualizar Transacciones")
                    print("[4] Eliminar Transacciones")
                    print("[5] Ver Transacciones por Categoria")
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
                                print("[1] Opción 1 (Ingreso)")
                                print("[2] Opción 2 (Egreso)")
                                print("---------------------------")
                                print("[0] Volver al menú anterior")
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

                            get_accounts(accounts)
                            id_account = int(input("Ingrese el número de la cuenta: "))
                            get_categories(categories)
                            id_category = int(input("Ingrese el número de la categoria: "))
                            date = input("Ingrese la fecha (formato: DD-MM-YYYY): ")
                            time = input("Ingrese la hora (formato: HH:MM): ")
                            amount = int(input("Ingrese el importe: "))
                            descripcion = input("Ingrese la descripcion: ")
                            month = input("Ingrese el mes: ")

                            if sub_option == "1":
                                add_transaction(transactions, accounts, categories, budgets, id_account, id_category, date, time, amount, descripcion, month)
                            elif sub_option == "2":
                                add_transaction(transactions, accounts, categories, budgets,id_account, id_category, date, time, amount, descripcion, month, "Expense")
                elif option == "3":   # Opción 3
                    permission = has_permission(user,READ_WRITE)
                    if permission: 
                        get_transactions(transactions, accounts, categories)

                        transaction = None
                        while True:
                            id_transaction = int(input("¿Qué transacción desea actualizar? Indique el numero o escriba 0 para salir: "))
                            if id_transaction < 0 or id_transaction > len(transactions):
                                print(f"{print_styles.RED}La transacción no existe.{print_styles.RESET}")
                                continue

                            if id_transaction == 0:
                                print(f"{print_styles.GREEN}No se actualizó ninguna transacción.{print_styles.RESET}")
                                break

                            transaction = get_raw_by_id(transactions, id_transaction)
                            
                            if transaction is not None:
                                break
                            else:
                                print(f"{print_styles.RED}La transacción no existe. Intente de nuevo.{print_styles.RESET}")

                        while transaction is not None:
                            print(f"\033[1;34m¿Qué campo de la transacción deseas actualizar?{print_styles.RESET}")
                            print("1. Cuenta")
                            print("2. Categoría")
                            print("3. Fecha")
                            print("4. Hora")
                            print("5. Importe")
                            print("6. Descripción")
                            print("7. Mes")
                            print("0. Guardar y salir")
                            
                            opcion = input("Seleccione una opción: ")
                            
                            if opcion == "1":
                                change_account_transaction(transaction, accounts)
                            elif opcion == "2":
                                change_category_transaction(transaction, categories)
                            elif opcion == "3":
                                change_date_transaction(transaction)
                            elif opcion == "4":
                                change_time_transaction(transaction)
                            elif opcion == "5":
                                change_amount_transaction(transaction, accounts, budgets)
                            elif opcion == "6":
                                change_description_transaction(transaction)
                            elif opcion == "7":
                                change_month_transaction(transaction)
                            elif opcion == "0":
                                print(f"{print_styles.GREEN}La transacción se actualizó con éxito.{print_styles.RESET}")
                                break
                            else:
                                print(f"{print_styles.RED}Opción no válida. Intente nuevamente.{print_styles.RESET}")
                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        delete_transaction(transactions, accounts, categories, budgets)
                elif option=='5':
                     permission = has_permission(user,READ)
                     if permission:
                        get_transactions_by_category(transactions, accounts, categories)
        elif option == "2":   # Opción 2

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Categorías")
                    print("---------------------------")
                    print("[1] Mostrar Categorías")
                    print("[2] Añadir Categoría")
                    print("[3] Actualizar Categoría")
                    print("[4] Eliminar Categoría")
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

        elif option == "3":   # Opción 3

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Presupuestos")
                    print("---------------------------")
                    print("[1] Mostrar Presupuestos")
                    print("[2] Añadir Presupuesto")
                    print("[3] Actualizar Presupuestos")
                    print("[4] Eliminar Presupuesto")
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
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        update_budget(budgets, categories)

                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        delete_budget(budgets, categories)

        elif option == "4":   # Opción 4

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Gestión de Cuentas")
                    print("---------------------------")
                    print("[1] Mostrar Cuentas")
                    print("[2] Añadir Cuentas")
                    print("[3] Actualizar Cuentas")
                    print("[4] Eliminar Cuentas")
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
                    if permission:update_account(accounts)

                elif option == "4":   # Opción 4
                    permission = has_permission(user,READ_WRITE)
                    if permission:
                        delete_account(accounts)

        elif option == "5":   # Opción 5

            while True:
                while True:
                    options = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > Resumen")
                    print("---------------------------")
                    print(f"Total Gastado en el mes: {total_last_month(transactions)}")
                    print(f"Promedio de total gastado por mes: {average_month(transactions)}")
                    print("Categoria con mas gastos: ")
                    print("Cuenta con mas gastos:")
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
              
        print("\n\n")


# Punto de entrada al programa
main()