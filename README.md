# API REST: Juego de Piedra, Papel o Tijera

Este proyecto implementa una API REST para jugar a piedra, papel o tijera.

## Pasos para poner en marcha el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/IrvinAlexanders/ppt-game-rest-api.git
cd ppt-game-rest-api
```

### 2. Levantar el proyecto con Docker Compose

Asegúrate de tener [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/) instalados.

```bash
docker-compose up --build
```

Esto iniciará todos los servicios necesarios para la API.

### 3. Acceder a la documentación de la API

Una vez que el proyecto esté en marcha, puedes acceder a la documentación generada automáticamente:

- **Esquema OpenAPI:**  
    [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

- **Swagger UI:**  
    [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)

- **Redoc UI:**  
    [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/)

---

¡Listo! Ahora puedes explorar y probar la API para el juego de piedra, papel o tijera.