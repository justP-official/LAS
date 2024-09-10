////////////////////////////////////////////////////////////////
// ИЗМЕНЕНИЕ ПОЛЯ "Денег заработано" ПРИ ИЗМЕНЕНИИ СВЯЗАННЫХ ПОЛЕЙ //
////////////////////////////////////////////////////////////////

function change_money(target, lesson_duration, pupil_price) {
    // функция для изменения поля "Денег заработано"
    // Если урок длился 1 час, то значение = цена за час урок
    target.value = lesson_duration == 1 ? pupil_price: pupil_price * lesson_duration;
}

let pupil_select = document.getElementById('id_pupil');

let lesson_duration_input = document.getElementById('id_lesson_duration');

let money_recived_input = document.getElementById('id_money_recived');

lesson_duration_input.addEventListener('change', async function(e) {
    // при изменении поля "Времени затрачено" вызывается функция change_money
    change_money(money_recived_input, e.target.value, await get_pupil_price(pupil_select.value));
});

pupil_select.addEventListener('change', async function(e) {
    // при изменении поля "Ученик" вызывается функция change_money
    let pupil_price = await get_pupil_price(e.target.value);
    let money_recived_input = document.getElementById('id_money_recived');

    let lesson_duration = lesson_duration_input.value;

    change_money(money_recived_input, lesson_duration, pupil_price);
});

async function get_pupil_price(pupil_id) {
    // функция для получения цены за час урока с определённым учеником
    let request_url = `/pupils/get-pupil-price/${pupil_id}/`;

    let response = await fetch(request_url);

    if (response.ok) {
        let json_data = await response.json();

        let pupil_price = json_data['price_per_hour'];

        return pupil_price        
    } else {
        return 0
    }
}

