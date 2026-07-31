import streamlit as st
import easyocr
from gtts import gTTS
import os
import tempfile
from PIL import Image
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Lector Portátil", page_icon="🔍", layout="centered")

st.title("🔍 Lector Portátil")
st.write("Toma o sube una foto de un texto para escucharlo en voz alta.")

# Cargar el modelo de EasyOCR (se guarda en caché para optimizar memoria)
@st.cache_resource
def cargar_ocr():
    return easyocr.Reader(['es'], gpu=False)

reader = cargar_ocr()

# Subir imagen
archivo_imagen = st.file_uploader("Selecciona una imagen o usa tu cámara", type=["jpg", "jpeg", "png"])

if archivo_imagen is not None:
    imagen = Image.open(archivo_imagen)
    
    # Optimización de memoria: Redimensionar si la imagen es gigante
    imagen.thumbnail((1024, 1024))
    
    st.image(imagen, use_container_width=True)
    
    with st.spinner("Leyendo texto..."):
        # Convertir a array NumPy
        img_np = np.array(imagen)
        
        # Extraer texto
        resultados = reader.readtext(img_np, detail=0)
        texto_extraido = " ".join(resultados).strip()
    
    if texto_extraido:
        st.success("¡Texto detectado con éxito!")
        st.subheader("Texto extraído:")
        st.write(texto_extraido)
        
        # Generar audio con archivo temporal seguro
        tts = gTTS(text=texto_extraido, lang='es')
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.subheader("🔊 Escuchar lectura:")
            st.audio(fp.name)
    else:
        st.warning("No se pudo detectar texto en la imagen. Intenta tomar la foto con más claridad.")
