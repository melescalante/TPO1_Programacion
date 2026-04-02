from matrix import accounts, transactions, categories, budgets
from transactions import * 
from budgets import *
from categories import *
from accounts import *

# Ejemplo con excepcion
add_transaction("Galicia","1","2-3-2026","20:20",1200000,"Sueldo","Marzo")
# Ejemplo correcto
add_transaction("Galicia","Sueldo","2-3-2026","20:20",1200000,"Sueldo","Marzo")
add_account("BBVA", 1200000)
add_category("Ropa")

# update_account(accounts)
# get_accounts(accounts)

# update_category(categories)
# get_categories(categories)

# update_budget(budgets, categories)

get_accounts(accounts)
# update_transaction(transactions, accounts, categories)
get_transactions(transactions)

# delete_account()
# delete_budget()
# get_budgets(budgets)

delete_category(transactions, budgets)
# get_budgets(budgets)
get_transactions(transactions)
# delete_transaction()
# get_accounts(accounts)
