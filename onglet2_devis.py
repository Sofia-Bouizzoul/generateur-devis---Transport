import streamlit as st
from utils import create_devis_pdf, extract_pdf_key_data


def run():

    st.title("Devis transport")

    # ===============================
    # SESSION STATE (anti-lag)
    # ===============================
    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = {}
        st.session_state.file_name = None

    # ===============================
    # IMPORT DEMANDE
    # ===============================
    devis_file = st.file_uploader("Importer la demande PDF", type=["pdf"])

    # ✅ Extraction UNE SEULE FOIS
    if devis_file is not None:

        if devis_file.name != st.session_state.file_name:

            with st.spinner("Analyse du PDF..."):
                st.session_state.extracted_data = extract_pdf_key_data(devis_file)
                st.session_state.file_name = devis_file.name

    # ✅ affichage rapide
    if st.session_state.extracted_data:
        st.info("📊 Données extraites du PDF")
        st.table(st.session_state.extracted_data)

    st.divider()

    # ===============================
    # PRIX
    # ===============================
    col1, col2 = st.columns(2)

    with col1:
        prix_transport = st.number_input("Prix transport (€)", min_value=0.0)

    with col2:
        prix_emballage = st.number_input("Prix emballage (€)", min_value=0.0)

    total = prix_transport + prix_emballage
    st.success(f"💰 Total : {total} €")

    st.divider()

    # ===============================
    # EMBALLAGE
    # ===============================
    emballage = st.radio("Emballage obligatoire ?", ["Non", "Oui"])

    type_emballage_devis = ""
    if emballage == "Oui":
        type_emballage_devis = st.selectbox(
            "Type imposé",
            ["Châssis", "Caisse", "Housse thermo soudable"]
        )

    st.divider()

    # ===============================
    # INFOS DEVIS
    # ===============================
    col3, col4 = st.columns(2)

    with col3:
        validite = st.selectbox("Validité", ["7 jours", "15 jours", "30 jours"])

    with col4:
        transit = st.text_input("Transit time")

    conditions = st.text_area("Conditions d'annulation")
    commentaire = st.text_area("Commentaire")

    st.divider()

    # ===============================
    # GENERATION
    # ===============================
    if st.button("✅ Générer devis"):

        if prix_transport == 0 and prix_emballage == 0:
            st.warning("⚠️ Tu dois renseigner au moins un prix")
            return

        extracted = st.session_state.extracted_data

        # ✅ TABLEAU PROPRE (pas de texte brut)
        summary_table = {
            "Incoterm": extracted.get("Incoterm", "N/A"),
            "Adresse": extracted.get("Adresse", "N/A"),
            "Colisage": extracted.get("Colisage", "N/A"),
            "Quantité": extracted.get("Quantité", "N/A"),
            "Transport": extracted.get("Transport", "N/A"),
            "Emballage": type_emballage_devis if emballage == "Oui" else "Non",
            "Prix transport": f"{prix_transport} €",
            "Prix emballage": f"{prix_emballage} €",
            "Total": f"{total} €"
        }

        data = {
            "prix_transport": prix_transport,
            "prix_emballage": prix_emballage,
            "total": total,
            "emballage": emballage,
            "type": type_emballage_devis if emballage == "Oui" else "N/A",
            "validite": validite,
            "transit": transit,
            "conditions": conditions,
            "commentaire": commentaire,
            "tableau": summary_table
        }

        # ✅ PDF propre (PAS de fusion)
        pdf = create_devis_pdf(data)

        st.success("✅ Devis généré proprement")

        st.download_button(
            "📄 Télécharger devis",
            data=pdf,
            file_name="DEVIS_TRANSPORT.pdf",
            mime="application/pdf"
        )
