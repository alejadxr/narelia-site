// Narelia — la página. Dos cosas y ninguna más: la tira de capturas y el borde de la
// cabecera al desplazarse. El idioma ya no lo cambia un script: cada idioma es su propia
// página (`tools/build.py`), que es lo que un buscador puede leer.

(() => {
  // La tira: los botones avanzan una captura y se apagan en los extremos.
  const strip = document.querySelector(".strip");
  const buttons = document.querySelectorAll("[data-strip]");
  if (strip && buttons.length) {
    const step = () => {
      const item = strip.querySelector("li");
      const gap = parseFloat(getComputedStyle(strip).columnGap) || 24;
      return item ? item.getBoundingClientRect().width + gap : 300;
    };
    const update = () => {
      const max = strip.scrollWidth - strip.clientWidth - 2;
      buttons[0].disabled = strip.scrollLeft <= 2;
      buttons[1].disabled = strip.scrollLeft >= max;
    };
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        strip.scrollBy({ left: Number(button.dataset.strip) * step(), behavior: "smooth" });
      });
    });
    strip.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // La cabecera gana su borde en cuanto hay contenido pasando por debajo.
  const top = document.querySelector(".top");
  if (top) {
    const onScroll = () => top.classList.toggle("is-scrolled", window.scrollY > 8);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
})();
