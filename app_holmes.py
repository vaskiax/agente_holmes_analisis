# app_holmes.py (Versión 6.7: El Analista Resiliente y Definitivo)

import streamlit as st
import pandas as pd
import google.generativeai as genai
from io import StringIO
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
from concurrent.futures import ThreadPoolExecutor

# --- Configuración de la Página ---
st.set_page_config(page_title="Agente Holmes v6.7", layout="wide", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Agente Holmes v6.7: El Analista Interactivo")
st.markdown("Sube un archivo CSV para recibir un análisis inicial y luego chatea con el Agente Holmes para profundizar en tus datos.")

# --- Funciones de los Agentes ---
def llamar_al_planificador_ia(api_key, df_info, df_head, prompt_adicional=""):
    try:
        genai.configure(api_key=api_key); prompt = f"""
        Eres un analista de datos experto. Tu misión es proponer un plan de análisis exploratorio (EDA) relevante.
        **Información del Dataset:**\n{df_info}\n\n**Primeras Filas:**\n{df_head}\n\n{prompt_adicional}
        **Tu Tarea:**
        Genera un plan de análisis con 3 a 4 pasos. Define una pregunta clara y el tipo de gráfico.
        Tipos de gráficos: 'countplot', 'histplot', 'boxplot', 'scatterplot'.
        **Formato de Salida Obligatorio (JSON):**
        Responde con un JSON con una clave "plan". Cada objeto debe tener:
        "pregunta_negocio", "tipo_grafico", "columnas" (lista de 1 o 2), y "hue" (Opcional).
        """; model = genai.GenerativeModel('gemini-1.5-flash'); response = model.generate_content(prompt)
        raw_text = response.text; json_match = re.search(r'```json\s*([\s\S]*?)\s*```', raw_text)
        json_str = json_match.group(1) if json_match else raw_text; return json.loads(json_str)
    except Exception as e: st.error(f"Error en el Agente Planificador: {e}"); return None

def llamar_al_interprete_ia(api_key, pregunta, tipo_grafico, columnas, hue):
    try:
        genai.configure(api_key=api_key)
        descripcion_grafico = f"Se ha generado un gráfico de tipo '{tipo_grafico}' que muestra '{', '.join(columnas)}'."
        if hue: descripcion_grafico += f" segmentado por '{hue}'."
        prompt = f"""
        Eres un analista de datos experto. Acabas de generar un gráfico para responder a: "{pregunta}"
        Descripción del Gráfico: {descripcion_grafico}. Tu Tarea: Proporciona un análisis en tres partes (Markdown):
        1.  **Observación:** Describe objetivamente qué muestra el gráfico.
        2.  **Insight:** ¿Qué significa esta observación en el contexto de los datos?
        3.  **Posible Siguiente Paso:** ¿Qué otra pregunta podría investigarse?
        """; model = genai.GenerativeModel('gemini-1.5-flash'); response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Error en el Agente Intérprete: {e}"

def llamar_al_agente_programador(api_key, df_info, df_head, chat_history, user_question):
    try:
        genai.configure(api_key=api_key)
        historial_str = "\n".join([f"  - {msg['role']}: {msg['content']}" for msg in chat_history])
        prompt = f"""
        Eres Agente Holmes, un asistente de análisis de datos que escribe código Python (Pandas) sobre un DataFrame `df`.
        **REGLA MÁS IMPORTANTE:** Un DataFrame `df` ya existe. **NUNCA crees un DataFrame de ejemplo.**
        **CONTEXTO DEL `df` REAL:**\n{df_info}\n**PRIMERAS FILAS DEL `df` REAL:**\n```{df_head}```
        **NUEVA PREGUNTA:** "{user_question}"
        **TAREA EN DOS PASOS:**
        1. CÓDIGO A EJECUTAR: Basado en el contexto, escribe código Python que calcule la respuesta. Usa `print()`.
        2. HALLAZGOGS CLAVE: Después del bloque de código, escribe "#### Hallazgos Clave:". Presenta una respuesta directa, citando los resultados numéricos de tu código.
        """; model = genai.GenerativeModel('gemini-1.5-flash'); response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Error al procesar la pregunta: {e}"

def ejecutar_codigo_de_ia(codigo, df_disponible):
    codigo_limpio = codigo.strip()
    if "plt.show()" in codigo_limpio or "sns." in codigo_limpio:
        try:
            fig, ax = plt.subplots(); exec(codigo_limpio, {'df': df_disponible, 'pd': pd, 'plt': plt, 'sns': sns, 'fig': fig, 'ax': ax})
            return fig
        except Exception as e: return f"Error al generar el gráfico: {e}"
    else:
        buffer = StringIO()
        try:
            from contextlib import redirect_stdout
            with redirect_stdout(buffer): exec(codigo_limpio, {'df': df_disponible, 'pd': pd})
            return buffer.getvalue()
        except Exception as e: return f"Error al ejecutar el código: {e}"

def ejecutar_plan_de_analisis(df, plan, interpretaciones):
    st.header("Análisis Inicial del Agente Holmes", divider="rainbow")
    for i, paso in enumerate(plan['plan']):
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.subheader(f"Pista #{i+1}: {paso['pregunta_negocio']}", divider="gray")
            try:
                # --- PRE-PROCESAMIENTO DE SEGURIDAD Y RESILIENCIA (v6.7) ---
                df_grafico = df.copy()
                columnas = paso['columnas']; hue = paso.get('hue')
                cols_to_process = columnas + ([hue] if hue and hue not in columnas else [])
                cols_a_revisar = []
                for item in cols_to_process:
                    if isinstance(item, list): cols_a_revisar.extend(item)
                    elif item: cols_a_revisar.append(item)
                for col_nombre in cols_a_revisar:
                    if col_nombre in df_grafico.columns:
                        if df_grafico[col_nombre].dtype == 'bool': df_grafico[col_nombre] = df_grafico[col_nombre].astype(str)
                        elif df_grafico[col_nombre].dtype == 'object': df_grafico[col_nombre] = df_grafico[col_nombre].astype(str)
                # --- FIN DEL PRE-PROCESAMIENTO ---
                
                fig, ax = plt.subplots(); sns.set_theme(style="whitegrid"); tipo_grafico = paso['tipo_grafico']
                if tipo_grafico == 'countplot': sns.countplot(x=columnas[0], hue=hue, data=df_grafico, ax=ax, palette="viridis")
                elif tipo_grafico == 'histplot': sns.histplot(x=columnas[0], hue=hue, data=df_grafico, ax=ax, kde=True, palette="mako")
                elif tipo_grafico == 'boxplot':
                    x_axis = columnas[0] if len(columnas) > 1 else None; y_axis = columnas[1] if len(columnas) > 1 else columnas[0]
                    sns.boxplot(x=x_axis, y=y_axis, hue=hue, data=df_grafico, ax=ax, palette="flare")
                elif tipo_grafico == 'scatterplot': sns.scatterplot(x=columnas[0], y=columnas[1], hue=hue, data=df_grafico, ax=ax, alpha=0.7, palette="crest")
                ax.set_title(paso['pregunta_negocio']); plt.tight_layout(); st.pyplot(fig)
            except Exception as e: st.error(f"Error al crear el gráfico: {e}")
        with col2:
            st.markdown("#### Análisis del Agente Holmes")
            if interpretaciones: st.markdown(interpretaciones[i])

def orquestar_analisis_completo(_df, api_key, prompt_adicional=""):
    info_buffer = StringIO(); _df.info(buf=info_buffer); df_info_str = info_buffer.getvalue()
    plan = llamar_al_planificador_ia(api_key, df_info_str, _df.head().to_string(), prompt_adicional)
    if not plan or 'plan' not in plan: return None, None
    interpretaciones = [None] * len(plan['plan'])
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_index = {executor.submit(llamar_al_interprete_ia, api_key, paso['pregunta_negocio'], paso['tipo_grafico'], paso['columnas'], paso.get('hue')): i for i, paso in enumerate(plan['plan'])}
        for future in future_to_index:
            index = future_to_index[future]
            try: interpretaciones[index] = future.result()
            except Exception as exc: interpretaciones[index] = f"Error al generar esta interpretación: {exc}"
    return plan, interpretaciones

# --- Interfaz Principal de la App ---
st.sidebar.header("Configuración")
api_key_input = st.sidebar.text_input("Ingresa tu clave de API de Google AI", type="password", key="api_key_main")
uploaded_file = st.file_uploader("1. Sube un archivo CSV", type="csv")

if 'df' not in st.session_state: st.session_state.df = None
if 'reporte_generado' not in st.session_state: st.session_state.reporte_generado = False
if 'messages' not in st.session_state: st.session_state.messages = []

if uploaded_file is not None:
    current_df = pd.read_csv(uploaded_file)
    if st.session_state.df is None or not st.session_state.df.equals(current_df):
        st.session_state.df = current_df; st.session_state.reporte_generado = False
        st.session_state.messages = []; st.rerun()

if st.session_state.df is not None:
    df = st.session_state.df
    st.header("Vista Preliminar de la Evidencia", divider="rainbow"); st.dataframe(df.head())
    
    col1_btn, col2_btn, col3_btn = st.columns([2,2,3])
    with col1_btn:
        if st.button("🕵️‍♂️ Generar Análisis Inicial", use_container_width=True):
            if api_key_input:
                with st.spinner("El Agente Holmes está dirigiendo una investigación completa..."):
                    plan, interpretaciones = orquestar_analisis_completo(df, api_key_input)
                    st.session_state.plan = plan; st.session_state.interpretaciones = interpretaciones
                    st.session_state.reporte_generado = True; st.rerun()
            else: st.error("Se requiere una clave de API de Google AI.")
    with col2_btn:
        if st.button("🔄 Regenerar Análisis", use_container_width=True):
            if api_key_input:
                enfoque = st.session_state.get("enfoque_usuario", "")
                with st.spinner("El Agente está replanificando la investigación..."):
                    prompt_adicional = f"\nINSTRUCCIÓN ADICIONAL: {enfoque}" if enfoque else ""
                    plan, interpretaciones = orquestar_analisis_completo(df, api_key_input, prompt_adicional)
                    st.session_state.plan = plan; st.session_state.interpretaciones = interpretaciones
                    st.session_state.reporte_generado = True; st.rerun()
            else: st.error("Se requiere una clave de API para regenerar.")
    with col3_btn:
        st.text_input("Opcional: Describe un enfoque para la regeneración", key="enfoque_usuario", placeholder="Ej: enfócate en la duración de las canciones")

    if st.session_state.reporte_generado:
        ejecutar_plan_de_analisis(df, st.session_state.plan, st.session_state.interpretaciones)
        st.header("Chatea con tus Datos", divider="rainbow")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if isinstance(message["content"], plt.Figure): st.pyplot(message["content"])
                else: st.markdown(message["content"])
        if prompt := st.chat_input("¿Qué más te gustaría investigar?"):
            if api_key_input:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"): st.markdown(prompt)
                with st.chat_message("assistant"):
                    with st.spinner("Holmes está analizando y programando..."):
                        df_info_buffer = StringIO(); df.info(buf=df_info_buffer); df_info_str = df_info_buffer.getvalue()
                        respuesta_completa = llamar_al_agente_programador(api_key_input, df_info_str, df.head().to_string(), st.session_state.messages, prompt)
                        codigo_match = re.search(r'```python\s*([\s\S]*?)\s*```', respuesta_completa)
                        if codigo_match:
                            codigo_ia = codigo_match.group(1).strip()
                            bloque_codigo_completo = codigo_match.group(0)
                            explicacion_ia = respuesta_completa.replace(bloque_codigo_completo, '').strip()
                            with st.expander("Ver el código que ejecutó el Agente"): st.code(codigo_ia, language='python')
                            resultado_ejecucion = ejecutar_codigo_de_ia(codigo_ia, df)
                            if isinstance(resultado_ejecucion, plt.Figure):
                                st.markdown("#### Gráfico Generado:"); st.pyplot(resultado_ejecucion)
                                st.markdown(explicacion_ia); st.session_state.messages.append({"role": "assistant", "content": resultado_ejecucion})
                                st.session_state.messages.append({"role": "assistant", "content": explicacion_ia})
                            elif isinstance(resultado_ejecucion, str):
                                st.markdown("#### Resultado del Cálculo:"); st.text(resultado_ejecucion)
                                st.markdown(explicacion_ia)
                                respuesta_final_para_historial = f"**Resultado:**\n```\n{resultado_ejecucion}\n```\n{explicacion_ia}"
                                st.session_state.messages.append({"role": "assistant", "content": respuesta_final_para_historial})
                        else:
                            st.markdown(respuesta_completa)
                            st.session_state.messages.append({"role": "assistant", "content": respuesta_completa})
            else: st.warning("Ingresa tu API key para chatear.")