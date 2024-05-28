document.addEventListener('DOMContentLoaded', function() {
  const hamburger = document.querySelector('.hamburger');
  const hamburgerMenu = document.querySelector('.hamburger_menu');
  const hamburgerOverlay = document.querySelector('.hamburger_overlay');

  hamburger.addEventListener('click', function() {
    hamburgerMenu.style.display = 'flex';
    hamburgerOverlay.style.display = 'block';
  });

  hamburgerOverlay.addEventListener('click', function() {
    hamburgerMenu.style.display = 'none';
    hamburgerOverlay.style.display = 'none';
  });
});