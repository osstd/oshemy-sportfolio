new Sortable(document.getElementById("imageContainer"), {
  animation: 100,
  ghostClass: "orange-background-class",
  dragClass: "dragging",
});

document
  .getElementById("imageContainer")
  .addEventListener("click", function (e) {
    if (e.target.classList.contains("deleteUrl")) {
      e.target.closest(".grid-item").remove();
    }
  });

document.getElementById("addNewUrl").addEventListener("click", function () {
  var newItem = document.createElement("div");
  newItem.className = "grid-item";
  newItem.draggable = true;
  newItem.innerHTML = `
        <div class="image-wrapper"><img src="" alt="New image"></div>
        <div class="input-wrapper"><input type="text" name="urls[]" value="New URL" placeholder=""></div>
        <button type="button" class="deleteUrl">Delete</button>
    `;
  document.getElementById("imageContainer").appendChild(newItem);

  var input = newItem.querySelector("input");
  var img = newItem.querySelector("img");
  input.addEventListener("input", function () {
    img.src = this.value;
  });
});

function imageViewer() {
  const images = document.querySelectorAll(".img-viewable");

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

document.addEventListener("DOMContentLoaded", () => {
  imageViewer();
});
