function editSlides() {
  const imageContainer = document.getElementById("imageContainer");

  if (imageContainer) {
    new Sortable(imageContainer, {
      animation: 100,
      ghostClass: "orange-background-class",
      dragClass: "dragging",
    });

    imageContainer.addEventListener("click", function (e) {
      if (e.target.classList.contains("deleteUrl")) {
        let confirmMessage = "Are you sure you want to delete this url?";

        if (confirm(confirmMessage)) {
          e.target.closest(".grid-item").remove();
        }
      }
    });
  }

  const addNewUrl = document.getElementById("addNewUrl");

  if (addNewUrl) {
    addNewUrl.addEventListener("click", function () {
      let newItem = document.createElement("div");
      newItem.className = "grid-item";
      newItem.draggable = true;
      newItem.innerHTML = `
        <div class="image-wrapper"><img src="" alt="New image"></div>
        <div class="input-wrapper"><input type="text" name="urls[]" value="New URL" placeholder=""></div>
        <div class="delete-wrapper">
                                <button type="button" class="deleteUrl"><i class="fas fa-trash-alt deleteUrl"></i></button>
                            </div>
    `;

      document.getElementById("imageContainer").appendChild(newItem);

      let input = newItem.querySelector("input");
      let img = newItem.querySelector("img");
      input.addEventListener("input", function () {
        img.src = this.value;
      });
    });
  }
}
function imageViewer() {
  const images = document.querySelectorAll(".img-viewable");

  if (images) {
    images.forEach(function (image) {
      image.addEventListener("click", function () {
        var imageInView = new Image();
        imageInView.src = image.src;
        var viewer = new Viewer(imageInView, {
          inline: false,
          navbar: false,
          title: false,
          toolbar: false,
          viewed: function (e) {
            var viewer = this.viewer;
            var imageData = viewer.imageData;
            var containerData = viewer.containerData;

            var zoomRatio =
              0.7 *
              Math.min(
                containerData.width / imageData.naturalWidth,
                containerData.height / imageData.naturalHeight
              );

            viewer.zoomTo(zoomRatio, true);

            var offsetX =
              (containerData.width - imageData.naturalWidth * zoomRatio) / 2;
            var offsetY =
              (containerData.height - imageData.naturalHeight * zoomRatio) / 2;

            viewer.moveTo(offsetX, offsetY);
          },
        });
        viewer.show();
      });
    });
  }
}

function execLinks() {
  document.addEventListener("submit", function (event) {
    if (event.target.classList.contains("delete-form")) {
      event.preventDefault();
      let userName = event.target.getAttribute("data-user-name");
      if (confirm(`Are you sure you want to delete ${userName}?`)) {
        event.target.submit();
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  imageViewer();
  editSlides();
  execLinks();
});
