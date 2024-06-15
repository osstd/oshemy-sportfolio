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

      const imgElements = document.querySelectorAll(
        ".card-banner.img-holder.admin"
      );
      if (imgElements.length > 0) {
        if (data.status === 1) {
          imgElements.forEach((imgElement) => {
            imgElement.style.display = "block";
          });
        } else {
          imgElements.forEach((imgElement) => {
            imgElement.style.display = "none";
          });
        }
      }

      const spanElements = document.querySelectorAll("span.admin");
      if (spanElements.length > 0) {
        if (data.status === 1) {
          spanElements.forEach((spanElement) => {
            if (spanElement.classList.contains("hidden")) {
              spanElement.classList.remove("hidden");
            }
          });
        } else {
          spanElements.forEach((spanElement) => {
            spanElement.classList.add("hidden");
          });
        }
      }
    })
    .catch((error) => console.error("Error fetching user status:", error));
}

document.addEventListener("DOMContentLoaded", checkUserStatus());
