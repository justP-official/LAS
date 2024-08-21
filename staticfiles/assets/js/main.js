const datetimepicker = document.querySelectorAll('input[type=datetime-local]');

const datetimepicker_config = {
    enableTime: true,
    dateFormat: "d-m-Y H:i",
    'locale': 'ru'
}

flatpickr(datetimepicker, datetimepicker_config)

// let f = document.querySelector('.form')

// f.addEventListener('submit', function(e) {
//     e.preventDefault()
//     console.log(f.datetime.value)
// })