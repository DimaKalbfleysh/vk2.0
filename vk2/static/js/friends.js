var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$('#button').on('click', (function () {
    event.preventDefault();
    var pk = document.location.search.split('=')[1];
    $.ajax({
        type: 'POST',
        url: '/im/?sel='+pk,
        data: {massage: $('#im_editable0').val(), user_pk: pk},
        dataType: 'json',
        contentType: 'application/x-www-form-urlencoded',
        cache: false,
        success: function (json) {

        }
    });
}));
