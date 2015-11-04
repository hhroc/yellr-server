<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Yellr - Login</title>

    <link href='https://fonts.googleapis.com/css?family=Open+Sans:300' rel='stylesheet' type='text/css'>
    <link href="${request.static_url('yellr_server:static/login.css')}" rel="stylesheet">

  </head>
  <body>
    <div class="login-wrapper">
      <h1>Yellr</h1>
      <p>Communicate with your community</p>
      <div class="login-box">
        <label>Username</label>
        <input type="text" id="input-username"></input>
        <label>Password</label>
        <input type="password" id="input-password"></input>
        <div id='bad-login-box'>
          Invalid credentials, try again
        </div>
        <button id="button-login">Login</button>
      </div>
    </div>

    <script src="static/jquery-1.11.3.min.js"></script>
    <script src="static/jquery.sha256.js"></script>
    <script>
      $(document).ready(function() {
        $('#button-login').on('click', function() {
          $.ajax({
            url: '/api/admin/login',
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                'username': $('#input-username').val(),
                'password': $.sha256($('#input-password').val())
            }),
            success: function(data) {
              if( data.user != null ) {
                window.location = '/moderator/';
              } else {
                $('#bad-login-box').show();
              }
            }
          });
        });
      });
    </script>

  </body>
</html>
