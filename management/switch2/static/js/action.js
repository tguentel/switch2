function rs_action(rs_action_value) {
  var arrInput = document.getElementsByTagName("input");
  for(var i = 0; i < arrInput.length; i++){
    if (arrInput[i].type == "range") {
      document.getElementById(arrInput[i].id).value = rs_action_value;
    }
  }
  document.getElementById('produce_rs').submit();
}
