#!/usr/bin/env python3
"""Genera la Guida Tropea PDF con immagini, voti e link."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Image, Flowable,
)

DIR = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(DIR, "immagini")
THUMBS = os.path.join(IMG, "thumbs")
OUTPUT = os.path.join(DIR, "Guida_Tropea_Camping_Marina_Isola.pdf")

BLU_MARE = HexColor("#0077A8")
BLU_SCURO = HexColor("#0A3D5C")
ACQUA = HexColor("#2AA8C4")
SABBIA = HexColor("#F5E6C8")
CORALLO = HexColor("#C45C26")
VERDE = HexColor("#2D6A4F")
GRIGIO = HexColor("#4A5568")
ORO = HexColor("#B8860B")
BIANCO = white

BASE_ADDR = "Via Lungomare Sorrentino, 89861 Tropea (VV)"
BASE_COORDS = "38°40'43\"N · 15°53'41\"E"


def img_path(name):
    for base in (THUMBS, IMG):
        p = os.path.join(base, name)
        if os.path.isfile(p):
            return p
    return None


def beach_thumb(name, w=16.5 * cm, h=4.8 * cm):
    p = img_path(name)
    if not p:
        return None
    try:
        return Image(p, width=w, height=h)
    except Exception:
        return None


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLU_SCURO)
    canvas.rect(0, A4[1] - 1.2 * cm, A4[0], 1.2 * cm, fill=1, stroke=0)
    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.5 * cm, A4[1] - 0.75 * cm, "Guida Tropea · da Camping Marina dell'Isola")
    canvas.drawRightString(A4[0] - 1.5 * cm, A4[1] - 0.75 * cm, "Costa degli Dei · Calabria")
    canvas.setFillColor(BLU_SCURO)
    canvas.rect(0, 0, A4[0], 1.0 * cm, fill=1, stroke=0)
    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 0.4 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLU_SCURO)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # foto cover se disponibile
    cover = img_path("cover.jpg") or img_path("marina_isola.jpg") or img_path("isola.jpg")
    if cover:
        try:
            from reportlab.lib.utils import ImageReader
            canvas.drawImage(ImageReader(cover), 0, A4[1] * 0.55, width=A4[0],
                             height=A4[1] * 0.45, preserveAspectRatio=False, anchor="c")
            canvas.setFillColor(BLU_SCURO)
            try:
                canvas.setFillAlpha(0.45)
                canvas.rect(0, A4[1] * 0.55, A4[0], A4[1] * 0.45, fill=1, stroke=0)
                canvas.setFillAlpha(1)
            except Exception:
                pass
        except Exception:
            pass
    canvas.setFillColor(ACQUA)
    canvas.rect(0, A4[1] * 0.42, A4[0], 0.4 * cm, fill=1, stroke=0)
    canvas.setFillColor(BLU_MARE)
    canvas.rect(0, A4[1] * 0.42 - 0.25 * cm, A4[0], 0.25 * cm, fill=1, stroke=0)

    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 3.2 * cm, "LA TUA GUIDA PERSONALE")
    canvas.setFont("Helvetica-Bold", 36)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 5.0 * cm, "TROPEA")
    canvas.setFont("Helvetica", 12)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 6.2 * cm, "Spiagge · Ristoranti · Tramonti · Chicche")
    canvas.setFillColor(SABBIA)
    canvas.setFont("Helvetica-Oblique", 11)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 7.2 * cm, "con foto, voti /5, distanze e link")

    canvas.setFillColor(HexColor("#0F4A6B"))
    canvas.roundRect(2.5 * cm, 3.8 * cm, A4[0] - 5 * cm, 4.5 * cm, 8, fill=1, stroke=0)
    canvas.setFillColor(ACQUA)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(A4[0] / 2, 7.6 * cm, "IL TUO PUNTO DI PARTENZA")
    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(A4[0] / 2, 6.6 * cm, "Camping Marina dell'Isola")
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(A4[0] / 2, 5.8 * cm, BASE_ADDR)
    canvas.drawCentredString(A4[0] / 2, 5.2 * cm, BASE_COORDS)
    canvas.setFont("Helvetica-Oblique", 9)
    canvas.drawCentredString(A4[0] / 2, 4.5 * cm, "Accesso diretto al mare · ai piedi di Santa Maria dell'Isola")
    canvas.setFillColor(SABBIA)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 2.2 * cm, "Foto: Wikimedia Commons · voti indicativi Google 2025–2026")
    canvas.restoreState()


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitoloSezione", fontName="Helvetica-Bold", fontSize=16,
        textColor=BLU_SCURO, spaceBefore=4, spaceAfter=6, leading=19,
    ))
    styles.add(ParagraphStyle(
        name="SottoTitolo", fontName="Helvetica", fontSize=9,
        textColor=GRIGIO, spaceAfter=8, leading=12,
    ))
    styles.add(ParagraphStyle(
        name="NomeLuogo", fontName="Helvetica-Bold", fontSize=10.5,
        textColor=BLU_MARE, spaceBefore=2, spaceAfter=2, leading=13,
    ))
    styles.add(ParagraphStyle(
        name="Meta", fontName="Helvetica-Bold", fontSize=8.5,
        textColor=ORO, spaceAfter=2, leading=11,
    ))
    styles.add(ParagraphStyle(
        name="Descrizione", fontName="Helvetica", fontSize=8.5,
        textColor=GRIGIO, alignment=TA_JUSTIFY, spaceAfter=2, leading=11,
    ))
    styles.add(ParagraphStyle(
        name="Nota", fontName="Helvetica-Oblique", fontSize=7.5,
        textColor=GRIGIO, spaceAfter=3, leading=9,
    ))
    styles.add(ParagraphStyle(
        name="Intro", fontName="Helvetica", fontSize=9.5,
        textColor=GRIGIO, alignment=TA_JUSTIFY, spaceAfter=8, leading=13,
    ))
    styles.add(ParagraphStyle(
        name="TabCell", fontName="Helvetica", fontSize=7.5,
        textColor=GRIGIO, leading=9,
    ))
    styles.add(ParagraphStyle(
        name="TabHead", fontName="Helvetica-Bold", fontSize=8,
        textColor=BIANCO, leading=10,
    ))
    styles.add(ParagraphStyle(
        name="Consiglio", fontName="Helvetica", fontSize=8,
        textColor=VERDE, spaceAfter=2, leading=10,
    ))
    styles.add(ParagraphStyle(
        name="Link", fontName="Helvetica", fontSize=8,
        textColor=BLU_MARE, spaceAfter=2, leading=10,
    ))
    styles.add(ParagraphStyle(
        name="SmallLeft", fontName="Helvetica", fontSize=8.5,
        textColor=GRIGIO, alignment=TA_LEFT, leading=11,
    ))
    return styles


def sezione_header(titolo, sottotitolo, styles):
    return [
        Paragraph(titolo, styles["TitoloSezione"]),
        HRFlowable(width="100%", thickness=2, color=ACQUA, spaceAfter=4),
        Paragraph(sottotitolo, styles["SottoTitolo"]),
    ]


def scheda_spiaggia(nome, distanza, voto, desc, styles, image_file=None, consiglio=None):
    elems = []
    thumb = beach_thumb(image_file) if image_file else None
    if thumb:
        elems.append(thumb)
        elems.append(Spacer(1, 3))
    elems.extend([
        Paragraph(nome, styles["NomeLuogo"]),
        Paragraph(f"Voto: {voto}/5  ·  Distanza: {distanza}", styles["Meta"]),
        Paragraph(desc, styles["Descrizione"]),
    ])
    if consiglio:
        elems.append(Paragraph(f"Consiglio: {consiglio}", styles["Consiglio"]))
    elems.append(Spacer(1, 8))
    return KeepTogether(elems)


def scheda_ristorante(nome, distanza, voto, desc, styles, link=None, consiglio=None):
    elems = [
        Paragraph(nome, styles["NomeLuogo"]),
        Paragraph(f"Voto: {voto}/5  ·  Distanza: {distanza}", styles["Meta"]),
        Paragraph(desc, styles["Descrizione"]),
    ]
    if link:
        elems.append(Paragraph(
            f'Link: <link href="{link}" color="#0077A8"><u>{link}</u></link>',
            styles["Link"],
        ))
    if consiglio:
        elems.append(Paragraph(f"Consiglio: {consiglio}", styles["Consiglio"]))
    elems.append(Spacer(1, 4))
    return KeepTogether(elems)


def scheda(nome, distanza, desc, styles, voto=None, consiglio=None, link=None):
    elems = [Paragraph(nome, styles["NomeLuogo"])]
    if voto is not None:
        elems.append(Paragraph(f"Voto: {voto}/5  ·  Distanza: {distanza}", styles["Meta"]))
    else:
        elems.append(Paragraph(f"Distanza: {distanza}", styles["Meta"]))
    elems.append(Paragraph(desc, styles["Descrizione"]))
    if link:
        elems.append(Paragraph(
            f'Link: <link href="{link}" color="#0077A8"><u>{link}</u></link>',
            styles["Link"],
        ))
    if consiglio:
        elems.append(Paragraph(f"Consiglio: {consiglio}", styles["Consiglio"]))
    elems.append(Spacer(1, 3))
    return KeepTogether(elems)


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=1.4 * cm, rightMargin=1.4 * cm,
        topMargin=1.8 * cm, bottomMargin=1.5 * cm,
        title="Guida Tropea – Camping Marina dell'Isola",
        author="Guida personale Tropea",
    )
    story = []
    story.append(PageBreak())

    story.append(Paragraph("Benvenuto a Tropea", styles["TitoloSezione"]))
    story.append(HRFlowable(width="100%", thickness=2, color=ACQUA, spaceAfter=6))
    story.append(Paragraph(
        "Sei ospite al <b>Camping Marina dell'Isola</b>. Guida con "
        "<b>foto delle spiagge</b>, <b>voti /5</b>, distanze e "
        "<b>link cliccabili</b> ai ristoranti (entro ~5 km e dintorni).",
        styles["Intro"],
    ))
    story.append(Paragraph(
        "Voti indicativi da Google (2025–2026). Foto da Wikimedia Commons "
        "(licenze libere). I link si aprono dal PDF con un clic.",
        styles["Nota"],
    ))

    # TABELLA DISTANZE
    story.append(Paragraph("Tabella distanze rapide", styles["TitoloSezione"]))
    story.append(HRFlowable(width="100%", thickness=2, color=ACQUA, spaceAfter=5))
    header = [Paragraph(h, styles["TabHead"]) for h in ("Destinazione", "Distanza", "Come", "Tempo")]
    rows = [
        ("Spiaggia Marina dell'Isola", "0 m", "a piedi", "immediato"),
        ("Santuario S. Maria dell'Isola", "~150 m", "a piedi", "3–5 min"),
        ("Spiaggia della Rotonda", "~400 m", "a piedi", "5–8 min"),
        ("Centro storico", "~450 m", "scale", "8–12 min"),
        ("Baia di Riaci", "~3 km", "auto", "8–10 min"),
        ("Formicoli / Scalea", "~4–5 km", "auto", "10–12 min"),
        ("Michelino (Parghelia)", "~4,5 km", "auto", "10–12 min"),
        ("Grotticelle / Capo Vaticano", "~11 km", "auto", "20–25 min"),
        ("Pizzo Calabro", "~22 km", "auto", "30–35 min"),
    ]
    data = [header] + [[Paragraph(c, styles["TabCell"]) for c in r] for r in rows]
    t = Table(data, colWidths=[7.0 * cm, 3.0 * cm, 3.0 * cm, 3.2 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU_SCURO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#E8F6FA"), BIANCO]),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#D0DCE4")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(PageBreak())

    # ========== SPIAGGE ==========
    story.extend(sezione_header(
        "Le spiagge (con foto e voti)",
        "Da quelle sotto il camping fino a Riaci, Formicoli e Capo Vaticano.",
        styles,
    ))

    spiagge = [
        {
            "nome": "1. Spiaggia Marina dell'Isola (Mare Piccolo)",
            "dist": "~0 m · accesso diretto dal camping",
            "voto": "4,6",
            "img": "marina_isola.jpg",
            "desc": (
                "La spiaggia del campeggio: sabbia chiara, mare cristallino e lo scoglio "
                "di Santa Maria dell'Isola. Ideale per snorkel e tramonti; con cielo limpido "
                "si scorge lo Stromboli. Tratti liberi e lidi."
            ),
            "tip": "Mattina presto o tardo pomeriggio per meno folla.",
        },
        {
            "nome": "2. Spiaggia della Rotonda (Le Roccette)",
            "dist": "~400 m · 5–8 min a piedi",
            "voto": "4,7",
            "img": "rotonda.jpg",
            "desc": (
                "La più fotografata di Tropea: mezzaluna sotto la rupe, vista Isola e "
                "Scoglio di San Leonardo. Mare azzurro intenso, sabbia fine. "
                "Molto frequentata in agosto."
            ),
            "tip": "Arriva presto; ottima anche solo per una passeggiata.",
        },
        {
            "nome": "3. Spiaggia del Cannone",
            "dist": "~900 m · 12–15 min a piedi",
            "voto": "4,4",
            "img": "cannone.jpg",
            "desc": (
                "Piccola insenatura verso il porto, meno affollata della Rotonda. "
                "Nome dai cannoni spagnoli ritrovati in zona. Atmosfera più riservata."
            ),
            "tip": None,
        },
        {
            "nome": "4. Spiaggia A Linguata / Mare Grande",
            "dist": "~1–1,5 km",
            "voto": "4,5",
            "img": "linguata.jpg",
            "desc": (
                "Tratto più lungo della costa tropeana: sabbia bianca, fondali limpidissimi, "
                "lidi e zone libere. Buona per famiglie che vogliono più spazio."
            ),
            "tip": None,
        },
        {
            "nome": "5. Spiaggia Passo del Cavaliere",
            "dist": "~1,8 km · 5 min in auto",
            "voto": "4,3",
            "img": "passo.jpg",
            "desc": (
                "Fondale sabbioso, atmosfera più rilassata rispetto alle spiagge sotto la rupe. "
                "Fa parte del tratto Mare Grande."
            ),
            "tip": None,
        },
        {
            "nome": "6. Spiaggia dell'Occhiale",
            "dist": "~2,5 km · ~8 min in auto",
            "voto": "4,5",
            "img": "occhiale.jpg",
            "desc": (
                "Più selvaggia: scogli a forma di occhiali, snorkel e paesaggio roccioso. "
                "Ambiente naturale, meno «da cartolina turistica»."
            ),
            "tip": "Scarpe comode: accesso un po' più impegnativo.",
        },
    ]
    for s in spiagge:
        story.append(scheda_spiaggia(
            s["nome"], s["dist"], s["voto"], s["desc"], styles,
            image_file=s["img"], consiglio=s.get("tip"),
        ))

    story.append(PageBreak())

    # Spiagge extra: Riaci etc.
    story.extend(sezione_header(
        "Spiagge dei dintorni: Riaci, Formicoli, Capo Vaticano",
        "Le baie più belle tra Tropea e Capo Vaticano (alcune oltre i 5 km).",
        styles,
    ))

    extra = [
        {
            "nome": "7. Baia di Riaci (Santa Domenica di Ricadi)",
            "dist": "~3 km · 8–10 min in auto",
            "voto": "4,7",
            "img": "riaci.jpg",
            "desc": (
                "Una delle spiagge più celebrate della Costa degli Dei (National Geographic "
                "tra le migliori d'Italia). Falesie di arenaria, Scoglio Grande iconico, "
                "mare limpidissimo e snorkel top. Lidi + tratti liberi. "
                "Non confondere con Riace (Bronzi) sul Jonio!"
            ),
            "tip": "Imperdibile dal camping: pochi minuti di auto. Parcheggio in zona baia.",
        },
        {
            "nome": "8. Spiaggia di Formicoli",
            "dist": "~4–5 km · 10–12 min in auto",
            "voto": "4,5",
            "img": "formicoli.jpg",
            "desc": (
                "Tra Riaci e Capo Vaticano. Mare bellissimo e fondali ricchi "
                "(snorkeling/immersioni). Nome legato all'antico porto romano Forum Herculis. "
                "Meno chiassosa di Grotticelle."
            ),
            "tip": "Ottima per chi cerca bellezza senza la folla massima.",
        },
        {
            "nome": "9. Spiaggia della Scalea (Santa Domenica)",
            "dist": "~3–4 km · ~10 min in auto",
            "voto": "4,4",
            "img": "scalea.jpg",
            "desc": (
                "Incastonata tra Riaci e Formicoli, ai piedi di un costone di arenaria "
                "(~70 m). Accesso tramite scalinata dal paese. Paesaggio suggestivo, "
                "spiaggia più raccolta."
            ),
            "tip": None,
        },
        {
            "nome": "10. Spiaggia di Michelino (Parghelia)",
            "dist": "~4,5 km · 10–12 min in auto",
            "voto": "4,6",
            "img": "michelino.jpg",
            "desc": (
                "A nord di Tropea: sabbia bianchissima e mare da cartolina. "
                "Una delle baie più belle entro 5 km, verso Parghelia/Zambrone."
            ),
            "tip": "Mezza giornata alternativa alle spiagge sotto Tropea.",
        },
        {
            "nome": "11. Grotticelle (Capo Vaticano)",
            "dist": "~11 km · 20–25 min in auto",
            "voto": "4,7",
            "img": "grotticelle.jpg",
            "desc": (
                "La «regina» di Capo Vaticano: sabbia fine, acque turchesi, scogli. "
                "Spesso chiamata il Caraibi della Calabria. Attrezzata e molto gettonata "
                "in alta stagione."
            ),
            "tip": "Arriva presto o scegli giorni feriali.",
        },
        {
            "nome": "12. Spiaggia di Santa Maria (Capo Vaticano)",
            "dist": "~10–11 km · ~20 min in auto",
            "voto": "4,5",
            "img": "santa_maria_cv.jpg",
            "desc": (
                "Vicino all'omonimo borgo marinaro. Acque calme e spesso poco profonde: "
                "adatta alle famiglie. Lungomare con locali per aperitivo al tramonto."
            ),
            "tip": None,
        },
        {
            "nome": "13. Praia i Focu (Capo Vaticano)",
            "dist": "~11 km · meglio via mare / discesa ripida",
            "voto": "4,8",
            "img": "praia_focu.jpg",
            "desc": (
                "Forse la caletta più spettacolare della costa: racchiusa tra alte rupi, "
                "mare incredibile. Spesso raggiungibile in barca o con discese impegnative. "
                "Una delle immagini iconiche di Capo Vaticano."
            ),
            "tip": "Consigliato tour in barca da Tropea (~35–45 €).",
        },
    ]
    for s in extra:
        story.append(scheda_spiaggia(
            s["nome"], s["dist"], s["voto"], s["desc"], styles,
            image_file=s["img"], consiglio=s.get("tip"),
        ))

    story.append(Paragraph(
        "Nota foto: immagini da Wikimedia Commons (Tropea, Riaci, Capo Vaticano). "
        "Alcune foto di zona Capo Vaticano sono rappresentative della costa ricadese.",
        styles["Nota"],
    ))
    story.append(PageBreak())

    # ========== RISTORANTI ==========
    story.extend(sezione_header(
        "Ristoranti entro circa 5 km (con link)",
        "Clicca i link nel PDF per aprire sito o Google Maps. Voti /5 indicativi.",
        styles,
    ))

    r_header = [Paragraph(h, styles["TabHead"]) for h in ("Ristorante", "Voto", "Dist.", "Link")]
    r_rows_data = [
        ("Camping Marina Isola", "4,2*", "0 m", "sito"),
        ("Tropical (lido)", "4,4", "400 m", "Maps"),
        ("Scacco Matto", "4,4", "550 m", "Maps"),
        ("La Villetta", "4,3", "550 m", "Maps"),
        ("Vicolo 34", "4,5", "500 m", "sito"),
        ("La Conchiglia da Patea", "4,7", "600 m", "Maps"),
        ("Incipit", "4,5", "650 m", "sito"),
        ("Pinturicchio", "4,3", "600 m", "sito"),
        ("Pimm's", "3,8", "700 m", "Maps"),
        ("De' Minimi", "4,6", "3–4 km", "sito"),
        ("Giardino del Mare", "4,3", "4 km", "Maps"),
        ("Miseria & Nobiltà", "4,5", "4–5 km", "Maps"),
    ]
    r_data = [r_header] + [[Paragraph(c, styles["TabCell"]) for c in r] for r in r_rows_data]
    rt = Table(r_data, colWidths=[6.2 * cm, 1.8 * cm, 2.4 * cm, 5.8 * cm])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU_SCURO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#E8F6FA"), BIANCO]),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#D0DCE4")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(rt)
    story.append(Paragraph("* Stima da recensioni ospiti campeggio.", styles["Nota"]))
    story.append(Spacer(1, 4))

    gmaps = lambda q: f"https://www.google.com/maps/search/?api=1&query={q.replace(' ', '+')}"

    ristoranti = [
        dict(
            nome="Ristorante / Pizzeria del Camping Marina dell'Isola",
            dist="0 m · nel campeggio", voto="4,2*",
            desc="Forno a legna, pesce, pizza e vista mare (Eolie nelle giornate limpide). Comodo senza salire in centro.",
            link="https://www.campingmarinaisola.it/",
            tip="Ideale dopo la spiaggia.",
        ),
        dict(
            nome="Tropical (lido / ristorante in spiaggia)",
            dist="~300–500 m", voto="4,4",
            desc="Menu snello, pesce e verdure a km 0. Spaghetti vongole, tonno scottato, fiori di zucca in tempura (~30 €).",
            link=gmaps("Tropical Beach Tropea"),
            tip=None,
        ),
        dict(
            nome="Scacco Matto",
            dist="~550 m · Via Umberto I", voto="4,4",
            desc="Pesce tipico, involtini pesce spada con cipolla rossa, tonno alla tropeana. Familiare, ~25 €. Gambero Rosso.",
            link=gmaps("Scacco Matto Tropea Via Umberto I"),
            tip="Da provare: tonno alla tropeana.",
        ),
        dict(
            nome="La Villetta Ristorante",
            dist="~550 m · Via Indipendenza 38", voto="4,3",
            desc="Tonno scottato, alici marinate, impiattamento curato. Elegante ma cordiale.",
            link=gmaps("La Villetta Ristorante Tropea"),
            tip=None,
        ),
        dict(
            nome="Vicolo 34 – Osteria Moderna Calabrese",
            dist="~500 m · centro", voto="4,5",
            desc="Biologico e km 0, specialità calabresi rivisitate, pesce del giorno, aperitivi e vini.",
            link="https://www.vicolo34tropea.it/",
            tip=None,
        ),
        dict(
            nome="La Conchiglia da Patea",
            dist="~600 m · Largo Sannio / Piazza Ercole", voto="4,7",
            desc="Tra i meglio votati: tonno, risotto alla pescatora, antipasti, tiramisù. Servizio attento (~40–50 €).",
            link=gmaps("La Conchiglia da Patea Tropea"),
            tip="Se cerchi il voto più alto vicino al camping.",
        ),
    ]
    for r in ristoranti:
        story.append(scheda_ristorante(
            r["nome"], r["dist"], r["voto"], r["desc"], styles,
            link=r["link"], consiglio=r.get("tip"),
        ))

    story.append(PageBreak())

    ristoranti2 = [
        dict(
            nome="Incipit Restaurant",
            dist="~650 m · Largo Galluppi 17", voto="4,5",
            desc="Cantine di palazzo 1720, pietra a vista. Cucina mediterranea e tipicità calabresi. Gambero Rosso.",
            link="https://www.incipitrestaurant.com/",
            tip=None,
        ),
        dict(
            nome="Ristorante Pinturicchio",
            dist="~500–700 m · centro", voto="4,3",
            desc="Pesce fresco del giorno e cucina mediterranea. Pasta fresca e tradizione.",
            link="https://www.ristorantedipesce.tropea.vv.it/",
            tip=None,
        ),
        dict(
            nome="Pimm's",
            dist="~700 m · Largo Migliarese 14", voto="3,8",
            desc="Balconcino a picco sul mare (prenota!). Location da tramonto; cucina più mista nelle recensioni.",
            link=gmaps("Pimm's Tropea Largo Migliarese"),
            tip="Vieni per la vista; prenota il tavolo sul balcone.",
        ),
        dict(
            nome="De' Minimi – Villa Paola",
            dist="~3–4 km · auto (entro 5 km)", voto="4,6",
            desc="Gourmet in ex convento, orto proprio, Michelin/Gambero. Menu degustazione (~95 € medio).",
            link="https://deminimi.com/",
            tip="Cena speciale del soggiorno.",
        ),
        dict(
            nome="Il Giardino del Mare (Parghelia)",
            dist="~4 km · 8–10 min auto", voto="4,3",
            desc="Pesce e pizza a prezzi più contenuti (~20–30 €). Fuori dal caos del centro.",
            link=gmaps("Il Giardino del Mare Parghelia"),
            tip=None,
        ),
        dict(
            nome="Miseria & Nobiltà (Parghelia)",
            dist="~4–5 km · Via F. Cilea", voto="4,5",
            desc="Pizza top: lievitazione 72 ore, forno a legna. Segnalata Gambero Rosso.",
            link=gmaps("Miseria e Nobiltà Parghelia"),
            tip="La pizza migliore nei dintorni.",
        ),
    ]
    for r in ristoranti2:
        story.append(scheda_ristorante(
            r["nome"], r["dist"], r["voto"], r["desc"], styles,
            link=r["link"], consiglio=r.get("tip"),
        ))

    story.append(Paragraph(
        "<b>Da assaggiare:</b> cipolla rossa IGP, fileja, tonno/pesce spada alla tropeana, "
        "'nduja, tartufo di Pizzo, gelato sul Corso.",
        styles["Descrizione"],
    ))
    story.append(PageBreak())

    # LUOGHI
    story.extend(sezione_header(
        "Luoghi da visitare",
        "Dal simbolo di Tropea ai borghi della Costa degli Dei.",
        styles,
    ))
    for item in [
        ("Santuario di Santa Maria dell'Isola", "~150 m", "4,5",
         "Simbolo di Tropea. Scalinata, giardino, vista Eolie/Stromboli. Biglietto ~2 €.",
         "Imperdibile al tramonto."),
        ("Centro storico di Tropea", "~450 m", "4,5",
         "Borgo dei Borghi 2021: vicoli, palazzi, tipicità. Corso = passeggiata serale.", None),
        ("Affaccio del Cannone", "~700 m", "4,7",
         "Belvedere iconico + finestrella cartolina su Isola e spiaggia.", None),
        ("Cattedrale & Museo Diocesano", "~650 m", "4,4",
         "Duomo romanico-normanno e museo diocesano.", None),
        ("Porto di Tropea", "~1,5 km", None,
         "Tour barca Capo Vaticano/grotte ed escursioni Eolie.", "Prenota in alta stagione."),
        ("Capo Vaticano", "~11 km", "4,7",
         "Faro, belvedere, Grotticelle e calette. Giornata intera.", None),
        ("Pizzo Calabro", "~22 km", "4,5",
         "Castello Murat + tartufo di Pizzo.", "Assaggia il tartufo al caffè."),
        ("Grotte di Zungri", "~18 km", "4,4",
         "Insediamento rupestre medievale nell'entroterra.", None),
    ]:
        nome, dist, voto, desc, tip = item
        story.append(scheda(nome, dist, desc, styles, voto=voto, consiglio=tip))

    story.append(PageBreak())

    # TRAMONTI
    story.extend(sezione_header(
        "Dove vedere i tramonti",
        "Arriva 20–30 minuti prima in alta stagione.",
        styles,
    ))
    for item in [
        ("Spiaggia Marina dell'Isola (dal camping)", "0 m", None,
         "Sole dietro il Santuario. A volte allineato allo Stromboli (fine apr / fine ago).",
         "Aperitivo dal bar del camping."),
        ("Terrazza del Santuario", "~150 m", "4,5",
         "Vista dall'alto su mare, costa ed Eolie.", None),
        ("Affaccio del Cannone / Largo Villetta", "~700 m", "4,7",
         "Il classico: Isola e spiaggia dalla balconata.", "Arriva in anticipo."),
        ("Affaccio dei Sospiri (Raf Vallone)", "~600–700 m", "4,9",
         "Uno dei più romantici; vicino a Pimm's per aperitivo.", None),
        ("Largo Duomo · Galluppi · Rico Ripa", "~500–700 m", None,
         "Altri affacci; Rico Ripa è nascosto tra due palazzi (caccia al tesoro!).", None),
        ("Belvedere Capo Vaticano & Giardino degli Dei", "~11 km", "4,7",
         "Tramonti verso Sicilia/Eolie, giardino botanico a picco sul mare.", None),
        ("Tramonto in barca", "Porto ~1,5 km", None,
         "Costa, grotte e sole sull'acqua.", None),
    ]:
        nome, dist, voto, desc, tip = item
        story.append(scheda(nome, dist, desc, styles, voto=voto, consiglio=tip))

    story.append(PageBreak())

    # CHICCHE
    story.extend(sezione_header(
        "Chicche e segreti",
        "Angoli nascosti e dettagli che fanno la differenza.",
        styles,
    ))
    for item in [
        ("Grotta del Palombaro (Grotta dell'Amore)", "~50 m a nuoto dallo scoglio",
         "Spiaggia nascosta sotto il Santuario. Solo mare calmo, a nuoto/kayak.",
         "Mai da soli se il mare è mosso."),
        ("Finestrella Affaccio del Cannone", "~700 m",
         "Piccola finestra = foto iconica Isola + mare.", None),
        ("Belvedere Rico Ripa", "~600 m",
         "Affaccio nascosto in Largo Migliarese.", None),
        ("Tramonto sullo Stromboli", "spiaggia / Santuario",
         "Fenomeno raro ~2 volte l'anno (fine apr / fine ago).",
         "Chiedi in campeggio le date indicative."),
        ("Tour grotte in barca", "Porto ~1,5 km",
         "Praia i Focu, grotte, snorkeling. Spesso 35–45 €.", None),
        ("Snorkel sotto gli scogli dell'Isola", "0–200 m",
         "Fondali chiari vicino al camping. Meglio al mattino.", None),
        ("Passeggiata serale + gelato", "~450–700 m",
         "Corso Vittorio Emanuele e affacci illuminati: l'anima di Tropea.", None),
    ]:
        nome, dist, desc, tip = item
        story.append(scheda(nome, dist, desc, styles, consiglio=tip))

    story.append(Spacer(1, 6))
    story.extend(sezione_header(
        "Idee di itinerario",
        "Tre proposte dal Camping Marina dell'Isola.",
        styles,
    ))
    story.append(Paragraph("<b>Giornata 1 – A piedi:</b> Marina Isola → Santuario → pranzo Tropical/"
                           "camping → Affaccio Cannone + finestrella → tramonto Sospiri → cena "
                           "La Conchiglia / Vicolo 34 / Scacco Matto.", styles["Descrizione"]))
    story.append(Paragraph("<b>Giornata 2 – Entro 5 km:</b> Baia di Riaci (mattina) → Formicoli o "
                           "Michelino → pizza Miseria & Nobiltà o Giardino del Mare → tramonto "
                           "dal camping.", styles["Descrizione"]))
    story.append(Paragraph("<b>Giornata 3 – Speciale:</b> barca grotte/Praia i Focu, oppure "
                           "Grotticelle + Capo Vaticano, oppure De' Minimi a cena, oppure Pizzo "
                           "(tartufo).", styles["Descrizione"]))

    story.append(Spacer(1, 8))
    story.extend(sezione_header("Info utili", "Contatti e note pratiche.", styles))
    for item in [
        "<b>Camping:</b> Tel. +39 0963 61970 / +39 339 1017016 · info@campingmarinaisola.it · "
        '<link href="https://www.campingmarinaisola.it/" color="#0077A8"><u>campingmarinaisola.it</u></link>',
        "<b>Centro:</b> scalinata ~100 m dall'ingresso (~8–12 min, 100–150 gradini).",
        "<b>Stazione FS Tropea:</b> ~1 km.",
        "<b>Alta stagione:</b> prenota cene e arriva presto in spiaggia/affacci.",
        "<b>Palombaro:</b> solo mare calmo e in sicurezza.",
        "<b>Da comprare:</b> cipolla rossa IGP, 'nduja, tonno Callipo, liquori tipici.",
    ]:
        story.append(Paragraph(f"• {item}", styles["Descrizione"]))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=ACQUA, spaceAfter=6))
    story.append(Paragraph(
        "Buona vacanza! Distanze, voti e link sono indicativi. "
        "Foto: Wikimedia Commons. Verifica orari sul posto.",
        styles["Nota"],
    ))
    story.append(Paragraph(
        "Guida personale · Camping Marina dell'Isola · Tropea 2026",
        styles["Nota"],
    ))

    doc.build(story, onFirstPage=cover_page, onLaterPages=header_footer)
    print(f"PDF creato: {OUTPUT}")
    print(f"Dimensione: {os.path.getsize(OUTPUT)} bytes")


if __name__ == "__main__":
    build()
