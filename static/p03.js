function error_trying(subject){
  return 'Woops... something went wrong trying to '+subject+' this post, please try again later or notify the admin'
}
//on document ready
$(function(){
  checkTextarea();
  checkCommentBtns();
})

// auto resizes text area on input
function checkTextarea(){
  $('textarea').each(function () {
    this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
  }).on('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
  });
}

// adds functionality for comment buttons (edit + delete)
function checkCommentBtns(){
  $('.edit-comment').on('click', function(e){
    e.preventDefault();
    var edit_btn = $(this)
    var edit_prompt = $(this).parent().find('span.edit-prompt')
    var error_msg = $(this).parent().find('span.error');
    var datetime_element = $(this).parent().parent().find('.comment-datetime');
    var content_element = $(this).parent().parent().parent().find('.comment-content');
    var content_element_height = content_element.height();
    var content = content_element.html().replace(/<br>/g, "\n");

    edit_btn.addClass('hidden');
    edit_prompt.removeClass('hidden');

    content_element.html('<textarea>'+content+'</textarea>');
    content_element.children().height(content_element_height);
    checkTextarea();

    $('.edit-yes').on('click', function(e){
      e.preventDefault();
      var key = $(this).data('key');
      var content_new = content_element.children().val().replace(/\n/g, "<br>");

      $.ajax({
        type: "post",
        url: "/blog/edit_comment",
        dataType: 'json',
        data: {"comment_id": key,"content_new":content_new},
        success: function(data){
          error_msg.html(data['msg']);
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
      content_element.html(content.replace(/\n/g, "<br>"));
      edit_btn.removeClass('hidden');
      edit_prompt.addClass('hidden');

    });
  });

  $('.delete-comment').on('click', function(e){
    e.preventDefault();

    $(this).parent().find('.delete-prompt').removeClass('hidden');

    var comment_element = $(this).parent().parent().parent()
    var error_msg = $(this).parent().find('span.error');
    var key = $(this).data('key');

    $.ajax({
      type: "post",
      url: "/blog/delete_comment",
      dataType: 'json',
      data: {"comment_id": key},
      success: function(data){
        comment_element.slideUp(1000);
        error_msg.html(data['msg']);
      },
      error: function(error){
        error_msg.html(error_trying('delete'));
      }
    });
  });
}

// adds comment functionality to the "add a comment "
$('.comment-btn').on('click', function(e){
  e.preventDefault();
  var comment_btn = $(this);
  if(comment_btn.hasClass('unclickable')){
    return
  }
  else{
    var comment_form = comment_btn.parent().find('.comment-add');
    var btn_yes = comment_btn.parent().find('.comment-yes')
    var btn_no = comment_btn.parent().find('.comment-no')
    var error_msg = $(this).parent().find('span.error');
    var comments = $(this).parent().parent().find('.comments');

    comment_btn.addClass('unclickable');
    comment_form.removeClass('hidden');

    btn_yes.on('click', function(e){
      e.preventDefault();
      var key = $(this).data('key');
      var comment = comment_form.find('.comment-text');

      $.ajax({
        type: "post",
        url: "/blog/new_comment",
        dataType: 'json',
        data: {"post_id": key,"comment":comment.val()},
        success: function(data){
          comments.append(data['comment']);
          comment.val('');
          comment_btn.removeClass('unclickable');
          comment_form.addClass('hidden');
        },
        error: function(error){
          error_msg.html(error_trying('comment'));
        }
      });
    });

    btn_no.on('click', function(e){
      e.preventDefault();
      comment_btn.removeClass('unclickable');
      comment_form.addClass('hidden');
    });
  }
});

// adds functionality to the edit post btn
$('.edit').on('click', function(e){
  e.preventDefault();
  var edit_btn = $(this)
  var edit_prompt = $(this).parent().find('span.edit-prompt')
  var error_msg = $(this).parent().find('span.error');
  var subject_element = $(this).parent().parent().find('.post-subject');
  var datetime_element = $(this).parent().parent().find('.post-datetime');
  var content_element = $(this).parent().parent().find('.post-content');
  var content_element_height = content_element.height();
  var subject = subject_element.html();
  var content = content_element.html().replace(/<br>/g, "\n");

  edit_btn.addClass('hidden');
  edit_prompt.removeClass('hidden');

  // transforms the post into a form for editing
  subject_element.html('<input type="text"/></input>');
  subject_element.children().val(subject);
  content_element.html('<textarea>'+content+'</textarea>');
  content_element.children().height(content_element_height);
  checkTextarea();

  $('.edit-yes').on('click', function(e){
    e.preventDefault();
    var key = $(this).data('key');
    var subject_new = subject_element.children().val();
    var content_new = content_element.children().val().replace(/\n/g, "<br>");
    // adds submit functionality to the edit post button that has appeared
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
  // adds cancel functionality to the edit post button that has appeared
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
  $(this).parent().find('.delete-prompt').removeClass('hidden');

  var post = $(this).parent().parent()
  var error_msg = $(this).parent().find('span.error');

  //adds delete functionality to prompt that has appeared
  $('.delete-yes').on('click', function(e){
    e.preventDefault();
    var key = $(this).data('key');
    // Ajax call to confirm deletion
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
  // adds cancel functionality to the button that has appeared
  $('.delete-no').on('click', function(e){
    e.preventDefault();
    $(this).parent().parent().find('.delete-prompt').addClass('hidden');
  });
});

// adds functionality to the like button
$('.like').on('click', function(e){
  e.preventDefault();
  var key = $(this).data('key');
  var error_msg = $(this).parent().find('span.error');
  var likes_counter = $(this).parent().find('span.likes_counter');
  var like_btn = $(this)
  // Ajax call to send like to back-end
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