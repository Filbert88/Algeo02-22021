document.addEventListener("DOMContentLoaded", function () {
  const cameraPreview = document.getElementById("camera-preview");
  const startCameraButton = document.getElementById("start-camera");
  const hiddenSearchButton = document.getElementById("hiddenSearchButton");
  let cameraStream = null;
  let captureInterval = null;
  let canvas = document.createElement("canvas");

  startCameraButton.addEventListener("click", function () {
    if (this.textContent === "Start") {
      startCamera();
      this.textContent = "Stop";
      captureInterval = setInterval(captureAndSearch, 10000);
    } else {
      stopCamera();
      this.textContent = "Start";
      clearInterval(captureInterval);
    }
  });

  function startCamera() {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        cameraStream = stream;
        cameraPreview.srcObject = stream;
      })
      .catch((err) => console.error("Error accessing camera: ", err));
  }

  function stopCamera() {
    if (cameraStream) {
      const tracks = cameraStream.getTracks();
      tracks.forEach((track) => track.stop());
      cameraPreview.srcObject = null;
    }
  }

  hiddenSearchButton.addEventListener("click", function (e) {
    e.preventDefault();
    const isColorSelected = document.getElementById("color").checked;
    const imageInput = document.createElement("input");
    imageInput.type = "hidden";
    imageInput.name = "image";
    const dataURL = canvas.toDataURL("image/png");
    const base64Data = dataURL.split(",")[1];
    imageInput.value = base64Data;

    if (isColorSelected) {
      const colorForm = document.getElementById("colorForm");
      colorForm.appendChild(imageInput);
      document.getElementById("colorSubmitButton").click();
      colorForm.removeChild(imageInput);
    } else {
      const textureForm = document.getElementById("textureForm");
      textureForm.appendChild(imageInput);
      document.getElementById("textureSubmitButton").click();
      textureForm.removeChild(imageInput);
    }
  });

  function captureAndSearch() {
    canvas.width = cameraPreview.videoWidth;
    canvas.height = cameraPreview.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(cameraPreview, 0, 0, canvas.width, canvas.height);

    hiddenSearchButton.click();
  }
});
