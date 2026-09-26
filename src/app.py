import os
import tempfile
import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from gtts import gTTS

# 1. Configuración de la página
st.set_page_config(
    page_title="Lector Portátil",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Cargar el archivo CSS externo desde css/styles.css
def cargar_css(ruta_css):
    if os.path.exists(ruta_css):
        with open(ruta_css, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Cargamos los estilos de la carpeta css
cargar_css("css/styles.css")

# 3. Encabezado en formato Banner Llamativo
st.markdown("""
    <div class="header-banner">
        <div class="titulo-principal">📚 Lector Portátil 📖</div>
        <div class="subtitulo">Toma o sube una foto de libros, etiquetas o productos para escucharlos en voz alta.</div>
    </div>
""", unsafe_allow_html=True)

# 4. Cargar modelo EasyOCR (en caché para evitar sobreconsumo)
@st.cache_resource
def cargar_ocr():
    return easyocr.Reader(['es'], gpu=False)

reader = cargar_ocr()

# 5. Entrada de imagen con diseño destacado
st.markdown("### 📷 Capturar o subir imagen")
archivo_imagen = st.file_uploader("Selecciona una foto o usa la cámara", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if archivo_imagen is not None:
    imagen = Image.open(archivo_imagen)
    imagen.thumbnail((1024, 1024))
    
    st.image(imagen, use_container_width=True)
    
    with st.spinner("⏳ Analizando e interpretando el texto..."):
        img_np = np.array(imagen)
        resultados = reader.readtext(img_np, detail=0)
        texto_extraido = " ".join(resultados).strip()
    
    if texto_extraido:
        st.markdown("### 📄 Texto detectado:")
        st.markdown(f'<div class="caja-texto">{texto_extraido}</div>', unsafe_allow_html=True)
        
        # Generar archivo de audio con gTTS
        tts = gTTS(text=texto_extraido, lang='es')
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.markdown("### 🔊 Escuchar la lectura:")
            st.audio(fp.name)
    else:
        st.warning("⚠️ No se pudo reconocer texto claro en la imagen. Intenta tomar la foto con mejor iluminación.")
