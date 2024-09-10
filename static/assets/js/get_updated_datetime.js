///////////////////////////////
// ОБНОВЛЕНИЕ ДАТЫ И ВРЕМЕНИ //
///////////////////////////////

// Пояснение:
// Почему-то, при рендере формы, не отображается дата и время,
// приходится создавать отдельный инпут с прописанным значением

(async function() {
    // получение id текущего урока из адреса страницы

    let lesson_path = window.location.pathname;

    const regexp = /\/(\d+)\/$/;

    let lesson_id = lesson_path.match(regexp)[1];

    let datetime_updater = document.querySelector('.datetime-updater');

    let default_date = await get_lesson_datetime(lesson_id);

    let datetime_updater_config = {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        defaultDate: default_date,
        'locale': 'ru'
    }

    flatpickr(datetime_updater, datetime_updater_config)
    }
)();

async function get_lesson_datetime(lesson_id) {
    // функция для получения даты и времени урока по id
    let request_url = `/lessons/get-lesson-datetime/${lesson_id}`;

    let response = await fetch(request_url);

    if (response.ok) {
        let json_data = await response.json();

        let lesson_datetime = json_data['lesson_datetime'];

        return lesson_datetime;
    }
}
