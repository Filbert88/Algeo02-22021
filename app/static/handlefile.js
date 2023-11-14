function updateFileName() {
  var input = document.getElementById("zipfile");
  var fileNameDisplay = document.getElementById("zip-file-name");
  if (input.files && input.files.length > 0) {
    var fileName = input.files[0].name;
    fileNameDisplay.textContent = fileName;
  } else {
    fileNameDisplay.textContent = "No file chosen";
  }
}

function updateFolderName() {
  var folderInput = document.getElementById("folder");
  var folderNameDisplay = document.getElementById("folder-name");
  if (folderInput.files.length > 0) {
    folderNameDisplay.textContent = "Folder selected";
  } else {
    folderNameDisplay.textContent = "No folder chosen";
  }
}
