document.addEventListener('DOMContentLoaded', (event) => {
    const fadeInElements = document.querySelectorAll('.fade-in-right, .fade-in-left, .fade-in-up, .fade-in-down');
  
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const target = entry.target;
          if (target.classList.contains('fade-in-right')) {
            target.classList.add('start-fade-in-right');
          } else if (target.classList.contains('fade-in-left')) {
            target.classList.add('start-fade-in-left');
          } else if (target.classList.contains('fade-in-up')) {
            target.classList.add('start-fade-in-up');
          } else if (target.classList.contains('fade-in-down')) {
            target.classList.add('start-fade-in-down');
          }
          observer.unobserve(target); // Stop observing the target after animation starts
        }
      });
    }, {
      threshold: 0.1 // Adjust if you want the animation to start earlier or later
    });
  
    fadeInElements.forEach((el) => {
      observer.observe(el); // Observe each element
    });
  });
  