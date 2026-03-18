import streamlit as st
import pytesseract
from PIL import Image
from deep_translator import GoogleTranslator
import datetime, cv2, numpy as np, pandas as pd, os

st.set_page_config(page_title="Ancient Text", page_icon="📜", layout="wide")

# Tesseract path
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------- CSS ----------
st.markdown("""
<style>
h1,h2,h3,h4,h5,h6,p,li,.stMarkdown{color:#2C3E50!important}

.hero{font-size:70px;font-weight:900;text-align:center;
background:linear-gradient(90deg,#008080,#C2B280,#20B2AA,#F4A460);
-webkit-background-clip:text;-webkit-text-fill-color:transparent}

.subtitle{text-align:center;font-size:22px;margin-bottom:40px;
background:rgba(255,255,255,.7);padding:10px 20px;border-radius:30px;
border:1px solid #C2B280}

.card{background:rgba(255,250,240,.95);padding:25px;border-radius:18px;
border:1px solid #C2B280;box-shadow:0 8px 32px rgba(0,128,128,.15);
transition:.3s;margin:10px 0}

.card:hover{transform:translateY(-5px);
box-shadow:0 12px 40px rgba(0,128,128,.25);border-color:#008080}

.card h3{color:#008080!important;border-bottom:2px solid #C2B280;padding-bottom:8px}

.result{background:rgba(255,250,240,.95);padding:20px;border-radius:12px;
border-left:4px solid #008080;font-family:monospace;white-space:pre-wrap}

[data-testid="stSidebar"]{background:linear-gradient(135deg,#008080,#20B2AA);color:white}

.stButton>button{background:linear-gradient(90deg,#008080,#20B2AA);
color:white;font-weight:700;border-radius:10px;padding:10px 25px}

.stDownloadButton>button{background:linear-gradient(90deg,#C2B280,#F4A460);
color:#2C3E50;font-weight:700;border-radius:10px}

</style>
""",unsafe_allow_html=True)

# ---------- FUNCTIONS ----------

def set_page_background(home=False):
    bg = """
    .stApp{background:linear-gradient(rgba(255,250,240,.1),rgba(255,250,240,.1)),
    url("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f");
    background-size:cover;background-attachment:fixed}
    """ if home else """
    .stApp{background:linear-gradient(135deg,#E6E6FA,#FDF5E6,#E0F2F1)}
    """
    st.markdown(f"<style>{bg}</style>",unsafe_allow_html=True)

def enhance_image(image):
    if image.mode!="RGB": image=image.convert("RGB")
    img=np.array(image)
    gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    enhanced=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY,11,2)
    return cv2.fastNlMeansDenoising(enhanced,None,10,7,21)

def verify_tesseract():
    path=pytesseract.pytesseract.tesseract_cmd
    return os.path.exists(path),f"Tesseract found at: {path}" if os.path.exists(path) else f"Tesseract not found at: {path}"

def card(title,text,items):
    li="".join([f"<li>{i}</li>" for i in items])
    return f"""
    <div class="card">
    <h3>{title}</h3>
    <p>{text}</p>
    <ul>{li}</ul>
    </div>
    """

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("# 📜 Ancient Text")
    page=st.radio("Navigation",["🏠 Home","🔍 Analyzer","ℹ️ About"],label_visibility="collapsed")

# ---------- HOME ----------
if page=="🏠 Home":
    set_page_background(True)

    st.markdown('<div class="hero">Ancient Text Interpreter</div>',unsafe_allow_html=True)
    st.markdown('<div class="subtitle">🔮 Deciphering the Voices of Ancient Civilizations</div>',unsafe_allow_html=True)

    col1,col2,col3=st.columns(3)

    with col1:
        st.markdown(card("🔍 OCR EXTRACTION",
        "Reading faded historical documents.",
        ["Hieroglyph detection","Cuneiform recognition","Damaged text recovery"]),
        unsafe_allow_html=True)

    with col2:
        st.markdown(card("🌍 TRANSLATION",
        "Translate ancient text to modern English.",
        ["Multi-language support","Auto detection","English translation"]),
        unsafe_allow_html=True)

    with col3:
        st.markdown(card("📜 PRESERVATION",
        "Digitally preserve ancient writings.",
        ["Image enhancement","Text recovery","Digital archiving"]),
        unsafe_allow_html=True)

# ---------- ANALYZER ----------
elif page=="🔍 Analyzer":
    set_page_background()

    st.title("🔎 Ancient Text → English Translator")
    ok,msg=verify_tesseract()

    if not ok:
        st.error(msg); st.stop()
    else:
        st.success(msg)

    uploaded=st.file_uploader("Upload ancient text image",
                              type=["png","jpg","jpeg","bmp","tiff"])

    if uploaded:
        image=Image.open(uploaded)
        col1,col2=st.columns(2)

        with col1: st.image(image,"Original Image")
        enhanced=enhance_image(image)
        with col2: st.image(enhanced,"Enhanced Image",clamp=True)

        with st.spinner("Extracting text..."):
            try: extracted=pytesseract.image_to_string(enhanced)
            except Exception as e: extracted=f"OCR Error: {e}"

        st.subheader("Extracted Text")
        if extracted.strip():
            st.markdown(f'<div class="result">{extracted}</div>',unsafe_allow_html=True)

            with st.spinner("Translating..."):
                translated=GoogleTranslator(source='auto',target='en').translate(extracted)

            st.subheader("English Translation")
            st.markdown(f'<div class="result">{translated}</div>',unsafe_allow_html=True)

            report=f"""
ANCIENT TEXT TRANSLATION REPORT
Date: {datetime.datetime.now()}

EXTRACTED TEXT:
{extracted}

ENGLISH TRANSLATION:
{translated}
"""

            st.download_button("📥 Download Report",report,
                               file_name=f"translation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

        else:
            st.warning("No text detected.")

# ---------- ABOUT ----------
elif page == "ℹ️ About":
    set_page_background("About")
    
    st.title("📚 About Ancient Text")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
        <h3>🎯 Our Mission</h3>
        <p>Ancient Text utilizes advanced technology to accurately read and translate historical writings into clear, modern language. It enables users to better understand and explore ancient texts with ease. Our objective is to preserve cultural heritage and make historical knowledge accessible to a wider audience.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
        <h3>🔧 Technology Stack</h3>
        <table>
        <tr><th>Component</th><th>Technology</th></tr>
        <tr><td>Frontend</td><td>Streamlit</td></tr>
        <tr><td>OCR Engine</td><td>Pytesseract</td></tr>
        <tr><td>Translation</td><td>Deep-Translator API</td></tr>
        <tr><td>Image Processing</td><td>OpenCV & PIL</td></tr>
        <tr><td>Data Processing</td><td>Pandas, NumPy</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
   
