import hashlib

def hash_from_file(filename):

    h = hashlib.sha256()
    with open(filename, 'rb') as file:
        while chunk := file.read(h.block_size):
            h.update(chunk)
    return h.hexdigest()


def from_file_object(file_obj):

    h = hashlib.sha256()
    file = file_obj.open('rb')
    while chunk := file.read(h.block_size):
        h.update(chunk)
    file.close()
    return h.hexdigest()
