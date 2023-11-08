window.onscroll = function() {
    var header = document.querySelector('.header');
    if (window.scrollY > 100) {  // Adjust the 100px offset as needed
        header.classList.add('shrink');
    } else {
        header.classList.remove('shrink');
    }
};