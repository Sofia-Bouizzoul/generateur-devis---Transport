import streamlit as st
import onglet1_demande
import onglet2_devis

st.set_page_config(page_title="Générateur de devis", layout="wide")

# ✅ STYLE GLOBAL
st.markdown("""
<style>
.main { background-color: #f4fbf6; }
h1, h2, h3 { color: #0a7d33; }
.stButton>button { background-color: #0a7d33; color: white; }
</style>
""", unsafe_allow_html=True)


# ✅ MENU
menu = st.sidebar.radio(
    "Navigation",
    ["Demande de devis", "Devis transport"]
)

if menu == "Demande de devis":
    onglet1_demande.run()

elif menu == "Devis transport":
    onglet2_devis.run()