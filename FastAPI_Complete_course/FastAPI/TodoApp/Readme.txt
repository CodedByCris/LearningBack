El primer paso es crear un ENV sobre el cual hacer las instalaciones -> python -m venv fastapienv

El segundo paso es activar el ENV creado con el comando Source fastapienv/Scripts/activate (en git bash)

El tercer paso es instalar fastapi -> pip install fastapi

El cuarto paso es instalar uvicorn -> pip install "uvicorn[standard]"

Para activar el servidor, utilizamos el comando -> uvicorn name:app -reload

#!
Para la base de datos SQL -> pip install sqlalchemy

Creamos un motor para la base de datos (database.py)

Creammos el archivo models con una tabla y el main vinculando la app con el engine

Ejecutamos uvicorn name:app -reload

Para hacer las consultas nos metemos en la tabla con sqlite3 name.db

Con .schema poodemos ver las tablas actuales

Una vez dentro del sqlite podemos hacer consultas normales, Insert, Select etc

Ejemplos: 
insert into todos (title, description, priority, completed) values ('Go to store', 'Pick up eggs', 5, False);
select * from todos;
delete from todos where id = 4;

Podemos modificar la vista del select con el comando .mode column, .mode markdown , .mode box, .mode table, etc.
Siendo .mode table el mejor

Utilizamos el Router para poder escalar la app de una manera muy sencilla

Para hashear las contraseñas instalamos los siguientes paquetes "passlib" y "bcrypt". Ambas deben de tener compatibilidad entre sus versiones
Ejemplo: 
PASSLIB -> 1.7.4
BCRYPT -> 4.0.1  (pip install bcrypt==4.0.1)

pip install python-multipart para hacer OAuth2PasswordRequestForm

Para los jwt necesitamos instalar jose -> pip install "python-jose[cryptography]"
Para la SECRET_KEY, nos vamos a la consola y escribimos openssl rand -hex 32 (nos genera una cadena de texto)

IMPORTANTE
En caso de tener 2 env por error, eliminar una con rm -rf nombre
Luego seleccionar en el interpreter la env que quieres utilizar
Abre el Command Palette con Ctrl+Shift+P.
Busca y selecciona Python: Select Interpreter.
Elige el intérprete dentro de .venv.

Si agregamos /docs en nuestra URL, podemos ver el swagger