<%inherit file="base.mak"/>

<div class="row">
  <div class="large-12 columns">
    <div class="tab-links">
      <div class="tab-link-container"><a class="tab-link top-link-divider" href="/local">Local</a></div>
      <div class="tab-link-container selected-tab"><a class="tab-link top-link-divider" href="/assignments">Assignments</a></div>
      <div class="tab-link-container"><a class="tab-link top-link-divider" href="/stories">Stories</a></div>
      <div class="tab-link-container"><a class="tab-link" href="/post">Post</a></div>
    </div>
    <hr/>
  </div>
</div>

<div class="row">
  <div class="medium-10 medium-centered columns">
    % for assignment in assignments:
    <div class="container-box">
      <div>
        <i class="fa fa-comments right"> ${assignment['post_count']}</i>
        <i class="fa fa-user organization-label"> ${assignment['organization']}</i> 
      </div>
      <div class="assignment-contents">
        <h3><a href="#">${assignment['question_text']}</a></h3>
        <span>${assignment['description']}</span>
      </div>
    </div>
    % endfor
  </div>
</div>

