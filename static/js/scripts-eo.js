function popupControl() {
  window.onclick = function (event) {
    if (event.target == popup) {
      hidePopup();
    }
  };

  document.onkeydown = function (event) {
    if (event.key === "Escape") {
      hidePopup();
    }
  };
}

function showPopup() {
  document.getElementById("popup").style.display = "block";
  popupControl();
  document.getElementById("section-container").style.display = "none";
}

function hidePopup() {
  document.getElementById("popup").style.display = "none";
  document.getElementById("section-container").style.display = "block";
}

function checkUserStatus() {
  fetch("/user_status")
    .then((response) => response.json())
    .then((data) => {
      const linkElements = document.querySelectorAll("a.not-tag.admin");
      linkElements.forEach((linkElement) => {
        if (data.status === 1) {
          linkElement.classList.add("clickable");
        } else {
          if (linkElement.classList.contains("clickable")) {
            linkElement.classList.remove("clickable");
          }
          linkElement.addEventListener("click", function (event) {
            event.preventDefault();
          });
        }
      });
    });
}

document.addEventListener("DOMContentLoaded", checkUserStatus());
