# Narelia · la página

La landing de [Narelia](https://alejadxr.github.io/narelia-site/), la app de salud para iPhone y Apple Watch que te compara contigo.

HTML, CSS y un poco de JavaScript, sin compilación. Se publica con GitHub Pages desde `main`.

## Qué hay

- `src/page.html`: **la plantilla**, con los tres idiomas de cada texto uno junto a otro. Es el único sitio donde se edita el texto.
- `tools/build.py`: genera `index.html` (español), `en/index.html` y `fr/index.html` desde la plantilla, con el título, la descripción, el `hreflang`, las etiquetas para redes, el banner de la App Store (`apple-itunes-app`), los datos estructurados de app (`MobileApplication`, con su URL de la App Store, la oferta gratuita y la de Narelia Pro) y los textos alternativos de cada idioma, y escribe `sitemap.xml`. **Después de tocar la plantilla: `python3 tools/build.py`** y se suben también los ficheros generados.
- `styles.css`: la paleta y el tipo. Los colores son los de la app: el blanco frío de su fondo, la tinta índigo, el violeta y el naranja de su malla, el azul de acento y el turquesa.
- `main.js`: la tira de capturas y la cabecera.
- `assets/film/narelia-{es,en}.{mp4,jpg}`: la película de lanzamiento en 16:9 (2 min 14 s), comprimida para la web desde `~/myhealth/motion-lanzamiento/narelia-lanzamiento-wide-*.mp4` (ffmpeg: 1280 px, H.264 CRF 25, 60 fps, AAC 64k, `+faststart`; ~8 MB) con su póster. La española va en la raíz; la inglesa en /en/ y /fr/. `main.js` la reproduce sin sonido y en bucle sólo mientras está a la vista, y no arranca sola con «reducir movimiento».
- `assets/badges/{es,en,fr}.svg`: la insignia oficial «Download on the App Store» de Apple, negra y sin tocar (de `toolbox.marketingtools.apple.com`, ver más abajo).

## SEO

Una URL por idioma y no un idioma cambiado por JavaScript, porque un buscador indexa el HTML, no lo que un script enseña después. Cada página lleva su `<html lang>`, su título y su descripción con las palabras que se buscan de verdad («app de salud», «Apple Watch», «VFC»), `canonical`, `hreflang` con `x-default`, Open Graph y Twitter, `MobileApplication` en JSON-LD y un `alt` descriptivo en cada imagen. La primera captura se precarga.

Pendiente fuera de este repo, porque necesita la cuenta del dueño:

- Dar de alta la web en **Google Search Console** y enviar `sitemap.xml`.
- Un **dominio propio**. En `github.io/narelia-site/` el `robots.txt` no cuenta (los buscadores sólo leen el de la raíz del dominio) y la autoridad es la de GitHub, no la de Narelia. Con un dominio basta con un fichero `CNAME` y cambiar `SITE` en `tools/build.py`.
- `assets/screens/{es,en,fr}/`: las seis capturas de la ficha, dibujadas por `StoreScreenshotTests` en el repositorio de la app con datos simulados, **dentro de un iPhone 17** de SutoScreen, en WebP con transparencia (663 × 1300).
- `assets/widgets/`: los widgets, recortados de `WidgetCatalogRenderTests` y `ReadinessWidgetRenderTests`.

## La App Store

La app está en https://apps.apple.com/app/narelia/id6809521455 (id `6809521455`, constantes `APP_ID` y `APPSTORE` en `tools/build.py`). La beta de TestFlight ya no se enlaza desde la página.

- **La insignia** es de Apple y no se modifica: negra (la preferida), una por página, a 54 px de alto (el mínimo en pantalla son 40) y con un cuarto de su alto de espacio libre. Se baja de `https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/<es-es|en-us|fr-fr>`. El resto de llamadas a la acción (cabecera y cierre) son botones de texto, no una segunda insignia. Los créditos de marcas de Apple van una sola vez, en el pie.
- **Lo que trae la versión de la tienda y lo que todavía no.** La 1.0 de la tienda es la build 72 (commit `3111d4d` de la app). Lo que llegó después —Siri y Atajos con todas las cifras, el índice para Apple Intelligence, la IA de comidas que mira la foto en iOS 27, «Sólo de día» y el aviso «muy fuera de tu rango habitual»— va en `src/page.html` entre las marcas `next`, y `python3 tools/build.py` **lo omite**. Cuando salga la actualización, `python3 tools/build.py --actualizacion` lo incluye (y conviene quitar las marcas y la bandera para siempre). Cada afirmación nueva se comprueba contra el código de la versión que se publica, no contra el de la rama.

## El héroe

La barra de rango personal: la franja es lo habitual para ti, el punto es hoy. Es el instrumento que la app usa en sus pantallas de constantes y en sus widgets. Al cargar, la franja crece y el punto se asienta, y ésa es la única animación de la página. Con «reducir movimiento» activado no se anima.

## Actualizar las capturas

1. En el repositorio de la app: `scripts/remote-build.sh <árbol> test -only-testing:MyHealthTests/StoreScreenshotTests`.
2. Meter cada `renders/tienda-69-<idioma>-<n>.png` en el iPhone con el CLI de SutoScreen, **dos veces**: sobre blanco y sobre negro liso.

   ```sh
   SutoScreen --render tienda.png blanco.png --ratio 9:16 --fit show-all --bezel black --ground studio-white --ground-style solid
   SutoScreen --render tienda.png negro.png  --ratio 9:16 --fit show-all --bezel black --ground studio-black --ground-style solid
   ```

3. Sacar la transparencia por diferencia entre las dos (el alfa es lo que cambia entre un fondo y otro, así que la sombra del teléfono sale con su transparencia real), recortar al teléfono y guardar a 1300 px de alto en `assets/screens/<idioma>/<n>.webp`. El guion está en `tools/matte.py`.
