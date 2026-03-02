import os
import datetime
import re
import time
import concurrent.futures
from google import genai
from google.genai import types

# --- CONFIGURACIÓN ---
# Usamos el modelo experimental más capaz para razonamiento. 
# Si te da error de acceso, cambia a "gemini-1.5-pro-latest"
MODEL_ID = "gemini-3.1-pro-preview"
MODEL_ID_FALLBACK = "gemini-3-pro-preview"

# --- 1. SYSTEM PROMPT (La Personalidad y Reglas Rigurosas) ---
SYS_INSTRUCT = """# ROL
Actúa como un Analista de Inteligencia Geopolítica y Riesgos Tecnológicos Estratégicos.

# CONTEXTO DE LA MISIÓN
Estamos monitoreando una tesis específica sobre el estado del orden mundial en 2026:
"La ONU sufre una parálisis política estructural debido al veto en el Consejo de Seguridad, volviéndose irrelevante para prevenir guerras, mientras que la Inteligencia Artificial y las armas autónomas emergen como los verdaderos catalizadores que forzarán un cambio de paradigma en la seguridad global".

# INSTRUCCIONES
Utiliza Search para realizar dos tipos de investigación:

1. **Monitoreo Reactivo (Últimas 24h):** Busca eventos, movimientos militares o resoluciones recientes que confirmen o refuten nuestra tesis.
2. **Monitoreo Prospectivo (Horizon Scanning):** Busca fechas específicas de eventos futuros programados (Cumbres, votaciones del Consejo, plazos de grupos de trabajo sobre LAWS en Ginebra, lanzamientos de modelos de IA de defensa) que tengan el potencial de ser "Puntos de Inflexión".

Debes investigar específicamente estos 4 PILARES:
1. **Parálisis vs. Acción en el CSNU:** (Vetos, bloqueos, unilateralismo).
2. **Estado de la "Sala de Emergencias" (Humanitario):** (Situación operativa de UNRWA, OCHA, PMA).
3. **El Catalizador Tecnológico (IA y Armas Autónomas):** (Avances en IA Soberana, incidentes con drones autónomos, regulación).
4. **Señales de Reforma:** (Movimientos del G4, Pacto del Futuro).

# REGLAS DE SALIDA
- **Lenguaje:** Español.
- **Formato:** Devuelve ÚNICAMENTE código HTML puro para el contenido del reporte (divs, h3, p, strong, ul). NO uses bloques markdown como ```html. NO incluyas etiquetas <html> o <body>.
- **Precisión:** Si no puedes encontrar datos recientes para una métrica específica, declara "DATOS NO DISPONIBLES" en lugar de inventar información.
"""

def get_gemini_analysis(previous_report=None):
    # Recomendado: exporta tu key en el entorno para no hardcodearla en el repo.
    # - Windows (PowerShell): $env:GOOGLE_API_KEY="..."
    # - Git Bash: export GOOGLE_API_KEY="..."
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
    # api_key = ""
    
    if not api_key:
        raise ValueError("Falta la API key. Define GEMINI_API_KEY o GOOGLE_API_KEY en las variables de entorno.")

    client = genai.Client(api_key=api_key)
    
    # Fecha exacta para evitar alucinaciones temporales
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    
    # Preparar contexto del reporte anterior si existe
    previous_context = ""
    if previous_report:
        previous_context = f"""
    
    --- CONTEXTO: REPORTE DEL DÍA ANTERIOR ---
    A continuación se encuentra el reporte generado el día anterior. Úsalo como referencia para:
    1. Identificar si hay evolución o cambios significativos en los 4 pilares.
    2. Mencionar explícitamente cualquier evento que se haya materializado o resuelto.
    3. Actualizar el nivel de riesgo si ha cambiado.
    
    REPORTE ANTERIOR:
    {previous_report}
    
    IMPORTANTE: Si detectas cambios relevantes, inclúyelos en tu análisis de forma natural (no crees una sección separada de "comparación", simplemente menciona el contexto cuando sea relevante, ej: "A diferencia de ayer...", "Como se anticipó en el reporte previo...", "La situación ha escalado desde...").
    --- FIN DEL CONTEXTO ANTERIOR ---
    """

    # --- 2. USER TASK (La Instrucción de Ejecución cada 24h) ---
    query = f"""
    CURRENT TIME: {now_str}{previous_context}
    
    **TASK: Ejecuta el Informe de Situación Geopolítica y Riesgos Tecnológicos.**
    
    Sigue estrictamente estos pasos de investigación usando Google Search:

    PASO 1: Monitoreo Reactivo (Últimas 24h)
    - Pilar 1: Busca "UN Security Council veto" OR "UNSC resolution blocked" de las últimas 24 horas.
    - Pilar 2: Busca "UNRWA operations" OR "OCHA humanitarian" OR "WFP crisis" de las últimas 24 horas.
    - Pilar 3: Busca "autonomous weapons" OR "military AI" OR "LAWS Geneva" de las últimas 24 horas.
    - Pilar 4: Busca "UN reform" OR "G4 Security Council" OR "Summit of the Future" de las últimas 24 horas.

    PASO 2: Monitoreo Prospectivo (Horizon Scanning)
    - Busca fechas confirmadas de próximas reuniones del Consejo de Seguridad.
    - Busca plazos de grupos de trabajo sobre armas autónomas en Ginebra.
    - Busca fechas de cumbres internacionales sobre reforma de la ONU.
    
    OUTPUT FORMAT (HTML puro):
    <div class="report-section">
      <h3>🚨 Resumen Ejecutivo (BLUF)</h3>
      <p>[Síntesis de 3 líneas sobre la evolución del riesgo hoy]</p>
      
      <h3>🔍 Análisis de las Últimas 24h</h3>
      <h4>1. Termómetro Político (Consejo de Seguridad)</h4>
      <p><strong>Evento:</strong> [Hecho concreto]</p>
      <p><strong>Impacto:</strong> [Análisis]</p>
      
      <h4>2. Frente Humanitario</h4>
      <p><strong>Estado:</strong> [Situación crítica / Estable]</p>
      
      <h4>3. Vigilancia Tecnológica (El Catalizador)</h4>
      <p><strong>Hallazgos:</strong> [Nuevos desarrollos]</p>
      <p><strong>Nivel de Riesgo:</strong> [Bajo / Medio / Crítico]</p>
      
      <h3>🔭 Radar de Eventos Críticos (Horizon Scanning)</h3>
      <p><strong>Fecha (Aprox/Confirmada):</strong> [Ej: "Próximo martes", "Marzo 2026", "Sin fecha definida aún"]</p>
      <p><strong>Evento Crítico:</strong> [Nombre de la Cumbre, Votación o Deadline]</p>
      <p><strong>Por qué es Determinante:</strong> [Explica brevemente qué cambio estructural podría desencadenar este evento específico. Si no hay eventos críticos próximos, indica "No se detectan hitos estratégicos inmediatos".]</p>
      
      <h3>📉 Conclusión Diaria</h3>
      <p><strong>DIAGNÓSTICO:</strong> [¿La tendencia general apunta hacia una reforma pacífica o hacia una disrupción forzada por la tecnología?]</p>
    </div>
    """


    # Configuración con Herramienta de Búsqueda
    tools = [types.Tool(google_search=types.GoogleSearch())]
    
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        system_instruction=[types.Part.from_text(text=SYS_INSTRUCT)],
        # Temperature 0 para máxima precisión, 0.3 para un poco de fluidez
        temperature=0.3 
    )

    CALL_TIMEOUT = 120  # segundos máximos esperando respuesta de la API

    def _stream_model(model_id):
        """Llama al modelo de forma bloqueante; se ejecuta dentro de un hilo."""
        response = ""
        for chunk in client.models.generate_content_stream(
            model=model_id,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=query)])],
            config=generate_content_config,
        ):
            if chunk.text:
                response += chunk.text
                print(".", end="", flush=True)  # Feedback visual de carga
        return response

    def _call_model(model_id):
        """Ejecuta _stream_model en un hilo y lanza TimeoutError si supera CALL_TIMEOUT."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_stream_model, model_id)
            try:
                return future.result(timeout=CALL_TIMEOUT)
            except concurrent.futures.TimeoutError:
                raise TimeoutError(
                    f"La API no respondió en {CALL_TIMEOUT}s (modelo: {model_id})"
                )

    # Secuencia de intentos: 2 con el modelo principal + 1 con el fallback
    RETRY_DELAY = 30  # segundos
    attempts = [
        (1, MODEL_ID,          "principal"),
        (2, MODEL_ID,          "principal"),
        (3, MODEL_ID_FALLBACK, "fallback"),
        (4, MODEL_ID_FALLBACK, "fallback"),
    ]

    print(">>>> Iniciando contacto con Gemini (Estratega Macro)...")

    for attempt, model_id, model_label in attempts:
        total = len(attempts)
        try:
            result = _call_model(model_id)
            print("\n>>> Análisis completado.")
            return result

        except Exception as e:
            error_message = str(e)
            is_503_error = "503" in error_message or "Service Unavailable" in error_message
            is_timeout  = isinstance(e, TimeoutError)

            if not is_503_error and not is_timeout:
                # Cualquier error distinto a 503/timeout se lanza inmediatamente
                raise

            if attempt < total:
                next_model_label = attempts[attempt][2]  # label del siguiente intento
                reason = f"Timeout ({CALL_TIMEOUT}s)" if is_timeout else "Error 503"
                print(f"\n⚠ {reason} en modelo {model_label} (Intento {attempt}/{total})")
                print(f">>> Esperando {RETRY_DELAY}s antes de reintentar con modelo {next_model_label}...")
                time.sleep(RETRY_DELAY)
            else:
                reason = f"timeout ({CALL_TIMEOUT}s)" if is_timeout else "Error 503"
                print(f"\n❌ {reason} persistente en todos los modelos ({total} intentos).")
                print(">>> Terminando ejecución para evitar costos en GitHub Actions.")
                raise Exception(f"API de Gemini no disponible después de {total} intentos ({reason})")

def get_current_year():
    """Obtiene el año actual del servidor."""
    return datetime.datetime.now().year

def update_html(new_report_content):
    filename = "index.html"
    now_display = datetime.datetime.now().strftime("%d-%b-%Y %H:%M UTC")
    current_year = get_current_year()

    REPORTS_START = "<!-- MR_REPORTS_START -->"
    REPORTS_END = "<!-- MR_REPORTS_END -->"
    CARD_START = "<!-- MR_REPORT_CARD_START -->"
    CARD_END = "<!-- MR_REPORT_CARD_END -->"
    MAX_REPORTS = 10

    # --- NUEVO DISEÑO: Dashboard Financiero Dark Mode ---
    base_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0f172a">
    <title>Monitor ONU - Inteligencia Geopolítica</title>
    <style>
        :root {{
            --bg-body: #0f172a;       /* Slate 900 */
            --bg-card: #1e293b;       /* Slate 800 */
            --text-main: #f1f5f9;     /* Slate 100 */
            --text-muted: #94a3b8;    /* Slate 400 */
            --border: #334155;        /* Slate 700 */
            --accent: #38bdf8;        /* Sky 400 */
            --accent-glow: rgba(56, 189, 248, 0.15);
            --success: #34d399;       /* Emerald 400 */
            --font-main: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
        }}

        body {{
            font-family: var(--font-main);
            background-color: var(--bg-body);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}

        .container {{
            max-width: 850px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 25px;
            border-bottom: 1px solid var(--border);
            animation: fadeIn 0.8s ease-out;
        }}

        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(to right, #fff, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .header p {{
            margin: 0;
            color: var(--text-muted);
            font-size: 0.95rem;
        }}

        /* Tarjetas de Reporte */
        .report-card {{
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .report-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            border-color: var(--accent);
        }}

        /* Borde lateral de acento */
        .report-card::before {{
            content: "";
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 4px;
            background: var(--accent);
            opacity: 0.8;
        }}

        .timestamp {{
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--accent);
            background: var(--accent-glow);
            padding: 4px 12px;
            border-radius: 99px;
            margin-bottom: 20px;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }}

        /* Estilos del contenido generado */
        .content h3 {{
            color: var(--text-main);
            font-size: 1.1rem;
            margin-top: 24px;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
        }}
        
        .content h3::before {{
            content: "▹";
            margin-right: 8px;
            color: var(--accent);
        }}

        .content p {{
            color: var(--text-muted);
            margin-bottom: 16px;
        }}

        .content strong {{
            color: var(--success); /* Resalta datos clave en verde */
            font-weight: 600;
        }}
        
        /* Diagnóstico final destacado */
        .content p:last-child strong {{
            color: #fbbf24; /* Amber para la conclusión */
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Mobile */
        @media (max-width: 600px) {{
            body {{ padding: 12px; }}
            .header h1 {{ font-size: 1.5rem; }}
            .report-card {{ padding: 20px; border-radius: 12px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Monitor ONU {current_year}</h1>
            <p>Análisis de Riesgos Geopolíticos &amp; Tecnológicos Estratégicos</p>
        </div>
        
        <div id="archive">
            <!-- MR_REPORTS_START -->
            <!-- MR_REPORTS_END -->
        </div>
    </div>
</body>
</html>"""

    existing_reports_html = ""
    # Intentar recuperar historial existente
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                old_content = f.read()
                s = old_content.find(REPORTS_START)
                e = old_content.find(REPORTS_END)
                if s != -1 and e != -1:
                    existing_reports_html = old_content[s + len(REPORTS_START) : e]
        except Exception:
            pass

    # Bloque del nuevo reporte
    new_block = f"""
        {CARD_START}
        <div class="report-card">
            <div class="timestamp">REPORTE GENERADO: {now_display}</div>
            <div class="content">
                {new_report_content}
            </div>
        </div>
        {CARD_END}
    """
    
    # Combinar
    card_re = re.compile(re.escape(CARD_START) + r".*?" + re.escape(CARD_END), flags=re.DOTALL)
    old_cards = card_re.findall(existing_reports_html)
    
    # Nuevo + Viejos (Max 10)
    all_cards = [new_block] + old_cards[:MAX_REPORTS-1]
    
    final_reports_section = "\n".join(c.strip() for c in all_cards)
    
    # Inyectar en la NUEVA base
    # Usamos replace con el formato exacto del string base_html de arriba
    final_html = base_html.replace(
        "            <!-- MR_REPORTS_START -->\n            <!-- MR_REPORTS_END -->",
        f"            <!-- MR_REPORTS_START -->\n{final_reports_section}\n            <!-- MR_REPORTS_END -->"
    )
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_html)

def extract_previous_report():
    """Extrae el contenido del reporte más reciente del HTML."""
    filename = "index.html"
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Buscar el primer report-card (el más reciente)
        CARD_START = "<!-- MR_REPORT_CARD_START -->"
        CARD_END = "<!-- MR_REPORT_CARD_END -->"
        
        start_idx = content.find(CARD_START)
        if start_idx == -1:
            return None
        
        end_idx = content.find(CARD_END, start_idx)
        if end_idx == -1:
            return None
        
        # Extraer el bloque completo
        card_block = content[start_idx:end_idx + len(CARD_END)]
        
        # Extraer solo el contenido dentro de <div class="content">
        content_start = card_block.find('<div class="content">')
        if content_start == -1:
            return None
        
        content_end = card_block.rfind('</div>', content_start)
        if content_end == -1:
            return None
        
        # Extraer el contenido HTML puro (sin las etiquetas de contenedor)
        previous_content = card_block[content_start + len('<div class="content">'):content_end].strip()
        
        # También extraer el timestamp para referencia
        timestamp_match = re.search(r'<div class="timestamp">REPORTE GENERADO: ([^<]+)</div>', card_block)
        timestamp = timestamp_match.group(1) if timestamp_match else "Fecha desconocida"
        
        return f"[Timestamp: {timestamp}]\n{previous_content}"
        
    except Exception as e:
        print(f"⚠ Advertencia: No se pudo extraer el reporte anterior: {e}")
        return None

if __name__ == "__main__":
    try:
        # Extraer el reporte del día anterior si existe
        previous_report = extract_previous_report()
        if previous_report:
            print(">>> Reporte anterior encontrado. Se usará como contexto para comparación.")
        else:
            print(">>> No se encontró reporte anterior. Generando primer reporte.")
        
        # Generar nuevo reporte con contexto del anterior
        report = get_gemini_analysis(previous_report=previous_report)
        update_html(report)
        print("SUCCESS: HTML actualizado correctamente.")
    except Exception as e:
        print(f"ERROR FATAL: {e}")