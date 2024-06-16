document.addEventListener("DOMContentLoaded", function () {
  const toggleBtns = document.querySelectorAll(".toggle-btn");

  toggleBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const dropdown = this.nextElementSibling;
      dropdown.classList.toggle("active");
    });
  });
});
