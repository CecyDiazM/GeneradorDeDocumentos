import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(page_title="Convertidor CSV a Excel", page_icon="📊")

st.title("📊 Convertidor de CSV a Excel")
st.markdown("""
Sube tu archivo **.csv** y lo convertiremos a **.xlsx** al instante. 
Ideal para abrir tus datos en Excel sin problemas de formato.
""")


# Selector de archivos
archivo_subido = st.file_uploader("Elige un archivo CSV", type=['csv'])

if archivo_subido is not None:
    try:
        # Leer el CSV cargado
        # Nota: Puedes ajustar el 'sep' si tus CSV usan punto y coma (sep=';')
        df = pd.read_csv(archivo_subido)
        
        # Mostrar una vista previa de los datos
        st.subheader("Vista previa de los datos")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Crear un buffer en memoria para el archivo Excel
        buffer = io.BytesIO()
        
        # Botón para procesar y descargar
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Datos')
            # El context manager guarda automáticamente el archivo en el buffer
            
        # Nombre del archivo de salida
        nombre_salida = archivo_subido.name.replace('.csv', '.xlsx')
        
        st.success(f"✅ ¡Archivo '{archivo_subido.name}' procesado con éxito!")
        
        # Botón de descarga
        st.download_button(
            label="⬇️ Descargar Excel",
            data=buffer.getvalue(),
            file_name=nombre_salida,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Hubo un error al procesar el archivo: {e}")

else:
    st.info("Esperando a que subas un archivo...")

st.caption("Hecho con ❤️ usando Streamlit y Pandas")
