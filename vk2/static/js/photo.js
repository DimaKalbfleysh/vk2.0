function photo_for_groups(id) {
    let url1 = document.getElementById(id).getAttribute('href');
    history.pushState(null, null, url1);
    let url = document.getElementById(id).getAttribute('style').split('background-image:')[1].split('url(')[1].split(')')[0];
    event.preventDefault();
    document.getElementById('layer_bg').setAttribute('style', 'display: block;');
    document.getElementById('layer_wrap').setAttribute('style', 'width: 1165px; height: 760px;display: block;');
    document.getElementById('img').setAttribute('src', url);
    document.getElementsByClassName('like_photo')[0].setAttribute('id', id)
}



function photo_for_main_photo(id) {
    let url = document.getElementById(id).getAttribute('src');
    console.log(url);
    event.preventDefault();
    document.getElementById('layer_bg').setAttribute('style', 'display: block;');
    document.getElementById('layer_wrap').setAttribute('style', 'width: 1165px; height: 760px;display: block;');
    document.getElementById('img').setAttribute('src', url);
    document.getElementsByClassName('like_photo')[0].setAttribute('id', id)
}

$('#pv_close_btn').on('click', (function () {
    document.getElementById('layer_bg').setAttribute('style', 'display: ;');
    document.getElementById('layer_wrap').setAttribute('style', 'width: 1165px; height: 760px; display: ;');
}));


function delete_photo() {
    let pk = document.location.search.split('-')[1];
    console.log(pk);
    event.preventDefault();
    $.ajax({
        type: 'GET',
        url: '/photo/delete/?id='+pk,
        data: {'pk': pk},
        dataType: 'json',
        contentType: 'application/x-www-form-urlencoded',
        cache: false,
        success: function () {
            document.getElementById("pv_tag_info").setAttribute('style', 'width: 784px; display: block;')
        }
    });
}


function make_main_photo(){
    let pk = document.location.search.split('-')[1];
    event.preventDefault();
    $.ajax({
        type: 'GET',
        url: '/photo/make-main/?id='+pk,
        data: {'pk': pk},
        dataType: 'json',
        contentType: 'application/x-www-form-urlencoded',
        cache: false,
        success: function () {

        }
    });
}


function like_photo(pk){
    event.preventDefault();
    $.ajax({
        type: 'GET',
        url: '/photo/put-like/?id='+pk,
        data: {'pk': pk},
        dataType: 'json',
        contentType: 'application/x-www-form-urlencoded',
        cache: false,
        success: function (json) {
            let data = JSON.parse(json.content);
            if (data.likes_put){
                document.getElementById(pk).setAttribute('class', 'like_btn like _like  like_photo active');
                document.getElementById('count_like_post'+pk).textContent = data.count_likes
            }else {
                document.getElementById(pk).setAttribute('class', 'like_btn like _like  like_photo');
                document.getElementById('count_like_post'+pk).textContent = data.count_likes
            }
        }
    });
}