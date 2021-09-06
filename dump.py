#!/usr/bin/env python
# encoding: utf-8

import pickle
from os import path

# Guarda la variable en el almacenamiento externo
def serialize(varname, value):
    # El nombre con el que se guardará la variable en el almacenamiento
    # externo
    filename = varname + '.obj'
    # Carga el valor de la variable al archivo externo
    with open(filename, 'wb') as file:
        pickle.dump(value, file)

# Genera la variable a partir del archivo
def deserialize(varname, value):
    # Nombre del archivo de donde se cargará la variable
    filename = varname + '.obj'
    # Si existe el archivo, carga los datos a la variable
    if path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    # De lo contrario, crea una nueva instancia 
    else:
        return value

