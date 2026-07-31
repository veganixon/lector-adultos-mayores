import os
import streamlit as st
import pytesseract
from PIL import Image
from gtts import gTTS

# Configuración principal de la página (Adaptable a móviles)
st.set_page_config(
    page_title="Lector para Adultos Mayores",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos visuales personalizados (Diseño bonito y moderno)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    h1 {
        color: #1f2937;
        text-align: center;
        font-size: 1.8rem !important;
    }
    p {
        color: #4b5563;
        text-align: center;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado limpio
st.title("🔍 Lector Portátil")
st.markdown("<p>Toma o sube una foto de un texto para escucharlo en voz alta.</p>", unsafe_allow_html=True)

st.markdown("---")

# Directorio temporal para audios
TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# Componente de carga optimizado para móviles (este permite abrir cámara o galería)
archivo_imagen = st.file_uploader(
    "📷 Selecciona una imagen o usa tu cámara", 
    type=["jpg", "jpeg", "png"],
    help="Puedes subir fotos de facturas, recetas médicas o etiquetas."
)

if archivo_imagen is not None:
    # Contenedor centrado para la imagen
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        imagen = Image.open(archivo_imagen)
        st.image(imagen, caption="Imagen cargada correctamente", use_container_width=True)
    
    st.markdown("---")
    
    with st.spinner("⏳ Analizando texto, por favor espera..."):
        try:
            # Extracción OCR en español
            texto = pytesseract.image_to_string(imagen, lang='spa')
            
            if texto.strip():
                st.success("¡Texto detectado con éxito!")
                
                # Caja de texto limpia y legible
                st.text_area("Texto extraído:", texto, height=160)
                
                # Generación de voz
                tts = gTTS(text=texto, lang='es')
                audio_path = os.path.join(TEMP_DIR, "audio.mp3")
                tts.save(audio_path)
                
                # Reproductor de audio adaptado
                st.markdown("### 🔊 Escuchar lectura:")
                st.audio(audio_path, format="audio/mp3")
            else:
                st.warning("⚠️ No se encontró texto legible. Intenta tomar la foto con mejor luz y enfoque.")
                
        except Exception as e:
            st.error(f"Ocurrió un error al procesar la imagen: {e}")