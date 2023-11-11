document.addEventListener('DOMContentLoaded', function() {
  const sharedFileInput = document.getElementById('sharedFileInput');
  const colorForm = document.getElementById('colorForm');
  const textureForm = document.getElementById('textureForm');
  const searchButton = document.getElementById('searchButton');
  const colorSubmitButton = document.getElementById('colorSubmitButton');
  const textureSubmitButton = document.getElementById('textureSubmitButton');

  searchButton.addEventListener('click', function(e) {
    e.preventDefault();
    const isColorSelected = document.getElementById('color').checked;
    if (isColorSelected) {
      colorForm.appendChild(sharedFileInput);
      colorSubmitButton.click();
    } else {
      textureForm.appendChild(sharedFileInput);
      textureSubmitButton.click();
    }
  });
});