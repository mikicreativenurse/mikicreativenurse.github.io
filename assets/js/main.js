const FORM_URL = "https://docs.google.com/forms/d/1GX3NAksEHVv_qAnvY70cq3SLPSN9TiDo5OHpiW-zgH4/viewform";

function applyFormLinks() {
  const links = document.querySelectorAll(".form-link");
  links.forEach((link) => {
    if (FORM_URL && !FORM_URL.startsWith("FORM_URL_")) {
      link.href = FORM_URL;
      link.target = "_blank";
      link.rel = "noopener";
    }
  });
}

function setupMenu() {
  const button = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#site-nav");
  if (!button || !nav) return;

  const closeMenu = () => {
    nav.classList.remove("is-open");
    button.setAttribute("aria-expanded", "false");
    button.textContent = "メニュー";
  };

  button.addEventListener("click", () => {
    const expanded = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!expanded));
    nav.classList.toggle("is-open", !expanded);
    button.textContent = expanded ? "メニュー" : "閉じる";
  });

  nav.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) closeMenu();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });
}

function setupFaq() {
  document.querySelectorAll(".faq-item button").forEach((button) => {
    const toggle = () => {
      const item = button.closest(".faq-item");
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      item?.classList.toggle("is-open", !expanded);
    };

    button.addEventListener("click", toggle);
    button.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        toggle();
      }
    });
  });
}

applyFormLinks();
setupMenu();
setupFaq();

