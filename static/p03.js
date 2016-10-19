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
      like_btn.html(data['like_btn_txt']);
      likes_counter.html(data['likes_counter']);
    },
    error: function(error){
      error_msg.html('error sending like, please try again later or notify the admin');
    }
  });
});