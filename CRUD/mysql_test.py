"""Este módulo maneja la conexión a la base de datos MySQL."""

import mysql.connector
from mysql.connector import Error

class MySQLDatabaseConnection:
    def __init__(self):
        self._dbname = "db_project"  # Nombre de la BD en Docker
        self._duser = "root"
        self._dpass = "PASS"       # Debe coincidir con Docker Compose
        self._dhost = "localhost"
        self._dport = 3308          # Número, no string
        self.connection = None

    def connect(self):
        """Establece la conexión con MySQL."""
        try:
            self.connection = mysql.connector.connect(
                host=self._dhost,
                user=self._duser,
                password=self._dpass,
                database=self._dbname,
                port=self._dport
            )
            if self.connection.is_connected():
                print("✅ Conexión a MySQL exitosa")
        except Error as e:
            print(f"❌ Error al conectar a MySQL: {e}")

# 🔹 Prueba la conexión cuando ejecutas el script
if __name__ == "__main__":
    db = MySQLDatabaseConnection()
    db.connect()
