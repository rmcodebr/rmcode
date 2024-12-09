/////////////////
// INSTALL PWA //
/////////////////

// Detect if app is running in standalone mode
if (window.matchMedia("(display-mode: standalone)").matches) {
  // Hide the install button if app is already installed
  document.getElementById("installApp").style.display = "none";
} else {
  // Show the install button and handle click to prompt installation if needed
  const installButton = document.getElementById("installApp");
  let deferredPrompt;

  // Listen for the 'beforeinstallprompt' event
  if(installButton){
    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      deferredPrompt = e; // Store the event
      installButton.style.display = "block";
  
      installButton.addEventListener("click", async () => {
        if (deferredPrompt) {
          deferredPrompt.prompt();
          const { outcome } = await deferredPrompt.userChoice;
          if (outcome === "accepted") {
            console.log("User accepted the installation");
            installButton.style.display = "none";
          }
          deferredPrompt = null;
        }
      });
    });
  }
}


//////////////////////////
// NO INTERNET FUNCTION //
//////////////////////////

(function () {
  "use strict";

  // Wait until the DOM is ready
  document.addEventListener("DOMContentLoaded", function () {
    const intStatus = document.getElementById("internetStatus");
    const backText = "Sua internet voltou";
    const lostText = "Oops! Você esta sem internet";
    const successColor = "#47cfca";
    const failureColor = "#dc3545";

    if (window.navigator.onLine) {
      intStatus.textContent = backText;
      intStatus.style.backgroundColor = successColor;
      intStatus.style.color = "black";
      intStatus.style.textAlign = "center";
      intStatus.style.display = "none";
    } else {
      intStatus.textContent = lostText;
      intStatus.style.backgroundColor = failureColor;
      intStatus.style.color = "white";
      intStatus.style.textAlign = "center";
      intStatus.style.display = "block";
    }

    window.addEventListener("online", function () {
      intStatus.textContent = backText;
      intStatus.style.backgroundColor = successColor;
      intStatus.style.color = "black";
      intStatus.style.textAlign = "center";
      intStatus.style.display = "block";
      var hideTime = setTimeout(function () {
        intStatus.style.display = "none";
      }, 5000);
    });

    window.addEventListener("offline", function () {
      intStatus.textContent = lostText;
      intStatus.style.backgroundColor = failureColor;
      intStatus.style.color = "white";
      intStatus.style.textAlign = "center";
      intStatus.style.display = "block";
    });
  });
})();
