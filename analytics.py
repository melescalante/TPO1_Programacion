from helper import get_month, get_raw_by_id

def total_last_month(transactions):
    """
    transactions: lista de transacciones a analizar
    Retorna: tupla (monto_absoluto_gastos, nombre_mes) del último mes con transacciones
    """
    last_year = 0
    last_month = 0
    month = ""

    for i in transactions:
        date = i['date']
        day, month, year = date.split("-")
        
        month = int(month)
        year = int(year)

        if year > last_year or (year == last_year and month > last_month):
            last_year = year
            last_month = month

    total_expenses = 0

    for i in transactions:
        date = i['date']
        day, month, year = date.split("-")

        month = int(month)
        year = int(year)

        if month == last_month and year == last_year and i['amount'] < 0:
            total_expenses += i['amount']

    return abs(total_expenses), get_month(last_month)

def sum_accounts_amount(data_accounts, index=0):
    """
    Calcula de forma recursiva la suma total de los montos de todas las cuentas.

    data_accounts: lista de diccionarios donde cada uno representa una cuenta y contiene la clave "amount"
    index: índice de la lista utilizado para controlar la recursión
    Retorna: La suma acumulada de todos los montos ("amount") de las cuentas
    """
    if index >= len(data_accounts):
        return 0
    return data_accounts[index]["amount"] + sum_accounts_amount(data_accounts, index + 1)

def average_month(transactions):
    """
    transactions: lista de transacciones a analizar
    Retorna: promedio absoluto mensual de gastos redondeado a dos decimales
    """
    total_month = {}

    for i in transactions:
        date = i['date']
        day, month, year = date.split("-")

        key = year + "-" + month  

        if i['amount'] < 0:
            if key not in total_month:
                total_month[key] = 0
            total_month[key] += i['amount']

    if len(total_month) == 0:
        return 0

    total = sum(total_month.values())
    average = round(total / len(total_month), 2)

    return abs(average)

def get_higher_expense(data_transactions, data_to_search, search_value):
    """
    data_transactions: matriz de transacciones
    search_value: indice para buscar dentro de transacciones
    Retorna: La categoría que tiene el gasto máximo
    """    
    category = {}
    
    for transaction in data_transactions:
        actual_category = transaction[search_value]
        amount = transaction['amount']         
        if actual_category in category:   
            category[actual_category] += amount
        else:
            category[actual_category] = amount
    
    return get_raw_by_id(data_to_search, min(category, key=category.get))