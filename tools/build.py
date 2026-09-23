#!/usr/bin/env python3
"""Genera las tres páginas de Narelia —español en la raíz, inglés en /en/, francés en /fr/—
a partir de una sola plantilla, `src/page.html`.

Por qué tres páginas y no una con el idioma cambiado por JavaScript: un buscador lee lo que
hay en el HTML, no lo que un script enseña después. Con los tres idiomas en una sola URL,
Google veía una página mezclada, con un solo título y una sola descripción. Así cada idioma
tiene su URL, su título, su descripción, su `hreflang` y su `lang`, y el texto sigue viviendo
en un único sitio: la plantilla.

    python3 tools/build.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://alejadxr.github.io/narelia-site/"
TESTFLIGHT = "https://testflight.apple.com/join/KAwauxRQ"

LANGS = ["es", "en", "fr"]
PATH = {"es": "", "en": "en/", "fr": "fr/"}
LOCALE = {"es": "es_ES", "en": "en_US", "fr": "fr_FR"}
NAME = {"es": "Español", "en": "English", "fr": "Français"}

# El título lleva la marca y lo que es la app, con las palabras que alguien busca de verdad
# («app de salud», «Apple Watch»). Alrededor de sesenta caracteres, para que no se corte.
TITLE = {
    "es": "Narelia: app de salud para Apple Watch que te compara contigo",
    "en": "Narelia: the Apple Watch health app measured against you",
    "fr": "Narelia : l’app santé Apple Watch qui vous compare à vous",
}
DESCRIPTION = {
    "es": "Recuperación, VFC, sueño y estrés de tu Apple Watch, medidos frente a tu propia historia y no frente a una tabla de población. Todo el análisis en tu iPhone, sin cuenta. Beta abierta en TestFlight.",
    "en": "Recovery, HRV, sleep and stress from your Apple Watch, measured against your own history instead of a population chart. All analysis on your iPhone, no account. Open beta on TestFlight.",
    "fr": "Récupération, VFC, sommeil et stress de votre Apple Watch, mesurés face à votre propre historique et non à une table de population. Toute l’analyse sur votre iPhone, sans compte. Bêta ouverte sur TestFlight.",
}
OG_TITLE = {
    "es": "Narelia · Tus datos, no los de nadie",
    "en": "Narelia · Your data, measured against you",
    "fr": "Narelia · Vos données, comparées à vous",
}
LANG_GROUP = {"es": "Idioma", "en": "Language", "fr": "Langue"}

# Textos alternativos: lo que se ve en cada captura, para quien no la ve y para el buscador.
ALT = {
    "1-hoy": {
        "es": "Pantalla Hoy de Narelia en un iPhone: la cifra de Readiness en su dial y el pulso del día.",
        "en": "Narelia’s Today screen on an iPhone: the Readiness figure on its dial and the day’s heart rate.",
        "fr": "L’écran Aujourd’hui de Narelia sur un iPhone : le chiffre Readiness sur son cadran et le pouls de la journée.",
    },
    "2-recuperacion": {
        "es": "Pantalla de recuperación: la cifra, las señales que la componen y su evolución día a día.",
        "en": "Recovery screen: the figure, the signals it is made of and its day-by-day trend.",
        "fr": "Écran de récupération : le chiffre, les signaux qui le composent et son évolution jour après jour.",
    },
    "3-noche": {
        "es": "Pantalla de estrés con las lecturas de la noche y del día sobre el reloj.",
        "en": "Stress screen with the night’s and the day’s readings along the clock.",
        "fr": "Écran de stress avec les mesures de la nuit et de la journée le long de l’horloge.",
    },
    "4-forma-fisica": {
        "es": "Pantalla de forma física: el esfuerzo de la semana frente a tus semanas habituales.",
        "en": "Fitness screen: the week’s effort against your usual weeks.",
        "fr": "Écran de forme : l’effort de la semaine face à vos semaines habituelles.",
    },
    "5-registro": {
        "es": "Registro de agua con el recipiente dibujado y las cantidades rápidas.",
        "en": "Water log with the drawn vessel and quick amounts.",
        "fr": "Journal d’eau avec le récipient dessiné et les quantités rapides.",
    },
    "6-privacidad": {
        "es": "Ajustes de Narelia con la sección de privacidad: sin cuenta y sin servidores.",
        "en": "Narelia settings with the privacy section: no account and no servers.",
        "fr": "Réglages de Narelia avec la section confidentialité : sans compte ni serveurs.",
    },
}
ALTW = {
    "pulso-mediano-noche": {"es": "Widget de frecuencia cardiaca: la lectura actual, el pico, el mínimo y el día en velas por hora.", "en": "Heart rate widget: the latest reading, peak, low and the day as hourly candles.", "fr": "Widget de fréquence cardiaque : la mesure actuelle, le pic, le minimum et la journée en bougies horaires."},
    "readiness-pequeno-clasico": {"es": "Widget de Readiness en estilo Clásico, con su arco y el estado de constantes, sueño y estrés.", "en": "Readiness widget in the Classic style, with its arc and the status of vitals, sleep and stress.", "fr": "Widget Readiness en style Classique, avec son arc et l’état des constantes, du sommeil et du stress."},
    "estres-pequeno-narelia": {"es": "Widget de estrés: una columna por hora con el color de su banda.", "en": "Stress widget: one column per hour in the colour of its band.", "fr": "Widget de stress : une colonne par heure, de la couleur de sa zone."},
    "sueno-mediano-narelia": {"es": "Widget de sueño: la noche por fases y lo que sumó cada una.", "en": "Sleep widget: the night by stage and how long each lasted.", "fr": "Widget de sommeil : la nuit par phases et la durée de chacune."},
    "agua-pequeno-noche": {"es": "Widget de agua: el nivel frente al objetivo del día.", "en": "Water widget: the level against the day’s goal.", "fr": "Widget d’eau : le niveau face à l’objectif du jour."},
    "actividad-pequeno-editorial": {"es": "Widget de actividad en estilo Editorial: los pasos como trama de puntos.", "en": "Activity widget in the Editorial style: steps as a dot pattern.", "fr": "Widget d’activité en style Éditorial : les pas en trame de points."},
    "vitales-mediano-clasico": {"es": "Widget de constantes vitales: cada una en su rango personal.", "en": "Vitals widget: each one on its personal range.", "fr": "Widget des constantes : chacune sur sa plage personnelle."},
    "pulso-pequeno-clasico": {"es": "Widget pequeño de frecuencia cardiaca en estilo Clásico.", "en": "Small heart rate widget in the Classic style.", "fr": "Petit widget de fréquence cardiaque en style Classique."},
    "sueno-pequeno-noche": {"es": "Widget pequeño de sueño en estilo Noche.", "en": "Small sleep widget in the Night style.", "fr": "Petit widget de sommeil en style Nuit."},
}
# Las etiquetas para lectores de pantalla que no van en ningún texto visible.
UI = {
    "Anterior": {"es": "Anterior", "en": "Previous", "fr": "Précédent"},
    "Siguiente": {"es": "Siguiente", "en": "Next", "fr": "Suivant"},
    "Capturas": {"es": "Capturas de Narelia", "en": "Narelia screenshots", "fr": "Captures de Narelia"},
    "Idioma / Language": {"es": "Idioma y beta", "en": "Language and beta", "fr": "Langue et bêta"},
}
SHOTS = ["1-hoy", "2-recuperacion", "3-noche", "4-forma-fisica", "5-registro", "6-privacidad"]


def head(lang: str, base: str) -> str:
    url = SITE + PATH[lang]
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE + PATH[l]}">' for l in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}">'
    og_alternates = "\n".join(
        f'<meta property="og:locale:alternate" content="{LOCALE[l]}">' for l in LANGS if l != lang
    )
    data = {
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "Narelia",
        "url": url,
        "description": DESCRIPTION[lang],
        "inLanguage": lang,
        "operatingSystem": "iOS 26",
        "applicationCategory": "HealthApplication",
        "applicationSubCategory": "Apple Watch",
        "image": SITE + "assets/og.jpg",
        "screenshot": [SITE + f"assets/screens/{lang}/{s}.webp" for s in SHOTS],
        "installUrl": TESTFLIGHT,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE[lang]}</title>
<meta name="description" content="{DESCRIPTION[lang]}">
<link rel="canonical" href="{url}">
{alternates}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Narelia">
<meta property="og:title" content="{OG_TITLE[lang]}">
<meta property="og:description" content="{DESCRIPTION[lang]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{LOCALE[lang]}">
{og_alternates}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{OG_TITLE[lang]}">
<meta name="twitter:description" content="{DESCRIPTION[lang]}">
<meta name="twitter:image" content="{SITE}assets/og.jpg">
<meta name="theme-color" content="#F5F6F8">
<link rel="icon" href="{base}assets/mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{base}assets/mark-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..700&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{base}assets/screens/{lang}/1-hoy.webp" fetchpriority="high">
<link rel="stylesheet" href="{base}styles.css">
<script type="application/ld+json">
{json.dumps(data, ensure_ascii=False, indent=2)}
</script>
</head>"""


def language_links(lang: str, base: str) -> str:
    links = []
    for l in LANGS:
        current = ' aria-current="page"' if l == lang else ""
        links.append(
            f'<a href="{(base + PATH[l]) or './'}" hreflang="{l}" lang="{l}" title="{NAME[l]}"{current}>{l.upper()}</a>'
        )
    return f'<div class="langs" role="group" aria-label="{LANG_GROUP[lang]}">' + "".join(links) + "</div>"


def render(template: str, lang: str) -> str:
    base = "" if lang == "es" else "../"
    page = template.replace("{{HEAD}}", head(lang, base))
    page = page.replace("{{LANGS}}", language_links(lang, base))
    page = page.replace("{{HOME}}", "./")
    page = page.replace("{{BASE}}", base).replace("{{LANG}}", lang)
    page = re.sub(r"\{\{ALT:([^}]+)\}\}", lambda m: ALT[m.group(1)][lang], page)
    page = re.sub(r"\{\{ALTW:([^}]+)\}\}", lambda m: ALTW[m.group(1)][lang], page)
    # De cada trío de traducciones, sólo la de esta página, sin su envoltorio.
    page = re.sub(r'<span lang="(es|en|fr)">([^<]*)</span>',
                  lambda m: m.group(2) if m.group(1) == lang else "", page)
    for key, words in UI.items():
        page = page.replace(f'aria-label="{key}"', f'aria-label="{words[lang]}"')
    leftover = re.findall(r"\{\{[^}]+\}\}", page)
    assert not leftover, f"{lang}: marcadores sin resolver {leftover}"
    return page


def sitemap() -> str:
    entries = []
    for lang in LANGS:
        alternates = "\n".join(
            f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE + PATH[l]}"/>' for l in LANGS
        )
        entries.append(f"""  <url>
    <loc>{SITE + PATH[lang]}</loc>
{alternates}
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}"/>
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(entries) + "\n</urlset>\n")


def main() -> None:
    template = (ROOT / "src" / "page.html").read_text(encoding="utf-8")
    for lang in LANGS:
        out = ROOT / PATH[lang] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(template, lang), encoding="utf-8")
        print("escrita", out.relative_to(ROOT))
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("escrito sitemap.xml")


if __name__ == "__main__":
    main()
