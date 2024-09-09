const datetimepicker = document.querySelectorAll('input[type=datetime-local]');

const datetimepicker_config = {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    'locale': 'ru'
}

flatpickr(datetimepicker, datetimepicker_config);

function change_money(target, lesson_duration, pupil_price=null) {
    target.value = lesson_duration == 1 ? pupil_price: pupil_price * lesson_duration
}

let pupil_select = document.getElementById('id_pupil');

let lesson_duration_input = document.getElementById('id_lesson_duration');

let money_recived_input = document.getElementById('id_money_recived');

lesson_duration_input.addEventListener('change', async function(e) {
    change_money(money_recived_input, e.target.value, await get_pupil_price(pupil_select.value));
})

async function get_pupil_price(pupil_id) {
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

pupil_select.addEventListener('change', async function(e) {
    let pupil_price = await get_pupil_price(e.target.value);
    let money_recived_input = document.getElementById('id_money_recived');

    let lesson_duration = lesson_duration_input.value;

    change_money(money_recived_input, lesson_duration, pupil_price)
});


(async function() {
    let lesson_path = window.location.pathname;

    const regexp = /\/(\d+)\/$/;

    let lesson_id = lesson_path.match(regexp)[1]

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
    let request_url = `/lessons/get-lesson-datetime/${lesson_id}`;

    let response = await fetch(request_url);

    if (response.ok) {
        let json_data = await response.json();

        let lesson_datetime = json_data['lesson_datetime']

        return lesson_datetime
    }
}
