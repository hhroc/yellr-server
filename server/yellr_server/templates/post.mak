<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Yellr Post</title>

    <style>
      .post {
        border: 1px solid #AAAAAA;
        border-radius: 5px;
        padding: 1rem;
      }
    </style>

  </head>

  <body>
    % if post:
    <div class="post">
      <p>${post.contents}</p>
    </div>
    % endif;
  </body>
</html>
