# Narelia · la página

La landing de [Narelia](https://alejadxr.github.io/narelia-site/), la app de salud para iPhone y Apple Watch que te compara contigo.

HTML, CSS y un poco de JavaScript, sin compilación. Se publica con GitHub Pages desde `main`.

## Qué hay

Tres páginas, cada una en es (raíz), en (`/en/`) y fr (`/fr/`):

| Página | Plantilla | URLs |
| --- | --- | --- |
| Portada | `src/inicio.html` | `/`, `/en/`, `/fr/` |
| Narelia para Mac (descarga) | `src/escritorio.html` | `/escritorio/`, `/en/desktop/`, `/fr/bureau/` |
| Guía «Conecta tu IA» | `src/guia.html` | `/conecta-tu-ia/`, `/en/connect-your-ai/`, `/fr/connecter-votre-ia/` |

- `src/*.html`: **las plantillas**, con los tres idiomas de cada texto uno junto a otro. `_cabecera.html` y `_pie.html` son la barra de arriba y el pie, comunes a todas. Es el único sitio donde se edita el texto.
- `src/clientes.json`: las 22 apps de IA de la guía, con su grupo, el fichero que Narelia escribe en el Mac y, en las 7 de paso a mano, el texto exacto. **No se edita a mano**: sale del código de Narelia para escritorio (`crates/nucleo/src/clientes.rs`, funciones `fichero_en` y `a_mano`) con `tools/fragmentos` (ver más abajo).
- `tools/build.py`: genera las nueve páginas y `sitemap.xml`, con título, descripción, `hreflang`, Open Graph y datos estructurados por página. **Después de tocar una plantilla: `python3 tools/build.py`** y se suben también los ficheros generados. Se niega a escribir una página que nombre el THC, el cannabis o el alcohol.
- `styles.css`: la paleta y el tipo. Los colores son los de las apps: el blanco frío del iPhone, la tinta índigo, el verde azulado y el resplandor de Narelia para escritorio, el violeta de la VFC. Letra: Source Serif 4 (la serif de la ventana de escritorio), Inter y JetBrains Mono. Claro y oscuro según el sistema.
- `main.js`: la tira de capturas, el borde de la cabecera, las animaciones de «El camino» y de la barra de rango (una vez, al verse; quietas con «reducir movimiento») y los botones de copiar de la guía.
- `assets/escritorio/`: la ventana real de Narelia para Mac (pantalla Hoy, datos de ejemplo), de las maquetas `promo-fullhd` de narelia-escritorio, en claro y oscuro.
- `assets/slint/`: la insignia oficial «Made with Slint». La licencia royalty-free 2.0 de Slint (§2(b)) la pide en la página pública de descarga; va en `/escritorio/`, junto al botón.
- `assets/badges/{es,en,fr}.svg`: la insignia oficial «Download on the App Store» de Apple, negra y sin tocar.
- `assets/film/`: la película de lanzamiento. **Ya no se enseña** en la portada: está pendiente de revisar que no salga en ella nada de lo que la página pública no puede nombrar.

## Huecos 3D

Dos imágenes que llegan aparte: **`img/3d-iphone.webp`** (héroe de la portada) e **`img/3d-escritorio.webp`** (sección «Narelia para Mac» y página de descarga). Basta con dejarlas en `img/`: cada hueco intenta cargar su fichero y, si está, lo enseña; si no, enseña lo de debajo (la captura de la ficha y la ventana real). En local (`localhost`/`127.0.0.1`) cada hueco vacío lleva una etiqueta con el nombre que espera; en la web publicada, no.

## La descarga de escritorio

El botón apunta a `https://github.com/alejadxr/narelia-site/releases/latest` (constante `RELEASE` en `tools/build.py`): la Release y su `.dmg` se suben aparte. La app aún no está firmada ni notarizada; la página explica cómo abrirla la primera vez (clic derecho → Abrir y, en macOS 15 o posterior, Ajustes del Sistema → Privacidad y seguridad → «Abrir igualmente»).

## Los fragmentos de la guía

```sh
cd tools/fragmentos
cargo run --offline -- "/Users/TU_USUARIO/Library/Mobile Documents/iCloud~com~diego~myhealth/Documents"
```

Imprime, en JSON, lo que `clientes.rs` genera para cada app con la binaria instalada (`/Applications/Narelia.app/Contents/MacOS/narelia-mcp`) y esa carpeta. Se corre una vez por idioma (`TU_USUARIO`, `YOUR_USER`, `VOTRE_UTILISATEUR`) y se juntan en `src/clientes.json`. El «dónde pegarlo» en francés va en `DONDE_FR` de `tools/build.py`, porque `clientes.rs` sólo lo trae en español e inglés. Necesita el repo `narelia-escritorio` al lado (`../../../narelia-escritorio`).

## SEO

Una URL por página e idioma y no un idioma cambiado por JavaScript, porque un buscador indexa el HTML, no lo que un script enseña después. Cada página lleva su `<html lang>`, su título y su descripción con las palabras que se buscan de verdad («app de salud», «Apple Watch», «VFC»), `canonical`, `hreflang` con `x-default`, Open Graph y Twitter, `MobileApplication` en JSON-LD y un `alt` descriptivo en cada imagen. La primera captura se precarga.

Pendiente fuera de este repo, porque necesita la cuenta del dueño:

- Dar de alta la web en **Google Search Console** y enviar `sitemap.xml`.
- Un **dominio propio**. En `github.io/narelia-site/` el `robots.txt` no cuenta (los buscadores sólo leen el de la raíz del dominio) y la autoridad es la de GitHub, no la de Narelia. Con un dominio basta con un fichero `CNAME` y cambiar `SITE` en `tools/build.py`.
- `assets/screens/{es,en,fr}/`: las capturas de la ficha (la página usa cinco: la de recuperación, `2-recuperacion`, se quitó porque su texto nombra el alcohol), dibujadas por `StoreScreenshotTests` en el repositorio de la app con datos simulados, **dentro de un iPhone 17** de SutoScreen, en WebP con transparencia (663 × 1300).
- `assets/widgets/`: los widgets, recortados de `WidgetCatalogRenderTests` y `ReadinessWidgetRenderTests`.

## La App Store

La app está en https://apps.apple.com/app/narelia/id6809521455 (id `6809521455`, constantes `APP_ID` y `APPSTORE` en `tools/build.py`). La beta de TestFlight (`https://testflight.apple.com/join/KAwauxRQ`, constante `TESTFLIGHT`) se enlaza sólo desde la descarga de escritorio y la guía, para «Conectar con tu IA» mientras la 1.1.21 no está en la tienda.

- **La insignia** es de Apple y no se modifica: negra (la preferida), una por página, a 54 px de alto (el mínimo en pantalla son 40) y con un cuarto de su alto de espacio libre. Se baja de `https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/<es-es|en-us|fr-fr>`. El resto de llamadas a la acción (cabecera y cierre) son botones de texto, no una segunda insignia. Los créditos de marcas de Apple van una sola vez, en el pie.

## La firma: «El camino de tus cifras»

En la portada, un panel oscuro con las cuatro paradas reales del dato —iPhone, carpeta, Mac, IA— y el «Servidor de Narelia» tachado, porque no existe. Al verse, un sobre con candado recorre la línea una vez y cada parada se enciende al llegar; después el sobre se desvanece. Es la única animación orquestada. La barra de rango personal (la franja es lo habitual para ti, el punto es hoy) sigue, en la sección de la app.

## Actualizar las capturas

1. En el repositorio de la app: `scripts/remote-build.sh <árbol> test -only-testing:MyHealthTests/StoreScreenshotTests`.
2. Meter cada `renders/tienda-69-<idioma>-<n>.png` en el iPhone con el CLI de SutoScreen, **dos veces**: sobre blanco y sobre negro liso.

   ```sh
   SutoScreen --render tienda.png blanco.png --ratio 9:16 --fit show-all --bezel black --ground studio-white --ground-style solid
   SutoScreen --render tienda.png negro.png  --ratio 9:16 --fit show-all --bezel black --ground studio-black --ground-style solid
   ```

3. Sacar la transparencia por diferencia entre las dos (el alfa es lo que cambia entre un fondo y otro, así que la sombra del teléfono sale con su transparencia real), recortar al teléfono y guardar a 1300 px de alto en `assets/screens/<idioma>/<n>.webp`. El guion está en `tools/matte.py`.
