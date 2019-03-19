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
    document.getElementById('submit_post_box').setAttribute('style', 'min-height: 400px; max-height: none;');
    document.getElementById('post_field').setAttribute('style', 'min-height: 100px; max-height: none; padding: 16px 20px 46px 12px;');
}));

jQuery(function($){
	$(document).mouseup(function (e){ // событие клика по веб-документу
		let div = $("#submit_post_box"); // тут указываем ID элемента
		if (!div.is(e.target) // если клик был не по нашему блоку
		    && div.has(e.target).length === 0) { // и не по его дочерним элементам
			document.getElementById('placeholder1').setAttribute('style', 'display: ;');
			document.getElementById('submit_post_box').setAttribute('style', 'min-height: 52px; max-height: 52px;');
			document.getElementById('post_field').textContent = '';
            document.getElementById('post_field').setAttribute('style', 'min-height: 52px; max-height: 52px;');
		}
	});
});

$('#send_post').on('click', (function () {
    event.preventDefault();
    let url = document.location.pathname;
    if(url.split('')[1] !== 'i'){
        public_pk = url.split('/public')[1].split('/')[0];
        console.log(public_pk)
    }else {public_pk = 0}
    $.ajax({
        type: 'POST',
        url: '/post/create/',
        data: {content: $('#post_field').text(), url: url, public_pk: public_pk},
        dataType: 'json',
        contentType: 'application/x-www-form-urlencoded',
        cache: false,
        success: function () {
            document.getElementById('placeholder1').setAttribute('style', 'display: ;');
            document.getElementById('post_field').textContent = '';
            document.getElementById('placeholder1').setAttribute('style', 'display: ;');
			document.getElementById('submit_post_box').setAttribute('style', 'min-height: 52px; max-height: 52px;');
			document.getElementById('post_field').setAttribute('style', 'min-height: 52px; max-height: 52px;');
        }
    });
}));
