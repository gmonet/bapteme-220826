/* Surligne dans la navigation collante la section actuellement visible.
   Aucune dépendance. Si le script ne s'exécute pas, le site reste
   parfaitement utilisable : les ancres et le défilement sont en HTML/CSS. */
(function () {
  "use strict";

  var links = document.querySelectorAll(".nav a[href^='#']");
  if (!links.length || !("IntersectionObserver" in window)) return;

  var byId = {};
  var sections = [];

  links.forEach(function (link) {
    var section = document.getElementById(link.hash.slice(1));
    if (!section) return;
    byId[section.id] = link;
    sections.push(section);
  });

  function setCurrent(id) {
    links.forEach(function (link) {
      if (byId[id] === link) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    });
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) setCurrent(entry.target.id);
      });
    },
    // la bande active suit le haut de l'écran, sous la nav collante
    { rootMargin: "-30% 0px -60% 0px", threshold: 0 }
  );

  sections.forEach(function (section) { observer.observe(section); });
})();
