function po_slider_value(value, id) {
  document.getElementById(`${id}_slider`).innerHTML = value.replace('1','AN').replace('0','AUS');
}

function lid_slider_value(value, id) {
  document.getElementById(`${id}_slider`).innerHTML = value * 100;
}

function li_slider_value(value, id) {
  document.getElementById(`${id}_slider`).innerHTML = value.replace('1','AN').replace('0','AUS');
}

function th_slider_value(value, id) {
  document.getElementById(`${id}_slider`).innerHTML = value;
}

function rs_slider_value(value, id) {
  document.getElementById(`${id}_slider`).innerHTML = value * 100;
}
