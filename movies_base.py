from cassandra.cluster import Cluster
import uuid
import sys
# ==============================
# CQL Statements
# ==============================
CREATE_KEYSPACE = """
CREATE KEYSPACE IF NOT EXISTS movies
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
"""
CREATE_TABLE_MOVIE_BY_TITLE = CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS movie_by_title (
movie_id UUID,
title TEXT,
release_year INT,
genre TEXT,
rating FLOAT,
director TEXT,
PRIMARY KEY (title, release_year)
)
"""
CREATE_TABLE_MOVIE_BY_GENRE = """
CREATE TABLE IF NOT EXISTS movie_by_genre (
movie_id UUID,
title TEXT,
release_year INT,
genre TEXT,
rating FLOAT,
director TEXT,
PRIMARY KEY (genre, rating,movie_id)
)WITH CLUSTERING ORDER BY (rating DESC)
"""
INSERT_MOVIE_TITLE = """
INSERT INTO movie_by_title
    (movie_id, title, release_year, director,
        genre, rating)
VALUES (?, ?, ?, ?, ?, ?)
"""
INSERT_MOVIE_GENRE = """
INSERT INTO movie_by_genre
    (movie_id, title, release_year, director,
    genre, rating)
VALUES (?, ?, ?, ?, ?, ?)
"""
DELETE_MOVIE_TITLE = "DELETE FROM movie_by_title WHERE title= ? AND release_year= ?"


DELETE_MOVIE_GENRE = "DELETE FROM movie_by_genre WHERE genre= ? AND rating= ?"


SELECT_BY_TITLE = "SELECT * FROM movie_by_title WHERE title = ? AND release_year = ?"
SELECT_BY_GENRE = "SELECT * FROM movie_by_genre WHERE genre = ? "

UPDATE_BY_TITLE="""
UPDATE movie_by_title 
SET director = ?
WHERE title = ? AND release_year = ?
"""

UPDATE_BY_GENRE="""
UPDATE movie_by_genre 
SET director = ?
WHERE genre = ? AND rating = ? AND movie_id = ?
"""




# ==============================
# Funciones base
# ==============================
def create_keyspace_and_tables(session):
    session.execute(CREATE_KEYSPACE)
    session.set_keyspace("movies")
    print("Keyspace movies seleccionado")
    stmt = session.prepare(CREATE_TABLE_MOVIE_BY_TITLE)
    session.execute(stmt)
    print("Tabla movie_by_title creada")
    stmt = session.prepare(CREATE_TABLE_MOVIE_BY_GENRE)
    session.execute(stmt)
    print("Tabla movie_by_genre creada")
    pass 

def insert_movie(session, title, year, director, genre, rating):
    movie_id = uuid.uuid4()
    stmt = session.prepare(INSERT_MOVIE_TITLE)
    session.execute(stmt, (movie_id, title, year, director, genre, rating))
    stmt = session.prepare(INSERT_MOVIE_GENRE)
    session.execute(stmt, (movie_id, title, year, director, genre, rating))
    pass  

def query_by_title(session, title, year):
    stmt = session.prepare(SELECT_BY_TITLE)
    rows = session.execute(stmt,(title, year))   
    for r in rows:
        print("-------Pelicula---------")
        print(f"TItulo: {r.title}\nAño de estreno: {r.release_year}")
    pass  

def query_by_genre(session, genre):
    stmt = session.prepare(SELECT_BY_GENRE)
    rows = session.execute(stmt,(genre,))  
    print(f"\nGenero: {genre}") 
    for r in rows:
        print(f"Pelicula: {r.title} - {r.rating}")
    pass  


def update_movie_director(session, title, year, new_director):
    select_query = "SELECT genre, rating, movie_id FROM movie_by_title WHERE title = %s AND release_year = %s"
    row = session.execute(select_query, (title, year)).one()
    genre = row.genre
    rating = row.rating
    movie_id = row.movie_id

    stmt_title = session.prepare(UPDATE_BY_TITLE)
    session.execute(stmt_title, (new_director, title, year))

    stmt_genre = session.prepare(UPDATE_BY_GENRE)
    session.execute(stmt_genre, (new_director, genre, rating, movie_id))
    
    print(f"\nEl director fue actualizado a '{new_director}' en ambas tablas.")

def delete_movie(session, title, genre, rating, release_year):
    stmt = session.prepare(DELETE_MOVIE_TITLE)
    session.execute(stmt, (title, release_year))
    stmt = session.prepare(DELETE_MOVIE_GENRE)
    session.execute(stmt, (genre, rating))
    print(f"Pelicula: {title} eliminada")
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
        print("5. Eliminar pelicula")
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
            year = int(input("Año: "))
            new_director = input("Nuevo Director: ")
            update_movie_director(session, title, year, new_director)
        elif choice == "5":
            # Eliminar de movie_by_title -> title, release_year
            # Eliminar de movie_by_genre -> genre, rating
            title = input("Título: ")
            genre = input("Género: ")
            rating = float(input("Rating: ")) 
            release_year = int(input("Año: ")) 
            delete_movie(session, title, genre, rating, release_year)
        elif choice == '0':
            # Cerrar conexión y salir
            cluster.shutdown()
            print("Sesión finalizada")
            sys.exit()
            pass
        else:
            print("Opción inválida")
            break

if __name__ == "__main__":
    main()