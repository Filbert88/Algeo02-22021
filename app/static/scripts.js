function showFileName(files) {
  var fileName = document.getElementById("file-chosen");

  if (files.length > 0) {
    fileName.textContent = files[0].name;
  } else {
    fileName.textContent = "No file chosen";
  }
}

function handleFiles(files) {
  var imageType = /^image\//;

  if (!files.length) {
    alert("Please select a file.");
    return;
  }

  var file = files[0];
  var validTypes = ["image/jpeg", "image/png", "image/jpg"];
  if (!validTypes.includes(file.type)) {
    alert("Please select a JPG, JPEG or PNG image.");
    return;
  }

  var img = document.createElement("img");
  img.classList.add("obj");
  img.file = file;

  var preview = document.getElementById("preview");
  preview.innerHTML = "";
  preview.appendChild(img);

  var reader = new FileReader();
  reader.onload = (function (aImg) {
    return function (e) {
      aImg.src = e.target.result;
    };
  })(img);
  reader.readAsDataURL(file);
}

function dragOverHandler(ev) {
  console.log("File(s) in drop zone");
  ev.preventDefault();
  ev.currentTarget.classList.add('dragover');
}

function dropHandler(ev) {
    console.log('File(s) dropped');
    ev.preventDefault();
    ev.currentTarget.classList.remove('dragover');
    if (ev.dataTransfer.items) {
      for (var i = 0; i < ev.dataTransfer.items.length; i++) {
        if (ev.dataTransfer.items[i].kind === 'file') {
          var file = ev.dataTransfer.items[i].getAsFile();
          
          if(['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
            console.log('... file[' + i + '].name = ' + file.name);
            document.getElementById('file-chosen').textContent = file.name;
            handleFiles([file]);
          } else {
            console.log('File type not supported: ', file.type);
            document.getElementById('file-chosen').textContent = 'File type not supported, please select an image.';
          }
        }
      }
    }
  }

  function dragLeaveHandler(ev) {
    ev.currentTarget.classList.remove('dragover');
  }

function updateImagePreview(file) {
  var reader = new FileReader();
  reader.onload = function (e) {
    var img = document.createElement("img");
    img.src = e.target.result;
    img.classList.add("obj");
    // Clear the preview and append the new image
    var preview = document.getElementById("preview");
    preview.innerHTML = "";
    preview.appendChild(img);
  };
  reader.readAsDataURL(file);
}

function loadFile(event) {
  updateImagePreview(event.target.files[0]);
}

document.addEventListener('DOMContentLoaded', function() {
  var preview = document.getElementById('preview');
  preview.addEventListener('dragover', dragOverHandler);
  preview.addEventListener('dragleave', dragLeaveHandler);
  preview.addEventListener('drop', dropHandler);
  preview.addEventListener('click', function() {
      document.getElementById('sharedFileInput').click();
  });
});