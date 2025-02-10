import psycopg2
from psycopg2 import OperationalError

class PostgresDatabaseConnection:
    def __init__(self):
        self._dbname = "shop"                # Cambiar el nombre de la tabla
        self._duser = "postgres"
        self._dpass = "password"             # Debe coincidir con la contraseña del docker-compose
        self._dhost = "localhost"
        self._dport = "5433"                 # Usa el puerto mapeado (5433 en este caso)
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self._dbname,
                user=self._duser,
                password=self._dpass,
                host=self._dhost,
                port=self._dport
            )
            print("Conexión a la base de datos exitosa")
        except OperationalError as e:
            print(f"Error al conectar a la base de datos: {e}")
        except Exception as i:
            print(f"Error desconocido: {i}")
