document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll("[data-flip-card]");
  const themeToggle = document.getElementById("themeToggle");
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebarToggle");

  cards.forEach((card) => {
    const flipCard = () => {
      const flipped = card.classList.toggle("is-flipped");
      card.setAttribute("aria-expanded", String(flipped));
    };

    card.addEventListener("click", (event) => {
      if (event.target.closest("button, a")) return;
      flipCard();
    });

    card.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      if (event.target.closest("button, a")) return;
      event.preventDefault();
      flipCard();
    });
  });

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const darkMode = document.body.classList.toggle("dark-mode");
      themeToggle.setAttribute("aria-pressed", String(darkMode));
    });
  }

  if (sidebar && sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {
      const isOpen = sidebar.classList.toggle("is-open");
      sidebarToggle.setAttribute("aria-expanded", String(isOpen));
    });

    document.addEventListener("click", (event) => {
      if (window.innerWidth > 680 || !sidebar.classList.contains("is-open")) return;
      if (sidebar.contains(event.target) || sidebarToggle.contains(event.target)) return;
      sidebar.classList.remove("is-open");
      sidebarToggle.setAttribute("aria-expanded", "false");
    });
  }
});
