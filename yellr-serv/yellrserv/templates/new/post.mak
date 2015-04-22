<%inherit file="base.mak"/>

  <style>

    #media-file {
    }

    #post-add-image {
      overflow: hidden;
    }

    #post-add-image input {
      opacity: 0;
      position: absolute;
      right: 0;
      top: 0;
      bottom: 0;
      font-size: 100px;
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
          <a class="button right" onclick="uploadMedia();">Submit</a>
          <a class="button" id="post-add-image">
            <i class="fa fa-camera"></i>
            <input id="media-file" type="file" name="media_file">
          </a>
      </form>
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
  var mediaId = undefined;
  var imageUpload = false;

  $('#media-file').change(function() {
    fileName = $(this).val();
    console.log('File selected: ' + fileName);
  });

  /*
  function selectMedia() {
    // taken from:
    //   http://stackoverflow.com/a/6888810
    $('#media-file').show();
    $('#media-file').focus();
    $('#media-file').trigger('click');
    //$('#media-file').hide();
  }
  */

  var url = '/upload_media.json?cuid=${cuid}&lat=${lat}&lng=${lng}&language_code=${language_code}';

  $(function () {
    console.log('inside ...');
    $('#media-file').fileupload({
      singleFileUploads : true,
      autoUpload : false,
      url: url,
      dataType: 'json',
      formData: {
        media_type: 'image',
        media_text: '', // not used for images
        media_caption: $('#post-contents').val(),
      },
      add: function(e, data) {
        data.submit();
      },
      done: function(e, data) {
        console.log('Image Media Uploaded Successfully.');
        mediaId = data.result.media_id;
        imageUpload = true;
        //publishPost(data.media_id);
      },
      fail: function(e, data) {
        console.log('FAILURE');
        console.log(data);
        console.log(e);
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
      while( mediaId == '' ) {
        // yea, this is bad if you have really slow interwebs.
      }
      publishPost( mediaId );
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
    console.log('publishPost(): mediaId = ' + textMediaId);
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
          alert("Post Successful!\r\nOnce approved, your post will show up in the local feed.");
          window.location = '/local';
        }
    });

  }

</script>
