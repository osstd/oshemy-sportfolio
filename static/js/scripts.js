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

const toggleNavbar = function () {
  navbar.classList.toggle("active");
};

navToggler.addEventListener("click", toggleNavbar);

const header = document.querySelector("[data-header]");
const mainElement = document.querySelector("main");

let lastScrollY = window.scrollY;

function isLandscape() {
  return window.innerWidth > window.innerHeight;
}

function isPhone() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
}

function activeHeader() {
  if (isPhone() && isLandscape()) {
    if (window.scrollY > lastScrollY) {
      header.style.transform = "translateY(-100%)";
      mainElement.classList.add("scroll");
    } else {
      header.style.transform = "translateY(0)";
      mainElement.classList.remove("scroll");
    }
  }

  if (!isPhone()) {
    window.scrollY > 50
      ? header.classList.add("active")
      : header.classList.remove("active");
  }

  lastScrollY = window.scrollY;
}

window.addEventListener("scroll", activeHeader);
