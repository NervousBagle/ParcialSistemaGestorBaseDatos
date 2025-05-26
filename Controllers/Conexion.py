### 
# Para instalar la libreria que permite la conexxion con mysql usar las siguientes lineas en la terminal
#   cd <direccion donde se clono el repositorio>
#   pip install mysql-connector-python
###

import mysql.connector

class CConexion:
    def ConexionBaseDeDatos():
        try:
            conexion = mysql.connector.connect(
                user = 'root', password = '',
                host = 'localhost', database = 'nations',
                port = '3306'
            )
            print("Conexion conectada =D")
        except mysql.connector.Error as error:
            print("Error al conectarse a la base de datos {}".format(error))