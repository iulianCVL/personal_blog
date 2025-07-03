const toggle = document.getElementById("toggle-theme");
toggle.addEventListener("change", () => {
  document.documentElement.setAttribute("data-theme", toggle.checked ? "dark" : "light");
});
