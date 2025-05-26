### 
# Controlador que recibe los datos de las vistas, las procesa y luego se las da al modelo Region
###
# from Views.Crear import *
from asyncio.windows_events import NULL
from Conexion import *
import sys

sys.path.append("Models")
from Region import Region # type: ignore

class ControlRegion:
# Obtiene los datos de una region, luego los ingresa
    def ingresarRegion(region):
        name = region.get_name()
        con_id = region.get_continent_id()

        try:
            conexion = CConexion.conexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = "insert into regions values(null, %s, %s);"
            valores = (name, con_id)
            cursor.execute(sql, valores)
            print(" nombre ", name, " continente", con_id)
            conexion.commit()
            print(cursor.rowcount, "Registro Ingresado")
            conexion.close()

        except mysql.connector.Error as error:
            print("Error de ingreso de datos {}".format(error))
# Obtiene todos los datos de todas las regiones
    def mostrarRegion():
        try:
            conexion = CConexion.conexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = "Select * from regions;"
            cursor.execute(sql)
            resultadoConsulta = cursor.fetchall()
            conexion.commit()
            print(cursor.rowcount, "Registro obtenido")
            conexion.close()
            return resultadoConsulta

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
# Cambiar el nombre y el continente de la region dada
    def actualizarRegion(id, region):
        aux_id = id
        reg_id = region.get_region_id()
        name = region.get_name()
        con_id = region.get_continent_id()

        try:
            conexion = CConexion.conexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = "update regions set regions.name = %s, regions.continent_id = %s where regions.region_id = %s;"
            valores = (name, con_id, aux_id)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Registro actualizado")
            conexion.close()

        except mysql.connector.Error as error:
            print("Error al actualizar datos {}".format(error))
            print(valores)
# Recibe el id de un renglon y lo elimina
    def borrarRegion(name):
        aux_name = name
        try:
            conexion = CConexion.conexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = "delete from regions where regions.name = %s;"
            valores = (aux_name,)
            cursor.execute(sql, valores)
            conexion.commit()
            print(cursor.rowcount, "Registro eliminado")
            conexion.close()

        except mysql.connector.Error as error:
            print("Error al eliminar datos {}".format(error))

# reg = Region(NULL, "Gondor", 8)
reg1 = Region(26, "Gondor", 7)
# ControlRegion.ingresarRegion(reg1)
for row in ControlRegion.mostrarRegion():
    print(row)
# ControlRegion.actualizarRegion(26, reg1)
# ControlRegion.borrarRegion("Gondor")
