import streamlit as st
from datetime import datetime
from utils import create_pdf, merge_pdfs


def run():

    st.title("Demande de Devis Transport")

    st.image(
        "https://cdn-s-www.estrepublicain.fr/images/1511D78B-A59C-471A-AC00-2D25AFDC7D0C/NW_raw/acheminement-d-un-alternateur-de-500-t-a-travers-belfort-photo-xavier-gorau-1351254698.jpg",
        use_container_width=True
    )

    st.divider()

    # ===============================
    # PRODUIT
    # ===============================
    produit_option = st.selectbox("Produit *", ["Stator", "Rotor", "Générateur", "Autre"])

    produit_custom = ""
    if produit_option == "Autre":
        produit_custom = st.text_input("Préciser le produit *")

    # ===============================
    # EMBALLAGE
    # ===============================
    emballage_choix = st.radio("Emballage souhaité *", ["Non", "Oui"])

    type_emballage = ""
    if emballage_choix == "Oui":
        type_emballage = st.selectbox(
            "Type d'emballage *",
            ["Châssis", "Caisse", "Housse thermo soudable"]
        )

    # ===============================
    # FORMULAIRE
    # ===============================
    with st.form("form"):

        commande = st.text_input("Commande *")
        client = st.text_input("Client *")
        adresse = st.text_input("Adresse *")
        code_postal = st.text_input("Code postal *")
        pays = st.text_input("Pays *")

        quantite = st.number_input("Quantité *", min_value=1)

        date_expedition = st.date_input("Date expédition")

        incoterm = st.selectbox("Incoterm *", [
"EXW",   # Ex Works
        "FCA",   # Free Carrier
        "FAS",   # Free Alongside Ship
        "FOB",   # Free On Board
        "CFR",   # Cost and Freight
        "CIF",   # Cost Insurance Freight
        "CPT",   # Carriage Paid To
        "CIP",   # Carriage Insurance Paid
        "DAP",   # Delivered At Place
        "DPU",   # Delivered at Place Unloaded (remplace DAT)
        "DDP"    # Delivered Duty Paid 
        ])


        transport_type = st.selectbox("Transport *", ["Route", "Air", "Mer"])
        service = st.selectbox("Service *", ["Basique", "Premium"])

        separe = st.radio("Machines séparées ?", ["Non", "Oui"])

        contraintes = st.text_area("Contraintes")
        contact = st.text_input("Contact")

        longueur = st.number_input("Longueur", value=100)
        largeur = st.number_input("Largeur", value=100)
        hauteur = st.number_input("Hauteur", value=100)
        poids = st.number_input("Poids", value=1000)

        uploaded_file = st.file_uploader("PDF technique", type=["pdf"])

        submitted = st.form_submit_button("Générer")

    # ===============================
    # GENERATION PDF
    # ===============================
    if submitted:

        if not commande or not client or not adresse or not code_postal or not pays:
            st.error("Champs obligatoires manquants")

        else:

            produit_final = produit_option if produit_option != "Autre" else produit_custom

            data = {
                "commande": commande,
                "date": datetime.today().strftime("%d/%m/%Y"),
                "client": client,
                "adresse": adresse,
                "code_postal": code_postal,
                "pays": pays,
                "produit": produit_final,
                "quantite": quantite,
                "date_expedition": date_expedition.strftime("%d/%m/%Y"),
                "incoterm": incoterm,
                "transport_type": transport_type,
                "service": service,
                "separe": separe,
                "contraintes": contraintes,
                "contact": contact,
                "emballage": emballage_choix,
                "type_emballage": type_emballage,
                "longueur": longueur,
                "largeur": largeur,
                "hauteur": hauteur,
                "poids": poids
            }

            pdf = create_pdf(data)
            final_pdf = merge_pdfs(pdf, uploaded_file)

            filename = f"DEMANDE_{commande}_{pays.replace(' ', '_')}.pdf"

            st.success("PDF généré ✅")
            st.download_button("Télécharger", final_pdf, filename)