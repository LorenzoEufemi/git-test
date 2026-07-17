#!/usr/bin/env python3
"""Genera la Guida Tropea PDF con distanze da Camping Marina dell'Isola."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable,
)

BLU_MARE = HexColor("#0077A8")
BLU_SCURO = HexColor("#0A3D5C")
ACQUA = HexColor("#2AA8C4")
SABBIA = HexColor("#F5E6C8")
CORALLO = HexColor("#C45C26")
VERDE = HexColor("#2D6A4F")
GRIGIO = HexColor("#4A5568")
ORO = HexColor("#B8860B")
BIANCO = white

OUTPUT = "/workspace/guida-tropea/Guida_Tropea_Camping_Marina_Isola.pdf"
BASE_ADDR = "Via Lungomare Sorrentino, 89861 Tropea (VV)"
BASE_COORDS = "38°40'43\"N · 15°53'41\"E"


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
    canvas.setFillColor(ACQUA)
    canvas.rect(0, A4[1] * 0.42, A4[0], 0.4 * cm, fill=1, stroke=0)
    canvas.setFillColor(BLU_MARE)
    canvas.rect(0, A4[1] * 0.42 - 0.25 * cm, A4[0], 0.25 * cm, fill=1, stroke=0)

    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 3.5 * cm, "LA TUA GUIDA PERSONALE")
    canvas.setFont("Helvetica-Bold", 36)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 5.5 * cm, "TROPEA")
    canvas.setFont("Helvetica", 14)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 6.8 * cm, "Spiagge · Ristoranti · Tramonti · Chicche")
    canvas.setFillColor(SABBIA)
    canvas.setFont("Helvetica-Oblique", 12)
    canvas.drawCentredString(A4[0] / 2, A4[1] - 8.0 * cm, "con distanze e voti da Camping Marina dell'Isola")

    canvas.setFillColor(HexColor("#0F4A6B"))
    canvas.roundRect(2.5 * cm, 4.2 * cm, A4[0] - 5 * cm, 4.5 * cm, 8, fill=1, stroke=0)
    canvas.setFillColor(ACQUA)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(A4[0] / 2, 8.0 * cm, "IL TUO PUNTO DI PARTENZA")
    canvas.setFillColor(BIANCO)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(A4[0] / 2, 7.0 * cm, "Camping Marina dell'Isola")
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(A4[0] / 2, 6.2 * cm, BASE_ADDR)
    canvas.drawCentredString(A4[0] / 2, 5.6 * cm, BASE_COORDS)
    canvas.setFont("Helvetica-Oblique", 9)
    canvas.drawCentredString(A4[0] / 2, 4.9 * cm, "Accesso diretto al mare · ai piedi di Santa Maria dell'Isola")
    canvas.setFillColor(SABBIA)
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(A4[0] / 2, 2.3 * cm, "Distanze indicative · voti /5 da Google (indicativi 2025–2026)")
    canvas.restoreState()


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitoloSezione", fontName="Helvetica-Bold", fontSize=17,
        textColor=BLU_SCURO, spaceBefore=4, spaceAfter=8, leading=20,
    ))
    styles.add(ParagraphStyle(
        name="SottoTitolo", fontName="Helvetica", fontSize=9.5,
        textColor=GRIGIO, spaceAfter=10, leading=13,
    ))
    styles.add(ParagraphStyle(
        name="NomeLuogo", fontName="Helvetica-Bold", fontSize=11,
        textColor=BLU_MARE, spaceBefore=6, spaceAfter=2, leading=14,
    ))
    styles.add(ParagraphStyle(
        name="Distanza", fontName="Helvetica-Bold", fontSize=9,
        textColor=CORALLO, spaceAfter=2, leading=11,
    ))
    styles.add(ParagraphStyle(
        name="Voto", fontName="Helvetica-Bold", fontSize=9,
        textColor=ORO, spaceAfter=3, leading=11,
    ))
    styles.add(ParagraphStyle(
        name="Descrizione", fontName="Helvetica", fontSize=9,
        textColor=GRIGIO, alignment=TA_JUSTIFY, spaceAfter=4, leading=12,
    ))
    styles.add(ParagraphStyle(
        name="Nota", fontName="Helvetica-Oblique", fontSize=8,
        textColor=GRIGIO, spaceAfter=4, leading=10,
    ))
    styles.add(ParagraphStyle(
        name="Intro", fontName="Helvetica", fontSize=9.5,
        textColor=GRIGIO, alignment=TA_JUSTIFY, spaceAfter=10, leading=13,
    ))
    styles.add(ParagraphStyle(
        name="TabCell", fontName="Helvetica", fontSize=8,
        textColor=GRIGIO, leading=10,
    ))
    styles.add(ParagraphStyle(
        name="TabHead", fontName="Helvetica-Bold", fontSize=8.5,
        textColor=BIANCO, leading=10,
    ))
    styles.add(ParagraphStyle(
        name="Consiglio", fontName="Helvetica", fontSize=8.5,
        textColor=VERDE, spaceAfter=3, leading=11,
    ))
    return styles


def sezione_header(titolo, sottotitolo, styles):
    return [
        Paragraph(titolo, styles["TitoloSezione"]),
        HRFlowable(width="100%", thickness=2, color=ACQUA, spaceAfter=4),
        Paragraph(sottotitolo, styles["SottoTitolo"]),
    ]


def scheda(nome, distanza, desc, styles, voto=None, consiglio=None):
    elems = [Paragraph(nome, styles["NomeLuogo"])]
    if voto is not None:
        elems.append(Paragraph(
            f"Voto: {voto}/5  ·  Distanza: {distanza}",
            styles["Voto"],
        ))
    else:
        elems.append(Paragraph(f"Distanza: {distanza}", styles["Distanza"]))
    elems.append(Paragraph(desc, styles["Descrizione"]))
    if consiglio:
        elems.append(Paragraph(f"Consiglio: {consiglio}", styles["Consiglio"]))
    elems.append(Spacer(1, 3))
    return KeepTogether(elems)


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.8 * cm, bottomMargin=1.5 * cm,
        title="Guida Tropea – Camping Marina dell'Isola",
        author="Guida personale Tropea",
    )
    story = []
    story.append(PageBreak())

    story.append(Paragraph("Benvenuto a Tropea", styles["TitoloSezione"]))
    story.append(HRFlowable(width="100%", thickness=2, color=ACQUA, spaceAfter=8))
    story.append(Paragraph(
        "Sei ospite al <b>Camping Marina dell'Isola</b>, in Via Lungomare Sorrentino, "
        "ai piedi della rupe e del Santuario di Santa Maria dell'Isola. "
        "Questa guida raccoglie spiagge, <b>ristoranti entro circa 5 km</b> con "
        "<b>voti /5</b> (indicativi da Google), luoghi da visitare, "
        "<b>posti per i tramonti</b> e <b>chicche</b> da non perdere.",
        styles["Intro"],
    ))
    story.append(Paragraph(
        "Nota sui voti: medie indicative da Google/recensioni pubbliche (2025–2026); "
        "possono variare. Prenota in alta stagione.",
        styles["Nota"],
    ))

    story.append(Paragraph("Tabella distanze rapide", styles["TitoloSezione"]))
    story.append(HRFlowable(width="100%", thickness=2, color=ACQUA, spaceAfter=6))
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
        ("Porto di Tropea", "~1,5 km", "a piedi / auto", "20 / 5 min"),
        ("Spiaggia Michelino (Parghelia)", "~4,5 km", "auto", "10–12 min"),
        ("Capo Vaticano / Grotticelle", "~11 km", "auto", "20–25 min"),
        ("Pizzo Calabro", "~22 km", "auto", "30–35 min"),
    ]
    data = [header] + [[Paragraph(c, styles["TabCell"]) for c in r] for r in rows_data]
    t = Table(data, colWidths=[7.0 * cm, 3.2 * cm, 3.2 * cm, 3.2 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU_SCURO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#E8F6FA"), BIANCO]),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#D0DCE4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(PageBreak())

    # SPIAGGE
    story.extend(sezione_header(
        "Le migliori spiagge",
        "Sabbia chiara e acque turchesi a portata di passo (o breve spostamento).",
        styles,
    ))
    story.append(scheda(
        "1. Spiaggia Marina dell'Isola (Mare Piccolo)",
        "~0 m · accesso diretto dal camping",
        "La spiaggia del campeggio: sabbia chiara, mare cristallino e lo scoglio di "
        "Santa Maria dell'Isola. Ideale per snorkel e tramonti (con cielo limpido si "
        "scorge lo Stromboli). Tratti liberi e lidi.",
        styles, consiglio="Meglio al mattino presto o nel tardo pomeriggio.",
    ))
    story.append(scheda(
        "2. Spiaggia della Rotonda (Le Roccette)",
        "~400 m · 5–8 min a piedi",
        "La più fotografata: mezzaluna sotto la rupe, vista sul Santuario e sullo "
        "Scoglio di San Leonardo. Mare intenso, sabbia fine. Molto frequentata in agosto.",
        styles,
    ))
    story.append(scheda(
        "3. Spiaggia del Cannone",
        "~900 m · 12–15 min a piedi",
        "Piccola insenatura verso il porto, meno affollata. Nome dai cannoni spagnoli "
        "ritrovati in zona. Atmosfera più riservata.",
        styles,
    ))
    story.append(scheda(
        "4. Spiaggia A Linguata / Mare Grande",
        "~1–1,5 km",
        "Tratto più lungo, sabbia bianca e fondali limpidissimi. Buona per famiglie "
        "che vogliono più spazio (lidi + zone libere).",
        styles,
    ))
    story.append(scheda(
        "5. Spiaggia Passo del Cavaliere",
        "~1,8 km · 5 min in auto",
        "Fondale sabbioso, atmosfera più rilassata rispetto alle spiagge sotto la rupe.",
        styles,
    ))
    story.append(scheda(
        "6. Spiaggia dell'Occhiale",
        "~2,5 km · ~8 min in auto",
        "Più selvaggia: scogli a forma di occhiali, snorkel e paesaggio roccioso.",
        styles, consiglio="Scarpe comode: accesso un po' più impegnativo.",
    ))
    story.append(scheda(
        "7. Spiaggia di Michelino (Parghelia)",
        "~4,5 km · 10–12 min in auto",
        "Sabbia bianchissima e mare da cartolina. Una delle baie più belle entro 5 km.",
        styles,
    ))
    story.append(scheda(
        "8. Grotticelle & Capo Vaticano",
        "~11 km · oltre i 5 km · 20–25 min in auto",
        "Tra le spiagge più belle d'Italia. Consigliato anche tour in barca dal porto "
        "di Tropea (~35–45 €) per grotte e calette (Praia i Focu).",
        styles,
    ))
    story.append(PageBreak())

    # RISTORANTI
    story.extend(sezione_header(
        "Ristoranti entro circa 5 km",
        "Dal campeggio al centro e fino a Parghelia. Voti /5 indicativi (Google). "
        "Ordinati per distanza approssimativa.",
        styles,
    ))

    r_header = [
        Paragraph("Ristorante", styles["TabHead"]),
        Paragraph("Voto", styles["TabHead"]),
        Paragraph("Distanza", styles["TabHead"]),
        Paragraph("Tipo", styles["TabHead"]),
    ]
    r_rows = [
        ("Ristorante/Pizzeria del Camping", "4,2*", "~0 m", "Pizza · pesce · vista mare"),
        ("Tropical (lido)", "4,4", "~400 m", "Pesce in spiaggia"),
        ("Scacco Matto", "4,4", "~550 m", "Pesce tipico · prezzi ok"),
        ("La Villetta", "4,3", "~550 m", "Pesce · elegante"),
        ("Vicolo 34", "4,5", "~500 m", "Osteria moderna calabrese"),
        ("La Conchiglia da Patea", "4,7", "~600 m", "Italiana · Piazza Ercole"),
        ("Incipit Restaurant", "4,5", "~650 m", "Mediterranea · pietra"),
        ("Pinturicchio", "4,3", "~600 m", "Pesce fresco"),
        ("Pimm's", "3,8", "~700 m", "Vista mare · romantico"),
        ("De' Minimi (Villa Paola)", "4,6", "~3–4 km", "Gourmet · Michelin"),
        ("Il Giardino del Mare", "4,3", "~4 km", "Pesce · Parghelia"),
        ("Miseria & Nobiltà", "4,5", "~4–5 km", "Pizza 72h · Parghelia"),
    ]
    r_data = [r_header] + [[Paragraph(c, styles["TabCell"]) for c in r] for r in r_rows]
    rt = Table(r_data, colWidths=[5.8 * cm, 1.6 * cm, 2.6 * cm, 6.0 * cm])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU_SCURO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#E8F6FA"), BIANCO]),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#D0DCE4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(rt)
    story.append(Paragraph(
        "* Voto stimato da recensioni ospiti del campeggio (non sempre presente su Google).",
        styles["Nota"],
    ))
    story.append(Spacer(1, 6))

    story.append(scheda(
        "Ristorante / Pizzeria del Camping Marina dell'Isola",
        "0 m · dentro il campeggio",
        "Bar-ristorante-pizzeria con forno a legna e vista mare (nelle giornate limpide "
        "verso le Eolie). Piatti tipici, pesce e pizza. Comodo senza salire in centro.",
        styles, voto="4,2*", consiglio="Ideale dopo la spiaggia o se non vuoi spostarti.",
    ))
    story.append(scheda(
        "Tropical (lido / ristorante in spiaggia)",
        "~300–500 m · zona Rotonda / Mare Piccolo",
        "Rara eccezione tra i lidi: menu snello, pesce e verdure a km 0. Spaghetti alle "
        "vongole, tonno scottato, fiori di zucca in tempura. Si mangia a pochi passi dal mare (~30 €).",
        styles, voto="4,4",
    ))
    story.append(scheda(
        "Scacco Matto",
        "~500–600 m · centro · 10–12 min a piedi",
        "Pesce locale, crudi, spaghetti alle vongole, involtini di pesce spada con "
        "cipolla rossa e tonno alla tropeana. Atmosfera familiare, circa 25 € a persona. "
        "Segnalato anche dal Gambero Rosso.",
        styles, voto="4,4", consiglio="Da provare: tonno alla tropeana.",
    ))
    story.append(scheda(
        "La Villetta Ristorante",
        "~550 m · Via Indipendenza",
        "Tra i pesce-ristoranti più apprezzati: tonno scottato, alici marinate, "
        "impiattamento curato. Ambiente elegante ma cordiale. Fascia media/alta.",
        styles, voto="4,3",
    ))
    story.append(scheda(
        "Vicolo 34 – Osteria Moderna Calabrese",
        "~500 m · centro storico",
        "Ingredienti freschi, biologici e a km 0. Specialità calabresi rivisitate, "
        "pesce del giorno, aperitivi e vini regionali. Cena contemporanea nel borgo.",
        styles, voto="4,5",
    ))
    story.append(scheda(
        "La Conchiglia da Patea",
        "~600 m · Largo Sannio / zona Piazza Ercole",
        "Uno dei meglio votati in città: tonno, risotto alla pescatora, antipasti "
        "e dolci (tiramisù, cheesecake). Servizio attento, atmosfera calma. "
        "Circa 40–50 € a persona.",
        styles, voto="4,7", consiglio="Ottima scelta se cerchi il voto più alto vicino.",
    ))
    story.append(PageBreak())

    story.append(scheda(
        "Incipit Restaurant",
        "~650 m · Largo Galluppi 17",
        "Nelle cantine di un palazzo del 1720: pietra a vista, cotto, spazi esterni. "
        "Cucina mediterranea e prodotti tipici calabresi. Carta dei vini curata. "
        "Consigliato da Gambero Rosso.",
        styles, voto="4,5",
    ))
    story.append(scheda(
        "Ristorante Pinturicchio",
        "~500–700 m · centro storico",
        "Punto di riferimento per pesce fresco e cucina mediterranea. Menu legato "
        "al pescato del giorno e pasta fresca.",
        styles, voto="4,3",
    ))
    story.append(scheda(
        "Pimm's",
        "~700 m · Largo Migliarese 14 · Affaccio",
        "Antico palazzo con balconcino a picco sul mare (molto ambito: prenota!). "
        "Pesce in combinazioni non banali e vini calabresi. Location da tramonto "
        "romantico; le recensioni sulla cucina sono più miste rispetto alla vista.",
        styles, voto="3,8", consiglio="Vieni per la vista al tramonto; prenota il tavolo sul balcone.",
    ))
    story.append(scheda(
        "De' Minimi – Villa Paola",
        "~3–4 km · pochi minuti in auto (entro 5 km)",
        "Gourmet in ex convento: orto di proprietà, menu degustazione, cocktail bar. "
        "Segnalato Guida Michelin. Da provare la «Tropeana» in terrazza. Prezzo alto "
        "(~95 € medio TheFork).",
        styles, voto="4,6", consiglio="Per una cena speciale del soggiorno.",
    ))
    story.append(scheda(
        "Il Giardino del Mare (Parghelia)",
        "~4 km · 8–10 min in auto",
        "Pesce, pizza e antipasti a prezzi più contenuti (~20–30 €). Atmosfera rilassata "
        "fuori dal caos del centro di Tropea.",
        styles, voto="4,3",
    ))
    story.append(scheda(
        "Miseria & Nobiltà (Parghelia)",
        "~4–5 km · Via F. Cilea",
        "Pizzeria top della zona: farine selezionate, lievitazione 72 ore, forno a legna. "
        "Anche piatti tradizionali. Segnalata dal Gambero Rosso.",
        styles, voto="4,5", consiglio="Se vuoi la pizza migliore nei dintorni.",
    ))
    story.append(Paragraph(
        "<b>Da assaggiare:</b> cipolla rossa IGP, fileja, tonno/pesce spada alla tropeana, "
        "'nduja, tartufo di Pizzo (escursione), gelato/granita sul Corso.",
        styles["Descrizione"],
    ))
    story.append(PageBreak())

    # LUOGHI
    story.extend(sezione_header(
        "Luoghi da visitare",
        "Dal simbolo di Tropea ai borghi della Costa degli Dei.",
        styles,
    ))
    story.append(scheda(
        "Santuario di Santa Maria dell'Isola",
        "~150 m · 3–5 min (scalinata)",
        "Simbolo di Tropea: chiesa sullo scoglio, giardino e terrazza con vista Eolie/"
        "Stromboli. Biglietto circa 2 €.",
        styles, voto="4,5", consiglio="Imperdibile al tramonto.",
    ))
    story.append(scheda(
        "Centro storico di Tropea",
        "~450 m · 8–12 min via scalinata",
        "Borgo dei Borghi 2021: vicoli, palazzi, tipicità e gelaterie. "
        "Corso Vittorio Emanuele = passeggiata serale.",
        styles, voto="4,5",
    ))
    story.append(scheda(
        "Affaccio del Cannone (Largo Villetta)",
        "~700 m · 10–15 min",
        "Belvedere iconico: Rotonda, Scoglio San Leonardo e Isola dall'alto. "
        "Anche una «finestrella» che inquadra la cartolina.",
        styles, voto="4,7",
    ))
    story.append(scheda(
        "Cattedrale & Museo Diocesano",
        "~650 m",
        "Duomo romanico-normanno e museo con tesori religiosi locali.",
        styles, voto="4,4",
    ))
    story.append(scheda(
        "Porto di Tropea",
        "~1,5 km",
        "Partenza tour barca (Capo Vaticano, grotte) e escursioni Eolie.",
        styles, consiglio="Prenota i tour in alta stagione.",
    ))
    story.append(scheda(
        "Capo Vaticano (Ricadi)",
        "~11 km · 20–25 min auto",
        "Faro, belvedere, Grotticelle e calette. Giornata intera consigliata.",
        styles,
    ))
    story.append(scheda(
        "Pizzo Calabro",
        "~22 km · 30–35 min auto",
        "Castello Murat + tartufo di Pizzo (gelato farcito). Combo mare + dolce.",
        styles, consiglio="Assaggia il tartufo al caffè.",
    ))
    story.append(scheda(
        "Grotte di Zungri («Sbariati»)",
        "~18 km · 25–30 min auto",
        "Insediamento rupestre: grotte abitate sin dal Medioevo. Escursione diversa dal mare.",
        styles,
    ))
    story.append(PageBreak())

    # TRAMONTI
    story.extend(sezione_header(
        "Dove vedere i tramonti",
        "I «tramonti di Ulisse»: sole che cala sul Tirreno, a volte sullo Stromboli. "
        "Arriva 20–30 minuti prima in alta stagione.",
        styles,
    ))
    story.append(scheda(
        "Spiaggia Marina dell'Isola (dal camping)",
        "0 m",
        "Il tramonto più comodo: sole dietro il Santuario, colori su sabbia e scoglio. "
        "Nelle giornate limpide (soprattutto fine aprile / fine agosto) puoi vedere "
        "il sole «baciare» lo Stromboli.",
        styles, consiglio="Resta in spiaggia con un aperitivo dal bar del camping.",
    ))
    story.append(scheda(
        "Terrazza del Santuario di Santa Maria dell'Isola",
        "~150 m",
        "Vista dall'alto su mare, costa e, con cielo limpido, Eolie. Magico e fotografico.",
        styles, voto="4,5",
    ))
    story.append(scheda(
        "Affaccio del Cannone / Largo Villetta",
        "~700 m",
        "Il classico: Isola e spiaggia inquadrate dalla balconata. Molto frequentato "
        "all'ora d'oro: arriva in anticipo.",
        styles, voto="4,7",
    ))
    story.append(scheda(
        "Affaccio dei Sospiri (Raf Vallone / Largo Migliarese)",
        "~600–700 m · fine Corso",
        "Uno dei più romantici: vista sulla costa, sulle spiagge e sull'Isola in primo piano. "
        "Vicino a Pimm's per un aperitivo con vista.",
        styles, voto="4,9",
    ))
    story.append(scheda(
        "Largo Duomo · Largo Galluppi · Belvedere Rico Ripa",
        "~500–700 m · centro",
        "Altri affacci storici: Duomo (verso il porto), Galluppi/Carabinieri, e il "
        "piccolo Rico Ripa (nascosto tra due palazzi in Largo Migliarese — una caccia al tesoro!).",
        styles,
    ))
    story.append(scheda(
        "Spiaggia della Rotonda",
        "~400 m",
        "Sole che cala dietro l'Isola, vista dalla sabbia. Alternativa al camping "
        "restando in basso.",
        styles,
    ))
    story.append(scheda(
        "Belvedere / Faro Capo Vaticano & Giardino degli Dei",
        "~11 km",
        "Tramonti diversi, verso Sicilia/Eolie. Il Giardino degli Dei (botaniche "
        "mediterranee a picco sul mare) è spettacolare al calar del sole.",
        styles, consiglio="Combina con una giornata spiaggia a Grotticelle.",
    ))
    story.append(scheda(
        "Tramonto in barca",
        "Partenza porto ~1,5 km",
        "Tour serali o privati: costa, grotte e sole sull'acqua. Esperienza diversa "
        "dagli affacci del borgo.",
        styles,
    ))
    story.append(PageBreak())

    # CHICCHE
    story.extend(sezione_header(
        "Chicche e segreti da non perdere",
        "Angoli nascosti, esperienze e dettagli che fanno la differenza.",
        styles,
    ))
    story.append(scheda(
        "Grotta del Palombaro (Grotta dell'Amore)",
        "~100–200 m a nuoto dallo scoglio · dal camping ~5 min a piedi fino alla spiaggia",
        "Spiaggia nascosta sotto il giardino del Santuario: sabbia fine, acque turchesi, "
        "raggiungibile a nuoto (~50 m) o in kayak/pedalò con mare calmo. "
        "Nome dai colombi (palumbi) o dai tuffi «a pettu i palumbu».",
        styles, consiglio="Solo con mare piatto e se sai nuotare bene. Mai da soli se il mare è mosso.",
    ))
    story.append(scheda(
        "La finestrella dell'Affaccio del Cannone",
        "~700 m",
        "Oltre la balconata principale, cerca la piccola finestra che apre sulla "
        "cartolina perfetta di Isola + mare. Foto iconica.",
        styles,
    ))
    story.append(scheda(
        "Belvedere Rico Ripa (affaccio nascosto)",
        "~600 m",
        "Piccolo balcone tra due palazzi in Largo Migliarese. Pochi lo trovano: "
        "è la «caccia al tesoro» degli affacci di Tropea.",
        styles,
    ))
    story.append(scheda(
        "Scalinata panoramica camping → centro",
        "~100 m dall'ingresso",
        "Non solo collegamento: la salita stessa è un panorama continuo su mare e Isola. "
        "Al tramonto e di sera è parte dell'esperienza.",
        styles,
    ))
    story.append(scheda(
        "Tramonto sullo Stromboli (fenomeno raro)",
        "Dalla spiaggia o dal Santuario",
        "Due volte l'anno circa (fine aprile e fine agosto), con cielo limpido, "
        "il sole tramonta allineato allo Stromboli: evento molto fotografato dalla Costa degli Dei.",
        styles, consiglio="Chiedi in campeggio le date indicative del periodo del tuo soggiorno.",
    ))
    story.append(scheda(
        "Tour grotte e calette in barca",
        "Porto ~1,5 km",
        "Oltre Capo Vaticano: grotte marine, Praia i Focu, snorkeling. "
        "Spesso 35–45 € a persona in tour di gruppo.",
        styles,
    ))
    story.append(scheda(
        "Cipolla rossa & street food tipico",
        "Centro ~450 m",
        "Assaggia la cipolla cruda (è dolce!), fileja nei ristoranti, e cerca "
        "negozi di tipicità sul Corso per 'nduja, tonno Callipo e liquori.",
        styles,
    ))
    story.append(scheda(
        "Passeggiata serale sul Corso + gelato",
        "~450–700 m",
        "Dopo cena: Corso Vittorio Emanuele, Piazza Ercole, affacci illuminati. "
        "L'anima di Tropea è la sera, non solo la spiaggia.",
        styles,
    ))
    story.append(scheda(
        "Panchina panoramica / lungomare",
        "~300–800 m zona mare",
        "Sul lungomare e nelle zone vicine alla Marina ci sono punti per sedersi "
        "con vista Isola: ideali per foto e pausa senza salire in centro.",
        styles,
    ))
    story.append(scheda(
        "Snorkel sotto gli scogli dell'Isola",
        "0–200 m dalla spiaggia del camping",
        "Fondali chiari e vita marina vicino agli scogli: maschera e boccaglio bastano. "
        "Meglio al mattino, mare calmo.",
        styles,
    ))

    story.append(Spacer(1, 8))
    story.extend(sezione_header(
        "Idee di itinerario",
        "Tre proposte pratiche dal Camping Marina dell'Isola.",
        styles,
    ))
    story.append(Paragraph("Giornata 1 – Tutto a piedi", styles["NomeLuogo"]))
    story.append(Paragraph(
        "Bagno Marina Isola → Santuario → pranzo Tropical o camping → pomeriggio "
        "centro, Affaccio Cannone, finestrella, Cattedrale → tramonto Affaccio "
        "Sospiri o Cannone → cena La Conchiglia / Vicolo 34 / Scacco Matto.",
        styles["Descrizione"],
    ))
    story.append(Paragraph("Giornata 2 – Entro 5 km", styles["NomeLuogo"]))
    story.append(Paragraph(
        "Mattina Michelino o Occhiale → pranzo Giardino del Mare o pizza Miseria "
        "& Nobiltà (Parghelia) → rientro, snorkel/Palombaro se mare calmo → "
        "tramonto dalla spiaggia del camping.",
        styles["Descrizione"],
    ))
    story.append(Paragraph("Giornata 3 – Speciale", styles["NomeLuogo"]))
    story.append(Paragraph(
        "Tour barca grotte/Capo Vaticano, oppure cena gourmet a De' Minimi, "
        "oppure Pizzo (tartufo) + rientro al tramonto sugli affacci.",
        styles["Descrizione"],
    ))

    story.append(Spacer(1, 10))
    story.extend(sezione_header(
        "Info utili",
        "Contatti e consigli pratici.",
        styles,
    ))
    for item in [
        "<b>Camping:</b> Via Lungomare Sorrentino, Tropea (VV) · Tel. +39 0963 61970 / +39 339 1017016 · info@campingmarinaisola.it",
        "<b>Centro:</b> scalinata a ~100 m dall'ingresso (~8–12 min). Circa 100–150 gradini.",
        "<b>Stazione FS Tropea:</b> ~1 km.",
        "<b>Alta stagione:</b> spiagge e affacci pieni; mattina presto e prenotazioni a cena.",
        "<b>Mare per Palombaro:</b> solo con condizioni calme e in sicurezza.",
        "<b>Da comprare:</b> cipolla rossa IGP, 'nduja, tonno Callipo, liquori tipici.",
    ]:
        story.append(Paragraph(f"• {item}", styles["Descrizione"]))

    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=ACQUA, spaceAfter=6))
    story.append(Paragraph(
        "Buona vacanza a Tropea! Distanze e voti sono indicativi e possono variare. "
        "Verifica orari e disponibilità sul posto.",
        styles["Nota"],
    ))
    story.append(Paragraph(
        "Guida personale · Camping Marina dell'Isola · Tropea 2026",
        styles["Nota"],
    ))

    doc.build(story, onFirstPage=cover_page, onLaterPages=header_footer)
    print(f"PDF creato: {OUTPUT}")


if __name__ == "__main__":
    build()
