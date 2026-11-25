# INGENIA AI 2.0

Versión web con asistente técnico conectado a OpenAI mediante la Responses API.

## Archivos
- `app.py`: aplicación Streamlit.
- `requirements.txt`: dependencias.

## Configurar en Streamlit Community Cloud
En App settings → Secrets agrega:

```toml
OPENAI_API_KEY = "PEGA_AQUI_TU_CLAVE"
```

No subas la clave a GitHub ni la compartas en chats. La API de OpenAI puede generar cargos según uso y modelo.

## Modelo
La aplicación usa `gpt-5.5` a través del SDK oficial de Python y la Responses API.

## Alcance
El asistente genera respuestas y borradores de apoyo. No sustituye revisión profesional ni certifica diseños, cálculos o cumplimiento normativo.
