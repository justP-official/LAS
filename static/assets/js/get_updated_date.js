/////////////////////
// ОБНОВЛЕНИЕ ДАТЫ //
/////////////////////

// Пояснение:
// Почему-то, при рендере формы, не отображается дата,
// приходится создавать отдельный инпут с прописанным значением

(async function() {
    // получение id текущего отчёта из адреса страницы

    let report_path = window.location.pathname;

    const regexp = /\/(\d+)\/$/;

    let report_id = report_path.match(regexp)[1];

    let start_period_updater = document.querySelector('.start-period-updater');

    let start_period_default_date = await get_report_period(report_id, 'start_period');

    let start_period_updater_config = {
        dateFormat: "Y-m-d",
        defaultDate: start_period_default_date,
        'locale': 'ru'
    }

    flatpickr(start_period_updater, start_period_updater_config);

    let end_period_updater = document.querySelector('.end-period-updater');

    let end_period_default_date = await get_report_period(report_id, 'end_period');

    let end_period_updater_config = {
        dateFormat: "Y-m-d",
        defaultDate: end_period_default_date,
        'locale': 'ru'
    }

    flatpickr(end_period_updater, end_period_updater_config);
    }
)();

async function get_report_period(report_id, key) {
    // функция для получения даты отчёта по id
    let request_url = `/reports/get-report-period/${report_id}`;

    let response = await fetch(request_url);

    if (response.ok) {
        let json_data = await response.json();

        return json_data[key];
    }
}