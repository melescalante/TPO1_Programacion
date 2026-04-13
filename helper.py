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