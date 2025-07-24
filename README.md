# 🕵️‍♂️ Agente Holmes: Un Analista de Datos Interactivo con IA

Este proyecto es una aplicación web construida con Streamlit y Python que actúa como un "Científico de Datos" automatizado. Permite a cualquier usuario subir un archivo CSV y, en segundos, recibir un análisis exploratorio inicial con gráficos e interpretaciones.

Pero su verdadero poder reside en su **interfaz de chat conversacional**, que permite al usuario "hablar con sus datos", haciendo preguntas complejas en lenguaje natural que el agente traduce a código Python, ejecuta en tiempo real y responde con hallazgos claros y directos.

### 🎥 Demostración en Vivo

<!-- 
    **TAREA CLAVE:** ¡Esta es la parte más importante! Graba un GIF o un video corto (usando herramientas como LICEcap, Giphy Capture, o la grabadora de tu SO) que muestre el flujo completo:
    1. Subir un archivo CSV (como el de Spotify o el de Churn).
    2. Hacer clic en "Generar Análisis Inicial" y mostrar el reporte que se crea.
    3. Bajar a la sección de chat y hacer una pregunta de seguimiento (ej. "¿cuáles son los 3 artistas más escuchados?").
    4. Mostrar cómo el agente genera el código, el resultado y la interpretación.
    Sube el GIF a tu repositorio de GitHub y reemplaza este comentario con: ![Demostración del Agente Holmes](nombre_de_tu_gif.gif)
-->

### El Problema: La Brecha entre los Datos y las Decisiones

Muchas empresas y profesionales tienen acceso a datos valiosos, pero se enfrentan a obstáculos significativos:
*   **Falta de Expertise Técnico:** No todo el mundo sabe usar Python, R, o SQL para analizar datos.
*   **Herramientas Costosas y Complejas:** Soluciones como Tableau o Power BI requieren licencias y una curva de aprendizaje considerable.
*   **Análisis Estáticos:** Los informes tradicionales son una foto fija. Si surge una nueva pregunta, el ciclo de análisis debe empezar de nuevo, causando retrasos.

### La Solución: Un Analista de Datos a tu Disposición 24/7

El Agente Holmes democratiza el análisis de datos. Actúa como un puente inteligente entre el usuario y sus datos, permitiendo un ciclo de preguntas y respuestas rápido e intuitivo.

#### Arquitectura del Agente
El sistema utiliza un enfoque de múltiples agentes de IA orquestados para realizar tareas complejas:
1.  **Agente Planificador:** Al cargar los datos, este agente examina su estructura (`df.info()`, `df.head()`) y diseña un plan de análisis exploratorio inicial, decidiendo qué preguntas son más relevantes y qué gráficos las responderían mejor.
2.  **Agente Intérprete:** Para cada gráfico del análisis inicial, este agente lo "observa" y genera una interpretación en texto, explicando los patrones, insights y posibles siguientes pasos.
3.  **Agente Programador (Conversacional):** Es el corazón del chat. Traduce las preguntas del usuario en lenguaje natural a código Pandas ejecutable, garantizando que las respuestas estén ancladas a los datos reales.
4.  **Agente Ejecutor de Código:** Un entorno seguro que ejecuta el código generado por la IA y captura los resultados (ya sea texto o visualizaciones) para presentarlos al usuario.

### ✨ Características Principales

*   **Análisis Automático:** Genera un reporte inicial con visualizaciones e insights sin necesidad de configuración.
*   **Chat Interactivo:** Permite un diálogo fluido para profundizar en los datos.
*   **Generación de Código Transparente:** Muestra el código Python que ejecuta para cada pregunta, ofreciendo total transparencia y oportunidades de aprendizaje.
*   **Soporte para Gráficos en el Chat:** El agente puede generar y mostrar visualizaciones complejas directamente en la conversación.
*   **Análisis Universal:** No está sesgado hacia ningún tipo de dato. Funciona igual de bien con datos financieros, de marketing, científicos o de uso de aplicaciones.
*   **Control del Usuario:** Permite regenerar el análisis inicial con un nuevo enfoque si los primeros resultados no son los deseados.

### 🛠️ Pila Tecnológica

*   **Lenguaje:** Python
*   **Interfaz:** Streamlit
*   **Análisis de Datos:** Pandas
*   **Visualización:** Matplotlib, Seaborn
*   **Inteligencia Artificial:** Google Generative AI (Gemini)
*   **Ejecución Paralela:** ThreadPoolExecutor para un rendimiento óptimo.

### 🚀 Cómo Ejecutarlo Localmente

Sigue estos pasos para poner en marcha al Agente Holmes en tu propia máquina.

**Prerrequisitos:**
*   Python 3.8+
*   Una clave de API de Google AI Studio.

**Instalación:**
1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/nombre-del-repositorio.git
    cd nombre-del-repositorio
    ```
2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Instala las dependencias:**
    <!-- **TAREA CLAVE:** Ejecuta este comando en tu terminal para crear el archivo requirements.txt -->
    ```bash
    pip freeze > requirements.txt
    ```
    Luego, instala las librerías:
    ```bash
    pip install -r requirements.txt
    ```

**Ejecución:**
1.  **Ejecuta la aplicación de Streamlit:**
    ```bash
    streamlit run app_holmes.py
    ```
2.  **Abre tu navegador:** Ve a la dirección `http://localhost:8501`.
3.  **Configura la API Key:** Ingresa tu clave de API de Google AI en la barra lateral.
4.  **Sube un archivo CSV y comienza a investigar!**

### 💡 Posibles Mejoras a Futuro

*   **Conexión a Bases de Datos:** Permitir que el agente se conecte directamente a bases de datos SQL.
*   **Exportación de Reportes:** Añadir un botón para descargar el análisis completo (gráficos y texto) como un archivo PDF o HTML.
*   **Soporte para Múltiples Archivos:** Capacidad para analizar y unir varios archivos CSV a la vez.
*   **Manejo de Archivos Más Grandes:** Integración con librerías como Dask o Polars para analizar datasets que no caben en memoria RAM.

---