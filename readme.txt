//Examen de la asginatura de Bases de datos//

# Plataforma de videojuegas que imita las funcionalidades de Steam.

Para usar se tiene unicamente que inciar python app.py desde la consola.

Para pruebas de la aplicación se aconseja usar credenciales de test:
Username: admin 
Password: admin

La aplicación consta con 3 funcionalidades mostradas en la pagina principal "Home"

Se puede consultar la librería:
Es decir los juegos que dicho usuario ha adquirido.

Se puede consultar la tienda:
Juegos disponibles con su precio.

Lista de Amigos:
Se puede añadir o eliminar a amigos con la condición de que estén registrados en la App.

Cada Funcionalidad tiene asociada si respectiva tabla de la base de datos.

La base de datos se compone de:

Tablas

    USUARIOS:
        idUsuario (PK): Identificador único del usuario.
        nombre (UNIQUE, NOT NULL): Nombre del usuario, único y con al menos 3 caracteres.
        email (NOT NULL): Correo del usuario con validación de formato.
        fechaRegistro: Fecha de registro en formato YYYY-MM-DD.
        contraseña (NOT NULL): Contraseña del usuario con al menos 4 caracteres.

    JUEGOS:
        idJuego (PK): Identificador único del juego.
        titulo (UNIQUE, NOT NULL): Nombre del juego.
        precio (NOT NULL): Precio del juego.
        fechaLanzamiento: Fecha en que el juego fue lanzado.

    GENEROS:
        idGenero (PK): Identificador único del género.
        nombre (NOT NULL): Nombre del género (Ej. "RPG", "Acción").

    JUEGOS_GENEROS (relación N:M):
        idJuego (PK, FK): Referencia a JUEGOS.
        idGenero (PK, FK): Referencia a GENEROS.

    BIBLIOTECA (relación N:M):
        idUsuario (PK, FK): Referencia a USUARIOS.
        idJuego (PK, FK): Referencia a JUEGOS.
        fechaCompra: Fecha en que el usuario adquirió el juego.

    AMIGOS (relación N:M recursiva):
        idUsuario (PK, FK): Usuario que tiene un amigo.
        idAmigo (PK, FK): Amigo del usuario.

2. Modelo Entidad-Relación (MER)

    USUARIOS:
        Atributos: idUsuario, nombre, email, fechaRegistro, contraseña.

    JUEGOS:
        Atributos: idJuego, titulo, precio, fechaLanzamiento.

    GENEROS:
        Atributos: idGenero, nombre.

    Relaciones:
        JUEGOS - GENEROS: Relación N:M (un juego puede pertenecer a varios géneros, y un género puede aplicarse a varios juegos).
        USUARIOS - BIBLIOTECA: Relación N:M (un usuario puede tener múltiples juegos, y un juego puede estar en múltiples bibliotecas).
        USUARIOS - AMIGOS: Relación N:M recursiva (un usuario puede tener varios amigos).



