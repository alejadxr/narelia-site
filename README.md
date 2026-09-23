# Narelia · la página

La landing de [Narelia](https://alejadxr.github.io/narelia-site/), la app de salud para iPhone y Apple Watch que te compara contigo.

HTML, CSS y un poco de JavaScript, sin compilación. Se publica con GitHub Pages desde `main`.

## Qué hay

- `src/page.html`: **la plantilla**, con los tres idiomas de cada texto uno junto a otro. Es el único sitio donde se edita el texto.
- `tools/build.py`: genera `index.html` (español), `en/index.html` y `fr/index.html` desde la plantilla, con el título, la descripción, el `hreflang`, las etiquetas para redes, los datos estructurados de app (`MobileApplication`) y los textos alternativos de cada idioma, y escribe `sitemap.xml`. **Después de tocar la plantilla: `python3 tools/build.py`** y se suben también los ficheros generados.
- `styles.css`: la paleta y el tipo. Los colores son los de la app: el blanco frío de su fondo, la tinta índigo, el violeta y el naranja de su malla, el azul de acento y el turquesa.
- `main.js`: la tira de capturas y la cabecera.

## SEO

Una URL por idioma y no un idioma cambiado por JavaScript, porque un buscador indexa el HTML, no lo que un script enseña después. Cada página lleva su `<html lang>`, su título y su descripción con las palabras que se buscan de verdad («app de salud», «Apple Watch», «VFC»), `canonical`, `hreflang` con `x-default`, Open Graph y Twitter, `MobileApplication` en JSON-LD y un `alt` descriptivo en cada imagen. La primera captura se precarga.

Pendiente fuera de este repo, porque necesita la cuenta del dueño:

- Dar de alta la web en **Google Search Console** y enviar `sitemap.xml`.
- Un **dominio propio**. En `github.io/narelia-site/` el `robots.txt` no cuenta (los buscadores sólo leen el de la raíz del dominio) y la autoridad es la de GitHub, no la de Narelia. Con un dominio basta con un fichero `CNAME` y cambiar `SITE` en `tools/build.py`.
- El **banner de la App Store** (`apple-itunes-app`), cuando la app esté publicada: hoy apuntaría a una ficha que todavía no existe.
- `assets/screens/{es,en,fr}/`: las seis capturas de la ficha, dibujadas por `StoreScreenshotTests` en el repositorio de la app con datos simulados, **dentro de un iPhone 17** de SutoScreen, en WebP con transparencia (663 × 1300).
- `assets/widgets/`: los widgets, recortados de `WidgetCatalogRenderTests` y `ReadinessWidgetRenderTests`.

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
