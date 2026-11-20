# Aplicación inicial — Caso 1 Parques Naturales

## Importante: incompatibilidades detectadas antes de implementar

1. El DDL del proyecto corresponde a Parques Naturales: contiene `VISITANTE` y `EXCURSION`, no tablas `CLIENTE` ni `ORDEN_REPARACION`. Por eso los DAO cuentan visitantes y excursiones, sin inventar tablas.
2. El `docker-compose.yml` existente declara `MYSQL_DATABASE: caso1_parquesNaturales`, mientras los scripts DDL y SQL usan `caso1_parques_naturales`. Debe unificarse el nombre. MySQL puede distinguir nombres de bases de datos en Linux; además, cambiar `MYSQL_DATABASE` no renombra automáticamente una base ya inicializada dentro del volumen.
3. El archivo `.env.example` mostrado contiene un valor de ejemplo, no debe usarse como contraseña real. Copiarlo a `.env`, reemplazar la contraseña y mantener `.env` ignorado por Git.

## Estructura mínima sugerida

```text
proyecto/
├── docker-compose.yml        # conservar db y phpmyadmin; agregar app
├── .env                    # local, no versionar
├── .env.example             # plantilla versionada
└── app/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    ├── db/
    │   ├── connection.py
    │   └── dao.py
    ├── services/
    │   └── metrics_service.py
    └── tests/
        └── test_database.py
```

## Configuración local

Desde la raíz del repositorio:


```bash
cp .env.example .env
```
Edita `.env` y cambia `MYSQL_ROOT_PASSWORD` por la contraseña que configuraste para el servicio MySQL. No compartas ni commits `.env`.

## Compose

Conserva el servicio `db` y `phpmyadmin` existentes y agrega el servicio `app` desde el fragmento `docker-compose.addition.yml`. La carpeta del Dockerfile debe quedar como `./app` respecto al `docker-compose.yml`.

Asegúrate de que `MYSQL_DATABASE` sea `caso1_parques_naturales`, el nombre usado por el DDL/scripts SQL del proyecto. Si el volumen `mysql_data` ya tiene una base inicializada con otro nombre, confirma/ajusta la base existente; la variable de entorno no cambia bases persistentes ya creadas.

## Ejecutar

```bash
docker compose up -d --build
```

En Codespaces, abre el puerto 8501 (Ports → Open in Browser). phpMyAdmin continúa en el puerto 8090.

## Verificar estado y logs

```bash
docker compose ps
docker compose logs -f app
docker compose logs -f db
docker compose logs --tail=100 phpmyadmin
```

## Pruebas de integración

Los tests requieren MySQL activo y el esquema poblado:


```bash
docker compose exec app python -m pytest -q
```

Las pruebas comprueban que las dos consultas DAO entregan enteros no negativos y que la población incluye visitantes y excursiones.

## Arquitectura de tres capas

- Presentación: `main.py`, Streamlit. Renderiza título y métricas.
- Lógica de negocio: `services/metrics_service.py`. Agrupa las métricas que solicita la página.
- Acceso a datos: `db/dao.py`. Ejecuta SQL mediante SQLAlchemy.
- Conexión/configuración: `db/connection.py`. Construye la URL con variables de entorno y reintenta conexión al arrancar.

## Git

```bash
git status
git add app Dockerfile  # si Dockerfile/requirements/archivos están bajo app, usar git add app
```
En la estructura propuesta, usa:
```bash
git add app docker-compose.yml .env.example .gitignore
git commit -m "Agregar aplicación Streamlit inicial conectada a MySQL"
git push
```
No agregues `.env` al commit.
