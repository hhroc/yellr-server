<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Yellr Post</title>

    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css"/>
    <!--<link rel="stylesheet" href="static/foundation/css/foundation.css" />-->

    <link rel="stylesheet" href="static/plyr/plyr.css"/>

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

      .header-media {
        width: 100%;
      }

      .header-media img {
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        max-width: 398px;*/
        width: 100%;
        border-bottom: 1px solid #FFCF13;
      }

      .header-media video {
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        max-width: 398px;*/
        width; 100%;
        border-bottom: 1px solid #FFCF13;
      }

      .header-media audio {
        padding: 10%;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        max-width: 398px;*/
        width: 80%;
        border-bottom: 1px solid #FFCF13;
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

      .results-container {
        padding-left: 1rem;
        padding-right: 1rem;
      }

      .poll-percentage {
        padding-right: 4rem;
      }

      .poll-results {
        margin-left: 1rem;
        margin-right: 1rem;
      }

      .poll-result {
        margin-bottom: .25rem;
        border-radius: 4px;
        border: 1px solid #AAAAAA;
        padding: .25rem;
      }

      .poll-bar {
        height: .5rem;
      }

      .first-result-bar {
        background-color: red;
      }

      .second-result-bar {
        background-color: green;
      }

      .third-result-bar {
        background-color: blue;
      }

      .fourth-result-bar {
        background-color: orange;
      }

      .fifth-result-bar {
        background-color: purple;
      }


    </style>

  </head>

<body>

% if assignment:
<div class="post">
  <div class="container-box">
    <div class="header-blank">Yellr</div>
    <div class="inside-container">
      <div class="question-container small-text">
        <span>
          <i class="fa fa-question-circle question-text icon"></i>
          ${assignment.questions[0].question_text}
        </span>
      </div>
      <div class="results-container">
      % for percent in assignment.percents:
      <label>${percent['name']}</label>
      <div class="poll-result">
        <div class="poll-percent">
          ${int(percent['percent'])}%  ${int(percent['count'])} / ${int(assignment.response_count)}
        </div>
        <div class="poll-bar ${percent['index']}-result-bar" style="width: ${percent['percent'] if percent['percent'] != 0 else '8px'};">
        </div>
      </div>
      % endfor
      </div>
    </div>
    <div class="yellr-label"><a href="https://yellr.net/get">Get Yellr</a></div>
  </div>
</div>
% endif;

<script src="static/plyr/plyr.js"></script>

</body>
</html>
