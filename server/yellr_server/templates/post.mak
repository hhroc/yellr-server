<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Yellr Post</title>

    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
    <!--<link rel="stylesheet" href="static/foundation/css/foundation.css" />-->

    <link href='https://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>

    <style>

      body {
        font-family: 'Lato', sans-serif;
      }

      .icon {
        padding-right: 5px;
      }

      .column-tiny {
          width: 7%;
      }

      .column-large {
        width: 92%;
      }
 
      .column {
        height: 100%;
        display: inline-block;
        vertical-align: top;
      }

      .post {
        margin: auto;
        min-width: 320px;
        max-width: 400px;
      }

      .container-box {
        border: 1px solid #FFCF13;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
      }

      .inside-container {
        padding: .5rem;
        padding-bottom: 1rem;
      }

      .header-blank {
        padding-top: 1rem;
        padding-bottom: 1rem;
        text-align: center;
        width: 100%;
        font-size: 200%;
        background-color: #FFCF13;
        color: black;
        font-weight: bold;
      }

      .votes-container {
        padding-left: .5rem;
        padding-right: .5rem;
        display: inline-block;
      }

      .question-text {
        padding-top: 10px;
        padding-bottom: 20px;
        font-style: italic;
      }

      .question-container {
        font-style: italic;
      }

      .post-text {
        font-size: 120%;
        padding-left: 1rem;
        padding-right: 1rem;
        font-weight: bold;
      }

      .vote-icon {
        font-size: 150%;
      }

      .up-vote-count {
        width: 100%;
        color: #1ABC9C;
        text-align: center;
      }

      .down-vote-count {
        width: 100%;
        color: #FF6347;
        text-align: center;
      }

      .up-vote {
        color: #1ABC9C;
      }

      .down-vote {
        color: #FF6347;
      }

      .assignment-contents {
        padding: 10px;
      }

      .anonymous-user-label {
        font-weight: bold;
        font-style: italic;
      }

      .yellr-label {
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
        background-color: #FFCF13;
        display: inline-block;
        padding: .5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        float: left;
      }

      .yellr-label a {
        text-decoration: none;
        color: black;
      }

      .right {
          float: right;
      }

      .small-text {
        font-size:80%;
      }

    </style>

  </head>

<body>

% if post:
<div class="post">
  <div class="container-box">
  <div class="header-blank">Yellr</div>
  <div class="inside-container">
    <div class="small-text">
      <span class="right"><i class="fa fa-pencil icon"></i> ${post.human_dt}</span>
      <i class="fa fa-user anonymous-user-label icon"></i> Anonymous User
    </div>
    % if post.assignment_id != None and post.assignment_id != 0:
    <div class="question-container small-text">
      <span>
        <i class="fa fa-question-circle question-text icon"></i>
        ${post.assignment.questions[0].question_text}
      </span>
    </div>
    % endif;
    <div class="column column-tiny">
      <div class="votes-container">
        <i class="fa fa-caret-up vote-icon up-vote"></i></br>
        <div class="up-vote-count">${post.up_vote_count}</div>
        <div class="down-vote-count">${post.down_vote_count}</div>
        <i class="fa fa-caret-down vote-icon down-vote"></i></br>
      </div>
    </div>
    <div class="column column-large">
      <p class="post-text">${post.contents}</p>
    </div>
  </div>
  </div>
  <div class="yellr-label"><a href="https://yellr.net/get">Get Yellr</a></div>
</div>
% endif;

</body>
</html>
