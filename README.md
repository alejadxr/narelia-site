# Narelia · la página

La landing de [Narelia](https://alejadxr.github.io/narelia-site/), la app de salud para iPhone y Apple Watch que te compara contigo.

HTML, CSS y un poco de JavaScript, sin compilación. Se publica con GitHub Pages desde `main`.

## Qué hay

- `index.html`: la página, en español, inglés y francés. El idioma se elige solo según el navegador y se puede cambiar arriba a la derecha.
- `styles.css`: la paleta y el tipo. Los colores son los de la app: el blanco frío de su fondo, la tinta índigo, el violeta y el naranja de su malla, el azul de acento y el turquesa.
- `main.js`: el cambio de idioma (texto y capturas), la tira de capturas y la cabecera.
- `assets/screens/{es,en,fr}/`: las seis capturas de la ficha, dibujadas por `StoreScreenshotTests` en el repositorio de la app con datos simulados, a 660 px de ancho en WebP.
- `assets/widgets/`: los widgets, recortados de `WidgetCatalogRenderTests` y `ReadinessWidgetRenderTests`.

## El héroe

La barra de rango personal: la franja es lo habitual para ti, el punto es hoy. Es el instrumento que la app usa en sus pantallas de constantes y en sus widgets. Al cargar, la franja crece y el punto se asienta, y ésa es la única animación de la página. Con «reducir movimiento» activado no se anima.

## Actualizar las capturas

1. En el repositorio de la app: `scripts/remote-build.sh <árbol> test -only-testing:MyHealthTests/StoreScreenshotTests`.
2. Convertir `renders/tienda-69-<idioma>-<n>.png` a WebP de 660 px de ancho en `assets/screens/<idioma>/<n>.webp`.
