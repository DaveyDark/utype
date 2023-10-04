const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const loginInfo = document.getElementById("loginInfo")
const registerInfo = document.getElementById("registerInfo")

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

registerForm.addEventListener('submit', (e) => {
  e.preventDefault()
  const username = document.getElementById("username2")
  const password = document.getElementById("password2")
  const passwordConfirm = document.getElementById("password-confirm")
  if(username.value.length > 25) {
    registerInfo.innerHTML = "Username is too long"
    return;
  }
  if(username.value.length == 0) {
    registerInfo.innerHTML = "Username cannot be empty"
    return;
  }
  if(!/^[a-zA-Z0-9._]+$/.test(username.value)){
    registerInfo.innerHTML = "Username can only contain characters A-Z, 0-9, _ and ."
    return;
  }
  if(password.value.length > 25) {
    registerInfo.innerHTML = "Password is too long"
    return;
  }
  if(password.value.length < 8) {
    registerInfo.innerHTML = "Password is too short"
    return;
  }
  if(password.value != passwordConfirm.value) {
    registerInfo.innerHTML = "Passwords do not match"
    return;
  }
  fetch('/api/register', {
    method: 'POST',
    body: new FormData(registerForm),
  }).then(res => {
      if(res.status == 201) {
        registerInfo.innerHTML = "Registration Successful"
        window.location = "/profile/edit";
      } else if(res.status == 409) {
        registerInfo.innerHTML = "Username already taken"
      }
  }).catch(err => {
    console.error(`Error: ${err}`)
  })
})
loginForm.addEventListener('submit', (e) => {
  e.preventDefault()
  const username = document.getElementById("username")
  const password = document.getElementById("password")
  fetch('/api/login', {
    method: 'POST',
    body: new FormData(loginForm),
  }).then(res => {
      if(res.status == 200) {
        window.location = "/home";
      } else if(res.status == 401) {
        loginInfo.innerHTML = "Incorrect username or password"
      } else if(res.status == 429) {
        loginInfo.innerHTML = "Too many attempts"
      }
  }).catch(err => {
    console.error(`Error: ${err}`)
  })
})
