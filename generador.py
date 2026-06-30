import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
import io
import zipfile
import re
import logging

# --- CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS PARA RESPONSIVE ---
st.set_page_config(
    page_title="Generador de Contratos", 
    page_icon="🔒",
    layout="centered"  # Ayuda a que no se estire demasiado en pantallas muy grandes
)

# CSS personalizado para mejorar la experiencia en móviles
st.markdown("""
    <style>
    /* Hacer que los botones principales ocupen todo el ancho en móviles */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-size: 1.1em;
    }
    /* Mejorar el espaciado de los uploaders */
    .stFileUploader {
        margin-bottom: 10px;
    }
    /* Ajustar el contenedor de alertas */
    .stAlert {
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN DE SEGURIDAD Y LÍMITES ---
MAX_FILE_SIZE_MB = 10
MAX_ROWS = 500
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Configuración de Logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def sanitize_filename(filename: str) -> str:
    name = re.sub(r'\.docx$', '', filename, flags=re.IGNORECASE)
    safe_name = re.sub(r'[^a-zA-Z0-9_\-\s]', '_', name)
    return f"{safe_name[:50]}.docx"

def validate_excel_structure(df: pd.DataFrame) -> bool:
    required_columns = {'Nombre', 'Apellidos', 'Sueldo'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        st.error(f"❌ El Excel no tiene las columnas requeridas: {missing}")
        return False
    return True

def check_file_size(file) -> bool:
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > MAX_FILE_SIZE_MB * 1024 * 1024:
        return False
    return True

# --- INTERFAZ DE USUARIO ---
st.title("🔒 Generador de Contratos")

# Contenedor para el mensaje de seguridad (Se ve como una tarjeta)
with st.container():
    st.info(f"""
        **Política de Seguridad:**  
        📱 Procesamiento 100% en tu navegador/sesión.  
        🚫 Límite: {MAX_ROWS} filas y {MAX_FILE_SIZE_MB}MB por archivo.
    """)

st.divider() # Línea separadora visual

# Contenedor principal para la entrada de datos
with st.container():
    st.subheader("1. Carga de Archivos")
    
    # En móviles, las columnas se apilan automáticamente. 
    # Usamos gap="small" para que no haya mucho espacio vacío.
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        excel_file = st.file_uploader("📊 Sube el Excel (Datos)", type=['xlsx', 'xls'], help="Debe tener columnas: Nombre, Apellidos, Sueldo")
    
    with col2:
        template_file = st.file_uploader("📄 Sube la Plantilla Word", type=['docx'], help="Archivo .docx con las variables {{ nombre }}, etc.")

    # El botón ocupa todo el ancho gracias al CSS y al parámetro use_container_width
    generate_btn = st.button("🚀 Generar Documentos", use_container_width=True, type="primary")

if generate_btn:
    # Validaciones iniciales
    if not excel_file or not template_file:
        st.warning("⚠️ Por favor sube ambos archivos antes de continuar.")
        st.stop()

    if not check_file_size(excel_file) or not check_file_size(template_file):
        st.error(f"❌ El archivo es demasiado grande. Límite: {MAX_FILE_SIZE_MB}MB.")
        st.stop()

    try:
        # --- PROCESAMIENTO SEGURO EN MEMORIA ---
        
        # 1. Leer y Validar Excel
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        if df.empty:
            st.error("❌ El Excel está vacío.")
            st.stop()
            
        if len(df) > MAX_ROWS:
            st.error(f"❌ Demasiados registros. Máximo permitido: {MAX_ROWS}.")
            st.stop()

        if not validate_excel_structure(df):
            st.stop()

        # 2. Cargar Plantilla
        template_bytes = io.BytesIO(template_file.getvalue())
        tpl = DocxTemplate(template_bytes)
        
        archivos_generados = []
        
        # Contenedor para la barra de progreso (para que no salte por toda la pantalla)
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()

        for index, row in df.iterrows():
            status_text.text(f"Generando contrato {index + 1} de {len(df)}...")
            
            contexto = {
                'nombre': str(row['Nombre']).strip(),
                'apellidos': str(row['Apellidos']).strip(),
                'sueldo': str(row['Sueldo']).strip()
            }
            
            tpl.render(contexto)
            
            buffer = io.BytesIO()
            tpl.save(buffer)
            buffer.seek(0)
            
            safe_filename = sanitize_filename(f"Contrato_{row['Nombre']}_{row['Apellidos']}.docx")
            
            archivos_generados.append({
                'name': safe_filename,
                'data': buffer.getvalue()
            })
            
            progress_bar.progress((index + 1) / len(df))
        
        status_text.text("Comprimiendo archivos finales...")

        # 3. Crear ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for arch in archivos_generados:
                zip_file.writestr(arch['name'], arch['data'])
        
        zip_buffer.seek(0)
        
        # 4. Éxito y Descarga
        st.success(f"✅ ¡Se generaron {len(archivos_generados)} documentos correctamente!")
        
        # Contenedor separado para la descarga para darle importancia visual
        with st.container():
            st.download_button(
                label="📥 Descargar ZIP con todos los contratos",
                data=zip_buffer,
                file_name="contratos_generados.zip",
                mime="application/zip",
                use_container_width=True # Clave para responsive
            )
        
        # Limpieza
        del archivos_generados
        del zip_buffer
        
    except Exception as e:
        logger.error(f"Error crítico: {str(e)}", exc_info=True)
        st.error("❌ Ocurrió un error interno. Revisa los logs o contacta al administrador.")
