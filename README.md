# Streaming Platform API

## Descripción de la Aplicación

Esta es una API para una plataforma de streaming que permite a los usuarios ver eventos en vivo, gestionar perfiles, realizar compras y administrar categorías y eventos. La API está construida usando FastAPI y SQLAlchemy, y está diseñada para manejar autenticación, autorización, y diferentes roles de usuario.

## Características Principales

- **Autenticación de Usuarios**: Los usuarios pueden registrarse e iniciar sesión en la plataforma.
- **Gestión de Perfiles**: Los usuarios pueden crear y gestionar múltiples perfiles, cada uno con sus propias configuraciones.
- **Eventos en Streaming**: Los usuarios pueden ver y comprar acceso a eventos en vivo.
- **Gestión de Categorías**: Los administradores pueden crear, actualizar y eliminar categorías de eventos.
- **Roles de Usuario**: La API implementa un sistema de roles para restringir el acceso a ciertas funcionalidades.

## Encriptación

La encriptación de las contraseñas de los usuarios se realiza en el archivo `utils/auth.py`. El protocolo utilizado es **bcrypt**, un algoritmo de hashing seguro diseñado para almacenar contraseñas.

- **Archivo**: `utils/auth.py`
- **Protocolo**: `bcrypt`
- **Función de encriptación**: `get_password_hash(password: str) -> str`
- **Verificación de contraseñas**: `verify_password(plain_password: str, hashed_password: str) -> bool`

## Autenticación basada en Tokens

La API utiliza tokens JWT para autenticar a los usuarios y asegurar las rutas. Cuando un usuario inicia sesión, se le proporciona un token JWT que debe ser incluido en las solicitudes subsecuentes para acceder a recursos protegidos.

### Generación de Tokens

- **Archivo**: `utils/auth.py`
- **Función de generación de tokens**: `create_access_token(data: dict, expires_delta: timedelta = None) -> str`

Cuando un usuario se autentica correctamente, se genera un token JWT que incluye información relevante como el identificador del usuario y sus roles.

### Definición de Roles

- **Archivo**: `models.py`
- **Modelo**: `Role`
- **Relación**: Los roles están relacionados con los usuarios a través de una tabla de asociación `user_roles`.

### Asignación y Verificación de Roles

- **Asignación de Roles**: Los roles pueden ser asignados a los usuarios mediante el endpoint `/assign-role` en el archivo `routers/roles.py`.
- **Verificación de Roles**: Antes de acceder a ciertas rutas, se verifica que el usuario tenga el rol adecuado utilizando la función `verify_role` definida en `utils/auth.py`.


## Documentación de la API

La documentación interactiva de la API está disponible en los siguientes enlaces:

- **Swagger UI**: [https://ctf.muud.cloud/docs](https://ctf.muud.cloud/docs)
- **Redoc**: [https://ctf.muud.cloud/redoc](https://ctf.muud.cloud/redoc)
