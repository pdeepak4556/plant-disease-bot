const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

// Check if there is a stored mode preference
const mode = localStorage.getItem("mode");

// If mode is stored and it's sign-up mode, add the class
if (mode === "sign-up-mode") {
  container.classList.add("sign-up-mode");
}

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
  // Store the mode preference in localStorage
  localStorage.setItem("mode", "sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
  // Store the mode preference in localStorage
  localStorage.setItem("mode", "");
});
