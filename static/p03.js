$('.like').on('click', function(e){
  e.preventDefault();
  var instance = $(this);
  var key = $(this).data('key');
  var error_msg = $(this).parent().find('span.error');
//  var youlike = instance.parent().find('span.you-like');
  $.ajax({
    type: "post",
    url: "/blog/like",
    dataType: 'json',
    data: {"post_id": key},
    success: function(data){
      // if there is a problem, display error (with fade out)
/*
      if (data['error']) {
        errormsg.html(data['error']);
        errormsg.fadeToggle(1500, 'swing', function(){
          errormsg.html('');
          errormsg.toggle(0);
        });
      }

      // if there is no problem, update like counter and let user know
      // that they like it
      else {
*/
      error_msg.html('success!'+data['msg']);
//      }
    },
    error: function(error){
      error_msg.html('error'+error['msg']);
//      console.log(err);
//      console.log('something went wrong');
    }
  });
});
/*
$('#btnCalc').click(function(){
  addlike()
});

function addLike(username){
  $.post('/like',
        username,
        function(data){
            $('.result').html(data);
        });
}
/*
    $('#btnCalc').click(function () {
        $.ajax({
          type: 'POST',
            url: "/update",
            data:'tournament='+tournament,
            cache: false,
            success: function(stuff){
                $("success").html(stuff);
            }
        });
        */