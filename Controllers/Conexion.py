### 
# Para instalar la libreria que permite la conexxion con mysql usar las siguientes lineas en la terminal
#   cd <direccion donde se clono el repositorio>
#   pip install mysql-connector-python
###

import mysql.connector

class CConexion:
    def conexionBaseDeDatos():
        config = {
            'user' : 'root', 
            'password' : '',
            'host' : '127.0.0.1', 
            'database' : 'nation',
            'port' : '3306', 
            'raise_on_warnings' : True
        }
        try:
            conexion = mysql.connector.connect(**config)
            print("Conexion conectada =D")
            return conexion
        except mysql.connector.Error as error:
            print("Error al conectarse a la base de datos {}".format(error))
            return conexion

    conexionBaseDeDatos()