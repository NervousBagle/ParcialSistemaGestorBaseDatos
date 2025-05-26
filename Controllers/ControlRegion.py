### 
# Controlador que recibe los datos de las vistas, las procesa y luego se las da al modelo Region
###
from Views.Crear import *
from Models.Region import *
class ControlRegion:
    def ingresarRegion(region_id, name, continent_id):
        try:
            Region.ingresarRegion(region_id = region_id, name = name, continent_id = continent_id)
            print("Se han guardado la informacion")
        except ValueError as error:
            print("Error al ingresar los datos{}".format())