# Plataforma Seguridad Eventos

## Requisitos

* Python 3.10 o superior
* Git
* Pip

---

## 1. Crear un entorno virtual

### Linux / macOS

```bash
python -m venv .venv
```

### Windows (PowerShell)

```powershell
python -m venv .venv
```

---

## 2. Activar el entorno virtual

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Verificar que el entorno está activo

### Linux / macOS

```bash
which python
```

### Windows (PowerShell)

```powershell
Get-Command python
```

Si la ruta apunta a `.venv`, el entorno virtual está funcionando correctamente.

---

## 4. Actualizar pip

```bash
python -m pip install --upgrade pip
```

Si aparece el error `No module named pip`, ejecuta:

```bash
python -m ensurepip --upgrade
```

---

## 5. Configurar Git

Agrega el entorno virtual al archivo `.gitignore`:

```gitignore
.venv/
```

---

## 6. Instalar dependencias

### Instalar FastAPI y dependencias recomendadas

```bash
pip install "fastapi[standard]"
```

### Instalar dependencias desde requirements.txt

```bash
pip install -r requirements.txt
```

### Generar o actualizar requirements.txt

```bash
pip freeze > requirements.txt
```

---

## 7. Ejecutar la aplicación FastAPI

Antes de levantar el servidor, aplica las migraciones:

```bash
alembic upgrade head
```

### Opción 1: FastAPI CLI (recomendado)

```bash
fastapi dev app/main.py
```

### Opción 2: Uvicorn

Si tu aplicación está definida como:

```python
app = FastAPI()
```

en el archivo `app/main.py`, ejecuta:

```bash
uvicorn app.main:app --reload
```

La primera creación de usuario se puede hacer sin credenciales. Después de eso,
las rutas bajo `/api/v1` requieren autenticación HTTP Basic usando `correo` y
`contrasena`.

---

## 8. Acceder a la aplicación

Una vez iniciado el servidor, podrás acceder a:

| Recurso    | URL                         |
| ---------- | --------------------------- |
| API        | http://127.0.0.1:8000       |
| Swagger UI | http://127.0.0.1:8000/docs  |
| ReDoc      | http://127.0.0.1:8000/redoc |

---

## 9. Estructura del proyecto

```text
plataforma-seguridadeventos/
│
├── .venv/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Comandos útiles

### Desactivar el entorno virtual

```bash
deactivate
```

### Ver paquetes instalados

```bash
pip list
```

### Actualizar dependencias

```bash
pip install --upgrade -r requirements.txt
```

### Ejecutar pruebas (si existen)

```bash
pytest
```
