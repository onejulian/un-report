# 🌍 Monitor ONU - Inteligencia Geopolítica

> **Analista de IA para Riesgos Geopolíticos**: Sistema autónomo que monitorea la evolución del orden mundial, enfocándose en la efectividad de la ONU y el impacto de la IA en la seguridad global.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/AI-Gemini%203%20Flash-orange)
![Status](https://img.shields.io/badge/Status-Activo-success)

## 🧠 ¿Qué es esto?

Este proyecto es un **sistema de inteligencia automatizado** que actúa como un analista geopolítico senior especializado en monitorear una tesis específica sobre el estado del orden mundial:

> *"La ONU sufre una parálisis política estructural debido al veto en el Consejo de Seguridad, volviéndose irrelevante para prevenir guerras, mientras que la Inteligencia Artificial y las armas autónomas emergen como los verdaderos catalizadores que forzarán un cambio de paradigma en la seguridad global."*

### 🎯 Objetivos

El sistema realiza dos tipos de investigación automatizada:

1. **Monitoreo Reactivo (Últimas 24h):** Busca eventos recientes, movimientos militares o resoluciones que confirmen o refuten la tesis.
2. **Monitoreo Prospectivo (Horizon Scanning):** Identifica fechas específicas de eventos futuros que puedan ser "Puntos de Inflexión" (Cumbres, votaciones del CSNU, plazos de trabajos sobre LAWS en Ginebra, etc.).

### 📊 Pilares de Análisis

El sistema investiga específicamente estos 4 pilares:

1. **Termómetro Político (CSNU):** Vetos, bloqueos, unilateralismo en el Consejo de Seguridad.
2. **Frente Humanitario:** Estado operativo de UNRWA, OCHA, PMA (Programa Mundial de Alimentos).
3. **Catalizador Tecnológico:** Avances en IA militar, incidentes con drones autónomos, regulación de armas autónomas.
4. **Señales de Reforma:** Movimientos del G4, implementación del Pacto del Futuro.

---

## 🚀 Características

- **Análisis Autónomo Diario:** Se ejecuta automáticamente cada 24 horas.
- **Acceso a Datos en Tiempo Real:** Utiliza Google Search para obtener noticias y eventos recientes.
- **Dashboard Web Moderno:** Genera reportes en HTML con diseño profesional dark mode y responsive.
- **Análisis Contextual:** Compara cada reporte con el día anterior para detectar evoluciones y cambios significativos.
- **Historial Persistente:** Mantiene los últimos 10 reportes para análisis de tendencias.
- **Manejo de Errores Robusto:** Sistema de reintentos automáticos ante errores de API (503).
- **Año Dinámico:** El título se actualiza automáticamente cada año sin intervención manual.

---

## 🛠️ Instalación y Uso Local

### Prerrequisitos
- Python 3.10 o superior
- Una API Key de Google Gemini ([Google AI Studio](https://aistudio.google.com/))

### Pasos

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/un-report.git
   cd un-report
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar API Key:**
   - **Mac/Linux:** `export GEMINI_API_KEY="tu_api_key_aqui"`
   - **Windows (PowerShell):** `$env:GEMINI_API_KEY="tu_api_key_aqui"`
   - **Git Bash (Windows):** `export GEMINI_API_KEY="tu_api_key_aqui"`

4. **Ejecutar el análisis:**
   ```bash
   python main.py
   ```
   *Esto generará o actualizará el archivo `index.html` en la raíz del proyecto.*

---

## 🤖 Automatización (GitHub Actions)

Este repositorio incluye un workflow configurado (`.github/workflows/monitor.yml`) para ejecutarse automáticamente en GitHub Actions de forma **100% gratuita**.

### Configuración Inicial

1. Ve a `Settings` > `Secrets and variables` > `Actions` en tu repositorio de GitHub.
2. Crea un **New repository secret** llamado `GEMINI_API_KEY` y pega tu clave API.
3. Habilita permisos de escritura en `Settings` > `Actions` > `General` > `Workflow permissions` (Selecciona "Read and write permissions").

### Funcionamiento

- **Frecuencia:** Se ejecuta automáticamente cada **24 horas** (configurable en `monitor.yml`).
- **Auto-Commit:** El sistema analiza la situación geopolítica, genera el reporte HTML y hace un `git push` automático.
- **GitHub Pages:** Puedes activar GitHub Pages (Source: `main` branch) para ver tu dashboard en vivo en `https://tu-usuario.github.io/un-report/`.

---

## 📂 Estructura del Proyecto

```text
un-report/
├── .github/workflows/
│   └── monitor.yml       # Configuración del workflow (GitHub Actions)
├── main.py               # Motor principal (IA + lógica de análisis)
├── index.html            # Dashboard (generado automáticamente)
├── requirements.txt      # Dependencias (google-genai)
├── CNAME                 # Configuración de dominio personalizado (opcional)
└── README.md             # Documentación
```

---

## 🔍 Cómo Funciona

### 1. **System Prompt (Personalidad del Analista)**
Define las reglas, el contexto de la tesis y las instrucciones de investigación que sigue la IA.

### 2. **Recopilación de Datos**
Utiliza la herramienta de búsqueda de Google (Google Search Tooling) para investigar cada uno de los 4 pilares.

### 3. **Análisis Comparativo**
Extrae el reporte del día anterior y lo usa como contexto para detectar cambios y evoluciones significativas.

### 4. **Generación del Reporte**
Produce un reporte estructurado en HTML con las siguientes secciones:
- 🚨 Resumen Ejecutivo (BLUF)
- 🔍 Análisis de las Últimas 24h (4 pilares)
- 🔭 Radar de Eventos Críticos (Próximos hitos)
- 📉 Conclusión Diaria (Diagnóstico de tendencia)

### 5. **Publicación**
Actualiza `index.html` con el nuevo reporte y hace commit automático (en GitHub Actions).

---

## ⚙️ Configuración Avanzada

### Cambiar la Frecuencia de Ejecución
Edita `.github/workflows/monitor.yml` y modifica la línea del cron:
```yaml
schedule:
  - cron: '0 */24 * * *'  # Cada 24 horas
```

### Cambiar el Modelo de IA
En `main.py`, línea 11, puedes cambiar el modelo:
```python
MODEL_ID = "gemini-3-flash-preview"  # O usa "gemini-1.5-pro-latest"
```

### Ajustar el Número Máximo de Reportes
En `main.py`, línea 177:
```python
MAX_REPORTS = 10  # Cambia este número según tus necesidades
```

---

## 🛡️ Manejo de Errores

El sistema incluye un mecanismo de reintentos para manejar errores 503 de la API:
- **Máximo de Intentos:** 2
- **Delay entre Intentos:** 30 segundos
- **Terminación Elegante:** Si persiste el error, termina la ejecución sin generar costos innecesarios en GitHub Actions.

---

## 📊 Formato de Salida

El reporte HTML incluye:
- **Dashboard Dark Mode** con diseño profesional
- **Tarjetas de Reporte** con animaciones hover
- **Tipografía Premium** (Inter, Segoe UI)
- **Responsive Design** para móviles y desktop
- **Timestamps** precisos para cada reporte
- **Historial Visual** de los últimos reportes

---

## ⚠️ Disclaimer

Esta herramienta es un **experimento de investigación en inteligencia geopolítica automatizada**. Los reportes generados son análisis automatizados basados en modelos de lenguaje y datos públicos. **No constituyen asesoramiento político, militar o de seguridad nacional.** Este proyecto es puramente académico y de investigación.

---

## 📝 Licencia

Este proyecto está disponible bajo licencia abierta para fines educativos y de investigación.

---

## 🤝 Contribuciones

¿Tienes ideas para mejorar el análisis o agregar nuevas fuentes de datos? ¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama con tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---
