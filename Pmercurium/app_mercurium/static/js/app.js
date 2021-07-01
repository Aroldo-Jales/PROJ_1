function modal_filter() {
    let modal_bg = document.querySelector('.modal-bg');
    modal_bg.classList.add('bg-active');
}

function close_modal_filter() {
    let modal_bg = document.querySelector('.modal-bg');
    modal_bg.classList.remove('bg-active');
}

function close_message() {
    let msg = document.querySelector('.messages');
    msg.style.display = 'none';
}

