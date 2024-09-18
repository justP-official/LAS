let current_page = `/${window.location.pathname.split('/')[1]}/`;
if (current_page) {
    let active_link = document.querySelector(`.nav-link[href='${current_page}']`);

    active_link.classList.add('active');
}

async function get_data(url) {
    // асинхронная функция для получения данных по url
    let response = await fetch(url);  // делаем запрос на адрес

    if (response.ok) {  // если запрос успешно выполнен
        let json_data = await response.json();  // парсим данные в json

        return Object.values(json_data);  // возвращаем значения json
    }

    return [];  // иначе возвращаем пустой массив
}

export {get_data}
