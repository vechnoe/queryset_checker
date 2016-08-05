// CRSF protect
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    function getCookie(name) {
      var cookieValue = null;
        if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1));
                break;
              }
          }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
  }
});


$(document).ready(function() {
  // remove django messages
  setTimeout(function() {
    $('.alert-success').remove();
  }, 10000);
});

$('#process').click(function() {
  var button = this;
  $.ajax({
    url : '/process/',
    type : 'POST',
    dataType: 'json',
    data : {},
    success: function(response){

      $('#checker-messages').html(
        '<div class="alert alert-success" role="alert">' +
          '<p>' + response.message + '<p>' +
        '</div>'
      );

      setTimeout(function() {
        $('.alert-success').remove();
      }, 10000);
    }
  });
});

var formatJson = function (id){
  var jsonfy = $('#' + id);
  if ( jsonfy.length ) {
    var _json = JSON.parse(jsonfy.text());
    jsonfy.text(JSON.stringify(_json, null, 4))
  }
};

var setUrl = function (id, port) {
  var a = $('#' + id);
  var host = window.location.href.split('/')[2].split(':')[0];
  var url = 'http://' + host + ':' + port;
  a.attr("href", url)
};

$(document).ready(function() {
  formatJson('query_data');
  formatJson('query_result');

  setUrl('celery', '9999');
  setUrl('rabbit-mq', '8888');
});