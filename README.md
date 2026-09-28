# restaurante_app - Semana 15

## Tema
**Conceptos fundamentales de manejo de eventos**

## Propósito
Esta versión continúa el proyecto `restaurante_app` de la Semana 14. Se conserva la arquitectura modular, el inicio de sesión, la consulta de usuarios, la gestión de productos y la persistencia en JSON. La nueva funcionalidad es una operación sencilla de **venta** que relaciona un usuario con un producto.

## Estructura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo_restaurante.png
│   ├── icono_restaurante.png
│   └── README.txt
├── main.py
└── README.md
```

## Evolución desde la Semana 14
Se conserva el proyecto existente y se incorpora una sección de Ventas. No se reconstruye la arquitectura.

La nueva operación permite:
1. Seleccionar un usuario existente.
2. Seleccionar un producto existente.
3. Pulsar el botón **Registrar venta**.
4. Ejecutar el callback mediante `command=`.
5. Delegar la validación y persistencia a `RestauranteServicio`.
6. Guardar la venta en `datos/ventas.json`.
7. Actualizar la tabla de ventas y mostrar el resultado al usuario.

## Fundamento de eventos
El flujo implementado es:

```text
Usuario
   ↓
Botón Registrar venta
   ↓
command=self.registrar_venta
   ↓
Callback registrar_venta()
   ↓
RestauranteServicio
   ↓
ventas.json
   ↓
Tabla de ventas + mensaje visual
```

Se utiliza `command=callback` sin paréntesis para que Tkinter ejecute el método cuando el usuario presiona el botón.

## Componentes utilizados
Se utilizan `Frame`, `LabelFrame`, `Label`, `Entry`, `Button`, `Combobox`, `Treeview` y `Scrollbar`, organizados mediante `pack()` y `grid()`.

## Assets
La carpeta `assets/` es obligatoria para esta semana. Se incorporan:
- `logo_restaurante.png`: logotipo utilizado en el encabezado.
- `icono_restaurante.png`: ícono de la aplicación.

## Persistencia
- `productos.json`: productos del restaurante.
- `usuarios.json`: usuarios registrados.
- `ventas.json`: ventas realizadas.

La lectura y escritura se realiza mediante `ArchivoServicio`; la lógica de negocio permanece en `RestauranteServicio`.

## Credenciales de prueba
- Usuario: `admin`
- Contraseña: `1234`

También existe:
- Usuario: `cajero`
- Contraseña: `1234`

## Ejecución
1. Tener Python 3 instalado.
2. Abrir una terminal dentro de la carpeta del proyecto.
3. Ejecutar:

```bash
python main.py
```

No se requieren librerías externas para ejecutar la aplicación.

## Comprobaciones de la Semana 15
- Inicio de sesión.
- Navegación.
- Consulta de usuarios.
- Gestión de productos.
- Sección visible de Ventas.
- Selección de usuario.
- Selección de producto.
- Registro mediante botón con `command=`.
- Callback de venta.
- Validación en `RestauranteServicio`.
- Persistencia en `ventas.json`.
- Actualización de la tabla de ventas.
- Recuperación de ventas al volver a ejecutar.

## Restricciones respetadas
No se implementan `bind()`, doble clic, `TreeviewSelect`, eventos avanzados de teclado/mouse, carrito, facturación, inventario avanzado ni bases de datos, porque no forman parte del objetivo de esta Semana 15.
