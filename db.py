import sqlite3

"""
En este fichero se centralizan todas las funcion usadas por la aplicacion.
Estas funciones son las que conectan la aplicación con la base de datos.

Hay 16 funciones:

1- get_connection(db_path="db/users.db"): 
    Se conecta a la base de datos

2: get_user_login(conn, username, password):
    Compara las credenciales con la base de datos, si coinciden se inicia sesión.
    
3: register_user(conn, username, email, password):
    Añade a la base de datos la informacion cuando una nueva persona se registra.
    
4: def get_all_games(conn):
    Devuelve todos los juegos disponibles en la base de datos.

5: insert_into_biblioteca(conn, user_id, juego_id):
    Se encarga de añadir el juego a la biblioteca del usuario que lo "compra"

6: get_biblioteca_by_user(conn, user_id):
    Sirve para mostrar todos los juegos que dicho usuario tiene en su biblioteca.

7: user_exists_by_name(conn, username):
    Devuelve True si existe un usuario con ese 'nombre', False si no existe.

8: get_user_id_by_name(conn, username):
    Retorna el idUsuario del usuario con nombre=? o None si no existe.

9: add_friend(conn, user_id, friend_id):
    Añade a un nuevo amigo a su lista de amigos
    
10: get_friends_of_user(conn, user_id):
    Muestra la lista de amigos del usuario
    
11: def get_username_by_id(conn, user_id):
    Devuelve el nombre a partir del id
    
12: buy_game(conn, user_id, juego_id):
    Añade el juego comprado a la biblioteca
    
13: remove_game_from_library(conn, user_id, juego_id):
    Elimina un juego ya comprado de la biblioteca
    
14: remove_friend(conn, user_id, friend_id):
    Elimina a un "amigo" de la lista de amigos

15: search_games(conn, search_text=None, genero_id=None, limit=15):
    Permite busqueda filtrada de juegos, y establece un limite de 15 items en la tienda
    
16: get_all_generos(conn):
    Devuelve todos los generos de los videojuegos
    
"""

def get_connection(db_path="db/users.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_login(conn, username, password):
    """
    Retorna la fila del usuario si nombre+contraseña coinciden.
    De lo contrario, None.
    """
    query = """
    SELECT * FROM USUARIOS
    WHERE nombre=? AND contraseña=?
    """
    cur = conn.cursor()
    cur.execute(query, (username, password))
    return cur.fetchone()

def register_user(conn, username, email, password):
    """
    Crea un nuevo usuario.
    """
    query = """
    INSERT INTO USUARIOS (nombre, email, fechaRegistro, contraseña)
    VALUES (?, ?, DATE('now'), ?)
    """
    cur = conn.cursor()
    cur.execute(query, (username, email, password))
    conn.commit()
    return cur.lastrowid


def get_all_games(conn):
    """
    Devuelve todos los juegos disponibles (LIST).
    """
    query = "SELECT * FROM JUEGOS"
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def insert_into_biblioteca(conn, user_id, juego_id):
    """
    Inserta un juego en la biblioteca de un usuario con fecha actual.
    """
    query = """
        INSERT INTO BIBLIOTECA (idUsuario, idJuego, fechaCompra)
        VALUES (?, ?, DATE('now'))
    """
    cur = conn.cursor()
    cur.execute(query, (user_id, juego_id))
    conn.commit()


def get_biblioteca_by_user(conn, user_id):
    """
    Retorna todos los juegos que posee un usuario.
    Incluye JOIN para traer datos del juego.
    """
    query = """
        SELECT B.idJuego, J.titulo, J.precio, B.fechaCompra
        FROM BIBLIOTECA B
        JOIN JUEGOS J ON B.idJuego = J.idJuego
        WHERE B.idUsuario = ?
    """
    cur = conn.cursor()
    cur.execute(query, (user_id,))
    return cur.fetchall()


def user_exists_by_name(conn, username):
    """
    Devuelve True si existe un usuario con ese 'nombre', False si no existe.
    """
    query = "SELECT idUsuario FROM USUARIOS WHERE nombre = ?"
    cur = conn.cursor()
    cur.execute(query, (username,))
    row = cur.fetchone()
    return (row is not None)

def get_user_id_by_name(conn, username):
    """
    Retorna el idUsuario del usuario con nombre=?
    o None si no existe.
    """
    query = "SELECT idUsuario FROM USUARIOS WHERE nombre = ?"
    cur = conn.cursor()
    cur.execute(query, (username,))
    row = cur.fetchone()
    if row:
        return row['idUsuario']
    return None

def add_friend(conn, user_id, friend_id):
    """
    Inserta el amigo (friend_id) en la tabla AMIGOS para user_id.
    """
    query = """
        INSERT INTO AMIGOS (idUsuario, idAmigo)
        VALUES (?, ?)
    """
    cur = conn.cursor()
    cur.execute(query, (user_id, friend_id))
    conn.commit()

def get_friends_of_user(conn, user_id):
    """
    Lista los amigos de un usuario, devolviendo 
    datos básicos del amigo (idUsuario, nombre).
    """
    query = """
        SELECT U.idUsuario, U.nombre
        FROM AMIGOS A
        JOIN USUARIOS U ON A.idAmigo = U.idUsuario
        WHERE A.idUsuario = ?
    """
    cur = conn.cursor()
    cur.execute(query, (user_id,))
    return cur.fetchall()

# db.py
def get_username_by_id(conn, user_id):
    """
    Retorna el nombre del usuario con el ID dado.
    """
    query = """
    SELECT nombre 
    FROM USUARIOS
    WHERE idUsuario = ?
    """
    cur = conn.cursor()
    cur.execute(query, (user_id,))
    row = cur.fetchone()
    return row['nombre'] if row else None

def buy_game(conn, user_id, juego_id):
    """
    Inserta un juego en la biblioteca de un usuario.
    Lanza una excepción si el juego ya está en la biblioteca.
    """
    query_check = """
    SELECT 1
    FROM BIBLIOTECA
    WHERE idUsuario = ? AND idJuego = ?
    """
    query_insert = """
    INSERT INTO BIBLIOTECA (idUsuario, idJuego, fechaCompra)
    VALUES (?, ?, DATE('now'))
    """

    cur = conn.cursor()
    
    # Verificar si el juego ya está en la biblioteca
    cur.execute(query_check, (user_id, juego_id))
    if cur.fetchone():
        raise ValueError("El juego ya está en tu biblioteca.")

    # Insertar el juego en la biblioteca
    cur.execute(query_insert, (user_id, juego_id))
    conn.commit()

def remove_game_from_library(conn, user_id, juego_id):
    """
    Elimina (borra) un juego de la biblioteca de un usuario.
    """
    query = """
    DELETE FROM BIBLIOTECA
    WHERE idUsuario = ? AND idJuego = ?
    """
    cur = conn.cursor()
    cur.execute(query, (user_id, juego_id))
    conn.commit()

def remove_friend(conn, user_id, friend_id):
    """
    Elimina a 'friend_id' de la lista de amigos de 'user_id'.
    """
    query = """
    DELETE FROM AMIGOS
    WHERE idUsuario = ? AND idAmigo = ?
    """
    cur = conn.cursor()
    cur.execute(query, (user_id, friend_id))
    conn.commit()

def search_games(conn, search_text=None, genero_id=None, limit=15):
    query = """
    SELECT J.idJuego, J.titulo, J.precio, J.fechaLanzamiento
    FROM JUEGOS J
    """
    params = []

    if genero_id:
        query += """
        JOIN JUEGOS_GENEROS JG ON J.idJuego = JG.idJuego
        WHERE JG.idGenero = ?
        """
        params.append(genero_id)
        if search_text:
            query += " AND J.titulo LIKE ?"
            params.append(f"%{search_text}%")
    else:
        if search_text:
            query += " WHERE J.titulo LIKE ?"
            params.append(f"%{search_text}%")

    query += " ORDER BY J.titulo ASC LIMIT ?"
    params.append(limit)

    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchall()


def get_all_generos(conn):
    """
    Retorna todos los generos (idGenero, nombre)
    """
    query = "SELECT idGenero, nombre FROM GENEROS ORDER BY nombre ASC"
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()
