# Suite de Pruebas Automatizadas - Urban Routes

## Descripción del Proyecto
Este proyecto contiene una suite de pruebas automatizadas de extremo a extremo (E2E) diseñadas para validar la funcionalidad principal de la plataforma **Urban Routes**. La automatización cubre todo el flujo de usuario: desde la selección de la ruta y tarifa Comfort, la validación del número telefónico mediante interceptación de SMS y vinculación de tarjeta de crédito, hasta la solicitud de servicios adicionales (manta, pañuelos y helados) y la verificación del modal de asignación del conductor.

## Tecnologías y Técnicas Utilizadas
- **Lenguaje de Programación:** Python 3.x
- **Herramienta de Automatización Web:** Selenium WebDriver
- **Framework de Pruebas:** Pytest
- **Patrón de Diseño:** Page Object Model (POM)
- **Sincronización:** Esperas explícitas (`WebDriverWait` y `expected_conditions`)
- **Control de Versiones:** Git y GitHub

## Estructura del Proyecto
```text
qa-project-Urban-Routes-es/
│
├── data.py         # Variables globales y datos de prueba estáticos.
├── main.py         # Page Object (UrbanRoutesPage), funciones helper y suite de pruebas (TestUrbanRoutes).
├── README.md       # Documentación general del proyecto.
└── .venv/          # Entorno virtual de Python.