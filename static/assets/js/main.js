let current_page = window.location.pathname;

console.log(current_page)

let active_link = document.querySelector(`.nav-link[href='${current_page}']`);

active_link.classList.add('active')