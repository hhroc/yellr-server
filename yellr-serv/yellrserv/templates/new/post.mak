<%inherit file="base.mak"/>

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
          <a class="button right" onclick="uploadMedia();">Submit</a>
          <a class="button" id="post-add-image">
            <i class="fa fa-camera"></i>
            <input id="media-file" type="file" name="media_file">
          </a>
        </form>
        <button id="submit-image" style="display: none;">Send Image</button>
      </div>
    </div>
  </div>
</div>

<script>
  $ = undefined;
</script>

<script src="static/new/js/jquery.min.js"></script>
<script src="static/new/js/jquery.ui.widget.js"></script>
<script src="static/new/js/jquery.iframe-transport.js"></script>
<script src="static/new/js/jquery.fileupload.js"></script>
<script>

  var assignment_id = ${assignment_id};
  var fileName = '';
  var imageUpload = false;

  $('#media-file').change(function() {
    fileName = $(this).val();
    console.log('File selected: ' + fileName);
    imageUpload = true;
  });

  var url = '/upload_media.json?cuid=${cuid}&lat=${lat}&lng=${lng}&language_code=${language_code}';

  $(function () {
    console.log('inside ...');
    $('#media-file').fileupload({
      singleFileUploads : true,
      autoUpload : false,
      url: url,
      dataType: 'json',
      add: function(e, data) {
        $('#submit-image').off('click').on('click', function() {
          data.submit();
        });
      },
      done: function(e, data) {
        console.log('Image Media Uploaded Successfully.');
        publishPost(data.result.media_id);
      },
      fail: function(e, data) {
        console.log('FAILURE');
      },
      always: function(e, data) {
        console.log('always()');
      }
    });
  });

  function uploadMedia() {
    console.log('uploadMedia()');
    if ( typeof $('#post-contents').val() == 'undefined' || $('#post-contents').val().trim() == '' ) {
      alert('Please tell us a bit about your community before submitting.');
      return;
    }

    if ( imageUpload == true ) {
      imageUpload = false;
      console.log("uploadMedia(): Submitting Image + Text to upload_media.json ...");
      // this will cause the image to be uploaded, and once done(), will call publishPost()
      $('#media-file').fileupload({
        formData: {
          media_type: 'image',
          media_text: '',
          media_caption: $('#post-contents').val()
        }
      });
      $('#submit-image').trigger('click');
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
              publishPost( data.media_id );
            } else {
              alert('Yikes!  Looks like something went wrong.  Please try again later.');
            }
          }
      });
    }
  }

  function publishPost( textMediaId ) {
    console.log('publishPost(): textMediaId = ' + textMediaId);
    var url = 'publish_post.json?cuid=${cuid}&lat=${lat}&lng=${lng}&language_code=${language_code}';
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: {
          'assignment_id': assignment_id,
          'media_objects': '["' + textMediaId + '"]'
        },
        success: function() {
          console.log('Post Published Successfully.');
          alert("Post Successful!\r\n\n\nOnce approved, your post will show up in the local feed.");
          window.location = '/local';
        }
    });

  }

</script>
