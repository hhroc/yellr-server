<%inherit file="base.mak"/>

<div class="row">
  <div class="large-12 columns">
    <div class="tab-links">
      <div class="tab-link-container"><a class="tab-link top-link-divider" href="/local">Local</a></div>
      <div class="tab-link-container"><a class="tab-link top-link-divider" href="/assignments">Assignments</a></div>
      <div class="tab-link-container selected-tab"><a class="tab-link top-link-divider" href="/stories">Stories</a></div>
      <div class="tab-link-container"><a class="tab-link" href="/post">Post</a></div>
    </div>
    <hr/>
  </div>
</div>

<div class="row">
  <div class="medium-10 medium-centered columns">
    % for story in stories:
    <div class="container-box">
      <div>
        <i class="fa fa-pencil right"> 24h</i>
        <i class="fa fa-user organization-label"> ${story['author_first_name']} ${story['author_last_name']}</i>
      </div>
      <div class="story-contents">
        <h3><!--<a href="#">-->${story['title']}<!--</a>--></h3>
        <span>${story['contents_rendered'] | n}</span>
      </div>
    </div>
    % endfor
  </div>
</div>

