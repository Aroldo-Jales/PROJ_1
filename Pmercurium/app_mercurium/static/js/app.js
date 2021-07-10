function modal_wallet() {
    let modal_wallet_bg = document.querySelector('.modal-wallet-bg');
    modal_wallet_bg.classList.add('bg-active');
}

function close_modal_wallet() {
    let modal_bg = document.querySelector('.modal-wallet-bg');
    modal_bg.classList.remove('bg-active');
}

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

let status_check = document.getElementById('id_status_payment');
document.getElementById('id_date_payment').style.display = 'none';
document.getElementById('id_fees').style.display = 'none';

status_check.onclick = () => {
    if (status_check.checked == true) {
        document.getElementById('id_date_payment').style.display = 'none';
        document.getElementById('id_fees').style.display = 'none';
    } else {
        document.getElementById('id_date_payment').style.display = 'block';
        document.getElementById('id_fees').style.display = 'block';
    }
};