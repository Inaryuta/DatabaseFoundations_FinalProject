from CRUD.database_connection import PostgresDatabaseConnection

if __name__ == "__main__":
    db = PostgresDatabaseConnection()
    db.connect()
    if db.connection:
        print("La conexión se estableció correctamente.")
    else:
        print("No se pudo establecer la conexión.")