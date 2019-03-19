function update_count_not_readed() {
        $.ajax({
            url: '/up/dialog/?cou=1',
            type: 'get',
            dataType: 'json',
            success: function (json) {
                let data = JSON.parse(json.content);
                console.log(data);
                if(data.number_not_read_messages === 0) {
                    $('#number_not_read_messages_span').addClass('left_void');
                }else {
                    $('#number_not_read_messages_span').removeClass('left_void');
                    document.getElementById('number_not_read_messages').innerHTML = data.number_not_read_messages;
                    if (document.location.pathname === '/di/'){
                        console.log(data.dialogs_values);
                        for(let i=0; i<data.dialogs_values.length; i++){
                            if(data.dialogs_values[i].number_not_read_messages !==0) {
                                document.getElementById('dialog' + data.dialogs_values[i].id).setAttribute('class', 'nim-dialog _im_dialog _im_dialog_512227035 nim-dialog_classic nim-dialog_unread ');
                                document.getElementById('number' + data.dialogs_values[i].id).innerHTML = data.dialogs_values[i].number_not_read_messages;
                            }
                        }
                    }
                }
            }
        })
    }
setTimeout(update_count_not_readed, 100);
setInterval(update_count_not_readed, 5000);

window.onscroll = function () {
    let value = 'transform: translateX(-' + Math.round(window.pageXOffset) + 'px)';
    if(document.getElementById('im-page--chat-header _im_dialog_actions')){
        document.getElementById('im-page--chat-header _im_dialog_actions').setAttribute('style', value);
    }
    if(document.getElementById('im-page--chat-input _im_chat_input_w')){
        document.getElementById('im-page--chat-input _im_chat_input_w').setAttribute('style', value);
    }
    if(document.getElementById('im-page--header ui_search _im_dialogs_search')){
        document.getElementById('im-page--header ui_search _im_dialogs_search').setAttribute('style', value);
    }
    document.getElementById('side_bar').setAttribute('style', value);
};