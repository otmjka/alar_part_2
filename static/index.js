'use strict';
var LOGIN_FORM_SEL = 'login-form';

console.log('epic!');

function fetch(opts) {
  var body = opts.body,
      method = opts.method,
      theUrl = opts.theUrl,
      callback = opts.callback,
      xmlHttp = new XMLHttpRequest()

  xmlHttp.onreadystatechange = function() {
      if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
          callback(xmlHttp.responseText);
  }

  xmlHttp.open(method, theUrl, true); // true for asynchronous
  xmlHttp.send(body);
}

function onsubmit(e) {
    console.log('obey!work!');
    fetch('POST', '/login', function(resp) {
      console.log(resp)
    })
    return false;

}

document.addEventListener('DOMContentLoaded', (event) => {
  //the event occurred
  var loginForm = document.getElementById(LOGIN_FORM_SEL);
})
