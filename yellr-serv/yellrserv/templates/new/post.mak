<%inherit file="base.mak"/>

  <style>

    #media-file {
      display: none;
      /*position: absolute;
      color: white;
      background-color: 
      top: 0;
      right: 0;
      margin: 0;
      opacity: 0;
      -ms-filter: 'alpha(opacity=0)';
      font-size: 200px;
      direction: ltr;
      cursor: pointer;
      padding-top: 1rem;
      padding-right: 2rem;
      padding-bottom: 1.0625rem;
      padding-left: 2rem;*/
    }

  </style>

<div class="row">
  <div class="large-12 columns">
    <div class="tab-links">
      <div class="tab-link-container"><a class="tab-link top-link-divider" href="/local">Local</a></div>
      <div class="tab-link-container"><a class="tab-link top-link-divider" href="/assignments">Assignments</a></div>
      <div class="tab-link-container"><a class="tab-link top-link-divider" href="/stories">Stories</a></div>
      <div class="tab-link-container selected-tab"><a class="tab-link" href="/post">Post</a></div>
    </div>
    <hr/>
  </div>
</div>

<div class="row">
  <div class="medium-8 medium-centered columns">
    % if is_response == False:
    <h3>Free Post</h3>
    % else:
    <h3>${question_text}</h3>
    <p>${question_description}</p>
    % endif
      <div class="new-post-contents">
        <form>
          <span class="anonymous-label">All posts are anonymous</span>
          <textarea id="post-contents" rows="6" placeholder="Tell us about your community"></textarea>
          <div>
            <a class="button right" onclick="uploadMedia();">Submit</a>
            <div class="post-add-media">
              <button id="post-add-image" onclick="selectMedia();"><i class="fa fa-camera"></i></button>
              <input id="media-file" type="file" name="meida_file"></input>
              <!--
              <button class="disabled" ><i class="fa fa-video-camera"></i></a>
              <button class="disabled" ><i class="fa fa-microphone"></i></a>
              -->
            </div>
          </div>
      </form>
      </div>
    </div>
  </div>
</div>

<script src="static/new/js/jquery.ui.widget.js"></script>
<script src="static/new/js/jquery.fileupload.js"></script>
<script>

  var assignment_id = ${assignment_id};
  var fileName = '';

  $('#media-file').change(function() {
    fileName = $(this).val();
    console.log('File selected: ' + fileName);
  });

  function selectMedia() {
    // taken from:
    //   http://stackoverflow.com/a/6888810
    $('#media-file').show();
    $('#media-file').focus();
    $('#media-file').click();
    $('#media-file').hide();
  }

  function uploadMedia() {
    console.log('uploadMedia()');
    var url = 'upload_media.json?cuid=${cuid}&lat=${lat}&lng=${lng}&language_code=${language_code}';
    if ( typeof $('#post-contents').val() == 'undefined' || $('#post-contents').val().trim() == '' ) {
      alert('Please tell us a bit about your community before submitting.');
      return;
    }

    if ( fileName != '' ) {
      console.log("uploadMedia(): Submitting Image + Text to upload_media.json ...");
      $('#media-file').fileupload({
        url: url,
        dataType: 'json',
        formData: {
          media_type: 'image',
          media_text: '', // not used for images
          media_caption: $('#post-contents').val(), 
        },
        done: function(e, data) {
          console.log('Image Media Uploaded Successfully.');
          publishPost(data.media_id);
        }
      });
    } else {
        console.log("uploadMedia(): Submitting Text to upload_media.json ...");
        console.log('submitting: ' + $('#post-contents').val());
        $.ajax({
          type: 'POST',
          url: url,
          dataType: 'json',
          data: {
            'media_type': 'text',
            'media_text': $('#post-contents').val(),
            'media_caption': '', // not used for text
          },
          success: function(data) {
            console.log('Text Media Uploaded Successfully.');
            if ( data.success == true ) {
              console.log('data:');
              console.log(data.media_id);
              publishPost(data.media_id);
            } else {
              alert('Yikes!  Looks like something went wrong.  Please try again later.');
            }
          }
      });
    }
  }

  function publishPost( mediaId ) {
    console.log('publishPost(): mediaId = ' + mediaId);
    var url = 'publish_post.json?cuid=${cuid}&lat=${lat}&lng=${lng}&language_code=${language_code}';
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: {
          'assignment_id': assignment_id,
          'media_objects': '["' + mediaId + '"]'
        },
        success: function() {
          console.log('Post Published Successfully.');
          alert("Post Successful!\r\nOnce approved, your post will show up in the local feed.");
          window.location = '/local';
        }
    });

  }

</script>
