let ifViewer = false;

function handleNavigation(event) {
  if (ifViewer) {
    return;
  }

  if (event.type === "click" && event.target.id === "prevBtn") {
    prevImage();
    prevBtn.classList.add("hover");
    setTimeout(() => {
      prevBtn.classList.remove("hover");
    }, 250);
  } else if (event.type === "click" && event.target.id === "nextBtn") {
    nextImage();
    nextBtn.classList.add("hover");
    setTimeout(() => {
      nextBtn.classList.remove("hover");
    }, 250);
  } else if (event.type === "keydown") {
    if (event.key === "ArrowLeft") {
      prevImage();
      prevBtn.classList.add("hover");
      setTimeout(() => {
        prevBtn.classList.remove("hover");
      }, 250);
    } else if (event.key === "ArrowRight") {
      nextImage();
      nextBtn.classList.add("hover");
      setTimeout(() => {
        nextBtn.classList.remove("hover");
      }, 250);
    }
  }
}

document.addEventListener("click", handleNavigation);
document.addEventListener("keydown", handleNavigation);

const wrapper = document.querySelector(".wrapper");
const images = document.querySelectorAll(".wrapper img");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

let currentImageIndex = 0;
let startX;
let currentX;
let isDragging = false;

// Hide or show navigation buttons based on current image index

function toggleNavButtons() {
  prevBtn.style.display = currentImageIndex === 0 ? "none" : "block";
  nextBtn.style.display =
    currentImageIndex === images.length - 1 ? "none" : "block";
}

function prevImage() {
  if (currentImageIndex > 0) {
    images[currentImageIndex].classList.remove("active");
    images[currentImageIndex].classList.add("not-active");
    currentImageIndex--;
    images[currentImageIndex].classList.remove("not-active");
    images[currentImageIndex].classList.add("active");
    debouncedUpdateLineHeight();
    updateLineHeight();
    toggleNavButtons();
  }
}

function nextImage() {
  if (currentImageIndex < images.length - 1) {
    images[currentImageIndex].classList.remove("active");
    images[currentImageIndex].classList.add("not-active");
    currentImageIndex++;
    images[currentImageIndex].classList.remove("not-active");
    images[currentImageIndex].classList.add("active");
    debouncedUpdateLineHeight();
    updateLineHeight();
    toggleNavButtons();
  }
}

// adjust nav icon size

const updateLineHeight = () => {
  const iElements = document.querySelectorAll(".wrapper i");
  iElements.forEach((iElement) => {
    const height = iElement.clientHeight;
    iElement.style.lineHeight = `${height}px`;
  });
};

let timeoutId;
const debouncedUpdateLineHeight = () => {
  clearTimeout(timeoutId);
  timeoutId = setTimeout(updateLineHeight, 10);
};

prevBtn.addEventListener("click", prevImage);
nextBtn.addEventListener("click", nextImage);
window.addEventListener("resize", debouncedUpdateLineHeight);
window.addEventListener("resize", updateLineHeight);

//Initial setup

debouncedUpdateLineHeight();
updateLineHeight();

toggleNavButtons();
images.forEach((image, index) => {
  if (index !== 0) {
    image.classList.add("not-active");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const wrapperIcons = document.querySelectorAll(".wrapper i");

  wrapperIcons.forEach((icon) => {
    icon.addEventListener("touchstart", function () {
      this.classList.add("hover");
    });

    icon.addEventListener("touchend", function () {
      this.classList.remove("hover");
    });

    icon.addEventListener("mouseenter", function () {
      if (!("ontouchstart" in window)) {
        icon.classList.add("hover");
      }
    });

    icon.addEventListener("mouseleave", function () {
      if (!("ontouchstart" in window)) {
        icon.classList.remove("hover");
      }
    });
  });
});

// touch slider

wrapper.addEventListener("touchstart", (e) => {
  isDragging = true;
  startX = e.touches[0].clientX;
});

wrapper.addEventListener("touchmove", (e) => {
  if (!isDragging) return;
  currentX = e.touches[0].clientX;
});

wrapper.addEventListener("touchend", () => {
  isDragging = false;
  const deltaX = currentX - startX;
  if (deltaX > 50) {
    prevImage();
  } else if (deltaX < -50) {
    nextImage();
  }
});

// handle orientation

function handleOrientationChange() {
  const orientationMessage = document.getElementById("orientation-message");
  const container = document.querySelector(".section");

  if (window.innerWidth <= 768 && window.innerHeight > window.innerWidth) {
    orientationMessage.classList.remove("hidden");
    container.style.display = "none";
  } else {
    orientationMessage.classList.add("hidden");
    container.style.display = "block";
  }
}

function imageViewer() {
  const images = document.querySelectorAll(".img-viewable");
  const imageUrls = Array.from(images).map((img) => img.src);

  let currentIndex = 0;

  images.forEach(function (image, index) {
    image.addEventListener("click", function () {
      currentIndex = index;

      const viewerContainer = document.createElement("div");
      document.body.appendChild(viewerContainer);

      imageUrls.forEach((url) => {
        const img = document.createElement("img");
        img.src = url;
        viewerContainer.appendChild(img);
      });

      const viewer = new Viewer(viewerContainer, {
        inline: false,
        navbar: true,
        title: false,
        toolbar: {
          prev: 1,
          next: 1,
        },
        viewed: function (e) {
          const viewer = this.viewer;
          const imageData = viewer.imageData;
          const containerData = viewer.containerData;

          const zoomRatio =
            0.7 *
            Math.min(
              containerData.width / imageData.naturalWidth,
              containerData.height / imageData.naturalHeight
            );

          viewer.zoomTo(zoomRatio, true);

          const offsetX =
            (containerData.width - imageData.naturalWidth * zoomRatio) / 2;
          const offsetY =
            (containerData.height - imageData.naturalHeight * zoomRatio) / 2;

          viewer.moveTo(offsetX, offsetY);
        },
        shown: function () {
          ifViewer = true;
          document.body.classList.add("no-scroll");
        },
        hidden: function () {
          ifViewer = false;
          document.body.classList.remove("no-scroll");
          document.body.removeChild(viewerContainer);
        },
      });

      viewer.show();
      viewer.view(currentIndex);
    });
  });
}

handleOrientationChange();

window.addEventListener("resize", handleOrientationChange);

document.addEventListener("DOMContentLoaded", () => {
  imageViewer();
});
