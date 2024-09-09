//////////////////////////////////////////
// СОЗДАНИЕ ПОЛЕЙ ВЫБОРА ДАТЫ И ВРЕМЕНИ //
//////////////////////////////////////////

const datetimepicker = document.querySelectorAll('input[type=datetime-local]');

const datetimepicker_config = {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    'locale': 'ru'
}

flatpickr(datetimepicker, datetimepicker_config);
