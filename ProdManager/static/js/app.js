
function do_display_toggle() {
  target = document.querySelector(this.getAttribute("target"))

  if (target) {
    target.classList.toggle("hidden")
  }
}

function register_display_toggles() {
  for (let el of document.querySelectorAll(".display-toggle")) {
    el.onclick = do_display_toggle
  }
}

function main() {
  register_display_toggles()
}

window.addEventListener("DOMContentLoaded", main, false)
