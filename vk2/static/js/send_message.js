let csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(window).scrollTop($(document).height());
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


jQuery(function($){
	$(document).mouseup(function (e){ // событие клика по веб-документу
		let div = $("#submit_post_box"); // тут указываем ID элемента
		if (!div.is(e.target) // если клик был не по нашему блоку
		    && div.has(e.target).length === 0) { // и не по его дочерним элементам
            document.getElementById('placeholder').setAttribute('style', 'display: ;');
		}
	});
});


$('#im_editable0').on('click', (function () {
    document.getElementById('placeholder').setAttribute('style', 'display: none;');
}));

$('#im-send-btn_send').on('click', (function () {
    event.preventDefault();
    let pk = document.location.search.split('=')[1];
    if(($('#im_editable0').text() !== '')){
        $.ajax({
        type: 'POST',
        url: '/im/?sel='+pk,
        data: {message: $('#im_editable0').text()},
        dataType: 'json',
        contentType: 'application/x-www-form-urlencoded',
        cache: false,
        success: function () {
            $(window).scrollTop($(document).height());
            document.getElementById('im_editable0').textContent = '';
            document.getElementById('placeholder').setAttribute('style', 'display: ;');
        }
    });
    }
}));
