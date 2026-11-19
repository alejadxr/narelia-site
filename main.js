// Narelia — la web. Lo justo: la tira de capturas, el borde de la cabecera, el camino y la barra
// de rango que se ponen en marcha al verse, y los botones de copiar de la guía. El idioma no lo
// cambia un script: cada idioma es su propia página (`tools/build.py`).

(() => {
  const root = document.documentElement;
  root.classList.add("js");

  // En local, cada hueco 3D sin su imagen enseña el nombre del fichero que espera.
  if (/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname)) root.classList.add("borrador");

  // La cabecera gana su borde en cuanto hay contenido pasando por debajo.
  const top = document.querySelector(".top");
  if (top) {
    const onScroll = () => top.classList.toggle("is-scrolled", window.scrollY > 8);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // El camino y la barra de rango: se animan una vez, cuando llegan a la vista. Con «reducir
  // movimiento», el CSS los deja quietos en su estado final.
  const live = document.querySelectorAll("[data-route], .range");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("is-live");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.45 });
    live.forEach((el) => io.observe(el));
  } else {
    live.forEach((el) => el.classList.add("is-live"));
  }

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
    buttons.forEach((b) => b.addEventListener("click", () => {
      strip.scrollBy({ left: Number(b.dataset.strip) * step(), behavior: "smooth" });
    }));
    strip.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // Copiar los fragmentos de configuración. El rótulo dice «Copiado» un momento y vuelve.
  const done = { es: "Copiado", en: "Copied", fr: "Copié" }[root.lang] || "Copied";
  document.querySelectorAll("[data-copy]").forEach((button) => {
    const label = button.querySelector(".copy-label");
    const original = label.textContent;
    let timer;
    button.addEventListener("click", async () => {
      const text = button.parentElement.querySelector("code").textContent;
      try {
        await navigator.clipboard.writeText(text);
      } catch {
        const range = document.createRange();
        range.selectNodeContents(button.parentElement.querySelector("code"));
        const sel = getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        return;
      }
      label.textContent = done;
      button.classList.add("is-done");
      clearTimeout(timer);
      timer = setTimeout(() => {
        label.textContent = original;
        button.classList.remove("is-done");
      }, 1600);
    });
  });
})();
