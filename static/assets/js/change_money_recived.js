/////////////////////////////////////////////////////////////////////
// ИЗМЕНЕНИЕ ПОЛЯ "Денег заработано" ПРИ ИЗМЕНЕНИИ СВЯЗАННЫХ ПОЛЕЙ //
/////////////////////////////////////////////////////////////////////

import {get_data} from '../js/main.js'


function change_money(target, lesson_duration, pupil_price) {
    // функция для изменения поля "Денег заработано"
    // Если урок длился 1 час, то значение = цена за час урок
    target.value = lesson_duration == 1 ? pupil_price: pupil_price * lesson_duration;
}

let pupil_price;

let pupil_select = document.getElementById('id_pupil');

let lesson_duration_input = document.getElementById('id_lesson_duration');

let money_recived_input = document.getElementById('id_money_recived');

lesson_duration_input.addEventListener('change', async function(e) {
    // при изменении поля "Времени затрачено" вызывается функция change_money
    let request_url = `/pupils/get-pupil-price/${pupil_select.value}/`;

    console.log(pupil_price)

    if (pupil_price == undefined) {
        [pupil_price = 0] = await get_data(request_url);  // получаем данные; если данных нет, ставим 0
    }

    change_money(money_recived_input, e.target.value, pupil_price);
});

pupil_select.addEventListener('change', async function(e) {
    // при изменении поля "Ученик" вызывается функция change_money
    let request_url = `/pupils/get-pupil-price/${e.target.value}/`;

    [pupil_price = 0] = await get_data(request_url);  // получаем данные; если данных нет, ставим 0

    let money_recived_input = document.getElementById('id_money_recived');

    let lesson_duration = lesson_duration_input.value;

    change_money(money_recived_input, lesson_duration, pupil_price);
});


