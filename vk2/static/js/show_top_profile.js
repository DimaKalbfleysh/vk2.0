function show_top_profile_menu(){
    event.preventDefault();
    document.getElementById('top_profile_menu').setAttribute('class', 'shown');
    document.getElementById('top_profile_link').setAttribute('class', 'top_nav_link top_profile_link active')
}

jQuery(function($){
	$(document).mouseup(function (e){ // событие клика по веб-документу
		let div = $("#submit_post_box"); // тут указываем ID элемента
		if (!div.is(e.target) // если клик был не по нашему блоку
		    && div.has(e.target).length === 0) { // и не по его дочерним элементам
            document.getElementById('top_profile_menu').setAttribute('class', '');
            document.getElementById('top_profile_link').setAttribute('class', 'top_nav_link top_profile_link')
		}
	});
});

