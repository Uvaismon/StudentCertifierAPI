import hashlib
from logging import root
from django.conf import settings
import os

from certification_api.settings import BASE_DIR

def hash_from_file(filename):

    root_filename = os.path.join(BASE_DIR, 'certification', 'file_buffer', filename)

    h = hashlib.sha256()
    with open(root_filename, 'rb') as file:
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
