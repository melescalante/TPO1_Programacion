from datetime import datetime, date, time

def obtain_id_by_name(matrix, name):
    for raw in matrix:
        if raw[1] == name:
            return raw[0]
    return -1

def create_id(matrix):
    id=len(matrix) + 1
    return id

def get_raw_by_id(matrix, id):
    for raw in matrix:
        if raw[0] == id:
            return raw
    return None

def slice_words(length, word):
    sliced_word=f"{word[:length-3]}..." if len(word)>length else word
    return sliced_word

def is_word_alpha(word):
    has_letters = False

    for car in word:
        if car == " ":
            continue

        if not car.isalpha():
            return False
    
        has_letters = True

    return has_letters

def validate_hour(hour_input):
    parse_hour = datetime.strptime(hour_input, "%H:%M").time()
    
    actual_hour = time(datetime.now().hour, datetime.now().minute)
    
    if parse_hour > actual_hour:
        return "Inválida. La hora ingresada es mayor a la actual", False
    
    return "", True

def validate_date(date_input):
    parse_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    
    min_limit = date(1980, 1, 1)
    max_limit = datetime.today().date()
    
    if parse_date < min_limit:
        return f"[{date_input}] Inválida: Es anterior a 1980.", False
    elif parse_date > max_limit:
        return f"[{date_input}] Inválida: Es una fecha futura.", False
    
    return "", True
    
months = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

def get_month(value_month):
    return months.get(value_month, "No existe el mes ingresado")