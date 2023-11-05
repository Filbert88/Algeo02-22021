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
    var validTypes = ['image/jpeg', 'image/png','image/jpg'];
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
