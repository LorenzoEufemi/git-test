#!/usr/bin/env python3
"""Genera la Guida Tropea PDF con distanze da Camping Marina dell'Isola."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Colori ispirati al mare di Tropea
BLU_MARE = HexColor("#0077A8")
BLU_SCURO = HexColor("#0A3D5C")
ACQUA = HexColor("#2AA8C4")
SABBIA = HexColor("#F5E6C8")
CORALLO = HexColor("#C45C26")
VERDE = HexColor("#2D6A4F")
GRIGIO = HexColor("#4A5568")
GRIGIO_CHIARO = HexColor("#F0F4F7")
BIANCO = white

OUTPUT = "/workspace/guida-tropea/Guida_Tropea_Camping_Marina_Isola.pdf"

# Punto di riferimento
BASE = "Camping Marina dell'Isola"
BASE_ADDR = "Via Lungomare Sorrentino, 89861 Tropea (VV)"
BASE_COORDS = "38°40'43\"N · 15°53'41\"E"


def header_footer(canvas, doc):
    canvas.saveState()
    # Header band
    canvas.setFillColor(BLU_SCURO)
    canvas.rect(0, A4[1] - 1.2 * cm, A4[0], 1.2 * cm, fill=1, stroke=0)
    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.5 * cm, A4[1] - 0.75 * cm, "Guida Tropea · da Camping Marina dell'Isola")
    canvas.drawRightString(A4[0] - 1.5 * cm, A4[1] - 0.75 * cm, "Costa degli Dei · Calabria")

    # Footer
    canvas.setFillColor(BLU_SCURO)
    canvas.rect(0, 0, A4[0], 1.0 * cm, fill=1, stroke=0)
    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 0.4 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    # Full cover background
    canvas.setFillColor(BLU_SCURO)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

    # Decorative wave band
    canvas.setFillColor(ACQUA)
    canvas.rect(0, A4[1] * 0.42, A4[0], 0.4 * cm, fill=1, stroke=0)
    canvas.setFillColor(BLU_MARE)
    canvas.rect(0, A4[1] * 0.42 - 0.25 * cm, A4[0], 0.25 * cm, fill=1, stroke=0)

    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 3.5 * cm, "LA TUA GUIDA PERSONALE")

    canvas.setFont("Helvetica-Bold", 36)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 5.5 * cm, "TROPEA")

    canvas.setFont("Helvetica", 16)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 6.8 * cm, "Spiagge · Ristoranti · Luoghi da visitare")

    canvas.setFillColor(SABBIA)
    canvas.setFont("Helvetica-Oblique", 12)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 8.2 * cm, "con distanze da Camping Marina dell'Isola")

    # Box base
    canvas.setFillColor(HexColor("#0F4A6B"))
    canvas.roundRect(2.5 * cm, 4.5 * cm, A4[0] - 5 * cm, 4.2 * cm, 8, fill=1, stroke=0)
    canvas.setFillColor(ACQUA)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(A4[0] / 2, 7.8 * cm, "IL TUO PUNTO DI PARTENZA")
    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(A4[0] / 2, 6.8 * cm, "Camping Marina dell'Isola")
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(A4[0] / 2, 6.0 * cm, BASE_ADDR)
    canvas.drawCentredString(A4[0] / 2, 5.4 * cm, BASE_COORDS)
    canvas.setFont("Helvetica-Oblique", 9)
    canvas.drawCentredString(A4[0] / 2, 4.8 * cm, "Accesso diretto al mare · ai piedi di Santa Maria dell'Isola")

    canvas.setFillColor(SABBIA)
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(A4[0] / 2, 2.5 * cm, "Distanze indicative a piedi / in auto · aggiornate 2026")
    canvas.restoreState()


def make_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="TitoloSezione",
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=BLU_SCURO,
        spaceBefore=6,
        spaceAfter=10,
        leading=22,
    ))
    styles.add(ParagraphStyle(
        name="SottoTitolo",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRIGIO,
        spaceAfter=14,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="NomeLuogo",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=BLU_MARE,
        spaceBefore=8,
        spaceAfter=3,
        leading=15,
    ))
    styles.add(ParagraphStyle(
        name="Distanza",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=CORALLO,
        spaceAfter=4,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name="Descrizione",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=GRIGIO,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name="Nota",
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        textColor=GRIGIO,
        spaceAfter=4,
        leading=11,
    ))
    styles.add(ParagraphStyle(
        name="Intro",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRIGIO,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="TabCell",
        fontName="Helvetica",
        fontSize=8.5,
        textColor=GRIGIO,
        leading=11,
    ))
    styles.add(ParagraphStyle(
        name="TabHead",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=BIANCO,
        leading=11,
    ))
    styles.add(ParagraphStyle(
        name="Consiglio",
        fontName="Helvetica",
        fontSize=9,
        textColor=VERDE,
        spaceAfter=4,
        leading=12,
    ))
    return styles


def sezione_header(titolo, sottotitolo, styles):
    return [
        Paragraph(titolo, styles["TitoloSezione"]),
        HRFlowable(width="100%", thickness=2, color=ACQUA, spaceAfter=4),
        Paragraph(sottotitolo, styles["SottoTitolo"]),
    ]


def scheda(nome, distanza, desc, styles, consiglio=None):
    elems = [
        Paragraph(nome, styles["NomeLuogo"]),
        Paragraph(f"Distanza: {distanza}", styles["Distanza"]),
        Paragraph(desc, styles["Descrizione"]),
    ]
    if consiglio:
        elems.append(Paragraph(f"Consiglio: {consiglio}", styles["Consiglio"]))
    elems.append(Spacer(1, 4))
    return KeepTogether(elems)


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.5 * cm,
        title="Guida Tropea – Camping Marina dell'Isola",
        author="Guida personale Tropea",
    )

    story = []

    # Pagina 1 = solo copertina (disegnata su canvas)
    story.append(PageBreak())

    # ===== INTRO =====
    story.append(Paragraph("Benvenuto a Tropea", styles["TitoloSezione"]))
    story.append(HRFlowable(width="100%", thickness=2, color=ACQUA, spaceAfter=8))
    story.append(Paragraph(
        "Sei ospite al <b>Camping Marina dell'Isola</b>, in Via Lungomare Sorrentino, "
        "ai piedi della rupe di Tropea e del Santuario di Santa Maria dell'Isola. "
        "Hai accesso diretto al mare e, tramite la scalinata panoramica, raggiungi "
        "il centro storico in pochi minuti a piedi. Questa guida raccoglie le "
        "<b>migliori spiagge</b>, i <b>ristoranti consigliati</b> e i "
        "<b>luoghi da visitare</b>, con distanze indicative calcolate dal campeggio.",
        styles["Intro"],
    ))
    story.append(Paragraph(
        "Le distanze a piedi sono stimate dal cancello/ingresso del camping. "
        "Per le località oltre Tropea è indicata la distanza in auto (percorso più breve).",
        styles["Nota"],
    ))

    # ===== TABELLA RIEPILOGO =====
    story.append(Paragraph("Tabella distanze rapide", styles["TitoloSezione"]))
    story.append(HRFlowable(width="100%", thickness=2, color=ACQUA, spaceAfter=8))

    header = [
        Paragraph("Destinazione", styles["TabHead"]),
        Paragraph("Distanza", styles["TabHead"]),
        Paragraph("Come", styles["TabHead"]),
        Paragraph("Tempo", styles["TabHead"]),
    ]
    rows_data = [
        ("Spiaggia Marina dell'Isola", "0 m", "a piedi", "immediato"),
        ("Santuario S. Maria dell'Isola", "~150 m", "a piedi", "3–5 min"),
        ("Spiaggia della Rotonda", "~400 m", "a piedi", "5–8 min"),
        ("Centro storico / Corso", "~450 m", "a piedi (scale)", "8–12 min"),
        ("Affaccio del Cannone", "~700 m", "a piedi", "10–15 min"),
        ("Spiaggia del Cannone", "~900 m", "a piedi", "12–15 min"),
        ("Cattedrale di Tropea", "~650 m", "a piedi", "10–12 min"),
        ("Porto di Tropea", "~1,5 km", "a piedi / auto", "20 min / 5 min"),
        ("Spiaggia Passo del Cavaliere", "~1,8 km", "a piedi / auto", "25 min / 5 min"),
        ("Spiaggia dell'Occhiale", "~2,5 km", "auto / a piedi", "8 min / 30 min"),
        ("Spiaggia Michelino (Parghelia)", "~4,5 km", "auto", "10–12 min"),
        ("Capo Vaticano / Grotticelle", "~11 km", "auto", "20–25 min"),
        ("Pizzo Calabro", "~22 km", "auto", "30–35 min"),
        ("Grotte di Zungri", "~18 km", "auto", "25–30 min"),
    ]
    data = [header]
    for r in rows_data:
        data.append([Paragraph(c, styles["TabCell"]) for c in r])

    t = Table(data, colWidths=[7.2 * cm, 3.2 * cm, 3.2 * cm, 3.2 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU_SCURO),
        ("BACKGROUND", (0, 1), (-1, 1), HexColor("#E8F6FA")),
        ("ROWBACKGROUNDS", (0, 2), (-1, -1), [BIANCO, GRIGIO_CHIARO]),
        ("TEXTCOLOR", (0, 0), (-1, 0), BIANCO),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#D0DCE4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Nota: la scalinata dal lungomare al centro storico ha circa 100–150 gradini. "
        "In alternativa puoi usare la strada per il porto o un taxi/navetta.",
        styles["Nota"],
    ))

    story.append(PageBreak())

    # ===== SPIAGGE =====
    story.extend(sezione_header(
        "Le migliori spiagge",
        "Sabbia chiara, acque turchesi e scogliere: la Costa degli Dei a portata di passo (o di breve spostamento).",
        styles,
    ))

    story.append(scheda(
        "1. Spiaggia Marina dell'Isola (Mare Piccolo)",
        "~0 m · accesso diretto dal camping",
        "La spiaggia del tuo campeggio: sabbia chiara, mare cristallino e lo scoglio di "
        "Santa Maria dell'Isola come cartolina. Ideale per snorkel vicino agli scogli e "
        "per i tramonti (nelle giornate limpide si scorge lo Stromboli). Ci sono tratti "
        "liberi e lidi attrezzati.",
        styles,
        "Perfetto per la prima mattina e il tardo pomeriggio, quando c'è meno folla.",
    ))

    story.append(scheda(
        "2. Spiaggia della Rotonda (Le Roccette)",
        "~400 m a piedi · 5–8 minuti",
        "La spiaggia più fotografata di Tropea: forma a mezzaluna, vista sulla rupe del "
        "centro storico e sul Santuario. Mare di un azzurro intenso, sabbia fine. "
        "Delimitata dallo Scoglio di San Leonardo. Molto frequentata in alta stagione.",
        styles,
        "Arriva presto o scegli i giorni feriali. Ottima anche solo per una passeggiata a piedi nudi.",
    ))

    story.append(scheda(
        "3. Spiaggia del Cannone",
        "~900 m a piedi · 12–15 minuti",
        "Piccola insenatura tra lo Scoglio di San Leonardo e il porto. Meno affollata "
        "della Rotonda, atmosfera più riservata. Il nome viene da cannoni spagnoli "
        "ritrovati in zona. Accessibile dalla scalinata verso il porto.",
        styles,
        "Ideale se cerchi un angolo più tranquillo restando a Tropea.",
    ))

    story.append(scheda(
        "4. Spiaggia A Linguata / Mare Grande",
        "~1–1,5 km · 15–20 min a piedi",
        "Tratto più lungo della costa tropeana, sabbia bianca e fondali limpidissimi. "
        "Ci sono lidi attrezzati e zone libere. Buona scelta per famiglie che vogliono "
        "più spazio.",
        styles,
    ))

    story.append(scheda(
        "5. Spiaggia Passo del Cavaliere (Passu i Cavaleri)",
        "~1,8 km · 5 min in auto / ~25 min a piedi",
        "Fondale sabbioso, atmosfera più rilassata rispetto al centro. Fa parte del "
        "tratto Mare Grande. Adatta a chi vuole allontanarsi un po' dalle spiagge "
        "più turistiche sotto la rupe.",
        styles,
    ))

    story.append(scheda(
        "6. Spiaggia dell'Occhiale",
        "~2,5 km · ~8 min in auto",
        "Spiaggia più selvaggia, prende il nome dagli scogli che ricordano un paio "
        "di occhiali. Ambiente più naturale e incontaminato: perfetta per chi ama "
        "paesaggi rocciosi e snorkel.",
        styles,
        "Porta scarpe comode: l'accesso può essere un po' più impegnativo.",
    ))

    story.append(scheda(
        "7. Spiaggia di Michelino (Parghelia)",
        "~4,5 km · 10–12 min in auto",
        "A nord di Tropea, sabbia bianchissima e mare da cartolina. Una delle baie "
        "più belle della zona, spesso citata tra le perle della Costa degli Dei.",
        styles,
        "Ottima meta per una mezza giornata in alternativa alle spiagge sotto Tropea.",
    ))

    story.append(scheda(
        "8. Grotticelle & Capo Vaticano",
        "~11 km · 20–25 min in auto",
        "Tra le spiagge più belle d'Italia: sabbia fine, acque turchesi, scogliere e "
        "grotte. Capo Vaticano offre anche Praia i Focu (spesso raggiungibile via mare "
        "o con discese ripide) e belvedere spettacolari.",
        styles,
        "Consigliato un tour in barca da Tropea (~35–45 €) per vedere grotte e calette nascoste.",
    ))

    story.append(PageBreak())

    # ===== RISTORANTI =====
    story.extend(sezione_header(
        "I migliori ristoranti",
        "Pesce fresco, cipolla rossa di Tropea IGP, fileja e 'nduja: dove mangiare bene vicino al camping.",
        styles,
    ))

    story.append(scheda(
        "Ristorante / Pizzeria del Camping Marina dell'Isola",
        "0 m · dentro il campeggio",
        "Bar-ristorante-pizzeria con forno a legna e vista mare (nelle giornate limpide "
        "verso le Eolie). Piatti tipici, pesce e pizza. Comodo dopo una giornata in spiaggia, "
        "senza dover salire in centro.",
        styles,
        "Perfetta soluzione per la sera se non vuoi spostarti.",
    ))

    story.append(scheda(
        "Scacco Matto",
        "~500–600 m · centro storico · 10–12 min a piedi",
        "Cucina di pesce locale: crudi, spaghetti alle vongole, involtini di pesce spada "
        "con cipolla rossa di Tropea e tonno alla tropeana. Atmosfera familiare e "
        "prezzi accessibili (circa 25 € a persona).",
        styles,
        "Da provare: tonno alla tropeana e involtini di pesce spada.",
    ))

    story.append(scheda(
        "La Villetta Ristorante",
        "~550 m · Via Indipendenza · 10–12 min a piedi",
        "Tra i ristoranti di pesce più apprezzati in città. Tonno scottato, alici marinate, "
        "impiattamento curato e ambiente elegante ma cordiale. Fascia media/alta.",
        styles,
    ))

    story.append(scheda(
        "Vicolo 34 – Osteria Moderna Calabrese",
        "~500 m · centro storico · ~10 min a piedi",
        "Osteria moderna con ingredienti freschi, biologici e a km 0. Specialità calabresi "
        "rivisitate, pesce del giorno, aperitivi e vini regionali. Ideale per una cena "
        "più contemporanea nel cuore del borgo.",
        styles,
    ))

    story.append(scheda(
        "Ristorante Pinturicchio",
        "~500–700 m · centro storico",
        "Punto di riferimento per il pesce fresco e la cucina mediterranea. Menu legato "
        "al pescato del giorno, pasta fresca e piatti della tradizione calabrese.",
        styles,
    ))

    story.append(scheda(
        "Tropical (lido / ristorante in spiaggia)",
        "~300–500 m · zona spiaggia Rotonda / Mare Piccolo",
        "Rara eccezione tra i ristoranti di lido: menu snello, pesce e verdure a km 0. "
        "Spaghetti alle vongole, tonno scottato, frittura e fiori di zucca in tempura. "
        "Si mangia a pochi passi dal mare (~30 €).",
        styles,
        "Ottimo per un pranzo senza lasciare la spiaggia.",
    ))

    story.append(scheda(
        "De' Minimi – Villa Paola",
        "~3–4 km · pochi minuti in auto",
        "Esperienza gourmet in dimora storica: menu degustazione e bistrot. Da provare "
        "in terrazza la «Tropeana» (insalata dell'orto, cipolla rossa in agrodolce, "
        "tonno Callipo, pomodori secchi e peperoncino).",
        styles,
        "Per una cena speciale durante il soggiorno.",
    ))

    story.append(Paragraph(
        "<b>Cosa assaggiare assolutamente:</b> cipolla rossa di Tropea IGP (anche cruda), "
        "fileja (pasta tipica), tonno / pesce spada alla tropeana, 'nduja, gelato o "
        "granita nei bar del Corso Vittorio Emanuele.",
        styles["Descrizione"],
    ))

    story.append(PageBreak())

    # ===== LUOGHI DA VISITARE =====
    story.extend(sezione_header(
        "Luoghi da visitare",
        "Dal simbolo di Tropea ai borghi e alle meraviglie della Costa degli Dei.",
        styles,
    ))

    story.append(scheda(
        "Santuario di Santa Maria dell'Isola",
        "~150 m · 3–5 minuti a piedi (scalinata)",
        "Il simbolo di Tropea: chiesa su uno scoglio di arenaria un tempo circondato "
        "dal mare. Scalinata panoramica scavata nella roccia, giardino mediterraneo e "
        "terrazza con vista sulla costa e, con cielo limpido, sulle Eolie e lo Stromboli. "
        "Ingresso con biglietto (circa 2 €).",
        styles,
        "Imperdibile al tramonto. Da qui parte anche la processione marina del 15 agosto.",
    ))

    story.append(scheda(
        "Centro storico di Tropea",
        "~450 m · 8–12 min via scalinata",
        "Borgo a picco sul mare (Borgo dei Borghi 2021): vicoli stretti, palazzi nobiliari, "
        "negozi di prodotti tipici e gelaterie. Il Corso Vittorio Emanuele è il cuore "
        "della passeggiata serale.",
        styles,
        "Salì a piedi la sera: luci, gelato e vista mare.",
    ))

    story.append(scheda(
        "Affaccio del Cannone",
        "~700 m · 10–15 min a piedi",
        "Uno dei belvedere più belli d'Italia: dal balcone a picco sul mare vedi la "
        "spiaggia della Rotonda, lo Scoglio di San Leonardo e Santa Maria dell'Isola. "
        "Si trova al termine del Corso Vittorio Emanuele.",
        styles,
        "Tappa obbligata per le foto e per capire perché Tropea è chiamata Perla del Tirreno.",
    ))

    story.append(scheda(
        "Cattedrale di Maria Santissima di Romania & Museo Diocesano",
        "~650 m · 10–12 min a piedi",
        "Duomo romanico-normanno nel centro storico, con opere d'arte e storia locale. "
        "Il Museo Diocesano arricchisce la visita con reperti e tesori religiosi.",
        styles,
    ))

    story.append(scheda(
        "Largo Villetta e gli «affacci»",
        "~500–700 m",
        "Oltre all'Affaccio del Cannone, Tropea offre diverse terrazze panoramiche "
        "(«affacci») sulla costa. Largo Villetta è tra i più suggestivi per guardare "
        "il mare e le scogliere.",
        styles,
    ))

    story.append(scheda(
        "Porto di Tropea",
        "~1,5 km · 5 min in auto / ~20 min a piedi",
        "Punto di partenza per tour in barca verso Capo Vaticano, grotte e calette, "
        "e per escursioni giornaliere alle Isole Eolie (Stromboli, Lipari, Vulcano).",
        styles,
        "Prenota i tour in anticipo in alta stagione.",
    ))

    story.append(scheda(
        "Capo Vaticano (Ricadi)",
        "~11 km · 20–25 min in auto",
        "Promontorio sacro già in epoca greca: faro, belvedere, spiagge da sogno "
        "(Grotticelle, Formicoli, Santa Maria) e calette come Praia i Focu. Ideale "
        "per una giornata intera fuori dal campeggio.",
        styles,
    ))

    story.append(scheda(
        "Pizzo Calabro",
        "~22 km · 30–35 min in auto",
        "Borgo famoso per il Castello Murat, il centro storico e soprattutto la "
        "<b>tartufo di Pizzo</b> (gelato farcito). Bella combinazione mare + dolce tipico.",
        styles,
        "Non tornare senza aver assaggiato un tartufo al caffè!",
    ))

    story.append(scheda(
        "Grotte di Zungri («Sbariati»)",
        "~18 km · 25–30 min in auto",
        "Insediamento rupestre unico: grotte scavate nella roccia abitate sin dal Medioevo. "
        "Un'escursione diversa dal mare, tra storia e paesaggio dell'entroterra vibonese.",
        styles,
    ))

    story.append(PageBreak())

    # ===== ITINERARI =====
    story.extend(sezione_header(
        "Idee di itinerario dal camping",
        "Tre proposte pratiche partendo da Camping Marina dell'Isola.",
        styles,
    ))

    story.append(Paragraph("Giornata 1 – Tutto a piedi (senza auto)", styles["NomeLuogo"]))
    story.append(Paragraph(
        "Mattina: bagno alla <b>Marina dell'Isola</b> (0 m) → visita al "
        "<b>Santuario</b> (~150 m) → pranzo al Tropical o al ristorante del camping. "
        "Pomeriggio: salita al <b>centro storico</b>, Affaccio del Cannone, Cattedrale, "
        "shopping tipico. Sera: cena in centro (Scacco Matto / Vicolo 34 / La Villetta) "
        "e discesa al camping con vista notturna sul mare.",
        styles["Descrizione"],
    ))

    story.append(Paragraph("Giornata 2 – Spiagge alternative", styles["NomeLuogo"]))
    story.append(Paragraph(
        "Mattina: auto verso <b>Michelino</b> (4,5 km) o <b>Occhiale</b> (2,5 km). "
        "Pomeriggio: ritorno e relax alla Rotonda. Oppure giornata intera a "
        "<b>Capo Vaticano / Grotticelle</b> (11 km) con belvedere e calette.",
        styles["Descrizione"],
    ))

    story.append(Paragraph("Giornata 3 – Mare + cultura / Eolie", styles["NomeLuogo"]))
    story.append(Paragraph(
        "Opzione A: tour in barca dal <b>porto</b> (1,5 km) verso grotte e Capo Vaticano. "
        "Opzione B: escursione alle <b>Eolie</b> (giornata intera). "
        "Opzione C: <b>Pizzo</b> (tartufo + castello) e/o <b>Grotte di Zungri</b>.",
        styles["Descrizione"],
    ))

    story.append(Spacer(1, 12))
    story.extend(sezione_header(
        "Info utili",
        "Piccoli consigli pratici per il tuo soggiorno.",
        styles,
    ))

    info_items = [
        "<b>Camping:</b> Via Lungomare Sorrentino, Tropea (VV) · Tel. +39 0963 61970 / +39 339 1017016 · info@campingmarinaisola.it",
        "<b>Centro storico:</b> scalinata panoramica a ~100 m dall'ingresso del camping (circa 8–12 minuti a piedi).",
        "<b>Stazione FS Tropea:</b> circa 1 km — comoda per treni regionali verso Pizzo, Lamezia, Capo Vaticano/Ricadi.",
        "<b>Alta stagione (lug–ago):</b> spiagge molto affollate; meglio arrivare al mattino presto.",
        "<b>Cosa portare:</b> scarpe comode per le scale, maschera da snorkel, crema solare, bottiglia d'acqua.",
        "<b>Specialità da comprare:</b> cipolla rossa IGP, 'nduja, tonno Callipo, liquori e dolci tipici.",
    ]
    for item in info_items:
        story.append(Paragraph(f"• {item}", styles["Descrizione"]))

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=ACQUA, spaceAfter=8))
    story.append(Paragraph(
        "Buona vacanza a Tropea! Tutte le distanze sono indicative e possono variare "
        "in base al percorso scelto (scale, lungomare, strada carrozzabile). "
        "Verifica orari di aperture e biglietti sul posto.",
        styles["Nota"],
    ))
    story.append(Paragraph(
        "Documento generato come guida personale · Camping Marina dell'Isola · Tropea 2026",
        styles["Nota"],
    ))

    def first_page(canvas, doc):
        cover_page(canvas, doc)

    def later_pages(canvas, doc):
        header_footer(canvas, doc)

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    print(f"PDF creato: {OUTPUT}")


if __name__ == "__main__":
    build()
