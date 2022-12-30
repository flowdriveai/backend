import os
from api.config import basedir

def internal_path(path, make=False):
    internal_path = os.path.join(basedir,path)
    if not os.path.exists(internal_path) and make:
        os.makedirs(internal_path)
    return internal_path

