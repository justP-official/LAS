///////////////////////////////
// ОБНОВЛЕНИЕ ДАТЫ И ВРЕМЕНИ //
///////////////////////////////

// Пояснение:
// Почему-то, при рендере формы, не отображается дата и время,
// приходится создавать отдельный инпут с прописанным значением

import {get_data} from '../js/main.js'

(async function() {
    // получение id текущего урока из адреса страницы

    let lesson_path = window.location.pathname;

    const regexp = /\/(\d+)\/$/;

    let lesson_id = lesson_path.match(regexp)[1];

    let datetime_updater = document.querySelector('.datetime-updater');

    let request_url = `/lessons/get-lesson-datetime/${lesson_id}`;

    let [default_datetime = Date.now()] = await get_data(request_url);  // получаем данные; если данных нет, ставим текущую дату

    let datetime_updater_config = {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        defaultDate: default_datetime,
        'locale': 'ru'
    }

    flatpickr(datetime_updater, datetime_updater_config)
    }
)();
