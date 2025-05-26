import pymysql
import os

class CConexion:
    def conexionBaseDeDatos():
        try:
            # Configurar variables de entorno
            os.environ['LC_ALL'] = 'C'
            os.environ['LANG'] = 'C'
            
            conexion = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='nation',
                port=3306,
                charset='utf8mb4'
            )
            print("Conexion conectada =D")
            return conexion
        except Exception as error:
            print("Error al conectarse a la base de datos {}".format(error))
            return None