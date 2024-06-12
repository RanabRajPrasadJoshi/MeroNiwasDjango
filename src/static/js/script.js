const toggle = document.querySelector(".toggle-DropDown");
const nav = document.querySelector(".naav");

toggle.addEventListener("click", () => {
  toggle.classList.toggle("active");
  nav.classList.toggle("active");
});

document.querySelectorAll(".nav-item").forEach((n) =>
  n.addEventListener("click", () => {
    toggle.classList.remove("active");
    nav.classList.remove("active");
  })
);
