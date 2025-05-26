from Controllers.Conexion import *

class Region:

# Constructor vacio
    def __init__(self):
        pass
# Constructor con todo
    def __init__(self, __region_id, __name, __continent_id, ):
        self.__region_id = __region_id
        self.__name = __name
        self.__continent_id = __continent_id

# Setters

    def set_region_id(self, __region_id):
        self.__region_id = __region_id

    def set_name(self, __name):
        self.__name = __name

    def set_continent_id(self, __continent_id):
        self.__continent_id = __continent_id

# Getters

    def get_region_id(self):
        return self.__region_id

    def get_name(self):
        return self.__name

    def get_continent_id(self):
        return self.__continent_id

# Metodos
    def ingresarRegion(region_id, name, continent_id):
        try:
            conexion = CConexion.conexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = "insert into usuarios values(null, %s, %s, %s);"
            valores = (region_id, name, continent_id)
            cursor.execute(sql, valores)
            conexion.commit()
            print(cursor.rowcount, "Registro Ingresado")
            conexion.close()

        except mysql.connector.Error as error:
            print("Error de ingreso de datos {}".format(error))
