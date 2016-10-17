function error_trying(subject){
  return 'Woops... something went wrong trying to '+subject+' this post, please try again later or notify the admin'
}

$('.edit').on('click', function(e){
  e.preventDefault();
  var edit_btn = $(this)
  var edit_prompt = $(this).parent().find('span.edit-prompt')
  var key = $(this).data('key');
  var error_msg = $(this).parent().find('span.error');
  var subject_element = $(this).parent().parent().find('.post-subject');
  var datetime_element = $(this).parent().parent().find('.post-datetime');
  var content_element = $(this).parent().parent().find('.post-content');
  var content_element_height = content_element.height();
  var subject = subject_element.html();
  var content = content_element.html().replace(/<br>/g, "\n");

  edit_btn.addClass('hidden');
  edit_prompt.removeClass('hidden');

  subject_element.html('<input type="text"/></input');
  subject_element.children().val(subject);
  content_element.html('<textarea>'+content+'</textarea>');
  content_element.children().height(content_element_height);

  $('.edit-yes').on('click', function(e){
    e.preventDefault();
    var key = $(this).data('key');
    var subject_new = subject_element.children().val();
    var content_new = content_element.children().val().replace(/\n/g, "<br>");

    $.ajax({
      type: "post",
      url: "/blog/edit",
      dataType: 'json',
      data: {"post_id": key,"post_subject":subject_new,"post_content":content_new},
      success: function(data){
        error_msg.html(data['msg']);
        subject_element.html(subject_new);
        content_element.html(content_new);
        datetime_element.html(data['datetime']);

        edit_prompt.addClass('hidden');
        edit_btn.removeClass('hidden');
      },
      error: function(error){
        error_msg.html(error_trying('edit'));
      }
    });
  });

  $('.edit-no').on('click', function(e){
    e.preventDefault();
    subject_element.html(subject);
    content_element.html(content.replace(/\n/g, "<br>"));
    edit_prompt.addClass('hidden');
    edit_btn.removeClass('hidden');
  });

});

$('.delete').on('click', function(e){
  e.preventDefault();
  $(this).parent().find('span.delete-prompt').removeClass('hidden');

  var post = $(this).parent().parent()
  var error_msg = $(this).parent().find('span.error');

  $('.delete-yes').on('click', function(e){
    e.preventDefault();
    var key = $(this).data('key');

    $.ajax({
      type: "post",
      url: "/blog/delete",
      dataType: 'json',
      data: {"post_id": key},
      success: function(data){
        post.slideUp(2000);
        error_msg.html(data['msg']);
      },
      error: function(error){
        error_msg.html(error_trying('delete'));
      }
    });
  });

  $('.delete-no').on('click', function(e){
    e.preventDefault();
    $(this).parent().parent().find('span.delete-prompt').addClass('hidden');
  });
});

$('.like').on('click', function(e){
  e.preventDefault();
  var key = $(this).data('key');
  var error_msg = $(this).parent().find('span.error');
  var likes_counter = $(this).parent().find('span.likes_counter');
  var like_btn = $(this)

  $.ajax({
    type: "post",
    url: "/blog/like",
    dataType: 'json',
    data: {"post_id": key},
    success: function(data){
      error_msg.html(data['msg']);
      like_btn.html(data['like_btn_txt']);
      likes_counter.html(data['likes_counter']);
    },
    error: function(error){
      error_msg.html(error_trying('like'));
    }
  });
});