const wrapper = document.querySelector(".wrapper");
const images = document.querySelectorAll(".wrapper img");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

let currentImageIndex = 0;
let touchStartX = 0;
let touchEndX = 0;

// Hide or show navigation buttons based on current image index
function toggleNavButtons() {
  prevBtn.style.display = currentImageIndex === 0 ? "none" : "block";
  nextBtn.style.display =
    currentImageIndex === images.length - 1 ? "none" : "block";
}

// Function to go to the previous image
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

// Function to go to the next image
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
    //        console.log(`height is${height}`)
    iElement.style.lineHeight = `${height}px`;
    //        console.log(`height is now ${iElement.style.lineHeight}`)
  });
};

let timeoutId;
const debouncedUpdateLineHeight = () => {
  clearTimeout(timeoutId);
  timeoutId = setTimeout(updateLineHeight, 10);
};

// Event listeners for navigation buttons
prevBtn.addEventListener("click", prevImage);
nextBtn.addEventListener("click", nextImage);
window.addEventListener("resize", debouncedUpdateLineHeight);
window.addEventListener("resize", updateLineHeight);

//Initial setup
debouncedUpdateLineHeight();
updateLineHeight();

// Initial images setup
toggleNavButtons();
images.forEach((image, index) => {
  if (index !== 0) {
    image.classList.add("not-active");
  }
});

// Touch events for mobile swipe
wrapper.addEventListener("touchstart", (e) => {
  touchStartX = e.changedTouches[0].screenX;
});

wrapper.addEventListener("touchmove", (e) => {
  touchEndX = e.changedTouches[0].screenX;
});

wrapper.addEventListener("touchend", () => {
  handleSwipe();
});

function handleSwipe() {
  const swipeThreshold = 50; // Minimum swipe distance to trigger navigation
  if (touchEndX < touchStartX - swipeThreshold) {
    nextImage();
  }
  if (touchEndX > touchStartX + swipeThreshold) {
    prevImage();
  }
}

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
