from CRUD.database_connection import MySQLDatabaseConnection
from typing import List
from pydantic import BaseModel

class UserData(BaseModel):
    UserID: int = None  # Opcional, ya que es autoincremental
    Username: str
    Password: str
    Role: int
    Email: str

class UserCRUD:
    def __init__(self):
        self.db_connection = MySQLDatabaseConnection()
        self.db_connection.connect()

    def _execution(self, query: str, values: tuple):
        """Ejecuta una consulta sin retorno de datos (INSERT, UPDATE, DELETE)."""
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            self.db_connection.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"❌ Error en la ejecución de la consulta: {e}")

    def create(self, data: UserData):
        """Inserta un nuevo usuario y devuelve su ID."""
        query = """
            INSERT INTO users (Username, Password, Role, Email)
            VALUES (%s, %s, %s, %s);
        """
        try:
            values = (data.Username, data.Password, data.Role, data.Email)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            self.db_connection.connection.commit()
            user_id = cursor.lastrowid  # MySQL obtiene el último ID insertado
            cursor.close()
            return user_id
        except Exception as e:
            print(f"❌ Error al crear usuario: {e}")
            return None

    def update(self, id_: int, data: UserData):
        """Actualiza el usuario por ID."""
        query = """
            UPDATE users
            SET Username = %s, Password = %s, Role = %s, Email = %s
            WHERE UserID = %s;
        """
        values = (data.Username, data.Password, data.Role, data.Email, id_)
        self._execution(query, values)

    def delete(self, id_: int):
        """Elimina un usuario por ID."""
        query = "DELETE FROM users WHERE UserID = %s;"
        values = (id_,)
        self._execution(query, values)

    def get_by_id(self, id_: int):
        """Obtiene un usuario por su ID."""
        query = "SELECT UserID, Username, Password, Role, Email FROM users WHERE UserID = %s;"
        try:
            values = (id_,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            print(f"❌ Error al obtener usuario por ID: {e}")
            return None

    def get_all(self):
        """Obtiene todos los usuarios."""
        query = "SELECT * FROM users;"
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()
            return users
        except Exception as e:
            print(f"❌ Error al obtener todos los usuarios: {e}")
            return []

    def get_by_name(self, name: str):
        """Busca usuarios por nombre."""
        query = "SELECT UserID, Username, Password, Role, Email FROM users WHERE Username LIKE %s;"
        try:
            values = (f"%{name}%",)  # Se usa % para el LIKE en MySQL
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            users = cursor.fetchall()
            cursor.close()
            return users
        except Exception as e:
            print(f"❌ Error al buscar usuario por nombre: {e}")
            return []

    def get_by_email(self, email: str):
        """Obtiene un usuario por su correo."""
        query = "SELECT UserID, Username, Password, Role, Email FROM users WHERE Email = %s;"
        try:
            values = (email,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            print(f"❌ Error al buscar usuario por email: {e}")
            return None
