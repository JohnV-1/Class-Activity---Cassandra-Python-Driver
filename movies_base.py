from cassandra.cluster import Cluster
import uuid
# ==============================
# CQL Statements
# ==============================
CREATE_KEYSPACE = """
CREATE KEYSPACE IF NOT EXISTS movies
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
"""
CREATE_TABLE_MOVIE_BY_TITLE = ""
CREATE_TABLE_MOVIE_BY_GENRE = ""
INSERT_MOVIE_TITLE = ""
INSERT_MOVIE_GENRE = ""
DELETE_MOVIE_TITLE = ""
DELETE_MOVIE_GENRE = ""
SELECT_BY_TITLE = ""
SELECT_BY_GENRE = ""

# ==============================
# Funciones base
# ==============================
def create_keyspace_and_tables(session):
    pass  

def insert_movie(session, title, year, director, genre, rating):
    pass  

def query_by_title(session, title, year):
    pass  

def query_by_genre(session, genre):
    pass  

def update_movie_director(session, title, genre, new_director):
    pass  

def delete_movie(session, title, genre, rating, release_year):
    pass
# ==============================
# Menú
# ==============================
def main():
    cluster = Cluster(['127.0.0.1'], port=9024)
    session = cluster.connect()

    create_keyspace_and_tables(session)

    while True:
        print("\n=== Movie Database Menu ===")
        print("1. Insertar película")
        print("2. Consultar por título")
        print("3. Consultar por género")
        print("4. Actualizar director")
        print("0. Salir")
        choice = input("Seleccione opción: ")

        if choice == "1":
            title = input("Título: ")
            year = int(input("Año: "))
            director = input("Director: ")
            genre = input("Género: ")
            rating = float(input("Rating: "))
            insert_movie(session, title, year, director, genre, rating)
        elif choice == "2":
            title = input("Título: ")
            year = int(input("Año: "))
            query_by_title(session, title, year)
        elif choice == "3":
            genre = input("Género: ")
            query_by_genre(session, genre)
        elif choice == "4":
            title = input("Título: ")
            genre = input("Género: ")
            new_director = input("Nuevo Director: ")
            update_movie_director(session, title, genre, new_director)
        elif choice == "5":
            # Eliminar de movie_by_title -> title, release_year
            # Eliminar de movie_by_genre -> genre, rating
            title = input("Título: ")
            genre = input("Género: ")
            rating = input("Rating: ")
            release_year = input("Año: ")
            delete_movie(session, title, genre, rating, release_year)
        elif choice == '0':
            # Cerrar conexión y salir
            pass
        else:
            print("Opción inválida")
            break

if __name__ == "__main__":
    main()