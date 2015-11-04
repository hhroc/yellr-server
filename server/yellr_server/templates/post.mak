<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Yellr Post</title>

    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="static/foundation/css/foundation.css" />

    <style>
      .post {
        padding: 1rem;
      }

      audio {
        width: 100%;
      }

      .container-box {
        border: 1px solid #FFCF13;
        padding: 20px;
        margin-bottom: 10px;
      }

      .container-box h3 {
        margin-top: 10px;
      }

      .votes-container {
        width: 100%;
        text-align: center;
      }

      .question-text {
        padding-top: 10px;
        padding-bottom: 20px;
        font-style: italic;
      }

      .post-contents {
        padding: 10px;
      }

      .post-text {
        font-size: 120%;
      }

      .vote-icon {
        font-size: 250%;
      }

      .up-vote-count {
        color: #1ABC9C;
      }

      .down-vote-count {
        color: #FF6347;
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

      .new-post-contents {
        padding: 10px;
      }

      .anonymous-label {
        font-size: 80%;
        font-weight: bold;
        font-style: italic;
      }

    </style>

  </head>

<body>

% if post:
<div class="post row">
  <div class="medium-10 medium-centered columns">
    <div class="container-box">
      <div class="row">
        <div class="small-2 columns">
          <div class="votes-container">
            <i class="fa fa-caret-up vote-icon up-vote"></i></br>
            <span id="post-up-vote-count-579" class="up-vote-count">${post.up_vote_count}</span></br>
            <span id="post-down-vote-count-579" class="down-vote-count">${post.down_vote_count}</span></br>
            <i class="fa fa-caret-down vote-icon down-vote"></i></br>
          </div>
        </div>
        <div class="small-10 columns">
          <div>
            <span class="right"><i class="fa fa-pencil"></i> ${post.creation_datetime}</span>
            <i class="fa fa-user anonymous-user-label"></i> Anonymous User
          </div>
          % if post.assignment_id != None and post.assignment_id != 0:
              <span><i class="fa fa-question-circle question-text"></i> ${post.assignment.questions[0].question_text}</span>
          % endif;
          <div class="post-contents">
            <p class="post-text">${post.contents}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
% endif;

</body>
</html>
