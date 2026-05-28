from io import BytesIO
from PyPDF2 import PdfMerger
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfMerger, PdfReader


# ===============================
# FUSION PDF
# ===============================
def merge_pdfs(main_pdf, uploaded_pdf):
    merger = PdfMerger()

    if main_pdf:
        main_pdf.seek(0)
        merger.append(main_pdf)

    if uploaded_pdf:
        try:
            merger.append(uploaded_pdf)
        except:
            pass

    output = BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)

    return output


# ===============================
# PDF DEMANDE
# ===============================
def create_pdf(data):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(
        Paragraph("<b><font color='#0a7d33'>DEMANDE DE DEVIS TRANSPORT</font></b>", styles['Title'])
    )
    elements.append(Spacer(1, 12))

    def section(title, rows):
        elements.append(Spacer(1, 8))
        elements.append(Paragraph(f"<b>{title}</b>", styles['Heading3']))
        elements.append(Spacer(1, 4))

        table = Table(rows, colWidths=[180, 290])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0a7d33")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))

        elements.append(table)

    section("Informations générales", [
        ["Commande", data['commande']],
        ["Client", data['client']],
        ["Date", data['date']]
    ])

    section("Destination", [
        ["Adresse", data['adresse']],
        ["Code postal", data['code_postal']],
        ["Pays", data['pays']]
    ])

    section("Transport", [
        ["Incoterm", data['incoterm']],
        ["Transport", data['transport_type']],
        ["Service", data['service']],
        ["Machines séparées", data['separe']]
    ])

    section("Produit", [
        ["Produit", data['produit']],
        ["Quantité", data['quantite']],
        ["Date expédition", data['date_expedition']]
    ])

    section("Emballage", [
        ["Emballage", data['emballage']],
        ["Type", data['type_emballage'] if data['emballage']=="Oui" else "N/A"]
    ])

    section("Colisage", [
        ["Dimensions", f"{data['longueur']} x {data['largeur']} x {data['hauteur']} cm"],
        ["Poids", f"{data['poids']} kg"]
    ])

    doc.build(elements)
    buffer.seek(0)
    return buffer


# ===============================
# PDF DEVIS


from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def create_devis_pdf(data):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    # ===============================
    # TITRE
    # ===============================
    elements.append(
        Paragraph("<b><font color='#0a7d33'>DEVIS TRANSPORT</font></b>", styles['Title'])
    )
    elements.append(Spacer(1, 15))

    # ===============================
    # TABLEAU PRIX
    # ===============================
    prix_table = Table([
        ["Prix transport", f"{data['prix_transport']} €"],
        ["Prix emballage", f"{data['prix_emballage']} €"],
        ["Total", f"{data['total']} €"]
    ], colWidths=[180, 290])

    prix_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0a7d33")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
    ]))

    elements.append(prix_table)
    elements.append(Spacer(1, 15))

    # ===============================
    # INFOS DEVIS
    # ===============================
    info_table = Table([
        ["Emballage obligatoire", data["emballage"]],
        ["Type emballage", data["type"]],
        ["Transit time", data["transit"]],
        ["Validité", data["validite"]],
    ], colWidths=[180, 290])

    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0a7d33")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # ===============================
    # ✅ TABLEAU RESUME (LE PLUS IMPORTANT)
    # ===============================
    elements.append(
        Paragraph("<b>Résumé de la demande</b>", styles['Heading3'])
    )
    elements.append(Spacer(1, 8))

    # 👉 transformation dict -> tableau
    table_data = []
    for key, value in data["tableau"].items():
        table_data.append([key, value])

    resume_table = Table(table_data, colWidths=[180, 290])

    resume_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0a7d33")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))

    elements.append(resume_table)
    elements.append(Spacer(1, 20))

    # ===============================
    # CONDITIONS
    # ===============================
    if data["conditions"]:
        elements.append(Paragraph("<b>Conditions d'annulation</b>", styles['Heading3']))
        elements.append(Spacer(1, 5))
        elements.append(Paragraph(data["conditions"], styles['Normal']))
        elements.append(Spacer(1, 10))

    # ===============================
    # COMMENTAIRE
    # ===============================
    if data["commentaire"]:
        elements.append(Paragraph("<b>Commentaire</b>", styles['Heading3']))
        elements.append(Spacer(1, 5))
        elements.append(Paragraph(data["commentaire"], styles['Normal']))

    # ===============================
    # BUILD
    # ===============================
    doc.build(elements)

    buffer.seek(0)
    return buffer

    # ===============================
    # TITRE
    # ===============================
    elements.append(
        Paragraph("<b><font color='#0a7d33'>DEVIS TRANSPORT</font></b>", styles['Title'])
    )
    elements.append(Spacer(1, 15))

    def table(rows):
        t = Table(rows, colWidths=[180, 290])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0a7d33")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ]))
        return t

    # ===============================
    # PRIX
    # ===============================
    elements.append(table([
        ["Prix transport", f"{data['prix_transport']} €"],
        ["Prix emballage", f"{data['prix_emballage']} €"],
        ["Total", f"{data['total']} €"]
    ]))

    elements.append(Spacer(1, 10))

    # ===============================
    # INFOS
    # ===============================
    elements.append(table([
        ["Emballage obligatoire", data['emballage']],
        ["Type", data['type']],
        ["Transit", data['transit']],
        ["Validité", data['validite']]
    ]))

    elements.append(Spacer(1, 10))

    # ✅ NOUVEAU : RESUME PDF
    elements.append(Paragraph("<b>Résumé de la demande</b>", styles['Heading3']))
    elements.append(Paragraph(data["resume_pdf"], styles['Normal']))

    elements.append(Spacer(1, 10))

    # ✅ CONDITIONS
    if data["conditions"]:
        elements.append(Paragraph("<b>Conditions</b>", styles['Heading3']))
        elements.append(Paragraph(data["conditions"], styles['Normal']))

    # ✅ COMMENTAIRE
    if data["commentaire"]:
        elements.append(Paragraph("<b>Commentaire</b>", styles['Heading3']))
        elements.append(Paragraph(data["commentaire"], styles['Normal']))

    doc.build(elements)
    buffer.seek(0)

    return buffer

from PyPDF2 import PdfReader


def extract_pdf_key_data(uploaded_pdf):

    data = {
        "Incoterm": "N/A",
        "Adresse": "N/A",
        "Colisage": "N/A",
        "Quantité": "N/A",
        "Transport": "N/A",
        "Emballage": "N/A",
    }

    if not uploaded_pdf:
        return data

    try:
        reader = PdfReader(uploaded_pdf)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        text = text.lower()

        # extraction simple (basique mais efficace)
        if "incoterm" in text:
            data["Incoterm"] = text.split("incoterm")[-1][:20]

        if "adresse" in text:
            data["Adresse"] = text.split("adresse")[-1][:40]

        if "quantité" in text or "quantite" in text:
            data["Quantité"] = text.split("quant")[-1][:10]

        if "poids" in text:
            data["Colisage"] = text.split("poids")[-1][:15]

        if "transport" in text:
            data["Transport"] = text.split("transport")[-1][:20]

        if "emballage" in text:
            data["Emballage"] = text.split("emballage")[-1][:20]

    except:
        pass

    return data
