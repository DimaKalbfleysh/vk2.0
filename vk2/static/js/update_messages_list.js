if (document.location.pathname === '/im/') {
    countLi = document.getElementsByClassName('message_li').length;
    function updateList() {
        let pk = document.location.search.split('=')[1];
        $.ajax({
            url: '/up?sel=' + pk,
            type: 'get',
            dataType: 'json',
            success: function (json) {
                let data = JSON.parse(json.content);
                console.log(data);
                let countElem = data.messages.length;
                if (countElem !== countLi) {
                    let lastMessage = data.messages[data.messages.length - 1];
                    let firstName = data.first_name;
                    let urlPhoto = data.url_photo;
                    let pubTime = data.pub_time;
                    let newElem = `<li id="message_element" class="im-mess im_in _im_mess _im_mess_9085">
                                                        <div class="im-mess-stack _im_mess_stack " data-peer="483686337" data-admin="">
                                                            <div class="im-mess-stack--photo">
                                                                <div class="nim-peer nim-peer_small fl_l">
                                                                    <div class="nim-peer--photo-w">
                                                                        <div class="nim-peer--photo">
                                                                            <a target="_blank" class="im_grid" href="/id${ lastMessage.author_id } ">
                                                                                <img alt="${ firstName }" src="${ urlPhoto }">
                                                                            </a>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="im-mess-stack--content">
                                                                <div class="im-mess-stack--info">
                                                                    <div class="im-mess-stack--pname">
                                                                        <a href="/id${ lastMessage.author_id }" class="im-mess-stack--lnk" title="" target="_blank">${ firstName }</a>
                                                                        <span class="im-mess-stack--tools">
                                                                            <a href="/im?sel=483686337&amp;msgid=9085" class="_im_mess_link">
                                                                                ${ pubTime }
                                                                            </a>
                                                                        </span>
                                                                    </div>
                                                                </div>
                                                                <ul class="ui_clean_list im-mess-stack--mess _im_stack_messages">
                                                                    <li class="im-mess im_in _im_mess _im_mess_9085"
                                                                        aria-hidden="false" data-ts="1549631228" data-msgid="9085" data-peer="483686337">
                                                                        <div class="im-mess--actions">
                                                                            <span role="link" aria-label="Переслать" class="im-mess--forward _im_mess_forward"></span>
                                                                            <span role="link" aria-label="Ответить" class="im-mess--reply _im_mess_reply"></span>
                                                                            <span role="link" aria-label="Редактировать" class="im-mess--edit _im_mess_edit"></span>
                                                                            <span role="link" aria-label="Важное сообщение" class="im-mess--fav _im_mess_fav"></span>
                                                                        </div>
                                                                        <div class="im-mess--check fl_l"></div>
                                                                        <div class="im-mess--text wall_module _im_log_body">
                                                                            ${ lastMessage.message }
                                                                        </div>
                                                                        <span tabindex="0" role="link" aria-label="Выделить сообщение" class="blind_label im-mess--blind-select _im_mess_blind_label_select"></span>
                                                                        <span class="blind_label im-mess--blind-read _im_mess_blind_unread_marker"></span>
                                                                        <span class="im-mess--marker _im_mess_marker"></span>
                                                                    </li>
                                                                </ul>
                                                            </div>
                                                        </div>
                                                    </li>`;
                    document.getElementById('messages_list').insertAdjacentHTML('beforeEnd', newElem);
                    countLi = countElem;
                    $(window).scrollTop($(document).height());
                }
            }
        })
    }

    setInterval(updateList, 1000);
} else {
    function update_count_not_readed() {
        $.ajax({
            url: '/up?cou=1',
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
}

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