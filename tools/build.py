#!/usr/bin/env python3
"""Genera la web de Narelia —tres páginas en tres idiomas— a partir de las plantillas de `src/`.

    python3 tools/build.py

Páginas (la plantilla y su carpeta en cada idioma):

- `src/inicio.html`      → `/`, `/en/`, `/fr/`
- `src/guia.html`        → `/conecta-tu-ia/`, `/en/connect-your-ai/`, `/fr/connecter-votre-ia/`
- `src/escritorio.html`  → `/escritorio/`, `/en/desktop/`, `/fr/bureau/`

Por qué una URL por idioma y no un idioma cambiado por JavaScript: un buscador lee lo que hay
en el HTML. Cada página lleva su `lang`, su título, su descripción, su `hreflang` y su
`canonical`, y el texto sigue viviendo en un único sitio: la plantilla, con los tres idiomas de
cada frase uno junto a otro (`<span lang="es">…</span><span lang="en">…</span>…`).

Marcadores de las plantillas:

- `{{HEAD}}`, `{{TOP}}`, `{{FOOT}}`: la cabecera del documento, la barra de arriba y el pie.
- `{{BASE}}`: ruta relativa a la raíz del sitio (`""`, `"../"`, `"../../"`).
- `{{URL:inicio}}`, `{{URL:guia}}`, `{{URL:escritorio}}`: enlace relativo a esa página en el
  mismo idioma.
- `{{APPSTORE}}`, `{{RELEASE}}`, `{{TESTFLIGHT}}`, `{{PRIVACY}}`, `{{LANG}}`, `{{BADGEW}}`.
- `{{ALT:clave}}`, `{{ALTW:clave}}`: textos alternativos de capturas y widgets.
- `{{CLIENTES}}`: la lista de las 22 apps de IA, de `src/clientes.json` (ver más abajo).

`src/clientes.json` sale del propio código de Narelia para escritorio (`clientes.rs`), no se
escribe a mano: `tools/fragmentos` lo genera con la función `a_mano` de verdad (ver README).
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://alejadxr.github.io/narelia-site/"
APP_ID = "6809521455"
APPSTORE = f"https://apps.apple.com/app/narelia/id{APP_ID}"
PRIVACY = "https://alejadxr.github.io/narelia-privacy/"
RELEASE = "https://github.com/alejadxr/narelia-site/releases/latest"
LAUNCH_DATE = "2026-10-04"

LANGS = ["es", "en", "fr"]
ROOTDIR = {"es": "", "en": "en/", "fr": "fr/"}
LOCALE = {"es": "es_ES", "en": "en_US", "fr": "fr_FR"}
NAME = {"es": "Español", "en": "English", "fr": "Français"}
LANG_GROUP = {"es": "Idioma", "en": "Language", "fr": "Langue"}

# Carpeta de cada página en cada idioma.
SLUG = {
    "inicio": {"es": "", "en": "", "fr": ""},
    # La guía es una página suelta, para mandarla por enlace; sólo en español e inglés.
    "guia": {"es": "guia-ia.html", "en": "guia-ia.html"},
    "escritorio": {"es": "escritorio/", "en": "desktop/", "fr": "bureau/"},
}

TITLE = {
    "inicio": {
        "es": "Narelia: app de salud para Apple Watch que te compara contigo",
        "en": "Narelia: the Apple Watch health app measured against you",
        "fr": "Narelia : l’app santé Apple Watch qui vous compare à vous",
    },
    "guia": {
        "es": "Conecta Narelia con tu IA: Claude, Codex, Cursor, OpenClaw y 18 más",
        "en": "Connect Narelia to your AI: Claude, Codex, Cursor, OpenClaw and 18 more",
        "fr": "Connecter Narelia à votre IA : Claude, Codex, Cursor, OpenClaw et 18 autres",
    },
    "escritorio": {
        "es": "Narelia para Mac: tus cifras de salud y tu IA, sin servidor",
        "en": "Narelia for Mac: your health figures and your AI, no server",
        "fr": "Narelia pour Mac : vos chiffres de santé et votre IA, sans serveur",
    },
}
DESCRIPTION = {
    "inicio": {
        "es": "Recuperación, VFC, sueño y estrés de tu Apple Watch, medidos frente a tu propia historia. Todo el análisis en tu iPhone, sin cuenta. Y ahora, Narelia para Mac lleva tus cifras a la IA que ya usas, sin servidor de por medio.",
        "en": "Recovery, HRV, sleep and stress from your Apple Watch, measured against your own history. All analysis on your iPhone, no account. And now Narelia for Mac brings your figures to the AI you already use, with no server in between.",
        "fr": "Récupération, VFC, sommeil et stress de votre Apple Watch, mesurés face à votre propre historique. Toute l’analyse sur votre iPhone, sans compte. Et désormais, Narelia pour Mac apporte vos chiffres à l’IA que vous utilisez déjà, sans serveur entre les deux.",
    },
    "guia": {
        "es": "Cómo conectar Narelia con Claude Desktop, Claude Code, Codex, Cursor, OpenClaw, Hermes Agent, Gemini CLI y 15 apps más con narelia-mcp, el servidor MCP de Narelia para escritorio. Paso a paso y con la configuración exacta.",
        "en": "How to connect Narelia to Claude Desktop, Claude Code, Codex, Cursor, OpenClaw, Hermes Agent, Gemini CLI and 15 more apps with narelia-mcp, the MCP server in Narelia for desktop. Step by step, with the exact configuration.",
        "fr": "Comment connecter Narelia à Claude Desktop, Claude Code, Codex, Cursor, OpenClaw, Hermes Agent, Gemini CLI et 15 autres apps avec narelia-mcp, le serveur MCP de Narelia pour ordinateur. Pas à pas, avec la configuration exacte.",
    },
    "escritorio": {
        "es": "Descarga Narelia para macOS: tus cifras de Narelia en el Mac y la conexión con tu IA por MCP. Lee el fichero cifrado que tu iPhone deja en tu carpeta de iCloud Drive. Sin cuenta y sin servidor.",
        "en": "Download Narelia for macOS: your Narelia figures on the Mac and the link to your AI over MCP. It reads the encrypted file your iPhone leaves in your iCloud Drive folder. No account, no server.",
        "fr": "Téléchargez Narelia pour macOS : vos chiffres Narelia sur le Mac et la connexion à votre IA par MCP. Elle lit le fichier chiffré que votre iPhone dépose dans votre dossier iCloud Drive. Sans compte, sans serveur.",
    },
}
OG_TITLE = {
    "inicio": {"es": "Narelia · Tus datos, no los de nadie", "en": "Narelia · Your data, measured against you", "fr": "Narelia · Vos données, comparées à vous"},
    "guia": {"es": "Narelia · Conecta tu IA", "en": "Narelia · Connect your AI", "fr": "Narelia · Connectez votre IA"},
    "escritorio": {"es": "Narelia para Mac", "en": "Narelia for Mac", "fr": "Narelia pour Mac"},
}

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
        "es": "Pantalla de estrés: el día lectura a lectura sobre el reloj, con sus marcas de lo que registraste y la noche medida aparte.",
        "en": "Stress screen: the day reading by reading along the clock, with marks for what you logged and the night measured apart.",
        "fr": "Écran de stress : la journée mesure par mesure le long de l’horloge, avec les repères de ce que vous avez noté et la nuit mesurée à part.",
    },
    "4-forma-fisica": {
        "es": "Pantalla de forma física: el esfuerzo de la semana frente a tus semanas habituales.",
        "en": "Fitness screen: the week’s effort against your usual weeks.",
        "fr": "Écran de forme : l’effort de la semaine face à vos semaines habituelles.",
    },
    "5-registro": {
        "es": "Registro de agua: tus recipientes (vaso con pajita, botella, termo, lata, taza) y las cantidades rápidas.",
        "en": "Water log: your vessels (tumbler with straw, bottle, flask, can, cup) and quick amounts.",
        "fr": "Journal d’eau : vos récipients (verre avec paille, bouteille, thermos, canette, tasse) et les quantités rapides.",
    },
    "6-privacidad": {
        "es": "Ajustes de Narelia, sección Datos y privacidad: sincronizar con iCloud, apagado, y la política de privacidad.",
        "en": "Narelia settings, Data and privacy section: sync with iCloud, switched off, and the privacy policy.",
        "fr": "Réglages de Narelia, section Données et confidentialité : synchroniser avec iCloud, désactivé, et la politique de confidentialité.",
    },
    "badge": {
        "es": "Descargar en el App Store",
        "en": "Download on the App Store",
        "fr": "Télécharger dans l’App Store",
    },
    "3d-iphone": {
        "es": "Narelia en un iPhone, con la pantalla Hoy: Readiness, lo tuyo y tu día, con datos de ejemplo.",
        "en": "Narelia on an iPhone, showing the Today screen (in Spanish): Readiness, your own figures and your day, with sample data.",
        "fr": "Narelia sur un iPhone, avec l’écran Aujourd’hui (en espagnol) : Readiness, vos chiffres et votre journée, avec des données d’exemple.",
    },
    "mac-conectar": {
        "es": "La ventana de Narelia para Mac en «Conectar con tu IA»: Claude Desktop conectada; LM Studio, Hermes Agent y Cursor con su botón «Conectar»; Claude Code y OpenClaw, a mano.",
        "en": "The Narelia for Mac window on “Connect with your AI”: Claude Desktop connected; LM Studio, Hermes Agent and Cursor with their “Connect” button; Claude Code and OpenClaw, by hand.",
        "fr": "La fenêtre de Narelia pour Mac sur « Connect with your AI » : Claude Desktop connectée ; LM Studio, Hermes Agent et Cursor avec leur bouton « Connect » ; Claude Code et OpenClaw, à la main.",
    },
    "slint": {
        "es": "Hecho con Slint",
        "en": "Made with Slint",
        "fr": "Fait avec Slint",
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
# Etiquetas para lectores de pantalla que no van en ningún texto visible.
UI = {
    "Anterior": {"es": "Anterior", "en": "Previous", "fr": "Précédent"},
    "Siguiente": {"es": "Siguiente", "en": "Next", "fr": "Suivant"},
    "Capturas": {"es": "Capturas de Narelia", "en": "Narelia screenshots", "fr": "Captures de Narelia"},
    "Navegación": {"es": "Navegación", "en": "Navigation", "fr": "Navigation"},
    "Copiar": {"es": "Copiar", "en": "Copy", "fr": "Copier"},
}
# Sin la de recuperación: su texto nombra el alcohol, que no va en la página pública.
SHOTS = ["1-hoy", "3-noche", "4-forma-fisica", "5-registro", "6-privacidad"]

# Lo que dice cada grupo de la lista de apps, y el «dónde pegarlo» en francés (clientes.rs sólo
# lo trae en español e inglés; esto es su traducción, frase por frase).
GRUPO = {
    "Chat": {"es": "Apps de chat", "en": "Chat apps", "fr": "Apps de discussion"},
    "Agente": {"es": "Agentes", "en": "Agents", "fr": "Agents"},
    "Editor": {"es": "Editores de código", "en": "Code editors", "fr": "Éditeurs de code"},
}
DONDE_FR = {
    "Claude Code": "Dans un terminal. Ensuite, ouvrez une nouvelle session de Claude Code.",
    "OpenClaw": "Dans un terminal, sur l’ordinateur où tourne le Gateway d’OpenClaw.",
    "Zed": "Dans Zed : « zed: open settings file », puis collez-le à l’intérieur des accolades extérieures.",
    "Jan": "Dans Jan : Settings → MCP Servers → « + ». Copiez la commande, les arguments et la variable NARELIA_DIR.",
    "Msty Studio": "Dans Msty Studio : Toolbox → Tools → Add New Tool → STDIO / JSON, puis collez-le.",
    "Cherry Studio": "Dans Cherry Studio : Settings → MCP → MCP Servers → Add → Import from JSON, puis collez-le.",
    "Chatbox": "Dans Chatbox : Settings → MCP → ajouter, « Local (stdio) ». Copiez la commande et la variable NARELIA_DIR, puis appuyez sur « Test ».",
}
SOLA = {"es": "Se configura sola", "en": "Set up for you", "fr": "Configurée pour vous"}
A_MANO = {"es": "A mano", "en": "By hand", "fr": "À la main"}
QUE_HACER = {
    "es": "En Narelia para Mac, pulsa «Conectar» junto a {}; después ciérrala del todo y vuelve a abrirla.",
    "en": "In Narelia for Mac, click “Connect” next to {}; then quit it completely and open it again.",
    "fr": "Dans Narelia pour Mac, cliquez sur « Connect » à côté de {} ; puis quittez-la complètement et rouvrez-la.",
}
FICHERO = {"es": "Su configuración:", "en": "Its configuration:", "fr": "Sa configuration :"}


def langs_of(page: str) -> list:
    return [l for l in LANGS if l in SLUG[page]]


def page_dir(page: str, lang: str) -> str:
    """La ruta de la página desde la raíz del sitio. Si la página no existe en ese idioma (la
    guía en francés), la inglesa."""
    if lang not in SLUG[page]:
        lang = "en"
    return ROOTDIR[lang] + SLUG[page][lang]


def out_file(page: str, lang: str) -> Path:
    d = page_dir(page, lang)
    return ROOT / (d if d.endswith(".html") else d + "index.html")


def base_of(page: str, lang: str) -> str:
    return "../" * page_dir(page, lang).count("/")


def head(page: str, lang: str, base: str) -> str:
    url = SITE + page_dir(page, lang)
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE + page_dir(page, l)}">' for l in langs_of(page)
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE + page_dir(page, "es")}">'
    og_alternates = "\n".join(
        f'<meta property="og:locale:alternate" content="{LOCALE[l]}">' for l in langs_of(page) if l != lang
    )
    og = SITE + ("assets/og.jpg" if lang == "es" else "assets/og-en.jpg")
    if page == "inicio":
        data = {
            "@context": "https://schema.org",
            "@type": "MobileApplication",
            "name": "Narelia",
            "url": url,
            "description": DESCRIPTION[page][lang],
            "inLanguage": lang,
            "operatingSystem": "iOS 26",
            "applicationCategory": "HealthApplication",
            "applicationSubCategory": "Apple Watch",
            "image": og,
            "screenshot": [SITE + f"assets/screens/{lang}/{s}.webp" for s in SHOTS],
            "installUrl": APPSTORE,
            "downloadUrl": APPSTORE,
            "sameAs": [APPSTORE],
            "datePublished": LAUNCH_DATE,
            "isAccessibleForFree": True,
            "offers": [{"@type": "Offer", "name": "Narelia", "price": "0", "priceCurrency": "USD",
                        "url": APPSTORE, "availability": "https://schema.org/InStock"}],
        }
    elif page == "escritorio":
        data = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Narelia para escritorio" if lang == "es" else ("Narelia for desktop" if lang == "en" else "Narelia pour ordinateur"),
            "url": url,
            "description": DESCRIPTION[page][lang],
            "inLanguage": lang,
            "operatingSystem": "macOS",
            "applicationCategory": "HealthApplication",
            "downloadUrl": RELEASE,
            "isAccessibleForFree": True,
            "license": "https://opensource.org/licenses/MIT",
            "offers": [{"@type": "Offer", "price": "0", "priceCurrency": "USD"}],
        }
    else:
        data = {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": TITLE[page][lang],
            "url": url,
            "description": DESCRIPTION[page][lang],
            "inLanguage": lang,
            "about": "Model Context Protocol (MCP)",
        }
    fonts = ("https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..700"
             "&family=Source+Serif+4:ital,opsz,wght@0,8..60,300..600;1,8..60,300..500"
             "&family=JetBrains+Mono:wght@400;500&display=swap")
    preload = ""
    itunes = f'<meta name="apple-itunes-app" content="app-id={APP_ID}">\n' if page == "inicio" else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE[page][lang]}</title>
<meta name="description" content="{DESCRIPTION[page][lang]}">
<link rel="canonical" href="{url}">
{alternates}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Narelia">
<meta property="og:title" content="{OG_TITLE[page][lang]}">
<meta property="og:description" content="{DESCRIPTION[page][lang]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{LOCALE[lang]}">
{og_alternates}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{OG_TITLE[page][lang]}">
<meta name="twitter:description" content="{DESCRIPTION[page][lang]}">
<meta name="twitter:image" content="{og}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f4f5f8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0c12" media="(prefers-color-scheme: dark)">
{itunes}<link rel="icon" href="{base}assets/mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{base}assets/mark-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
{preload}<link rel="stylesheet" href="{base}styles.css">
<script type="application/ld+json">
{json.dumps(data, ensure_ascii=False, indent=2)}
</script>
</head>"""


def language_links(page: str, lang: str, base: str) -> str:
    links = []
    for l in langs_of(page):
        current = ' aria-current="page"' if l == lang else ""
        href = (base + page_dir(page, l)) or "./"
        links.append(f'<a href="{href}" hreflang="{l}" lang="{l}" title="{NAME[l]}"{current}>{l.upper()}</a>')
    return f'<div class="langs" role="group" aria-label="{LANG_GROUP[lang]}">' + "".join(links) + "</div>"


def badge_width(lang: str, height: int = 54) -> str:
    """El ancho de la insignia a su alto, de su propio viewBox: se escala sin deformarla."""
    svg = (ROOT / "assets" / "badges" / f"{lang}.svg").read_text(encoding="utf-8")
    w, h = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups()
    return f"{float(w) * height / float(h):.1f}".rstrip("0").rstrip(".")


def clientes(lang: str) -> str:
    """La lista de las 22 apps, agrupada como en la pantalla «Conectar» de la app."""
    apps = json.loads((ROOT / "src" / "clientes.json").read_text(encoding="utf-8"))
    out = []
    for grupo in ["Chat", "Agente", "Editor"]:
        filas = []
        # Primero las que se configuran solas (rejilla) y después las de paso a mano (a lo ancho).
        for a in sorted([a for a in apps if a["grupo"] == grupo], key=lambda a: a["a_mano"]):
            nombre = html.escape(a["nombre"])
            if a["a_mano"]:
                donde = a["donde"].get(lang) or DONDE_FR[a["nombre"]]
                ident = "app-" + re.sub(r"[^a-z0-9]+", "-", a["nombre"].lower()).strip("-")
                filas.append(f"""<li class="app app-mano" id="{ident}">
  <div class="app-head"><h4>{nombre}</h4><span class="tag tag-mano">{A_MANO[lang]}</span></div>
  <p class="app-where">{html.escape(donde)}</p>
  <div class="snippet"><button type="button" class="copy" data-copy aria-label="Copiar"><span class="copy-label">{UI["Copiar"][lang]}</span></button><pre><code>{html.escape(a["texto"][lang])}</code></pre></div>
</li>""")
            else:
                ident = "app-" + re.sub(r"[^a-z0-9]+", "-", a["nombre"].lower()).strip("-")
                filas.append(f"""<li class="app app-sola" id="{ident}">
  <div class="app-head"><h4>{nombre}</h4><span class="tag tag-sola">{SOLA[lang]}</span></div>
  <p class="app-where">{FICHERO[lang]} <code>{html.escape(a["fichero"])}</code></p>
  <p class="app-do">{QUE_HACER[lang].format(nombre)}</p>
</li>""")
        out.append(f'<section class="apps-group" aria-label="{GRUPO[grupo][lang]}"><h3 class="apps-group-title">{GRUPO[grupo][lang]}</h3><ul class="apps">{"".join(filas)}</ul></section>')
    return "\n".join(out)


def include(name: str) -> str:
    return (ROOT / "src" / f"_{name}.html").read_text(encoding="utf-8")


def render(page: str, lang: str) -> str:
    base = base_of(page, lang)
    t = (ROOT / "src" / f"{page}.html").read_text(encoding="utf-8")
    t = t.replace("{{TOPMIN}}", include("cabecera-min")).replace("{{FOOTMIN}}", include("pie-min"))
    t = t.replace("{{TOP}}", include("cabecera")).replace("{{FOOT}}", include("pie"))
    t = t.replace("{{HEAD}}", head(page, lang, base))
    t = t.replace("{{CLIENTES}}", clientes(lang))
    # El botón de la barra de arriba: la App Store en la portada; el instalador en las de escritorio.
    t = t.replace("{{TOPCTA}}", APPSTORE if page == "inicio" else RELEASE)
    t = t.replace("{{LANGS}}", language_links(page, lang, base))
    t = re.sub(r"\{\{URL:(\w+)\}\}", lambda m: (base + page_dir(m.group(1), lang)) or "./", t)
    t = t.replace("{{APPSTORE}}", APPSTORE).replace("{{BADGEW}}", badge_width(lang))
    t = t.replace("{{RELEASE}}", RELEASE).replace("{{PRIVACY}}", PRIVACY)
    t = t.replace("{{BASE}}", base).replace("{{LANG}}", lang).replace("{{PAGE}}", page)
    t = t.replace("{{SHOTLANG}}", "es" if lang == "es" else "en")
    t = re.sub(r"\{\{ALT:([^}]+)\}\}", lambda m: ALT[m.group(1)][lang], t)
    t = re.sub(r"\{\{ALTW:([^}]+)\}\}", lambda m: ALTW[m.group(1)][lang], t)
    # De cada trío de traducciones, sólo la de esta página, sin su envoltorio (con etiquetas
    # dentro, como <strong> o un enlace, sin saltar a otro <span>).
    t = re.sub(r'<span lang="(es|en|fr)">((?:(?!</span>).)*)</span>',
               lambda m: m.group(2) if m.group(1) == lang else "", t, flags=re.S)
    for key, words in UI.items():
        t = t.replace(f'aria-label="{key}"', f'aria-label="{words[lang]}"')
    # La página actual, marcada en la navegación.
    t = t.replace(f'data-nav="{page}"', 'aria-current="page"')
    t = re.sub(r' data-nav="\w+"', "", t)
    leftover = re.findall(r"\{\{[^}]+\}\}", t)
    assert not leftover, f"{page}/{lang}: marcadores sin resolver {leftover}"
    return t


def sitemap() -> str:
    entries = []
    for page in SLUG:
        for lang in langs_of(page):
            alternates = "\n".join(
                f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE + page_dir(page, l)}"/>' for l in langs_of(page)
            )
            entries.append(f"""  <url>
    <loc>{SITE + page_dir(page, lang)}</loc>
{alternates}
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE + page_dir(page, "es")}"/>
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(entries) + "\n</urlset>\n")


# Nada de esto puede aparecer en la web pública (norma de Narelia para la página).
PROHIBIDO = re.compile(r"\b(thc|cannabis|alcohol|alcool|marihuana|marijuana)\b", re.I)


def main() -> None:
    for page in SLUG:
        for lang in langs_of(page):
            out = out_file(page, lang)
            out.parent.mkdir(parents=True, exist_ok=True)
            text = render(page, lang)
            bad = PROHIBIDO.search(text)
            assert not bad, f"{page}/{lang}: «{bad.group(0)}» no puede ir en la página pública"
            out.write_text(text, encoding="utf-8")
            print("escrita", out.relative_to(ROOT))
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("escrito sitemap.xml")


if __name__ == "__main__":
    main()
