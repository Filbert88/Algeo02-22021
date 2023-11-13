document.addEventListener("DOMContentLoaded", function () {
    const cameraPreview = document.getElementById("camera-preview");
    const startStopButton = document.getElementById("start-camera");
    const captureInterval = 10000;
    let intervalId = null;
    let stream = null;
  
    async function startCapture() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraPreview.srcObject = stream;
        startStopButton.textContent = "Stop";
  
        intervalId = setInterval(() => {
          captureAndSubmitImage();
        }, captureInterval);
      } catch (error) {
        console.error("Error accessing camera:", error);
      }
    }
  
    function stopCapture() {
      if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach((track) => track.stop());
        stream = null;
      }
  
      cameraPreview.srcObject = null;
      startStopButton.textContent = "Start";
  
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
    }
  
    function captureAndSubmitImage() {
        const canvas = document.getElementById("frame-canvas");
        const context = canvas.getContext("2d");
      
        canvas.width = cameraPreview.videoWidth;
        canvas.height = cameraPreview.videoHeight;
        context.drawImage(cameraPreview, 0, 0, canvas.width, canvas.height);
      
        canvas.toBlob(function(blob) {
          const selectedForm = document.querySelector(
            'input[name="search-toggle"]:checked'
          ).value;
          const form = selectedForm === "color"
            ? document.getElementById("colorForm")
            : document.getElementById("textureForm");
      
          const formData = new FormData(form);
          formData.append("image", blob, "image.png"); // Add the image blob to the form data
      
          // HTMX AJAX submission (assuming HTMX is set up to handle this)
          htmx.trigger(form, 'submit', {values: formData});
        }, 'image/png');
      }
      
  
    startStopButton.addEventListener("click", () => {
      if (startStopButton.textContent === "Start") {
        startCapture();
      } else {
        stopCapture();
      }
    });
  });
  