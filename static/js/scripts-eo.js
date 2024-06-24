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

function imageViewer() {
  const images = document.querySelectorAll(".img-holder-viewable img");

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

function handleTechGuide(imageURL) {
  var image = new Image();
  image.src = imageURL;
  var viewer = new Viewer(image, {
    inline: false,
    navbar: false,
    toolbar: false,
    title: false,
    hidden: function () {
      viewer.destroy();
    },
  });

  viewer.show();
}

document.addEventListener("DOMContentLoaded", () => {
  checkUserStatus();
  imageViewer();
});
