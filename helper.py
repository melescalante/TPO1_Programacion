def obtain_id_by_name(matrix, name):
    for raw in matrix:
        if raw[1] == name:
            return raw[0]
    return -1

def create_id(matrix):
    id=len(matrix) + 1
    return id

def get_by_id(matrix, id):
    for raw in matrix:
        if raw[0] == id:
            return raw
    return None

def slice_words(len, word):
    sliced_word=word[:len-3]+"..."
    return sliced_word