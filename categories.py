from Styles import print_styles
from data import categories
from helper import create_id, get_raw_by_id, replace_spaces

def get_categories(matrix_categories):
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    print(f'{"Categorias":^50}')
    print("="*print_styles.MAX_SPACES_CATEGORIES)
    print(f"{print_styles.BOLD}{'Numero':<20}{'Categoria':<30}{print_styles.RESET}")
    for i in range(len(matrix_categories)):
        id=matrix_categories[i][0]
        amount = matrix_categories[i][1]
        print(f"{print_styles.BOLD}{id:<20}{print_styles.RESET}{amount:<30}")
    return

def add_category(category_name):
    id=create_id(categories)
    for category in categories:
        if category[1] == category_name:
            return
    categories.append([id, category_name])

def delete_category(matrix_transactions, matrix_budgets):
    get_categories(categories)
    id = int(input("Que categoria deseas eliminar? Indique el numero o escriba 0 para salir: "))
    delete=[]
    index=0
    
    if id == 1:
        print("\033[31mLa categoría deseada no puede ser eliminada.\033[0m")
        return
    
    if id <= 0:
        print("\033[32mNo se elimino ninguna categoria.\033[0m")
        return
    
    # Eliminar la categoría de la transacción
    for transaccion in matrix_transactions:
        if transaccion[2] == id:
            transaccion[2] = 1
    
    # Lambda
    # Filter
    # Slicing
    matrix_budgets[:] = list(filter(lambda x : x[1] != id, matrix_budgets))
    
    for category in categories:
        if category[0]==id:
            index=categories.index(category)
            delete=categories.pop(index)
            print("\033[32mOperación realizada con éxito. Categoria eliminada correctamente.\033[0m")
            break
    
    print()

def update_category(matrix_categories):
    get_categories(matrix_categories)
    id_category = int(input("¿Que categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
    
    if id_category == 1:
        print("\033[31mLa categoría deseada no puede ser actualizada.\033[0m")
        return

    if id_category == 0:
        print("\033[32mNo se actualizo ninguna categoría.\033[0m")
        return

    category = get_raw_by_id(matrix_categories, id_category)
    while category is None:
        print("\033[31mLa categoría no existe.\033[0m")

        id_category = int(input("¿Que categoría desea actualizar? Indique el numero o escriba 0 para salir: "))
        if id_category == 0:
            print("\033[32mNo se actualizo ninguna categoría.\033[0m")
            return
                
        category = get_raw_by_id(matrix_categories, id_category)
    
    change_category(category)

def change_category(category):
    name_category = input("Ingrese un nuevo nombre de categoría: ")
    while len(name_category) == 0 or not replace_spaces(name_category).isalpha():
        print("\033[33mEl valor que ingreso no tiene valor o no es una palabra.\033[0m")
        name_category = input("Ingrese un nuevo nombre de categoría: ")
    category[1] = name_category

