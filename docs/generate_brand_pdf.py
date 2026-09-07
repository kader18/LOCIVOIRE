#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du document PDF - Charte d'Identité de Marque LocIvoire
Exécuter avec: pip install fpdf2 && python generate_brand_pdf.py
"""

from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    print("Installation de fpdf2 requise: pip install fpdf2")
    exit(1)


class BrandIdentityPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "Document officiel LocIvoire - Charte d'identité de marque", align="C")

    def add_section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(37, 99, 235)  # Bleu primaire
        self.ln(8)
        self.multi_cell(0, 8, title)
        self.set_draw_color(229, 231, 235)
        self.line(10, self.get_y() + 2, 200, self.get_y() + 2)
        self.ln(10)
        self.set_text_color(0, 0, 0)

    def add_subtitle(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(55, 65, 81)
        self.ln(4)
        self.multi_cell(0, 7, title)
        self.ln(4)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)

    def add_highlight_box(self, text):
        self.set_fill_color(240, 249, 255)
        self.set_draw_color(37, 99, 235)
        self.set_line_width(0.5)
        self.set_x(15)
        self.set_y(self.get_y() + 5)
        self.cell(2, 20, "", border="L", fill=True)
        self.set_xy(17, self.get_y() - 20)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(5)

    def add_body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(3)


def generate_pdf():
    pdf = BrandIdentityPDF()
    pdf.add_page()

    # Couverture
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(37, 99, 235)
    pdf.ln(40)
    pdf.cell(0, 12, "LocIvoire", align="C", ln=True)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(17, 24, 39)
    pdf.ln(15)
    pdf.cell(0, 10, "Charte d'Identite de Marque", align="C", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(107, 114, 128)
    pdf.ln(8)
    pdf.cell(0, 8, "Document officiel - Identite visuelle et valeurs", align="C", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 6, "Version 1.0 - Fevrier 2025", align="C", ln=True)
    pdf.ln(20)
    pdf.set_draw_color(37, 99, 235)
    pdf.set_line_width(1)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(15)

    # Section 1
    pdf.add_section_title("1. Presentation de la marque")
    pdf.add_body_text(
        "LocIvoire est une plateforme web de location de maisons en Cote d'Ivoire. Elle met en relation "
        "les proprietaires et promoteurs immobiliers avec les locataires potentiels, tout en offrant des "
        "experiences innovantes comme les visites virtuelles en realite augmentee."
    )
    pdf.add_highlight_box(
        "Nom de la marque : LocIvoire\n"
        "Activite : Plateforme de location immobiliere en Cote d'Ivoire\n"
        "Promesse : Trouver facilement son logement en Cote d'Ivoire, avec une experience moderne et fiable."
    )

    # Section 2
    pdf.add_section_title("2. Origine du nom et du logo")

    pdf.add_subtitle("2.1 Etymologie du nom LocIvoire")
    pdf.add_body_text(
        "Le nom LocIvoire est une contraction volontaire et memorisable de deux elements :"
    )
    pdf.add_body_text("- Loc : abreviation de Location, l'activite principale de la plateforme ;")
    pdf.add_body_text("- Ivoire : reference directe a la Cote d'Ivoire, le pays cible et le marche d'ancrage de la marque.")
    pdf.add_body_text(
        "Cette fusion cree une identite claire, facile a prononcer et immediatement associee a la "
        "location immobiliere en Cote d'Ivoire."
    )

    pdf.add_subtitle("2.2 Symbolisme du logo")
    pdf.add_body_text(
        "Le logo de LocIvoire se compose de deux elements indissociables :"
    )
    pdf.add_body_text(
        "- L'icone maison : Elle represente le logement, le foyer et la propriete, au coeur de l'activite "
        "de la plateforme. Elle evoque la securite, l'abri et la serenite du chez-soi, valeurs essentielles "
        "en matiere de location."
    )
    pdf.add_body_text(
        "- Le nom LocIvoire : En association avec l'icone, il renforce l'identification a la marque et a son territoire."
    )
    pdf.add_body_text(
        "L'icone maison a ete choisie pour sa simplicite, sa reconnaissance universelle et son lien direct "
        "avec le secteur immobilier. Elle traduit a la fois l'offre (biens a louer) et la demande "
        "(recherche d'un logement)."
    )

    pdf.add_subtitle("2.3 Choix du logotype")
    pdf.add_body_text(
        "Ce logotype a ete retenu pour sa capacite a communiquer rapidement l'activite de la marque sans "
        "recourir a des elements decoratifs superflus. Il est adapte aux supports numeriques (site web, "
        "applications, reseaux sociaux) tout en restant lisible a differentes tailles."
    )

    # Section 3
    pdf.add_section_title("3. Charte graphique")

    pdf.add_subtitle("3.1 Palette de couleurs")
    pdf.add_body_text(
        "La palette de LocIvoire repose sur des couleurs modernes et professionnelles, refletant la confiance, "
        "l'innovation et l'ancrage ivoirien."
    )
    pdf.add_body_text("Bleu primaire (#2563eb) : professionnalisme, fiabilite et serenite.")
    pdf.add_body_text("Violet secondaire (#7c3aed) : modernite, creativite et innovation.")
    pdf.add_body_text("Orange accent (#f59e0b) : dynamisme et energie.")

    pdf.add_subtitle("3.2 Typographie")
    pdf.add_body_text(
        "La police principale de la marque est Inter (Google Fonts). Elle a ete choisie pour sa lisibilite "
        "sur tous les supports, son caractere contemporain et son excellente restitution a differentes tailles."
    )

    # Section 4
    pdf.add_section_title("4. Valeurs et positionnement")
    pdf.add_body_text("- Confiance : Verification des proprietaires, transparence des informations.")
    pdf.add_body_text("- Innovation : Visites virtuelles en realite augmentee, interface moderne.")
    pdf.add_body_text("- Proximite : Ancrage ivoirien et comprehension des besoins locaux.")
    pdf.add_body_text("- Simplicite : Processus de recherche et reservation facilites.")

    # Section 5
    pdf.add_section_title("5. Utilisation de la marque")
    pdf.add_body_text(
        "Le nom LocIvoire et le logotype doivent etre utilises de maniere coherente sur tous les supports "
        "officiels : site web, documents administratifs, communications marketing et partenariats. "
        "Il est recommande de conserver l'association icone + nom pour une reconnaissance optimale."
    )

    pdf.ln(20)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 6, "(c) 2025 LocIvoire. Tous droits reserves.", align="C", ln=True)

    # Sauvegarde
    output_path = Path(__file__).parent / "IDENTITE_MARQUE_LOCIVOIRE.pdf"
    pdf.output(str(output_path))
    return output_path


if __name__ == "__main__":
    try:
        path = generate_pdf()
        print(f"PDF genere avec succes : {path}")
    except Exception as e:
        print(f"Erreur : {e}")
        raise
