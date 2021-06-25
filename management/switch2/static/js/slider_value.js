function th_slider_value(value, id) {
  document.getElementById(`${id}_slider`).innerHTML = value;
}

function rs_slider_value(value, id) {
  document.getElementById(`${id}_slider`).innerHTML = value * 100;
}
