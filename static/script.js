document.addEventListener("DOMContentLoaded", function () {
  let currentImageIndex = 0;
  const images = document.querySelectorAll(".carousel img");
  const totalImages = images.length;

  function showImage(index) {
    images.forEach((img, i) => {
      img.classList.toggle("active", i === index);
    });
  }

  function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % totalImages;
    showImage(currentImageIndex);
  }

  setInterval(nextImage, 5000);
  showImage(currentImageIndex);
});

const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});
