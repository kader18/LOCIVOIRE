#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pitch + proposition de valeur Locivoire (PDF).
Exécuter : python docs/generate_pitch_pdf.py
"""

from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    print("Installation requise : pip install fpdf2")
    raise SystemExit(1)

DOCS = Path(__file__).resolve().parent
OUT = DOCS / "LOCIVOIRE_Pitch_Proposition_de_valeur.pdf"
FONT_REG = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")

NAVY = (16, 26, 48)
NAVY2 = (27, 42, 74)
GOLD = (217, 164, 65)
INK = (30, 36, 48)
MUTED = (90, 98, 112)
LINE = (220, 218, 210)
WHITE = (255, 255, 255)
SOFT = (248, 247, 244)


class PitchPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=True, margin=18)
        self.add_font("Body", "", str(FONT_REG))
        self.add_font("Body", "B", str(FONT_BOLD))

    def footer(self):
        self.set_y(-12)
        self.set_font("Body", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, f"Locivoire — Pitch & proposition de valeur  ·  p. {self.page_no()}", align="C")

    def cover(self):
        self.add_page()
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 297, "F")
        self.set_fill_color(*GOLD)
        self.rect(0, 0, 8, 297, "F")

        self.set_xy(24, 70)
        self.set_font("Body", "", 11)
        self.set_text_color(*GOLD)
        self.cell(0, 8, "DOCUMENT STRATÉGIQUE")

        self.set_xy(24, 88)
        self.set_font("Body", "B", 36)
        self.set_text_color(*WHITE)
        self.cell(0, 16, "Locivoire")

        self.set_xy(24, 110)
        self.set_font("Body", "B", 16)
        self.set_text_color(185, 193, 209)
        self.multi_cell(160, 9, "Pitch, proposition de valeur\net cibles prioritaires")

        self.set_draw_color(*GOLD)
        self.set_line_width(0.6)
        self.line(24, 150, 100, 150)

        self.set_xy(24, 160)
        self.set_font("Body", "", 11)
        self.set_text_color(185, 193, 209)
        self.multi_cell(
            160,
            7,
            "Pourquoi cette plateforme a sa place face aux agences\n"
            "agréées et aux sites d'annonces déjà existants.\n\n"
            "Côte d'Ivoire · Abidjan et grandes villes\n"
            "Juillet 2026",
        )

    def h1(self, title):
        self.ln(4)
        self.set_font("Body", "B", 15)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 8, title)
        y = self.get_y() + 1
        self.set_draw_color(*GOLD)
        self.set_line_width(0.8)
        self.line(10, y, 70, y)
        self.ln(6)

    def h2(self, title):
        self.ln(2)
        self.set_font("Body", "B", 12)
        self.set_text_color(*NAVY2)
        self.multi_cell(0, 7, title)
        self.ln(2)

    def body(self, text):
        self.set_font("Body", "", 10)
        self.set_text_color(*INK)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Body", "", 10)
        self.set_text_color(*INK)
        self.set_x(self.l_margin + 2)
        self.multi_cell(0, 5.5, f"•  {text}")
        self.ln(0.5)

    def callout(self, text):
        self.ln(2)
        x = self.l_margin
        y = self.get_y()
        width = self.epw
        self.set_font("Body", "B", 10)
        # Mesure
        lines = self.multi_cell(width - 12, 5.8, text, dry_run=True, output="LINES")
        h = 8 + len(lines) * 5.8
        self.set_fill_color(*SOFT)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.rect(x, y, width, h, "FD")
        self.set_xy(x + 6, y + 4)
        self.set_text_color(*NAVY)
        self.multi_cell(width - 12, 5.8, text)
        self.set_y(y + h + 3)

    def kv_row(self, left, right, fill=False):
        self.set_fill_color(*(SOFT if fill else WHITE))
        self.set_draw_color(*LINE)
        y = self.get_y()
        self.set_font("Body", "B", 9)
        self.set_text_color(*NAVY)
        self.cell(58, 9, f"  {left}", border=1, fill=True)
        self.set_font("Body", "", 9)
        self.set_text_color(*INK)
        self.cell(132, 9, f"  {right}", border=1, fill=True, ln=True)


def build():
    pdf = PitchPDF()
    pdf.cover()

    pdf.add_page()
    pdf.h1("1. Contexte du marché")
    pdf.body(
        "Ce genre de site existe déjà. Dans la pratique ivoirienne, beaucoup de "
        "propriétaires préfèrent confier leurs maisons à une agence agréée par l'État. "
        "L'agence trouve les clients, prend souvent l'équivalent d'un mois de loyer "
        "(ex. : 5 mois d'avance deviennent 6), et peut gérer suivi, pression sur le "
        "paiement et parfois le maintien du bien."
    )
    pdf.body(
        "Conséquence : un site d'annonces classique qui dit seulement « publiez et "
        "on vous appelle » ne remplace pas une agence pour le propriétaire qui veut "
        "tout déléguer."
    )
    pdf.h2("Ce que l'agence apporte vraiment")
    for t in [
        "Trouver le locataire",
        "Sécuriser la transaction (souvent via la commission d'un mois)",
        "Gérer entrées / sorties et la relation locataire",
        "Réduire le stress du propriétaire",
    ]:
        pdf.bullet(t)

    pdf.h1("2. Positionnement Locivoire")
    pdf.callout(
        "Locivoire n'est pas une agence immobilière. C'est la plateforme qui fait "
        "gagner du temps et de la confiance grâce aux visites immersives — surtout "
        "pour locataires et propriétaires-gestionnaires — et un outil pour les "
        "petites agences."
    )
    pdf.body(
        "L'objectif n'est pas d'éliminer les agences agréées, mais d'occuper un "
        "espace sous-servi : transparence, preuve visuelle du bien, et coût plus "
        "clair pour ceux qui ne veulent pas « perdre » un mois à chaque location."
    )

    pdf.h1("3. Avantages concurrentiels")
    pdf.h2("Face aux agences")
    for t in [
        "Moins cher / plus transparent qu'une commission systématique d'un mois",
        "Le propriétaire garde le contrôle et le contact client s'il le souhaite",
        "Accessible 24h/24, sans déplacement en agence pour consulter le catalogue",
        "Visite immersive avant le rendez-vous physique : moins de visites inutiles",
    ]:
        pdf.bullet(t)

    pdf.h2("Face aux sites d'annonces déjà existants")
    for t in [
        "Différenciateur technique : visites immersives (pas seulement 4 photos floues)",
        "Confiance : vérification des prestataires / annonces plus fiables",
        "Expérience locale pensée pour la Côte d'Ivoire (quartiers, usages, mobile)",
        "Message clair : gagner du temps, réduire les arnaques, mieux juger le bien à distance",
    ]:
        pdf.bullet(t)

    pdf.h2("Tableau synthétique")
    pdf.ln(1)
    pdf.set_font("Body", "B", 8)
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    for label, w in [
        ("  Besoin", 42),
        ("  Agence", 48),
        ("  Sites classiques", 50),
        ("  Locivoire", 50),
    ]:
        pdf.cell(w, 8, label, border=1, fill=True)
    pdf.ln()

    rows = [
        ("Tout déléguer", "Fort", "Faible", "Faible*"),
        ("Voir sans se déplacer", "Faible", "Photos limitées", "Fort (immersif)"),
        ("Diaspora / hors ville", "Moyen", "Moyen", "Fort"),
        ("Coût clair", "Commission lourde", "Opaque", "À clarifier"),
        ("Proprio actif", "Faible", "Possible", "Fort"),
        ("Petites agences", "—", "Peu d'outils", "Outil + vitrine"),
    ]
    pdf.set_font("Body", "", 8)
    for i, (a, b, c, d) in enumerate(rows):
        pdf.set_fill_color(*(SOFT if i % 2 == 0 else WHITE))
        pdf.set_text_color(*INK)
        pdf.cell(42, 7, f"  {a}", border=1, fill=True)
        pdf.cell(48, 7, f"  {b}", border=1, fill=True)
        pdf.cell(50, 7, f"  {c}", border=1, fill=True)
        pdf.cell(50, 7, f"  {d}", border=1, fill=True)
        pdf.ln()
    pdf.ln(2)
    pdf.set_font("Body", "", 8)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 4.5, "*Sauf partenariats agences / options de gestion ajoutées plus tard.")

    pdf.add_page()
    pdf.h1("4. Pourquoi utiliser Locivoire ?")
    pdf.body(
        "Trois raisons crédibles — sans l'une d'elles, Locivoire reste "
        "« un site de plus » :"
    )
    pdf.h2("1) La visite immersive comme preuve")
    pdf.body(
        "Le locataire voit le salon, la cuisine, l'état réel — avant de prendre un taxi. "
        "Cela réduit déplacements, désillusions et arnaques. C'est le vrai "
        "différenciateur technique du produit."
    )
    pdf.h2("2) La confiance (vérification)")
    pdf.body(
        "Prestataires validés, annonces plus contrôlées, moins de faux numéros et de "
        "maisons déjà louées. Si Locivoire n'est pas plus fiable que Facebook / "
        "WhatsApp / petites annonces classiques, l'argument disparaît."
    )
    pdf.h2("3) Un modèle économique moins punitif")
    pdf.body(
        "Exemple d'orientation : pas « un mois à chaque location », mais abonnement, "
        "petite commission transparente, ou l'agence partenaire utilise Locivoire "
        "comme vitrine. Le message doit être : moins cher + plus clair."
    )

    pdf.h1("5. Qui est le plus visé ?")
    pdf.h2("Ordre de priorité recommandé")

    pdf.set_font("Body", "B", 10)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 6, "Cible n°1 — Locataires (Abidjan + diaspora)", ln=True)
    pdf.body(
        "Ce sont eux qui souffrent le plus : visites inutiles, transport, photos "
        "trompeuses. S'ils viennent, les annonceurs suivent. Inclure étudiants, "
        "jeunes actifs, mutation professionnelle, diaspora qui loue à distance."
    )

    pdf.set_font("Body", "B", 10)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 6, "Cible n°2 — Propriétaires particuliers actifs", ln=True)
    pdf.body(
        "1 à 5 biens, veulent louer vite, acceptent de gérer (ou ont un gardien), "
        "refusent de « donner un mois » à chaque location. Pas le gros investisseur "
        "qui délègue tout à une agence agréée."
    )

    pdf.set_font("Body", "B", 10)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 6, "Cible n°3 — Petites agences / courtiers", ln=True)
    pdf.body(
        "Pas comme ennemis : comme clients. Locivoire = outil (visite immersive, "
        "fiche pro, leads). L'agence garde sa logique commerciale ; vous vendez "
        "la techno et la vitrine."
    )

    pdf.h2("Moins prioritaire au démarrage")
    pdf.body(
        "Les gros propriétaires « je ne veux rien faire » resteront chez l'agence "
        "agréée. Ne pas les cibler en premier."
    )

    pdf.h1("6. Orientation modèle économique")
    pdf.body("Pistes compatibles avec le positionnement (à valider) :")
    for t in [
        "Freemium annonceur : publication limitée gratuite, options payantes (mise en avant, visite immersive assistée)",
        "Commission légère à la réservation / mise en relation (bien inférieure à 1 mois de loyer)",
        "Abonnement mensuel pour propriétaires multi-biens ou petites agences",
        "Partenariat agences : licence d'outil + leads qualifiés",
    ]:
        pdf.bullet(t)
    pdf.body(
        "Principe : ne jamais se présenter comme « l'agence digitale qui prend un mois », "
        "sinon collision frontale avec le modèle dominant — sans agrément ni force "
        "de gestion terrain."
    )

    pdf.h1("7. Feuille de route produit (simple)")
    pdf.h2("Phase 1 — Preuve & confiance")
    for t in [
        "Découverte des biens + filtres locaux",
        "Visite immersive de qualité",
        "Mise en relation vérifiée",
    ]:
        pdf.bullet(t)
    pdf.h2("Phase 2 — Écosystème")
    for t in [
        "Outils pour petites agences",
        "Options de partenariat / gestion",
        "Extension hors Abidjan",
    ]:
        pdf.bullet(t)
    pdf.body(
        "Risque à éviter : vouloir être à la fois Airbnb + agence + bail + maintenance. "
        "Trop large = personne ne comprend. Un positionnement net vaut mieux qu'une "
        "promesse totale."
    )

    pdf.add_page()
    pdf.h1("8. Synthèse")
    pdf.ln(1)
    pdf.kv_row("Avantage clé", "Visite immersive + confiance + coût plus clair")
    pdf.kv_row("Pourquoi venir ?", "Moins de déplacements / arnaques ; bien « vu pour de vrai »", fill=True)
    pdf.kv_row("Vs autres sites", "Eux montrent des photos — vous montrez l'expérience du bien")
    pdf.kv_row("Cible n°1", "Locataires (Abidjan + diaspora)", fill=True)
    pdf.kv_row("Cible n°2", "Propriétaires particuliers actifs")
    pdf.kv_row("Cible n°3", "Petites agences / courtiers", fill=True)
    pdf.kv_row("À ne pas viser d'abord", "Propriétaires 100 % délégation (reste aux agences)")

    pdf.ln(8)
    pdf.callout(
        "En une phrase : Locivoire digitalise la preuve et la confiance autour de la "
        "location — sans prétendre remplacer l'agence agréée pour ceux qui veulent "
        "tout confier."
    )

    pdf.ln(10)
    pdf.set_font("Body", "", 9)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        5,
        "Document interne / présentation partenaires · Locivoire · Juillet 2026\n"
        "À actualiser avec le business model détaillé et les tarifs retenus.",
    )

    pdf.output(str(OUT))
    print(f"PDF créé : {OUT}")


if __name__ == "__main__":
    build()
