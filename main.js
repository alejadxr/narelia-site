// Narelia — la página. Tres cosas y ninguna más: el idioma, la tira de capturas y el borde
// de la cabecera al desplazarse.

(() => {
  const root = document.documentElement;
  const languages = ["es", "en", "fr"];

  const titles = {
    es: "Narelia · Tus datos, no los de nadie",
    en: "Narelia · Your data, measured against you",
    fr: "Narelia · Vos données, comparées à vous",
  };

  // El idioma guardado, si lo hay; si no, el del navegador; si no, español.
  function initialLanguage() {
    try {
      const saved = localStorage.getItem("narelia-lang");
      if (languages.includes(saved)) return saved;
    } catch (_) { /* navegación privada: se sigue sin recordar */ }
    const preferred = (navigator.languages || [navigator.language || "es"])
      .map((tag) => String(tag).slice(0, 2).toLowerCase())
      .find((code) => languages.includes(code));
    return preferred || "es";
  }

  function setLanguage(lang, remember) {
    root.dataset.lang = lang;
    root.lang = lang;
    document.title = titles[lang];

    document.querySelectorAll("[data-set-lang]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.setLang === lang));
    });

    // Las capturas de la app, en el mismo idioma que la página: la app las dibuja en los tres.
    document.querySelectorAll("img[data-shot]").forEach((img) => {
      const src = `assets/screens/${lang}/${img.dataset.shot}.webp`;
      if (!img.src.endsWith(src)) img.src = src;
    });

    if (remember) {
      try { localStorage.setItem("narelia-lang", lang); } catch (_) { /* sin almacenamiento */ }
    }
  }

  setLanguage(initialLanguage(), false);

  document.querySelectorAll("[data-set-lang]").forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.setLang, true));
  });

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
