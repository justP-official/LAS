////////////////////////////////
// СОЗДАНИЕ ПОЛЕЙ ВЫБОРА ДАТЫ //
////////////////////////////////

const datepicker = document.querySelectorAll('input[type=date]');

const datepicker_config = {
    dateFormat: "Y-m-d",
    'locale': 'ru'
}

flatpickr(datepicker, datepicker_config);