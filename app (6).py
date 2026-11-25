import os
import json
from datetime import date

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="INGENIA AI 2.0", page_icon="📐", layout="wide")

# --------------------------- ESTILO -----------------------------------------
st.markdown("""
<style>
.stApp {background:#f4f7fb}
[data-testid="stSidebar"] {background:#10243a}
[data-testid="stSidebar"] * {color:#fff}
.hero {padding:25px;border-radius:16px;background:linear-gradient(120deg,#10243a,#246b9c);color:white}
.hero h1 {color:white;margin:0}
.hero p {color:#e0edf7;margin-bottom:0}
div[data-testid="stMetric"] {background:white;padding:12px;border-radius:12px;border:1px solid #e3eaf1}
.small-note {font-size:0.85rem;color:#64748b}
</style>
""", unsafe_allow_html=True)

# --------------------------- CONFIGURACIÓN SEGURA ---------------------------
def get_api_key():
    key = os.getenv("OPENAI_API_KEY", "")
    try:
        key = st.secrets.get("OPENAI_API_KEY", key)
    except Exception:
        pass
    return key.strip() if key else ""

@st.cache_resource
def get_openai_client(api_key):
    return OpenAI(api_key=api_key)

MODEL = "gpt-5.5"

SYSTEM_PROMPT = """
Eres INGENIA AI, un asistente técnico en español especializado en Ingeniería Civil,
construcción, arquitectura, gestión de proyectos, AutoCAD y metodología BIM/Revit.

Reglas de trabajo:
1. Responde en español claro, estructurado y profesional.
2. No inventes datos, resultados de laboratorio, dimensiones, precios ni citas normativas.
3. Si faltan datos, enumera qué información necesitas antes de concluir.
4. Expón unidades, fórmulas, supuestos y pasos cuando corresponda.
5. Distingue claramente datos proporcionados, supuestos, cálculos y recomendaciones.
6. Para cálculos estructurales, geotécnicos, hidráulicos y de seguridad, entrega orientación
   preliminar y solicita validación por un profesional habilitado y normativa local vigente.
7. No declares que un diseño es seguro ni que cumple una norma si no hay información suficiente.
8. Para código CAD/BIM, indica versión, dependencias, cómo ejecutarlo y cómo probarlo
   primero en una copia del archivo/modelo.
9. Si el usuario pide un informe, usa títulos, objetivo, datos de entrada, desarrollo,
   resultados, observaciones y pendientes de revisión.
"""

def call_ai(api_key, prompt, history=None):
    client = get_openai_client(api_key)
    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=(history or []) + [{"role": "user", "content": prompt}],
    )
    return response.output_text or "No se recibió una respuesta de la IA."

def show_ai_output(label, text):
    st.markdown(f"### {label}")
    st.markdown(text)
    st.download_button(
        "⬇️ Descargar respuesta (.md)",
        data=text,
        file_name="ingenia_ai_respuesta.md",
        mime="text/markdown",
        key=f"download_{label}_{len(text)}",
    )

# --------------------------- BARRA LATERAL ----------------------------------
with st.sidebar:
    st.markdown("## 📐 INGENIA AI 2.0")
    st.caption("INGENIERÍA · CONSTRUCCIÓN · CAD · BIM")
    st.info("Asistente técnico con IA")
    moneda = st.selectbox("Moneda", ["PEN (S/)", "USD ($)", "EUR (€)"])
    st.markdown("---")
    api_key = get_api_key()
    if api_key:
        st.success("Conexión IA configurada")
    else:
        st.warning("Falta configurar OPENAI_API_KEY")
    st.caption("Modelo: " + MODEL)

# --------------------------- CABECERA ---------------------------------------
st.markdown(
    '<div class="hero"><h1>INGENIA AI 2.0</h1>'
    '<p>Asistente inteligente para proyectos de Ingeniería Civil</p></div>',
    unsafe_allow_html=True,
)
st.write("")
p1, p2 = st.columns(2)
with p1:
    proyecto = st.text_input("Nombre del proyecto", "Mi proyecto de ingeniería")
with p2:
    responsable = st.text_input("Responsable / área", "Oficina técnica")

if not api_key:
    st.warning(
        "La aplicación abre en modo limitado hasta configurar la clave API. "
        "No escribas la clave en el chat ni en el código de GitHub."
    )

# --------------------------- PESTAÑAS ---------------------------------------
inicio, obra, informe, cad, bim, asistente = st.tabs([
    "🏠 Inicio", "🏗️ Gestión de obra", "📄 Informes", "📐 AutoCAD", "🏢 BIM / Revit", "🤖 Asistente IA"
])

with inicio:
    st.subheader("Panel de trabajo")
    a, b, c = st.columns(3)
    a.metric("Módulos", "5")
    b.metric("Proyecto activo", proyecto[:18] or "Sin nombre")
    c.metric("Fecha", date.today().strftime("%d/%m/%Y"))
    st.markdown("### Funciones de INGENIA AI 2.0")
    st.write("- Consultar dudas técnicas con un asistente de IA.")
    st.write("- Preparar borradores de informes técnicos.")
    st.write("- Analizar observaciones de obra y datos de avance.")
    st.write("- Diseñar requerimientos y propuestas de código CAD/BIM.")
    st.info("La IA es una herramienta de apoyo. Verifica cálculos, normativa, diseños y código antes de usarlos en obra.")

with obra:
    st.subheader("Control de avance y costos")
    col1, col2 = st.columns(2)
    with col1:
        programado = st.number_input("Avance programado (%)", 0.0, 100.0, 75.0, 0.5)
        costo_plan = st.number_input("Costo planificado acumulado", min_value=0.0, value=120000.0, step=500.0)
    with col2:
        real = st.number_input("Avance real (%)", 0.0, 100.0, 69.5, 0.5)
        costo_real = st.number_input("Costo real acumulado", min_value=0.0, value=126500.0, step=500.0)
    desviacion = real - programado
    variacion = costo_real - costo_plan
    x, y, z = st.columns(3)
    x.metric("Avance real", f"{real:.1f}%")
    y.metric("Desviación de avance", f"{desviacion:+.2f} pp")
    z.metric("Variación de costo", f"{variacion:,.2f}")
    if desviacion < 0:
        st.warning(f"El avance está {abs(desviacion):.2f} puntos porcentuales por debajo del programa.")
    else:
        st.success("El avance real está igual o por encima del programa.")
    if variacion > 0:
        st.warning("El costo real supera al costo planificado.")
    metricas = {
        "proyecto": proyecto, "avance_programado_pct": programado,
        "avance_real_pct": real, "desviacion_pp": desviacion,
        "costo_planificado": costo_plan, "costo_real": costo_real,
        "variacion_costo": variacion, "moneda": moneda,
    }
    st.download_button(
        "Descargar indicadores JSON",
        json.dumps(metricas, indent=2, ensure_ascii=False),
        file_name="indicadores_obra.json", mime="application/json",
    )
    st.markdown("#### Análisis de obra con IA")
    notas_obra = st.text_area("Observaciones del periodo", key="notas_obra", height=120)
    if st.button("Analizar avance con IA", type="primary", disabled=not bool(api_key)):
        prompt = (
            f"Analiza los siguientes indicadores de control de obra. Proyecto: {proyecto}. "
            f"Responsable: {responsable}. Datos: {json.dumps(metricas, ensure_ascii=False)}. "
            f"Observaciones: {notas_obra}. Explica desviaciones, posibles causas solo como hipótesis, "
            "riesgos, información faltante y acciones de seguimiento. No inventes causas."
        )
        try:
            with st.spinner("INGENIA AI está analizando los datos..."):
                answer = call_ai(api_key, prompt)
            show_ai_output("Análisis técnico de obra", answer)
        except Exception as e:
            st.error(f"No se pudo consultar la IA: {e}")

with informe:
    st.subheader("Generador de informes técnicos con IA")
    tipo = st.selectbox("Tipo de informe", [
        "Visita técnica", "Avance de obra", "Incidencias",
        "Control de calidad", "Memoria descriptiva preliminar"
    ])
    fecha = st.date_input("Fecha", date.today())
    ubicacion = st.text_input("Ubicación / frente de trabajo")
    objetivo = st.text_area("Objetivo del informe")
    observaciones = st.text_area("Antecedentes, observaciones y datos de campo", height=160)
    if st.button("Generar informe con IA", type="primary", disabled=not bool(api_key)):
        if not observaciones.strip():
            st.error("Añade observaciones o datos de campo.")
        else:
            prompt = f"""
            Prepara un BORRADOR editable de {tipo}.
            Proyecto: {proyecto}
            Responsable: {responsable}
            Fecha: {fecha}
            Ubicación: {ubicacion}
            Objetivo: {objetivo}
            Observaciones y datos recibidos: {observaciones}
            Usa secciones: objetivo, alcance, antecedentes, información recibida,
            desarrollo, hallazgos, conclusiones preliminares, recomendaciones y
            pendientes de verificación. No inventes resultados ni normativa.
            """
            try:
                with st.spinner("Redactando el informe..."):
                    answer = call_ai(api_key, prompt)
                st.session_state["informe_ia"] = answer
            except Exception as e:
                st.error(f"No se pudo generar el informe: {e}")
    if st.session_state.get("informe_ia"):
        edited = st.text_area("Revisa y edita el borrador", st.session_state["informe_ia"], height=350)
        show_ai_output("Borrador de informe", edited)

with cad:
    st.subheader("Generador asistido de código AutoCAD")
    formato = st.selectbox("Formato", ["SCR (script de comandos)", "LISP (AutoLISP)", "DXF (archivo de intercambio)"])
    version = st.selectbox("Versión AutoCAD", ["No especificada", "2022", "2023", "2024", "2025", "2026"])
    tarea = st.text_area("Describe qué necesitas automatizar", height=150,
                         placeholder="Ej.: crear capas, dibujar ejes y colocar cotas...")
    if st.button("Generar propuesta CAD con IA", type="primary", disabled=not bool(api_key)):
        if not tarea.strip():
            st.error("Describe la tarea.")
        else:
            prompt = f"""
            Diseña una propuesta para AutoCAD en formato {formato}, versión {version}.
            Proyecto: {proyecto}. Unidades: confirma con el usuario si no están indicadas.
            Requerimiento: {tarea}
            Entrega: explicación, requisitos, código completo si es viable, instrucciones
            de ejecución, supuestos y pruebas. No inventes comandos ni asegures compatibilidad
            sin verificar. Si no hay datos suficientes, pregunta primero.
            """
            try:
                with st.spinner("Generando propuesta CAD..."):
                    answer = call_ai(api_key, prompt)
                st.session_state["cad_ia"] = answer
            except Exception as e:
                st.error(f"No se pudo generar código CAD: {e}")
    if st.session_state.get("cad_ia"):
        show_ai_output("Propuesta AutoCAD", st.session_state["cad_ia"])

with bim:
    st.subheader("Generador asistido de automatización Revit / BIM")
    revit = st.selectbox("Versión Revit", ["No especificada", "2022", "2023", "2024", "2025", "2026"])
    proceso = st.text_area("Describe el proceso BIM que deseas automatizar", height=150)
    if st.button("Generar propuesta BIM con IA", type="primary", disabled=not bool(api_key)):
        if not proceso.strip():
            st.error("Describe el proceso.")
        else:
            prompt = f"""
            Propón una automatización BIM para Revit {revit}, preferentemente pyRevit.
            Proyecto: {proyecto}. Proceso solicitado: {proceso}.
            Explica versión de Python/API cuando se conozca, dependencias, código de ejemplo
            si es posible, instalación, ejecución y pruebas en una copia del modelo.
            Señala incertidumbres y no inventes compatibilidad.
            """
            try:
                with st.spinner("Preparando propuesta BIM..."):
                    answer = call_ai(api_key, prompt)
                st.session_state["bim_ia"] = answer
            except Exception as e:
                st.error(f"No se pudo generar propuesta BIM: {e}")
    if st.session_state.get("bim_ia"):
        show_ai_output("Propuesta BIM / Revit", st.session_state["bim_ia"])

with asistente:
    st.subheader("Asistente técnico INGENIA AI")
    st.caption("Chat técnico con contexto del proyecto durante esta sesión.")
    area = st.selectbox("Área de consulta", [
        "Ingeniería Civil", "Estructuras", "Geotecnia y suelos",
        "Construcción y obra", "Materiales", "Costos y programación",
        "AutoCAD", "Revit / BIM", "Normativa y documentación"
    ])
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    prompt_user = st.chat_input("Escribe tu consulta técnica...")
    if prompt_user:
        if not api_key:
            st.error("La IA aún no está configurada. El administrador debe agregar OPENAI_API_KEY en los secretos de Streamlit.")
        else:
            context = (
                f"Contexto del proyecto: {proyecto}. Responsable/área: {responsable}. "
                f"Área de consulta seleccionada: {area}."
            )
            st.session_state.chat_history.append({"role": "user", "content": prompt_user})
            with st.chat_message("user"):
                st.markdown(prompt_user)
            history_for_api = []
            # Mantiene el contexto reciente, limitado para controlar el uso de tokens.
            for item in st.session_state.chat_history[-12:]:
                history_for_api.append({"role": item["role"], "content": item["content"]})
            try:
                with st.chat_message("assistant"):
                    with st.spinner("Consultando INGENIA AI..."):
                        answer = call_ai(api_key, context + "\n\nConsulta: " + prompt_user, history=history_for_api[:-1])
                    st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error al consultar OpenAI: {e}")
                st.session_state.chat_history.pop()
    if st.button("Limpiar conversación"):
        st.session_state.chat_history = []
        st.rerun()

st.caption("INGENIA AI 2.0 · Asistente de apoyo. Verifica cálculos, normativa, diseños y código con profesionales competentes.")
