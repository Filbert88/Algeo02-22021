window.onscroll = function () {
  var header = document.querySelector(".header");
  if (window.scrollY > 100) {
    header.classList.add("shrink");
  } else {
    header.classList.remove("shrink");
  }
};
