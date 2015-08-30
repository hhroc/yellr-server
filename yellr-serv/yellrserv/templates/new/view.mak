<html>
<head>

  <title>Yellr - Hyper-local, community driven news</title>

  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <link rel="stylesheet" href="static/new/foundation/css/foundation.css" />
  <!--<link rel="stylesheet" href="static/new/css/font-awesome.min.css" />-->
  <!-- TODO: pull this from our server locally -->
  <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="static/new/css/site.css" />

  <style>
    .embedded-post-wrapper {
        margin: 1rem;
    }
  </style>

</head>
<body>
<div class="embedded-post-wrapper">
% if valid == True:
<div class="row">
  <div class="medium-10 medium-centered columns">
    <div class="container-box">
      <div class="row">
        <div class="small-2 columns">
          <div class="votes-container">
            ##<a onclick="doUpVote(${post['post_id']});">
              ##% if post['has_voted'] == True and post['is_up_vote'] == True:
              <i id="post-up-vote-${post['post_id']}" class="fa fa-caret-up vote-icon up-vote"></i></br>
              ##% else:
              ##<i id="post-up-vote-${post['post_id']}" class="fa fa-caret-up vote-icon no-vote"></i></br>
            ##</a>
            ##% endif
            <span id="post-up-vote-count-${post['post_id']}" class="up-vote-count">${post['up_vote_count']}</span></br>
            <span id="post-down-vote-count-${post['post_id']}" class="down-vote-count">${post['down_vote_count']*(-1)}</span></br>
            ##<a onclick="doDownVote(${post['post_id']});">
              ##% if post['has_voted'] == True and post['is_up_vote'] == False:
              <i id="post-down-vote-${post['post_id']}" class="fa fa-caret-down vote-icon down-vote"></i></br>
              ##% else:
              ##<i id="post-down-vote-${post['post_id']}" class="fa fa-caret-down vote-icon no-vote"></i></br>
              ##% endif
            ##</a>
          </div>
        </div>
        <div class="small-10 columns">
          <div>
            <span class="right"><i class="fa fa-pencil"></i> ${post['post_datetime_ago']}</span>
            <i class="fa fa-user anonymous-user-label"></i> Anonymous User
          </div>
          % if post['question_text'] != None:
          <span><i class="fa fa-question-circle question-text"></i> ${post['question_text']}</span>
          % endif
          <div class="post-contents">
            ## post an image
            % if post['media_objects'][0]['media_type_name'] == "image":
            <p class="post-text">${post['media_objects'][0]['caption']}</p>
            <img src="/media/${post['media_objects'][0]['preview_file_name']}"/>
            ## post video
            % elif post['media_objects'][0]['media_type_name'] == "video":
            <p class="post-text">${post['media_objects'][0]['caption']}</p>
            <video width="640" height="360" poster="/media/${post['media_objects'][0]['preview_file_name']}" type="video/mp4" id="player1" src="/media/${post['media_objects'][0]['file_name']}" controls="controls" preload="none"></video>
            ## post audio
            % elif post['media_objects'][0]['media_type_name'] == "audio":
            <p class="post-text">${post['media_objects'][0]['caption']}</p>
            ## <img src=""/>
             <h4>Audio Recording:</h4>
            <audio id="player-${post["media_objects"][0]["media_id"]}" src="/media/${post['media_objects'][0]['file_name']}" controls> </audio>
            ## text
            % else:
            <p class="post-text">${post['media_objects'][0]['media_text']}</p>
            % endif
          </div>
        </div>
        </br></br></br>
        <div>
          <div class="right"><a style="padding-right: 1rem;" href="yellr.net/local">Join The Conversation</a></div>
          <div><a style="padding-left: 1rem;" href="https://yellr.net/">yellr.net</a></div>
        </div>
      </div>
    </div>

% endif
</div>

<script src="static/new/js/mediaelement-and-player.min.js"></script>
<link rel="stylesheet" href="static/new/css/mediaelementplayer.min.css" />

</html>
</body>
