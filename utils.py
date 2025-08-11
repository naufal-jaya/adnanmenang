import streamlit as st

def load_css(file_path: str):
    """Load CSS dari file dan terapkan ke Streamlit."""
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def div(content: str, class_name: str = "", id_name: str = ""):
    """Bungkus konten HTML dalam div dengan class dan id opsional."""
    class_attr = f' class="{class_name}"' if class_name else ""
    id_attr = f' id="{id_name}"' if id_name else ""
    return f'<div{class_attr}{id_attr}>{content}</div>'
