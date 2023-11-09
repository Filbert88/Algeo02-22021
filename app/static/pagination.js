document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".card");
  const cardsPerPage = 4;
  let currentPage = 1;

  function showPage(page) {
    const startIndex = (page - 1) * cardsPerPage;
    const endIndex = startIndex + cardsPerPage;
    cards.forEach((card, index) => {
      card.style.display =
        index >= startIndex && index < endIndex ? "" : "none";
    });
    currentPage = page;
    updatePageButtons();
  }

  function updatePageButtons() {
    const pageButtonsContainer = document.getElementById("page-buttons");
    pageButtonsContainer.innerHTML = "";
  
    const totalPages = Math.ceil(cards.length / cardsPerPage);
    const pageButtons = getPageButtons(totalPages, currentPage);
  
    // Create Previous button
    const prevBtn = document.createElement("button");
    prevBtn.textContent = "prev";
    prevBtn.disabled = currentPage === 1;
    prevBtn.addEventListener("click", () => showPage(currentPage - 1));
    pageButtonsContainer.appendChild(prevBtn);
  
    // Create page number buttons
    pageButtons.forEach((button) => {
      const buttonElement = document.createElement("button");
      buttonElement.textContent = button;
      buttonElement.disabled = button === currentPage;
      if (button !== "...") {
        buttonElement.addEventListener("click", () =>
          showPage(parseInt(button))
        );
      }
      pageButtonsContainer.appendChild(buttonElement);
    });
  
    // Create Next button
    const nextBtn = document.createElement("button");
    nextBtn.textContent = "next";
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.addEventListener("click", () => showPage(currentPage + 1));
    pageButtonsContainer.appendChild(nextBtn);
  }
  

  function getPageButtons(totalPages, currentPage) {
    const pageButtons = [];
    const maxVisiblePages = 5;

    if (totalPages <= maxVisiblePages) {
      for (let i = 1; i <= totalPages; i++) {
        pageButtons.push(i);
      }
    } else {
      const leftEllipsis = currentPage > 3;
      const rightEllipsis = currentPage < totalPages - 2;

      if (leftEllipsis) {
        pageButtons.push(1, "..");
      }

      let startPage = currentPage;
      let endPage = currentPage + 1;

      if (endPage > totalPages) {
        endPage = totalPages;
      }

      if (rightEllipsis) {
        endPage = totalPages - 2;
        startPage = Math.max(1, currentPage - 2);
      } else if (leftEllipsis) {
        startPage = totalPages - 4;
        endPage = totalPages;
      } else {
        startPage = currentPage - 2;
        endPage = currentPage + 2;
      }

      if (rightEllipsis) {
        if (currentPage <= 3) {
          for (let i = startPage; i <= startPage + 2; i++) {
            pageButtons.push(i);
          }
        } else {
          for (let i = startPage; i <= startPage; i++) {
            pageButtons.push(i + 2);
          }
        }
      } else if (leftEllipsis) {
        for (let i = totalPages - 2; i <= totalPages; i++) {
          pageButtons.push(i);
        }
      }

      if (rightEllipsis) {
        pageButtons.push("..", totalPages);
      }
    }

    return pageButtons;
  }
  
 

  

  // Initialize
  showPage(1);
  updatePageButtons();
});
