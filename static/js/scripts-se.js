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

document.addEventListener("keydown", function (event) {
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
