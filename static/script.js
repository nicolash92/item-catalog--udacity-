function signOut() {
  localStorage.removeItem('token');
  if (gapi.auth2) {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function() {
      console.log('User signed out.');
    });
  }
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:5000/oauthcallback');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    window.location.href = 'http://localhost:5000/';
  };
  xhr.send('signout');
}

function onSignIn(googleUser) {
  var id_token = googleUser.getAuthResponse().id_token;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:5000/oauthcallback');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (localStorage.getItem('token')) {
      localStorage.setItem('token', xhr.responseText);
    } else {
      localStorage.setItem('token', xhr.responseText);
      window.location.href = 'http://localhost:5000/';
    }
  };
  xhr.send('idtoken=' + id_token);
}

function getRequestHandler(url) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'http://localhost:5000' + url);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  if (localStorage.getItem('token')) {
    xhr.setRequestHeader(
      'Authorization',
      'Token ' + localStorage.getItem('token')
    );
  }
  xhr.onload = function() {
    if (xhr.responseText == 'Unauthorized Access') {
      window.location.href = 'http://localhost:5000/';
    } else {
      document.querySelector('#response').innerHTML = xhr.responseText;
      window.history.pushState('object or string', 'Title', url);

      if (localStorage.getItem('token')) {
        refreshToken();
      }
    }
    /*document.open();
    document.write(xhr.responseText);
    document.close();
    */
    //document.querySelector('response').innerHTML(responseText);
  };
  xhr.send();
}

function deleteItem(item) {
  var xhr = new XMLHttpRequest();
  xhr.open('DELETE', 'http://localhost:5000/catalog/' + item + '/delete');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  if (localStorage.getItem('token')) {
    xhr.setRequestHeader(
      'Authorization',
      'Token ' + localStorage.getItem('token')
    );
  }
  xhr.onload = function() {
    window.location.href = 'http://localhost:5000/';
  };
  xhr.send();
}

function submitForm(ev, method, url, formid) {
  ev.preventDefault();

  var xhr = new XMLHttpRequest();
  var form = document.getElementById(formid);
  var FD = new FormData(form);

  xhr.open(method, 'http://localhost:5000' + url);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader(
    'Authorization',
    'Token ' + localStorage.getItem('token')
  );
  xhr.onload = function() {
    window.location.href = 'http://localhost:5000/';
  };
  xhr.onerror = function() {
    console.error('Unable to complete Request');

    window.location.href = 'http://localhost:5000/';
  };
  var object = {};
  FD.forEach(function(value, key) {
    object[key] = value;
  });
  var json = JSON.stringify(object);
  xhr.send(json);

  console.log(json);
}

function refreshToken() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'http://localhost:5000/token');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader(
    'Authorization',
    'Token ' + localStorage.getItem('token')
  );

  xhr.onload = function() {
    localStorage.setItem('token', xhr.responseText);
  };
  xhr.send();
}
