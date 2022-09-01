
function do_display_toggle() {
  const targets = document.querySelectorAll(this.getAttribute("target"))

  for (let target of targets) {
    target.classList.toggle("hidden")
  }
}

function register_display_toggles() {
  for (let el of document.querySelectorAll(".display-toggle")) {
    el.onclick = do_display_toggle
  }
}

function remove_filter(search_param, old_param) {
  new_params = new URLSearchParams()

  for (let param of search_param.entries()) {
    if (param[0] != old_param[0] || param[1] != old_param[1]) {
      new_params.append(param[0], param[1])
    }
  }

  window.location.search = new_params
}

function handle_filters() {
  const params = new URLSearchParams(window.location.search)

  var filters = []

  for (let param of params.entries()) {
    if (VALID_FILTERS.includes(param[0]) && param[1]) {
      filters.push(param)
    }
  }

  if (filters.length > 0) {
    document.querySelector("h3#filters").classList.toggle("hidden")
  }

  const filter_holder = document.querySelector("div#list_filters")
  const filter_template = filter_holder.querySelector("div.filter#template")

  for (let filter of filters) {
    let element = filter_template.cloneNode(true)

    element.classList.toggle("hidden")
    element.setAttribute("id", filter[0])
    element.querySelector(".name").innerText = filter[0]
    element.querySelector(".value").innerText = filter[1]

    element.onclick = () => { remove_filter(params, filter) }

    filter_holder.append(element)
  }
}

AUTO_RELOAD_TIMEOUT = null

function enable_disable_auto_reload(value) {
  if (value) {
    console.log("Enabling auto reload")
    AUTO_RELOAD_TIMEOUT = setTimeout(() => window.location.reload(), 60000)
  } else if (AUTO_RELOAD_TIMEOUT) {
    console.log("Disabling auto reload")
    clearTimeout(AUTO_RELOAD_TIMEOUT)
  }
}

function do_auto_reload_toggle() {
  toggle = document.querySelector(".auto_reload .switch input")

  last_value = JSON.parse(localStorage.getItem('auto-reload'))
  new_value = !last_value
  localStorage.setItem('auto-reload', new_value)

  enable_disable_auto_reload(new_value)
}

function register_auto_reload_toggles() {
  el = document.querySelector(".auto_reload .switch input")
  el.onclick = do_auto_reload_toggle

  el.checked = JSON.parse(localStorage.getItem('auto-reload'))
  enable_disable_auto_reload(el.checked)
}

function main() {
  register_display_toggles()
  register_auto_reload_toggles()

  if (typeof VALID_FILTERS !== 'undefined') {
    handle_filters()  
  }
}

window.addEventListener("DOMContentLoaded", main, false)
