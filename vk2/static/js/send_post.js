let csrftoken = Cookies.get('csrftoken');
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

$('#post_field').on('click', (function () {
    document.getElementById('submit_post').setAttribute('style', 'overflow: visible;');
    document.getElementById('placeholder1').setAttribute('style', 'display: none;');
    document.getElementById('submit_post_box').setAttribute('style', 'min-height: 80px; max-height: none;')
}));

jQuery(function($){
	$(document).mouseup(function (e){ // событие клика по веб-документу
		let div = $("#submit_post_box"); // тут указываем ID элемента
		if (!div.is(e.target) // если клик был не по нашему блоку
		    && div.has(e.target).length === 0) { // и не по его дочерним элементам
			document.getElementById('placeholder1').setAttribute('style', 'display: ;');
			document.getElementById('submit_post_box').setAttribute('style', 'min-height: 52px; max-height: 52px;')

		}
	});
});

$('#send_post').on('click', (function () {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/ps/',
        data: {content: $('#post_field').text()},
        dataType: 'json',
        contentType: 'application/x-www-form-urlencoded',
        cache: false,
        success: function () {
            document.getElementById('placeholder1').setAttribute('style', 'display: ;');
            document.getElementById('post_field').textContent = '';
            document.getElementById('placeholder1').setAttribute('style', 'display: ;');
			document.getElementById('submit_post_box').setAttribute('style', 'min-height: 52px; max-height: 52px;')
        }
    });
}));
