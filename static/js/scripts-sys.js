"use strict";

const addEventOnElements = function (elements, eventType, callback) {
  for (let i = 0, len = elements.length; i < len; i++) {
    elements[i].addEventListener(eventType, callback);
  }
};

const preloader = document.querySelector("[data-preloader]");
window.addEventListener("load", function () {
  preloader.classList.add("loaded");
  document.body.classList.add("loaded");
});

const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const navToggler = document.querySelector("[data-nav-toggler]");
const header = document.querySelector("[data-header]");

const toggleNavbarMenu = function () {
  navbar.classList.toggle("active");
};

navToggler.addEventListener("click", toggleNavbarMenu);

function isLandscape() {
  return window.innerWidth > window.innerHeight;
}

function isPhone() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
}

let lastScrollTop = 0;
let scrollDirection = "down";
const scrollThreshold = 10;

function handleHeaderVisibility() {
  const scrollPosition = window.scrollY;
  const viewportHeight = window.innerHeight;
  const mainElement = document.querySelector("main");

  const currentScrollTop =
    window.pageYOffset || document.documentElement.scrollTop;

  if (currentScrollTop > lastScrollTop) {
    scrollDirection = "down";
  } else if (currentScrollTop < lastScrollTop) {
    scrollDirection = "up";
  }

  if (Math.abs(currentScrollTop - lastScrollTop) > scrollThreshold) {
    if (isPhone && isLandscape() && scrollDirection === "down") {
      header.style.transform = "translateY(-100%)";
    } else {
      header.style.transform = "translateY(0)";
    }
  }

  if (Math.abs(currentScrollTop - lastScrollTop) > scrollThreshold) {
    if (!isPhone() && isLandscape() && scrollDirection === "down") {
      header.style.transform = "translateY(-100%)";
      mainElement.classList.add("scroll");
    } else {
      header.style.transform = "translateY(0)";
      mainElement.classList.remove("scroll");
    }
  }

  lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop;
}

function debounce(func, wait = 10, immediate = true) {
  let timeout;
  return function () {
    const context = this,
      args = arguments;
    const later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}

handleHeaderVisibility();

window.addEventListener("resize", handleHeaderVisibility);
window.addEventListener("scroll", handleHeaderVisibility);
