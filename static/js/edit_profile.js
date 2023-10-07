const pfpOptions = document.getElementsByClassName('pfp-option')

const selected = document.getElementById('pfp')

function updateSelected() {
  for(const opt of pfpOptions) {
    opt.classList.toggle('pfp-option-selected',opt.getAttribute('src') == selected.value)
  }
}

for(const opt of pfpOptions) {
  opt.addEventListener('click', e => {
    selected.value = opt.getAttribute('src')
    updateSelected()
  })
}

const form = document.getElementById('pfp-form')

form.addEventListener('submit', e => {
  e.preventDefault()
  fetch('/api/update-profile', {
    method: 'POST',
    headers: {
      'Cookie': document.cookie
    },
    body: new FormData(form),
  }).then(res => {
      if(res.status == 200) {
        location.href = '/profile'
      } else {
        console.log(`Error updating profile: Server returned ${res.status}(${res.statusText})`)
      }
    }).catch(err => {
      console.log(`Error updating profile: ${err}`)
    })
})

updateSelected()
