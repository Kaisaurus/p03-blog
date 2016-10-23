function error_trying(subject){
  return 'Woops... something went wrong trying to '+subject+' this post, please try again later or notify the admin'
}
//on document ready
$(function(){
  checkTextarea();
  checkCommentBtns();
})

// scans for all textareas and adds a auto resize on input
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
    // assigning elements and content to comprehensable variables
    var edit_btn = $(this)
    var edit_prompt = $(this).parent().find('span.edit-prompt')
    var error_msg = $(this).parent().find('span.error');
    var datetime_element = $(this).parent().parent().find('.comment-datetime');
    var content_element = $(this).parent().parent().parent().find('.comment-content');
    var content_element_height = content_element.height();
    var content = content_element.html().replace(/<br>/g, "\n");

    edit_btn.addClass('hidden');
    edit_prompt.removeClass('hidden');

    // change the comment element into a textarea so it can be edited
    content_element.html('<textarea>'+content+'</textarea>');
    content_element.children().height(content_element_height);
    checkTextarea();

    $('.edit-yes').on('click', function(e){
      e.preventDefault();
      var key = $(this).data('key');
      var content_new = content_element.children().val().replace(/\n/g, "<br>");
      // Ajax call to send the edited comment to the backend
      $.ajax({
        type: "post",
        url: "/blog/edit_comment",
        dataType: 'json',
        data: {"comment_id": key,"content_new":content_new},
        success: function(data){
          // show the edited comment in formal html format
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
      // restore elements to the way it was
      content_element.html(content.replace(/\n/g, "<br>"));
      edit_btn.removeClass('hidden');
      edit_prompt.addClass('hidden');
    });
  });

  $('.delete-comment').on('click', function(e){
    e.preventDefault();

    var comment_element = $(this).parent().parent().parent()
    var error_msg = $(this).parent().find('span.error');
    var key = $(this).data('key');

    // Ajax call to delete the comment
    $.ajax({
      type: "post",
      url: "/blog/delete_comment",
      dataType: 'json',
      data: {"comment_id": key},
      success: function(data){
        if(data['msg']=='success'){
          // deletes comment html element with a sliding animation
          comment_element.slideUp(1000);
        } else{
          // returns error msg in case something funny is happening
          error_msg.html(data['msg']);
        }
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
    // assigning elements and content to comprehensable variables
    var comment_form = comment_btn.parent().find('.comment-add');
    var btn_yes = comment_btn.parent().find('.comment-yes')
    var btn_no = comment_btn.parent().find('.comment-no')
    var error_msg = $(this).parent().find('span.error');
    var comments = $(this).parent().parent().find('.comments');

    comment_btn.addClass('unclickable');
    comment_form.removeClass('hidden');

    btn_yes.one('click', function(e){
      e.preventDefault();
      var key = $(this).data('key');
      var comment = comment_form.find('.comment-text');

      $.ajax({
        // Ajax call to send comment to the back-end
        type: "post",
        url: "/blog/new_comment",
        dataType: 'json',
        data: {"post_id": key,"comment":comment.val()},
        success: function(data){
          // empties the comment textarea so a new comment could be added
          comment.val('');
          // adds the new comment to html
          comments.prepend(data['comment']);
          // restores comment btn
          comment_btn.removeClass('unclickable');
          // hides the comment form
          comment_form.addClass('hidden');
          // adds edit / delete comment btns
          checkCommentBtns();
          // empties the error msgs if it displays any errors
          error_msg.html('');
        },
        error: function(error){
          error_msg.html(error_trying('comment'));
        }
      });
    });

    btn_no.one('click', function(e){
      // restore to elements to the way it was
      e.preventDefault();
      comment_btn.removeClass('unclickable');
      comment_form.addClass('hidden');
    });
  }
});

// adds functionality to the edit post btn
$('.edit').on('click', function(e){
  e.preventDefault();
  // assigning elements and content to comprehensable variables
  var edit_btn = $(this)
  var edit_prompt = $(this).parent().find('span.edit-prompt')
  var error_msg = $(this).parent().find('span.error');
  var subject_element = $(this).parent().parent().parent().find('.post-subject');
  var datetime_element = $(this).parent().parent().find('.post-datetime');
  var content_element = $(this).parent().parent().find('.post-content');
  var content_element_height = content_element.height();
  var subject = subject_element.html();
  var content = $.trim(content_element.html().replace(/<br>/g, "\n"));

  // hides edit btn
  edit_btn.addClass('hidden');
  // shows prompt btn
  edit_prompt.removeClass('hidden');

  // transforms the post into a form for editing
  subject_element.html('<input type="text"/></input>');
  subject_element.children().val(subject);
  content_element.html('<textarea>'+content+'</textarea>');
  content_element.children().height(content_element_height);
  checkTextarea();

  // adds submit functionality to the edit post button that has appeared
  $('.edit-yes').one('click', function(e){
    e.preventDefault();
    var key = $(this).data('key');
    var subject_new = subject_element.children().val();
    var content_new = content_element.children().val().replace(/\n/g, "<br>");
    if(subject_new != '' && content_new !=''){
      // Ajax call to send the new subject and content to the back-end
      $.ajax({
        type: "post",
        url: "/blog/edit",
        dataType: 'json',
        data: {"post_id": key,"post_subject":subject_new,"post_content":content_new},
        success: function(data){
          // shows the edited post in not editable html format
          subject_element.html(subject_new);
          content_element.html(content_new);
          datetime_element.html(data['datetime']);

          // restore edit btns
          edit_prompt.addClass('hidden');
          edit_btn.removeClass('hidden');
        },
        error: function(error){
          error_msg.html(error_trying('edit'));
        }
      });
    } else{
      error_msg.html('The subject and content cannot be empty.');
    }
  });
  // adds cancel functionality to the edit post button that has appeared
  $('.edit-no').one('click', function(e){
    e.preventDefault();
    // restore elements to the way it was
    subject_element.html(subject);
    content_element.html(content.replace(/\n/g, "<br>"));
    edit_prompt.addClass('hidden');
    edit_btn.removeClass('hidden');
  });
});

$('.delete').on('click', function(e){
  e.preventDefault();
  // assigning elements and content to comprehensable variables
  var post = $(this).parent().parent().parent()
  var error_msg = $(this).parent().find('span.error');
  var delete_prompt = $(this).parent().find('.delete-prompt')

  // show the prompt button
  delete_prompt.removeClass('hidden');

  //adds delete functionality to prompt that has appeared
  $('.delete-yes').one('click', function(e){
    e.preventDefault();
    var key = $(this).data('key');
    // Ajax call to confirm deletion
    $.ajax({
      type: "post",
      url: "/blog/delete",
      dataType: 'json',
      data: {"post_id": key},
      success: function(data){
        if(data['msg']=='success'){
          // deletes post from html with sliding animation
          post.slideUp(1000);
        } else{
          // returns error msg in case something funny is happening
          error_msg.html(data['msg']);
        }
      },
      error: function(error){
        error_msg.html(error_trying('delete')+error);
      }
    });
  });
  // adds cancel functionality to the button that has appeared
  $('.delete-no').one('click', function(e){
    e.preventDefault();
    // restore elements to the way it was
    delete_prompt.addClass('hidden');
  });
});

// adds functionality to the like button
$('.like').on('click', function(e){
  e.preventDefault();
  // assigning elements and content to comprehensable variables
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
      if(data['msg']){
        // returns error msg in case something funny is happening
        error_msg.html(data['msg']);
      } else{
        // returns like or unlike
        like_btn.html(data['like_btn_txt']);
        // updates like counter
        likes_counter.html(data['likes_counter']);
      }
    },
    error: function(error){
      error_msg.html(error_trying('like'));
    }
  });
});