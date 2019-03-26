function set_border_buttom_all_friends() {
    document.getElementById('all_friends').setAttribute('style', 'border-bottom: 2px solid #5181b8; padding-bottom: 13px;');
    document.getElementById('friendship_request').setAttribute('style', 'border-bottom: none; padding-bottom: 13px;')
}

function set_border_buttom_friendship_request() {
    document.getElementById('friendship_request').setAttribute('style', 'border-bottom: 2px solid #5181b8; padding-bottom: 13px;');
    document.getElementById('all_friends').setAttribute('style', 'border-bottom: none; padding-bottom: 13px;')
}

function update_friendship_request() {
        $.ajax({
            url: '/up/friendship/',
            type: 'get',
            dataType: 'json',
            success: function (json) {
                console.log(json);
                let data = JSON.parse(json.content);
                if(data.unrejected_requests === 0){
                    $('#number_unrejected_requests').addClass('left_void');
                }else{
                    $('#number_unrejected_requests').removeClass('left_void');
                    document.getElementById('number_unrejected_requests').innerHTML = data.unrejected_requests;
                }
            }
        })
}
setTimeout(update_friendship_request, 100);
setInterval(update_friendship_request, 5000);