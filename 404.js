/*
  Inspired by: "错误, 404"
  By: Sujeet Mishra
  Link: https://dribbble.com/shots/4571035-Error-404
*/

let oh = document.querySelector('.circle.oh');

document.addEventListener('mousemove', event => {
  let domainX = [0, document.body.clientWidth],
  domainY = [0, document.body.clientHeight],
  range = [-10, 10];

  let translate = {
    x: range[0] + (event.clientX - domainX[0]) * (range[1] - range[0]) / (domainX[1] - domainX[0]),
    y: range[0] + (event.clientY - domainY[0]) * (range[1] - range[0]) / (domainY[1] - domainY[0]) };


  oh.style.animation = 'none';
  oh.style.transform = `translate(${translate.x}px, ${translate.y}px)`;
});

document.addEventListener('mouseleave', event => {
  oh.style.animation = 'floating 3s linear infinite';
});

// Ensure the "返回首页" control navigates home.
// Preferred: use the anchor's default behavior. As a fallback (if the element
// is still a non-anchor with id 'home-button' or 'index.html'), attach a click
// handler that navigates to the homepage.
(function() {
  const home = document.getElementById('home-button') || document.getElementById('index.html');
  if (!home) return;
  // If it's an anchor, do nothing and let the browser handle the navigation.
  if (home.tagName && home.tagName.toUpperCase() === 'A') return;
  // Otherwise, attach a click handler to navigate to the site root or index page.
  home.addEventListener('click', function() {
    // Use absolute root path to be safe on GitHub Pages; falls back to './index.html'
    const target = '/';
    window.location.href = target;
  });
})();
