(() => {
  const intro = document.querySelector(".intro");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finishIntro = () => {
    if (!intro) return;
    intro.classList.add("done");
    sessionStorage.setItem("huolide-intro", "seen");
    setTimeout(() => intro.remove(), 500);
  };
  if (intro) {
    if (reduced || sessionStorage.getItem("huolide-intro")) intro.remove();
    else {
      intro.querySelector(".skip-intro")?.addEventListener("click", finishIntro);
      setTimeout(finishIntro, 1750);
    }
  }
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); }
  }), {threshold: .12});
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));
  const top = document.querySelector(".to-top");
  addEventListener("scroll", () => top?.classList.toggle("show", scrollY > 700), {passive:true});
  top?.addEventListener("click", () => scrollTo({top:0,behavior:"smooth"}));
  document.querySelector(".menu")?.addEventListener("click", () => document.querySelector(".nav nav")?.classList.toggle("open"));
  document.querySelector(".lang")?.addEventListener("click", e => {
    const en = document.documentElement.lang !== "en";
    document.documentElement.lang = en ? "en" : "zh-Hans";
    e.currentTarget.textContent = en ? "EN 简" : "简 EN";
    document.body.classList.toggle("is-en", en);
  });
})();
