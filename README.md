# FarmaChasqui

Prototipo Django para atención inicial en una botica. Consulta un catálogo local,
permite solicitudes preliminares de productos de venta libre y deriva los casos
que requieren criterio profesional.

## Límites de seguridad

- No diagnostica, prescribe ni recomienda dosis.
- No confirma automáticamente productos que requieren receta.
- Deriva consultas sobre receta, dosis, interacciones, embarazo, alergias o
  síntomas al químico farmacéutico.
- El catálogo es la única fuente de precios y disponibilidad.

## Inicio local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_catalog
python manage.py createsuperuser
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`. El panel de gestión está en `/admin/`.

## Estructura

- `products`: catálogo, precio, stock y condición de venta.
- `chat`: reglas de clasificación y respuesta conversacional segura.
- `orders`: solicitudes preliminares de productos sin receta.
- `core`: interfaz web principal y configuración compartida.

Antes de operar con datos reales, el químico farmacéutico debe validar el
catálogo y las reglas de derivación.
