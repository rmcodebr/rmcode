///////////////
// CSRFToken //
///////////////

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');



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


// Sticky Navbar
$(window).scroll(function () {
  if ($(this).scrollTop() > 25) {
    $(".nav-bar").addClass("sticky-top");
    $(".nav-bar").removeClass("mx-2");
    $(".nav-bar-2").removeClass("mx-2 sm:mx-6 md:mx-10 lg:mx-20 xl:mx-40");

    $(".nav-cart-value").addClass("bg-slate-900/20");
    $(".nav-cart-value").removeClass("bg-slate-900/10");
  } else {
    $(".nav-bar-2").addClass("sm:mx-6 md:mx-10 lg:mx-20 xl:mx-40");
    $(".nav-bar").addClass("mx-2");

    $(".nav-cart-value").removeClass("bg-slate-900/20");
    $(".nav-cart-value").addClass("bg-slate-900/10");
  }
});

/////////////////////
// DARK LIGHT MODE //
/////////////////////


// Persistência do tema
if (
  localStorage.theme === 'dark' ||
  (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
) {
  document.documentElement.classList.add('dark');
} else {
  document.documentElement.classList.remove('dark');
}

// Alternar o tema com ícones
const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;
const lightIcon = document.getElementById('light-icon');
const darkIcon = document.getElementById('dark-icon');

themeToggle.addEventListener('click', () => {
  const isDark = html.classList.toggle('dark'); // Alterna a classe 'dark'
  localStorage.theme = isDark ? 'dark' : 'light';

  // Atualiza visibilidade dos ícones
  lightIcon.classList.toggle('hidden', isDark);
  darkIcon.classList.toggle('hidden', !isDark);
});

