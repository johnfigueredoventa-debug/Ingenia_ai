import streamlit as st
from datetime import date
import json

st.set_page_config(page_title="INGENIA AI", page_icon="📐", layout="wide")

st.markdown("""
<style>
.stApp {background:#f4f7fb}
[data-testid="stSidebar"] {background:#10243a}
[data-testid="stSidebar"] * {color:#fff}
.hero {padding:24px;border-radius:16px;background:linear-gradient(120deg,#10243a,#246b9c);color:white}
.hero h1 {color:white;margin:0}
.hero p {color:#e0edf7;margin-bottom:0}
div[data-testid="stMetric"] {background:white;padding:12px;border-radius:12px;border:1px solid #e3eaf1}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📐 INGENIA AI")
    st.caption("INGENIERÍA · CONSTRUCCIÓN · CAD · BIM")
    st.info("Plataforma de apoyo técnico")
    moneda = st.selectbox("Moneda", ["PEN (S/)", "USD ($)", "EUR (€)"])

st.markdown('<div class="hero"><h1>INGENIA AI</h1><p>Tu espacio inteligente para proyectos de Ingeniería Civil</p></div>', unsafe_allow_html=True)
st.write("")
proyecto = st.text_input("Nombre del proyecto", "Mi proyecto de ingeniería")
responsable = st.text_input("Responsable / área", "Oficina técnica")

inicio, obra, informe, cad, bim, asistente = st.tabs([
    "🏠 Inicio", "🏗️ Gestión de obra", "📄 Informes", "📐 AutoCAD", "🏢 BIM / Revit", "🤖 Asistente"
])

with inicio:
    st.subheader("Panel de trabajo")
    a,b,c = st.columns(3)
    a.metric("Módulos", "5")
    b.metric("Proyecto activo", proyecto[:18] or "Sin nombre")
    c.metric("Fecha", date.today().strftime("%d/%m/%Y"))
    st.markdown("### ¿Qué puedes hacer?")
    st.write("- Controlar avance físico y costos.")
    st.write("- Preparar borradores de informes técnicos.")
    st.write("- Redactar requerimientos para automatización CAD y BIM.")
    st.write("- Consultar conceptos y procedimientos de ingeniería.")
    st.info("Esta versión inicial funciona en modo web. Las salidas técnicas deben ser revisadas por un profesional.")

with obra:
    st.subheader("Control de avance y costos")
    col1,col2 = st.columns(2)
    with col1:
        programado = st.number_input("Avance programado (%)",0.0,100.0,75.0,0.5)
        costo_plan = st.number_input("Costo planificado acumulado",min_value=0.0,value=120000.0,step=500.0)
    with col2:
        real = st.number_input("Avance real (%)",0.0,100.0,69.5,0.5)
        costo_real = st.number_input("Costo real acumulado",min_value=0.0,value=126500.0,step=500.0)
    desviacion = real-programado
    variacion = costo_real-costo_plan
    x,y,z = st.columns(3)
    x.metric("Avance real",f"{real:.1f}%")
    y.metric("Desviación de avance",f"{desviacion:+.2f} pp")
    z.metric("Variación de costo",f"{variacion:,.2f}")
    if desviacion < 0: st.warning(f"El avance está {abs(desviacion):.2f} puntos porcentuales por debajo del programa.")
    else: st.success("El avance real está igual o por encima del programa.")
    if variacion > 0: st.warning("El costo real supera al costo planificado.")
    st.download_button("Descargar indicadores JSON",json.dumps({
        "proyecto":proyecto,"avance_programado_pct":programado,"avance_real_pct":real,
        "desviacion_pp":desviacion,"costo_planificado":costo_plan,"costo_real":costo_real,
        "variacion_costo":variacion},indent=2,ensure_ascii=False),
        file_name="indicadores_obra.json",mime="application/json")

with informe:
    st.subheader("Generador de borradores de informes")
    tipo = st.selectbox("Tipo de informe",["Visita técnica","Avance de obra","Incidencias","Control de calidad","Memoria descriptiva preliminar"])
    fecha = st.date_input("Fecha",date.today())
    ubicacion = st.text_input("Ubicación / frente de trabajo")
    objetivo = st.text_area("Objetivo")
    observaciones = st.text_area("Antecedentes, observaciones y datos de campo",height=180)
    if st.button("Preparar borrador de informe",type="primary"):
        if not observaciones.strip():
            st.error("Añade observaciones o datos de campo.")
        else:
            st.session_state["informe"] = f"""# {tipo}\n\n**Proyecto:** {proyecto}\n\n**Responsable:** {responsable}\n\n**Fecha:** {fecha}\n\n**Ubicación:** {ubicacion}\n\n## Objetivo\n{objetivo}\n\n## Observaciones y datos recibidos\n{observaciones}\n\n## Pendiente de revisión\n- Verificar datos, unidades y evidencias.\n- Incorporar planos, fotografías y anexos cuando corresponda.\n- Revisión y aprobación del profesional responsable.\n"""
    if "informe" in st.session_state:
        st.text_area("Editar borrador",key="informe_edit",value=st.session_state["informe"],height=300)
        st.download_button("Descargar informe Markdown",st.session_state.get("informe_edit",st.session_state["informe"]),file_name="informe_tecnico.md")

with cad:
    st.subheader("Asistente de requerimientos AutoCAD")
    formato = st.selectbox("Formato",["SCR (script de comandos)","LISP (AutoLISP)","DXF (especificación de dibujo)"])
    version = st.selectbox("Versión AutoCAD",["No especificada","2022","2023","2024","2025","2026"])
    tarea = st.text_area("Describe qué necesitas automatizar",height=160,placeholder="Ej.: crear capas, dibujar ejes y colocar cotas...")
    st.info("En esta versión puedes estructurar y descargar el requerimiento. La ejecución de scripts debe validarse en AutoCAD.")
    if st.button("Generar especificación CAD"):
        if tarea.strip():
            texto=f"PROYECTO: {proyecto}\nFORMATO: {formato}\nVERSIÓN: {version}\nREQUERIMIENTO:\n{tarea}\n\nRevisar unidades, capas, coordenadas y compatibilidad antes de ejecutar."
            st.download_button("Descargar requerimiento TXT",texto,file_name="requerimiento_cad.txt")
        else: st.error("Describe la tarea.")

with bim:
    st.subheader("Asistente de requerimientos Revit / BIM")
    revit = st.selectbox("Versión Revit",["No especificada","2022","2023","2024","2025","2026"])
    proceso = st.text_area("Describe el proceso BIM que deseas automatizar",height=160)
    st.info("Los scripts pyRevit deben comprobarse en una copia del modelo y con la versión correspondiente.")
    if st.button("Preparar especificación BIM"):
        if proceso.strip():
            texto=f"PROYECTO: {proyecto}\nREVIT: {revit}\nPROCESO:\n{proceso}\n\nSolicitar revisión de API, dependencias, unidades y transacciones del modelo."
            st.download_button("Descargar requerimiento BIM",texto,file_name="requerimiento_bim.txt")
        else: st.error("Describe el proceso.")

with asistente:
    st.subheader("Asistente técnico (modo inicial)")
    area = st.selectbox("Área",["Ingeniería Civil","Construcción","Materiales","Costos y programación","AutoCAD","Revit / BIM"])
    pregunta = st.text_area("Escribe tu consulta",height=160)
    st.info("La conexión con un proveedor de IA se habilitará en una siguiente etapa mediante una clave API protegida en los secretos de la aplicación.")
    if st.button("Preparar consulta"):
        if pregunta.strip():
            st.text_area("Consulta estructurada",f"Área: {area}\nProyecto: {proyecto}\nConsulta: {pregunta}\n\nIndicar datos faltantes, unidades y normativa aplicable.",height=180)
        else: st.error("Escribe una consulta.")

st.caption("INGENIA AI · Versión web inicial · Los cálculos y documentos son auxiliares y requieren verificación profesional.")
