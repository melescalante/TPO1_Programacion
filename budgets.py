from Styles import print_styles
from categories import get_categories
from data import budgets, categories
from helper import create_id, get_raw_by_id

def get_budgets(matrix_budgets):
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f'{"Presupuestos":^60}')
    print("="*print_styles.MAX_SPACES_BUDGETS)
    print(f"{print_styles.BOLD}{'Numero':<10}{'Categoria':<25}{'Monto':<25}{print_styles.RESET}")
    for i in range(len(matrix_budgets)):
        id=matrix_budgets[i][0]
        category = get_raw_by_id(categories,matrix_budgets[i][1])
        amount = "$"+str(matrix_budgets[i][2])
        print(f"{print_styles.BOLD}{id:<10}{print_styles.RESET}{category[1]:<25}{amount:<25}")
    return

def create_budget(category_id, limit_amount, matrix_categories):
    id_budget = create_id(budgets)
    print("Id creado:", id_budget)
    category = get_raw_by_id(matrix_categories, category_id)
    id_category = category[0]
    if (id_category is None):
        print("\033[31mLa categoría no existe. Por favor, cree una.\033[0m", id_category)
        return
    
    for category in matrix_categories:
        if category[0] == id_category:
            budgets.append([id_budget, id_category, limit_amount])
            return

def delete_budget(matrix_budgets):    
    get_budgets(budgets)    
    id = int(input("Ingrese el id o 0 para no eliminar ningún presupuesto: "))

    if id <= 0:
        return
    
    budget_deleted = None
    index = -1
    
    for budget in matrix_budgets:
        if (budget[0] == id):
            index = matrix_budgets.index(budget)
            budget_deleted = matrix_budgets.pop(index)
            print("\033[32mOperación realizada con éxito. Presupuesto eliminado correctamente.\033[0m")
            return
    
    print("\033[31mNo se encontró el presupuesto a eliminar.\033[0m")

def update_budget(matrix_budgets, matrix_categories):
    get_budgets(matrix_budgets)
    id_budget = int(input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: "))    
    if id_budget == 0:
        print("\033[32mNo se actualizó ningún presupuesto.\033[0m")
        return
    
    budget = get_raw_by_id(matrix_budgets, id_budget)
    while budget is None:
        print("\033[31mEl presupuesto no existe.\033[0m")
        
        id_budget = int(input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: "))
        while id_budget < 0 or id_budget >= matrix_budgets[-1][0]:
            print("\033[31mEntrada inválida. Debe ingresar un número.\033[0m")
            id_budget = int(input("¿Qué presupuesto desea actualizar? Indique el número o escriba 0 para salir: "))
            
        if id_budget == 0:
            print("\033[32mNo se actualizó ningún presupuesto.\033[0m")
            return
                
        budget = get_raw_by_id(matrix_budgets, id_budget)
    
    while True:
        print("\033[1;34m¿Qué campo del presupuesto deseas actualizar?\033[0m")
        print("1. Categoría")
        print("2. Monto")
        print("0. Guardar y salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            change_category_for_budget(budget, matrix_categories)
        elif opcion == "2":
            change_budget_amount(budget)
        elif opcion == "0":
            print("\033[32mEl presupuesto se actualizó con éxito.\033[0m")
            return
        else:
            print("\033[31mOpción no válida. Intente nuevamente.\033[0m")

def change_category_for_budget(budget, matrix_categories):
    get_categories(matrix_categories)
    id_category = int(input("¿Qué categoría desea asignar? Indique el número o escriba 0 para cancelar: "))
    if id_category == 0:
        print("\033[32mNo se actualizó la categoría.\033[0m")
        return
    
    category = get_raw_by_id(matrix_categories, id_category)
    while category is None:
        print("\033[31mLa categoría no existe.\033[0m")

        id_category = int(input("¿Por cuál categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_category == 0:
            print("\033[32mNo se actualizo la categoría.\033[0m")
            return
                
        category = get_raw_by_id(matrix_categories, id_category)

    budget[1] = id_category
    print("\033[32mCategoría actualizada.\033[0m")

def change_budget_amount(budget):
    budget_amount = input("Ingrese el nuevo monto del presupuesto: ")
    while not budget_amount.isnumeric():
        print("\033[33mEl valor que ingresó no es un número válido.\033[0m")
        budget_amount = input("Ingrese el nuevo monto del presupuesto: ")
        
    budget[2] = int(budget_amount)
    print("\033[32mMonto actualizado.\033[0m")

