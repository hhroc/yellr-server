<%inherit file="base.mak"/>

<div class="row">
  <div class="large-12 columns">
    <div class="tab-links">
      <div class="tab-link-container selected-tab"><a class="tab-link top-link-divider" href="/local">Local</a></div>
      <div class="tab-link-container"><a class="tab-link top-link-divider" href="/assignments">Assignments</a></div>
      <div class="tab-link-container"><a class="tab-link top-link-divider" href="/stories">Stories</a></div>
      <div class="tab-link-container"><a class="tab-link" href="/post">Post</a></div>
    </div>
    <hr/>
  </div>
</div>

<div class="row">
  <div class="medium-10 medium-centered columns">
    % for post in posts:
    <div class="container-box">
      <div class="row">
        <div class="small-2 columns">
          <div class="votes-container">
            <a onclick="doUpVote(${post['post_id']});">
              % if post['has_voted'] == True and post['is_up_vote'] == True:
              <i id="post-up-vote-${post['post_id']}" class="fa fa-caret-up vote-icon up-vote"></i></br>
              % else:
              <i id="post-up-vote-${post['post_id']}" class="fa fa-caret-up vote-icon no-vote"></i></br>
            </a>
            % endif
            <span id="post-up-vote-count-${post['post_id']}">${post['up_vote_count']}</span></br>
            <span id="post-down-vote-count-${post['post_id']}">${post['down_vote_count']}</span></br>
            <a onclick="doDownVote(${post['post_id']});">
              % if post['has_voted'] == True and post['is_up_vote'] == False:
              <i id="post-down-vote-${post['post_id']}" class="fa fa-caret-down vote-icon down-vote"></i></br>
              % else:
              <i id="post-down-vote-${post['post_id']}" class="fa fa-caret-down vote-icon no-vote"></i></br>
              % endif
            </a>
          </div>
        </div>
        <div class="small-10 columns">
          <div>
            <i class="fa fa-pencil right"> 20h</i>
            <i class="fa fa-user anonymous-user-label"> Anonymous User</i>
          </div>
          <i class="fa fa-question-circle question-text"> ${post['question_text']}</i>
          <div class="post-contents">
            % if post['media_objects'][0]['media_type_name'] == "image":
            <p>${post['media_objects'][0]['caption']}</p>
            <img src="/media/${post['media_objects'][0]['file_name']}"></img>
            % else:
            <span>${post['media_objects'][0]['media_text']}</span>
            % endif
          </div>
        </div>
      </div>
    </div>
    % endfor
  </div>
</div>

<script>

  function doUpVote(postId) {
    voteAction(postId, true);
  }

  function doDownVote(postId) {
    voteAction(postId, false);
  }

  function voteAction(postId, isUpVote) {

    var is_up_vote = 1;
    var d = 'up';
    var nd = 'down'
    if ( !isUpVote ) {
      is_up_vote = 0;
      d = 'down';
      nd = 'up';
    }

    if ( $('#post-'+nd+'-vote-' + postId).hasClass(nd + '-vote') ) {
      var count = parseInt($('#post-'+nd+'-vote-count-' + postId).html());
      count--;
      $('#post-'+nd+'-vote-count-' + postId).html(count);
    }

    $('#post-'+nd+'-vote-' + postId).removeClass(nd + '-vote');
    $('#post-'+nd+'-vote-' + postId).removeClass('no-vote');
    $('#post-'+nd+'-vote-' + postId).addClass('no-vote');

    url = "/register_vote.json?cuid=${cuid}&language_code=en&lat=${lat}&lng=${lng}";
    $.ajax({
        type: 'POST',
        url: url,
        data: {
          post_id: postId,
          is_up_vote: is_up_vote,
        },
        dataType: 'json',
        success: function() {
          var count = parseInt($('#post-'+d+'-vote-count-' + postId).html());
          if ( $('#post-'+d+'-vote-' + postId).hasClass(d+'-vote')) {
            $('#post-'+d+'-vote-' + postId).removeClass(d+'-vote');
            $('#post-'+d+'-vote-' + postId).addClass('no-vote');
            count--;
          } else {
            // client has not yet voted
            $('#post-'+d+'-vote-' + postId).removeClass(d+'-vote');
            $('#post-'+d+'-vote-' + postId).addClass(d+'-vote');
            count++;
          }
          $('#post-'+d+'-vote-count-' + postId).html(count)
        },
      });
  }

</script>
