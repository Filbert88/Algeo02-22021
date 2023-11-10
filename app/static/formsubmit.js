document.addEventListener("DOMContentLoaded", function() {
    var searchButton = document.getElementById("searchButton");
    var hiddenSubmitButton = document.getElementById("hiddenSubmitButton");

    if (searchButton && hiddenSubmitButton) {
      searchButton.addEventListener("click", function() {
        // Trigger a click event on the hidden submit button
        hiddenSubmitButton.click();
      });
    }
  });