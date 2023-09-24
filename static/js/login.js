const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

loginTab.addEventListener("click", () => {
  loginForm.style.display = "flex";
  registerForm.style.display = "none";
  loginTab.classList.add("active");
  registerTab.classList.remove("active");
});

registerTab.addEventListener("click", () => {
  loginForm.style.display = "none";
  registerForm.style.display = "flex";
  loginTab.classList.remove("active");
  registerTab.classList.add("active");
});

loginForm.addEventListener('submit', (e) => {
  e.preventDefault()
  const formData = new FormData(loginForm)
  fetch('/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: new FormData(loginForm),
  }).then(res => {
    console.log(res)
  }).catch(err => {
    console.log(`Error: ${err}`)
  })
})
