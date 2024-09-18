/////////////////////
// ОБНОВЛЕНИЕ ДАТЫ //
/////////////////////

// Пояснение:
// Почему-то, при рендере формы, не отображается дата,
// приходится создавать отдельный инпут с прописанным значением

import {get_data} from '../js/main.js'

(async function() {
    // получение id текущего отчёта из адреса страницы

    let report_path = window.location.pathname;

    const regexp = /\/(\d+)\/$/;

    let report_id = report_path.match(regexp)[1];

    let start_period_updater = document.querySelector('.start-period-updater');

    let end_period_updater = document.querySelector('.end-period-updater');

    let request_url = `/reports/get-report-period/${report_id}`;

    let [
        start_period_default_date = Date.now(), 
        end_period_default_date = Date.now()
    ] = await get_data(request_url);  // получаем данные; если данных нет, ставим текущую дату

    let start_period_updater_config = {
        dateFormat: "Y-m-d",
        defaultDate: start_period_default_date,
        'locale': 'ru'
    }

    let end_period_updater_config = {
        dateFormat: "Y-m-d",
        defaultDate: end_period_default_date,
        'locale': 'ru'
    }

    flatpickr(start_period_updater, start_period_updater_config);

    flatpickr(end_period_updater, end_period_updater_config);
    }
)();
